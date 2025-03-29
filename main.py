import asyncio
from playwright.async_api import async_playwright
from playwright.async_api import expect

async def load_hero_name(page):
    all_hero_info = await page.locator("span.jcc-herocard-info-name").all()
    hero_names = []
    for hero_info in all_hero_info:
        hero_name = await hero_info.all_inner_texts()
        hero_names.append(*hero_name)
        # print(f"hero_name: {hero_name}")
    return hero_names


async def load_hero_price(page):
    all_hero_info = await page.locator("span.jcc-herocard-info-price").all()
    hero_prices = []
    for hero_info in all_hero_info:
        hero_price = await hero_info.all_inner_texts()
        hero_prices.append(*hero_price)
        # print(f"hero_price: {hero_price}")
    return hero_prices

async def load_hero_relation(browser, page):
    h_relations_link = await load_hero_relation_link(page)
    sem = asyncio.Semaphore(10)
    hero_relation_task = [deal_hero_link(sem, browser, h_relation_link) for h_relation_link in h_relations_link]
    return await asyncio.gather(*hero_relation_task)

async def load_hero_relation_link(page):
    all_hero_info = await page.locator("a.href-mask").all()
    hero_relation_links = []
    for hero_info in all_hero_info:
        hero_relation_link = await hero_info.get_attribute("href")
        # print(f"hero_relation_links: {hero_relation_link}")
        hero_relation_links.append(hero_relation_link)
    return hero_relation_links


async def deal_hero_link(sem, browser, hero_link):
    async with sem:
        detail_page = await browser.new_page()
        base_url = "https://jcc.qq.com/ingame/"
        await detail_page.goto(base_url + hero_link)
        await asyncio.sleep(3)
        detail_info = await detail_page.locator("span.jcc-contact-paster-text").all()
        single_hero_relations = []
        for relation in detail_info:
            hero_relation = await relation.all_inner_texts()
            single_hero_relations.append(*hero_relation)
            # print(f"hero_relation: {hero_relation}")
        await detail_page.close()
        return single_hero_relations


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge", headless=False)
        content_url = "https://jcc.qq.com/ingame/#/view-herolist-mode13s14"

        page = await browser.new_page()
        await page.goto(content_url)
        await asyncio.sleep(3)

        load_info = await asyncio.gather(load_hero_name(page), load_hero_price(page), load_hero_relation(browser, page))
        with open("hero_info.csv", "w", encoding="utf-8") as f:
            f.write("name,prc,relation\n")
            for hero_name, hero_prc, hero_relation in zip(load_info[0], load_info[1], load_info[2]):
                print(hero_name, hero_prc, *hero_relation)
                f.write(f"{hero_name},{hero_prc},{'|'.join(hero_relation)}\n")

        await browser.close()

asyncio.run(main())