import pandas as pd

def save_leads_to_csv(companies, emails, industry="default", country="default"):
        # Save the results into a CSV file
        df = pd.DataFrame({"Company": companies, "Emails": emails, })
        df.to_csv(f"./data/{industry}_b2b_leads_{country}.csv", index=False)
        print(f"Scraping complete. Data saved to {industry}_b2b_leads_{country}.csv")