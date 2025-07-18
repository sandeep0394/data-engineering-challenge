from playwright.sync_api import sync_playwright
import csv
import os
import time

# Category URLs to scrape
CATEGORY_URLS = {
    "Industrial Machinery": "https://www.alibaba.com/Industrial-Machinery_p43",

}

def scrape_alibaba_categories_to_csv(output_path="data/alibaba_all_products.csv"):
    os.makedirs("data", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=200)
        page = browser.new_page()

        all_data = []

        for category, url in CATEGORY_URLS.items():
            print(f"\n🔍 Scraping category: {category}")
            page.goto(url, timeout=60000)

            # Scroll to load products
            for _ in range(10):
                page.mouse.wheel(0, 5000)
                time.sleep(2)

            try:
                page.wait_for_selector("div.hugo4-product", timeout=10000)
            except Exception:
                print(f"❌ Could not find products for {category}. Skipping.")
                continue

            products = page.query_selector_all("div.hugo4-product")
            print(f"✅ Found {len(products)} products in {category}.\n")

            for product in products:
                title_el = product.query_selector("div.subject span")
                title = title_el.get_attribute("title") if title_el else "N/A"

                price_el = product.query_selector("div.price")
                price = price_el.inner_text().strip() if price_el else "N/A"

                moq_el = product.query_selector("div.moq span.moq-number")
                moq = moq_el.inner_text().strip() if moq_el else "N/A"

                img_el = product.query_selector("img.picture-image")
                img_url = "https:" + img_el.get_attribute("src") if img_el else "N/A"

                all_data.append([category, title, price, moq, img_url])

        # Save to CSV
        with open(output_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Category", "Title", "Price", "MOQ", "Image_URL"])
            writer.writerows(all_data)

        print(f"\n📁 All categories scraped and saved to {output_path}")
        browser.close()

if __name__ == "__main__":
    scrape_alibaba_categories_to_csv()
