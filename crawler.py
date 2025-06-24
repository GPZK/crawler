import bs4
import asyncio
import aiohttp
from urllib.parse import urljoin

url = 'https://books.toscrape.com/'
result = []
broken_list = []

async def check_page(page_url, depth):
    async with aiohttp.ClientSession() as session:
        async with session.get(page_url) as response:
            html = await response.text()
            if response.status != 200:
                broken_list.append(page_url)
                return
            soup = bs4.BeautifulSoup(html, 'html.parser')
            tasks = []
            for el in soup.find_all('a'):
                link = urljoin(page_url, el.get('href'))
                all_url = list(map(lambda x: x[0], result))
                if link not in all_url:
                    result.append((link, depth))
                    task = check_page(link, depth + 1)
                    tasks.append(task)
            await asyncio.gather(*tasks)
            print('checked url', page_url, 'at depth', depth, 'q:', len(tasks))

def output():
    with open('result.txt', 'w') as f:
        f.write(f'{result} \nBroken:\n {broken_list}')


async def main(page_url):
    await check_page(page_url, 0)
    output()

if __name__ == '__main__':
    asyncio.run(main(url))
    
    