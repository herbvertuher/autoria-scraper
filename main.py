from utils.config import URL_TEMPLATE, DUMP_TIME, SCRAPPER_TIME, logger
import utils.db_helper
import utils.async_scraper

import asyncio
import aiohttp
import datetime


async def run_at(time, coro):
    now = datetime.datetime.now()
    delay = ((time - now) % datetime.timedelta(days=1)).total_seconds()
    delay = ((time - now) % datetime.timedelta(days=1)).total_seconds()
    await asyncio.sleep(delay)

    return await coro


async def create_database_dump():
    utils.db_helper.create_database_dump()
    logger.info("Dump has been created successfully!")


async def scrap_data():
    number_of_pages = utils.async_scraper.get_number_of_pages(URL_TEMPLATE.format(1))
    logger.info("Found {} pages to parse".format(number_of_pages))

    scraped_urls = await utils.async_scraper.get_all_urls(number_of_pages)

    conn = utils.db_helper.create_conn()
    utils.db_helper.connect_to_database(conn)
    urls_in_database = utils.db_helper.get_urls_from_database(conn)

    tasks = []
    async with aiohttp.ClientSession() as session:
        for urls in scraped_urls.values():
            for url in urls:
                if url not in urls_in_database:
                    task = asyncio.create_task(utils.async_scraper.get_data_from_url(url, session))
                    tasks.append(task)

                    if len(tasks) == 30 or len(tasks) > 0:  # 10
                        result = await asyncio.gather(*tasks)
                        result = list(filter(lambda item: item is not None, result))
                        if len(result) > 0:
                            utils.db_helper.insert_row(conn, result)
                        tasks = []

    conn.close()

    logger.info("Data has been scraped successfully!")


async def main():
    dump_time = datetime.datetime.combine(datetime.date.today(), datetime.time(DUMP_TIME))
    scrapper_time = datetime.datetime.combine(datetime.date.today(), datetime.time(SCRAPPER_TIME))

    while True:
        await asyncio.gather(
            run_at(dump_time, create_database_dump()),
            run_at(scrapper_time, scrap_data())
        )

if __name__ == '__main__':
    asyncio.run(main())
