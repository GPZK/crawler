import bs4
import asyncio
import aiohttp
from urllib.parse import urljoin

url = 'https://books.toscrape.com/'
result = []
broken_list = []

async def main(page_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(page_url) as response:
            html = await response.text()
            soup = bs4.BeautifulSoup(html, 'html.parser')
            depth = 1
            tasks = []
            for el in soup.find_all('a'):
                link = urljoin(page_url, el.get('href'))
                task = check_page(link, depth + 1)
                tasks.append(task)
                all_url = list(map(lambda x: x[0], result))
                if link not in all_url:
                    result.append((link, depth))
            await asyncio.gather(*tasks)
            output()

                

async def check_page(page_url, depth):
    async with aiohttp.ClientSession() as session:
        async with session.get(page_url) as response:
            html = await response.text()
            if response.status != 200:
                broken_list.append(page_url)
                return
            soup = bs4.BeautifulSoup(html, 'html.parser')
            tasks1 = []
            for el in soup.find_all('a'):
                link = urljoin(page_url, el.get('href'))
                all_url = list(map(lambda x: x[0], result))
                if link not in all_url:
                    result.append((link, depth))
                    task = check_page(link, depth + 1)
                    tasks1.append(task)
            await asyncio.gather(*tasks1)
            print('checked url', page_url, 'at depth', depth, 'q:', len(tasks1))

def output():
    with open('result.txt', 'w') as f:
        f.write(f'{result} \nBroken:\n {broken_list}')

if __name__ == '__main__':
    asyncio.run(main(url))
    
    