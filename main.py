import argparse
from scrapers.scrap_AT import scrape_b2b_leads_AT
from scrapers.save_leads import save_leads_to_csv

# Main function to handle CLI input
def main():
    parser = argparse.ArgumentParser(description="Scrape B2B email leads from EU countries.")
    parser.add_argument("country", type=str, help="Country code (e.g., 'DE' for Germany, 'AT' for Austria)")
    parser.add_argument("industry", type=str, help="Industry to search for (e.g., 'software', 'construction')")
    args = parser.parse_args()

    scrappers_map = {
        "AT": scrape_b2b_leads_AT,
        "FR": scrape_b2b_leads_AT,
    }


    # Run the scraper with the provided country and industry
    if(scrappers_map[args.country]):
        emails, companies = scrappers_map[args.country](args.industry)
        save_leads_to_csv(emails, companies, args.industry, args.country)
    else:
        raise ValueError(f"Country {args.country} is not supported for this script.")

if __name__ == "__main__":
    main()
