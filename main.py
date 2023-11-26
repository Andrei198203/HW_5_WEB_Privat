import platform
import asyncio
import logging
import datetime

import aiohttp

urls = ['https://www.google.com.ua/', 'https://duckduckgo.com/', 'https://docs.aiohttp.org/', 'https://goit.global/asdf/', 'https://mail.ru']


async def main():

    async with aiohttp.ClientSession() as session:
        for url in urls:
            logging.info('Starting: {url}')
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        print(html[:100])
                    else:
                        logging.error(f"Error status {response.status} for {url}")
            except aiohttp.ClientConnectionError as e:
                logging.error(f"Connection error {url}: {e}")


async def custom_main(url):

    session = aiohttp.ClientSession()
    logging.info('Starting: {url}')
    try:
        response = await session.get(url)
        if response.status == 200:
            html = await response.text()
            await session.close()
            return html[:150]
        else:
            logging.error(f"Error status {response.status} for {url}")
    except aiohttp.ClientConnectionError as e:
        logging.error(f"Connection error {url}: {e}")
    await session.close()

async def run():
    r = []
    for url in urls:
        r.append(custom_main(url))

    result = await asyncio.gather(*r)
    return result

async def request(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    r = await response.json()
                    return r
                logging.error(f"Error status {response.status} for {url}")
        except aiohttp.ClientConnectionError as e:
            logging.error(f"Connection error {url}: {e}")
        return None

async def get_exchange():
    res = await request('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5')
    # res = await request('https://api.privatbank.ua/p24api/exchange_rates?json&date')
    return res

# async def get_exchange():
#     end_date = datetime.date.today()
#     start_date = end_date - datetime.timedelta(days=10)

    # exchange_rates = {}
    # for i in range(10):
    #     current_date = end_date - datetime.timedelta(days=i)
    #     formatted_date = current_date.strftime('%d.%m.%Y')
    #     rates = await request(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={formatted_date}')
    #
    #     if rates:
    #         exchange_rates[formatted_date] = {
    #             'USD': {
    #                 'sale': rates['exchangeRate'][0]['saleRate'],
    #                 'buy': rates['exchangeRate'][0]['buyRate']
    #             },
    #             'EUR': {
    #                 'sale': rates['exchangeRate'][9]['saleRate'],
    #                 'buy': rates['exchangeRate'][9]['buyRate']
    #             }
    #         }
    #
    # return exchange_rates

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # asyncio.run(main())
    # r = asyncio.run(run())
    # print(r)
    r = asyncio.run(get_exchange())
    print(r)







