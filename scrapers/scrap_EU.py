from playwright.sync_api import sync_playwright
from scrapers.save_leads import save_leads_to_csv
import re

def block_unwanted_requests(route, request):
    ad_domains = ["googleads.g.doubleclick.net", "adservice.google.com"]
    if (request.resource_type in ["image", "font", "stylesheet", "javascript"] or
        "text/css" in request.headers.get("content-type", "") or
        any(domain in request.url for domain in ad_domains)):
        route.abort()
    else:
        route.continue_()
def scrape_b2b_leads_EU(industry="", country=""):
    url = f"https://ch.bizin.eu/eng/search/all?what={industry}&where=&country={country}&lang=eng"
    batch_size=50
    companies = []
    emails = []
    
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=False)  
        context = browser.new_context(viewport={"width": 800, "height": 768})
        page = context.new_page()

        page.route("**/*", block_unwanted_requests)

        page.goto(url)
            
        current_page = 1

        while current_page:
            try: 
                page.wait_for_selector(".span12.number_found + .span8.organization_list")
                company_cards = page.locator(".span12.number_found + .span8.organization_list > .row-fluid.organization")
                count = company_cards.count()

                for i in range(count):
                    company_card = company_cards.nth(i)
                    company_link = company_card.locator(('.span10 h2 > a')).nth(0)
                    company_name = company_link.inner_text()
                    company_url = company_link.get_attribute('href')
                    company_email = "N/A"
                    company_page = context.new_page()
                    company_page.route("**/*", block_unwanted_requests)
                    
                    # Retry logic for navigation
                    retries = 3
                    for attempt in range(retries):
                        try:
                            company_page.goto(f"https://ch.bizin.eu{company_url}")
                            break  # Break if navigation is successful
                        except Exception as e:
                            print(f"Attempt {attempt + 1} failed for {company_url}. Retrying...")
                            if attempt > retries - 1:
                                print(f"Failed to load {company_url} after {retries} attempts.")
                                company_page.close()
                                continue

                    
                    try:
                        company_page.wait_for_selector("span[itemprop='email']", timeout=5000)  
                        if company_page.locator("span[itemprop='email']").is_visible():
                            company_email = company_page.locator("span[itemprop='email']").inner_text()
                    except Exception as e:
                        pass

                    companies.append(company_name)
                    emails.append(company_email)

                    if len(companies) >= batch_size:
                                save_leads_to_csv(companies, emails, industry=industry, country=country)
                                companies.clear()
                                emails.clear()
                    company_page.close()

                current_page += 1
                # "/eng/search/all?p=2&amp;what=software&amp;where="
                if(page.is_visible(f"a[href='/eng/search/all?p={current_page}&what={industry}&where={country}']")):
                     page.click(f"a[href='/eng/search/all?p={current_page}&what={industry}&where={country}']")
                else:
                     break

            except Exception as e:
                print(f"Error on page {current_page}: {e}")
                break
        
        browser.close()

