from playwright.sync_api import sync_playwright
from scrapers.save_leads import save_leads_to_csv
import re

def scrape_b2b_leads_AT(industry):
    batch_size = 50
    url = f"https://www.herold.at/gelbe-seiten/{industry}/seite/1/"
    companies = []
    emails = []
    current_page = 1

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  
        context = browser.new_context(viewport={"width": 800, "height": 768})
        page = context.new_page()

        page.route("**/*", lambda route, request: route.abort() if request.resource_type in ["image", "font", "stylesheet"] or "text/css" in request.headers.get("content-type", "") else route.continue_())
        
        page.goto(url)
        page.wait_for_selector('a.cmpboxbtnyes')
        page.click('a.cmpboxbtnyes')

        page.wait_for_selector("nav[aria-label='Seitennummerierung']")
        page_numbers = page.locator("nav[aria-label='Seitennummerierung'] > div")
        page_numbers = [int(num) for num in re.findall(r'aria-label="Seite (\d+)"', page_numbers.inner_html())]

        # Get the maximum page number
        max_pages = max(page_numbers) if page_numbers else None
        while current_page < max_pages:
            try:
                page.wait_for_selector('li[data-ht-label="company_impression"]')
                li_elements = page.locator('li[data-ht-label="company_impression"]')
                count = li_elements.count()

                for i in range(count):
                    try:         
                        details_button = li_elements.nth(i).locator('a[data-ht-label="go_to_company_detail"]')
                        if details_button.is_visible():
                            detail_page = context.new_page()
                            detail_page.route("**/*", lambda route, request: route.abort() if request.resource_type in ["image", "font", "stylesheet"] or "text/css" in request.headers.get("content-type", "") else route.continue_())
                            
                            detail_page.goto(f"https://www.herold.at/{details_button.get_attribute("href")}")
                            detail_page.wait_for_selector("h1[data-yxt='nam']")

                            company_name = detail_page.locator("h1[data-yxt='nam']").inner_text()
                            company_email = "N/A"
                            if detail_page.locator("a[data-ht-label='send_mail']").is_visible():
                                company_email = detail_page.locator("a[data-ht-label='send_mail']").inner_text()
                            companies.append(company_name)
                            emails.append(company_email)

                            if len(companies) >= batch_size:
                                save_leads_to_csv(companies, emails, industry=industry, country="AT")
                                companies.clear()
                                emails.clear()

                            detail_page.close()

                            # page.goto(f"https://www.herold.at/gelbe-seiten/{industry}/seite/{current_page}")
                    except Exception as e:
                        print(f"Error on item {i + 1}: {e}")
                        continue

                next_page_button = page.locator(f"a[href='https://www.herold.at/gelbe-seiten/{industry}/seite/{current_page + 1}/']").nth(0)
                if next_page_button.is_visible() and current_page < max_pages:
                    next_page_button.click()
                    current_page += 1
                else:
                    break

            except Exception as e:
                print(f"Error on page {current_page}: {e}")
                break

        browser.close()



