import argparse
from scrapers.scrap_AT import run_parallel_scraping
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
    run_parallel_scraping(args.industry, 6, 10)
    end_time = time.time()
    total_seconds = int(end_time - start_time)  # total time in seconds
    # Format seconds into HH:MM:SS
    formatted_time = str(datetime.timedelta(seconds=total_seconds))
    print(f"Scraping completed in {formatted_time}.")
    # save_leads_to_csv(companies, emails, args.industry, args.country)
    # Run the scraper with the provided country and industry
    # if(scrappers_map[args.country]):
    #     emails, companies = scrappers_map[args.country](args.industry)
    #     save_leads_to_csv(emails, companies, args.industry, args.country)
    # else:
    #     raise ValueError(f"Country {args.country} is not supported for this script.")

if __name__ == "__main__":
    main()
