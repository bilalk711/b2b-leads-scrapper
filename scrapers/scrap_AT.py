from concurrent.futures import ThreadPoolExecutor
from playwright.sync_api import sync_playwright

# Function to scrape B2B email leads for a specific page
def scrape_b2b_leads_AT(industry, start_page, max_pages):
    url = f"https://www.herold.at/gelbe-seiten/{industry}/seite/{start_page}/"
    print(f"Fetching leads for Austrian Companies (Pages {start_page} to {start_page + max_pages - 1}):")

    companies = []
    emails = []

    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=True)  
        context = browser.new_context(
            viewport={"width": 1280, "height": 800}  # Set your desired viewport size
        )

        page = context.new_page()

        # Block images, stylesheets, and scripts to save bandwidth and speed up scraping
        page.route("**/*", lambda route, request: route.continue_() if request.resource_type not in ["image", "stylesheet"] else route.abort())
        
        # Navigate to the first page
        page.goto(url)
        
        # Accept cookies if required
        page.wait_for_selector('a.cmpboxbtnyes')
        page.click('a.cmpboxbtnyes')
        print(f"Accepted cookies on page {start_page}...")

        current_page = start_page
        while current_page < start_page + max_pages:
            try:
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
                            page.wait_for_selector("h1[data-yxt='nam']")
                            
                            company_name = page.locator("h1[data-yxt='nam']").inner_text()
                            company_email = "N/A"
                            if page.locator("a[data-ht-label='send_mail']").is_visible():
                                company_email = page.locator("a[data-ht-label='send_mail']").inner_text()
                            companies.append(company_name)
                            emails.append(company_email)
                            
                            # Go back to the listing page
                            page.goto(f"https://www.herold.at/gelbe-seiten/{industry}/seite/{current_page}")

                    except Exception as e:
                        print(f"Error on item {i + 1}: {e}")
                        continue
                
                # Move to the next page if there is one and within max_pages limit
                next_page_button = page.locator(f"a[href='https://www.herold.at/gelbe-seiten/{industry}/seite/{current_page + 1}/']").nth(0)
                if next_page_button.is_visible() and current_page < start_page + max_pages:
                    next_page_button.click()
                    current_page += 1
                    print(f"Moving to page {current_page}...")
                else:
                    break

            except Exception as e:
                print(f"Error on page {current_page}: {e}")
                break
        
        # Close the browser
        browser.close()

    return companies, emails


# Function to run multiple instances concurrently
def run_parallel_scraping(industry, num_instances, max_pages_per_instance):
    start_pages = [1, 10, 20, 30]  # Starting page for each instance
    with ThreadPoolExecutor(max_workers=num_instances) as executor:
        results = executor.map(lambda start_page: scrape_b2b_leads_AT(industry, start_page, max_pages_per_instance), start_pages)
    
    # Combine the results from all threads
    all_companies = []
    all_emails = []
    for companies, emails in results:
        all_companies.extend(companies)
        all_emails.extend(emails)
    
    return all_companies, all_emails


# Run the scraping process with 3 instances
# industry = "industrie"
# num_instances = 3
# max_pages_per_instance = 5  # Adjust as needed

# all_companies, all_emails = run_parallel_scraping(industry, num_instances, max_pages_per_instance)
# print(f"Total Companies: {len(all_companies)}")
# print(f"Total Emails: {len(all_emails)}")
