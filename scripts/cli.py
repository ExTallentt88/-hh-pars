
import argparse
import sys
from tqdm import tqdm
from hh_parser.api import HHClient
from hh_parser.storage import save_to_csv, save_to_sqlite

def parse_args():
    p = argparse.ArgumentParser(description='hh.ru parser — search and save vacancies using API')
    p.add_argument('--text', type=str, help='search text / keywords', default=None)
    p.add_argument('--area', type=str, help='region id (e.g. 1 for Moscow)', default=None)
    p.add_argument('--per-page', type=int, default=20)
    p.add_argument('--max-pages', type=int, default=1)
    p.add_argument('--out', choices=['csv','sqlite'], default='csv')
    p.add_argument('--out-file', type=str, default='results.csv', help='output file path')
    return p.parse_args()

def main():
    args = parse_args()
    client = HHClient()
    generator = client.search_vacancies(text=args.text, area=args.area, per_page=args.per_page, max_pages=args.max_pages)
    items = []
    total = 0
    try:
        for it in tqdm(generator, desc='Fetching'):
            items.append(it)
            total += 1
    except KeyboardInterrupt:
        print('\nInterrupted by user, saving what we have...', file=sys.stderr)
    if not items:
        print('No items fetched.')
        return
    if args.out == 'csv':
      
        keys = sorted({k for d in items for k in d.keys()})
        save_to_csv(items, args.out_file, fieldnames=keys)
        print(f'Saved {len(items)} items to {args.out_file}')
    else:
        inserted = save_to_sqlite(items, args.out_file)
        print(f'Inserted (or ignored) rows into {args.out_file}: approx {inserted}')

if __name__ == '__main__':
    main()
