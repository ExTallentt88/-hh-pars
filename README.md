# hh-parser --> Парсер вакансий с HeadHunter API

> Парсер вакансий для [hh.ru](https://hh.ru), использующий официальный API HeadHunter.  
> Создан для аналитики, мониторинга рынка труда и автоматизации HR-задач.

---

## Основные возможности

-  **Работа через официальный API** — без HTML-скрейпинга и блокировок.  
-  **Фильтрация поиска**: `text`, `area`, `employment`, `page`, `per_page` и другие параметры.  
-  **Экспорт данных** в `CSV` и `SQLite` с защитой от дубликатов.  
-  Чистая архитектура и расширяемая структура проекта.  
-  Готовый CLI-инструмент для использования из терминала.  

---

## Установка

```bash
git clone https://github.com/ExTallentt88/-hh-pars
cd -hh-pars
python -m venv .venv
source .venv/bin/activate    # линукс/макОС
# .\.venv\Scripts\activate   # виндовс
pip install -r requirements.txt
