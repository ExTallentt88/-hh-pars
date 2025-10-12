from __future__ import annotations
import requests
from requests.adapters import HTTPAdapter, Retry
from dateutil import parser as dateparser
from typing import Generator, Optional, Dict, Any

BASE_URL = "https://api.hh.ru"
VACANCIES_ENDPOINT = "/vacancies"


class HHClient:
   
    def __init__(
        self,
        base_url: str = BASE_URL,
        timeout: int = 10,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
    ) -> None:
       
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        
        self.session = requests.Session()
        retries = Retry(
            total=max_retries,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods={"GET"},
            backoff_factor=backoff_factor,
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

   
    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
       
        url = f"{self.base_url}{path}"
        response = self.session.get(url, params=params or {}, timeout=self.timeout)
        response.raise_for_status()
        return response.json()


    def search_vacancies(
        self,
        text: Optional[str] = None,
        area: Optional[int | str] = None,
        per_page: int = 20,
        max_pages: int = 1,
        **kwargs,
    ) -> Generator[Dict[str, Any], None, None]:
       
        params = {k: v for k, v in dict(text=text, area=area, per_page=per_page, page=0, **kwargs).items() if v is not None}

        for page in range(max_pages):
            params["page"] = page
            data = self._get(VACANCIES_ENDPOINT, params=params)

            for item in data.get("items", []):
                published = item.get("published_at")
                try:
                    item["_published_at"] = dateparser.parse(published) if published else None
                except Exception:
                    item["_published_at"] = published
                yield item

           
            if page + 1 >= data.get("pages", 1):
                break

    
    def get_vacancy(self, vacancy_id: str) -> Dict[str, Any]:
       
        return self._get(f"{VACANCIES_ENDPOINT}/{vacancy_id}")