from playwright.sync_api import sync_playwright

# Function to scrape B2B email leads based on country and industry, with pagination support
def scrape_b2b_leads_AT(industry, max_pages=1):
    url = f"https://www.herold.at/gelbe-seiten/{industry}/"
    print(f"Fetching leads for Austrian Companies (up to {max_pages} pages):")

    companies = []
    emails = []

    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=True)  
        page = browser.new_page()
        
        # Navigate to the first page
        page.goto(url)
        
        # Wait for the cookie consent button to appear and click it
        page.wait_for_selector('a.cmpboxbtnyes')
        page.click('a.cmpboxbtnyes')
        print("Accepted cookies..")

        current_page = 1
        while current_page <= max_pages:
            try:
                # Wait for the page to fully load
                page.wait_for_load_state('networkidle')
                page.wait_for_selector('li[itemprop="itemListElement"]') 
                
                # Select all <li> elements
                li_elements = page.locator('li[itemprop="itemListElement"]')
                
                # Get the count of <li> elements
                count = li_elements.count()

                # Iterate over all <li> elements and extract data
                for i in range(count):
                    try:
                        details_button = li_elements.nth(i).locator('a:has-text("Details ansehen")')
                        if details_button.is_visible():
                            details_button.click()
                            
                            # Wait for navigation and extract details
                            page.wait_for_load_state('networkidle')
                            page.wait_for_selector("h1[data-yxt='nam']")
                            
                            company_name = page.locator("h1[data-yxt='nam']").inner_text()
                            company_email = "N/A"
                            if page.locator("a[data-ht-label='send_mail']").is_visible():
                                company_email = page.locator("a[data-ht-label='send_mail']").inner_text()

                            print(company_name, company_email)
                            companies.append(company_name)
                            emails.append(company_email)
                            
                            # Go back to the listing page
                            if(current_page == 1): 
                                page.goto(url)
                            else:
                                page.goto(f"{url}seite/{current_page}/")
                            page.wait_for_load_state('networkidle')
                            page.wait_for_selector('li[itemprop="itemListElement"]')

                    except Exception as e:
                        print(f"Error on item {i + 1}: {e}")
                        continue
                
                # Move to the next page if there is one and within max_pages limit
                next_page_button = page.locator(f"a[href='{url}seite/{current_page + 1}/']").nth(0)
                if next_page_button.is_visible() and current_page < max_pages:
                    next_page_button.click()
                    current_page += 1
                    print(f"Moving to page {current_page}...")
                    page.wait_for_load_state('networkidle')
                else:
                    break

            except Exception as e:
                print(f"Error on page {current_page}: {e}")
                break
        
        # Close the browser
        browser.close()

    return companies, emails
