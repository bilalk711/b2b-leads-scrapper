from playwright.sync_api import sync_playwright

# Function to scrape B2B email leads based on country and industry, with pagination support
def scrape_b2b_leads_DK(industry, max_pages=10):
    url = f"https://www.degulesider.dk/{industry}/firmaer"
    print(f"Fetching leads for Denmark Companies:")
    companies = []
    emails = []
    
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=False)  
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state('networkidle')
        page.wait_for_selector('button[id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]')
        page.click('button[id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]')
        print("Accepted Cookies...")
        current_page = 1
        while current_page <= max_pages:
            try: 
                page.wait_for_selector("div[data-guv-click='company_card']")
                company_cards = page.locator("div[data-guv-click='company_card']")
                count = company_cards.count()

                for i in range(count):
                    company_card = company_cards.nth(i)

                    # Locate the company name inside the card
                    company_name = company_card.locator('#company-link-name').inner_text()
                    company_email = "N/A"

                    # Click the company card to open the details
                    company_card.click()

                    if(page.locator("button[data-guv-click='company_email']").is_visible()):
                        # Click to reveal the email button
                        page.click("button[data-guv-click='company_email']")

                        # Wait for the dialog with the email to appear
                        page.wait_for_selector('#headlessui-dialog-panel-\\:rv\\:')
                        container = page.locator('#headlessui-dialog-panel-\\:rv\\:')

                        # Get the email address from the dialog
                        company_email = container.locator('p.font-serif.font-normal.text-sm.text-secondary-500').inner_text()

                    # Print and save the company name and email
                    print(f"{company_name} {company_email}")
                    companies.append(company_name)
                    emails.append(company_email)
                    page.goto(url)

                current_page += 1

            except Exception as e:
                print(f"Error on page {current_page}: {e}")
                break
        
        # Close the browser
        browser.close()

    return companies, emails
