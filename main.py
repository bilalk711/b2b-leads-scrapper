import argparse
from scrapers.run_parallel_scraping import run_parallel_scraping
from scrapers.scrap_DK import scrape_b2b_leads_DK
from scrapers.save_leads import save_leads_to_csv
import time
import datetime

# Main function to handle CLI input
def main():
    parser = argparse.ArgumentParser(description="Scrape B2B email leads from EU countries.")
    # parser.add_argument("country", type=str, help="Country code (e.g., 'DE' for Germany, 'AT' for Austria)")
    parser.add_argument("industry", type=str, help="Industry to search for (e.g., 'software', 'construction')")
    args = parser.parse_args()

    # scrappers_map = {
    #     "AT": scrape_b2b_leads_AT,
    #     "DK": scrape_b2b_leads_DK,
    # }
    start_time = time.time()
    # scrape_b2b_leads_DK(args.industry)
    run_parallel_scraping(args.industry)
    end_time = time.time()
    total_seconds = int(end_time - start_time)  
    # Format seconds into HH:MM:SS
    formatted_time = str(datetime.timedelta(seconds=total_seconds))
    print(f"Scraping completed in {formatted_time}.")

if __name__ == "__main__":
    main()
