from concurrent.futures import ThreadPoolExecutor
from scrapers.scrap_AT import scrape_b2b_leads_AT
from scrapers.scrap_DK import scrape_b2b_leads_DK
from scrapers.scrap_EU import scrape_b2b_leads_EU

def run_parallel_scraping(industry, country):
    print("Scraping data, please wait...")
    
    with ThreadPoolExecutor() as executor:
        if(country.strip().lower() == "austria"):
            executor.submit(scrape_b2b_leads_AT, industry)
        elif(country.strip().lower() == "denmark"):
            executor.submit(scrape_b2b_leads_DK, industry)
        else:
            executor.submit(scrape_b2b_leads_EU, industry)
            executor.submit(scrape_b2b_leads_AT, industry)
            executor.submit(scrape_b2b_leads_DK, industry)

    print("Scraping completed.")