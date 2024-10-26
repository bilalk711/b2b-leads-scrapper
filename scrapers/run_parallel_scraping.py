from concurrent.futures import ThreadPoolExecutor
from scrapers.scrap_AT import scrape_b2b_leads_AT
from scrapers.scrap_DK import scrape_b2b_leads_DK

def run_parallel_scraping(industry):
    print("Scraping data, please wait...")
    
    with ThreadPoolExecutor() as executor:
        executor.submit(scrape_b2b_leads_AT, industry)
        executor.submit(scrape_b2b_leads_DK, industry)

    print("Scraping completed.")