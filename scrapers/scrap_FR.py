# from playwright.sync_api import sync_playwright

# # Function to scrape B2B email leads based on country and industry, with pagination support
# def scrape_b2b_leads_FR(industry, max_pages=10):
#     url = f"https://www.leboncoin.fr/recherche/?category=200&q={industry}"
#     print(f"Fetching leads for French Companies:")
#     companies = []
#     emails = []
    
#     with sync_playwright() as p:
#         # Launch the browser
#         browser = p.chromium.launch(headless=True)  
#         page = browser.new_page()
#         page.goto(url)
#         page.wait_for_selector('button[class="c-btn c-btn--primary c-btn--medium c-btn--medium-large"]')
        
#         while current_page <= m