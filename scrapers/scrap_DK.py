from playwright.sync_api import sync_playwright
from scrapers.save_leads import save_leads_to_csv
import re

def scrape_b2b_leads_DK(industry):
    url = f"https://www.degulesider.dk/{industry}/firmaer"
    batch_size=5
    companies = []
    emails = []
    
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=False)  
        context = browser.new_context(viewport={"width": 800, "height": 768})
        page = context.new_page()

        page.route("**/*", lambda route, request: route.abort() if request.resource_type in ["image", "font", "stylesheet"] or "text/css" in request.headers.get("content-type", "") else route.continue_())

        page.goto(url)
        page.wait_for_selector('button[id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]')
        page.click('button[id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]')

        try:
            last_page_element = page.locator("nav.flex.items-center a").last
            href_value = last_page_element.get_attribute("href")

            # Extract the page number from the href using regular expressions
            max_pages = int(re.search(r"/(\d+)$", href_value).group(1)) if href_value else None
        except Exception as e:
            print(f"Error getting max page number: {e}")
            
        current_page = 1
        while current_page < max_pages:
            try: 
                page.wait_for_selector("div[data-guv-click='company_card']")
                company_cards = page.locator("div[data-guv-click='company_card']")
                count = company_cards.count()

                for i in range(count):
                    company_card = company_cards.nth(i)
                    company_link = company_card.locator(('a[data-guv-click="company_name"]'))
                    company_name = company_link.inner_text()
                    company_url = company_link.get_attribute('href')
                    company_email = "N/A"
                    company_page = context.new_page()
                    company_page.goto(f"https://www.degulesider.dk{company_url}")

                    try:
                        company_page.wait_for_selector("button[data-guv-click='company_email']", timeout=5000)  
                        if company_page.locator("button[data-guv-click='company_email']").is_visible():
                            company_page.click("button[data-guv-click='company_email']")
                            company_page.wait_for_selector('div.flex.flex-col.gap-5', timeout=1000) 
                            container = company_page.locator('div.flex.flex-col.gap-5')
                            company_email = container.locator('p.font-serif.font-normal.text-sm.text-secondary-500').inner_text()
                    except Exception as e:
                        pass

                    companies.append(company_name)
                    emails.append(company_email)

                    if len(companies) >= batch_size:
                                save_leads_to_csv(companies, emails, industry=industry, country="DK")
                                companies.clear()
                                emails.clear()
                    company_page.close()

                current_page += 1
                if(page.is_visible(f"a[href='/{industry}/firmaer/{current_page}']")):
                     page.click(f"a[href='/{industry}/firmaer/{current_page}']")
                else:
                     break

            except Exception as e:
                print(f"Error on page {current_page}: {e}")
                break
        
        browser.close()

