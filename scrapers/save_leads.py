import pandas as pd
import threading

# Initialize a lock for concurrent file access
file_lock = threading.Lock()

def save_leads_to_csv(companies, emails, industry="default", country="default"):
    # Save the results into a CSV file in batches without overwriting
    file_path = f"./data/{industry}_b2b_leads_{country}.csv"
    
    # Use lock for thread-safe access to the file
    with file_lock:
        df = pd.DataFrame({"Company": companies, "Email": emails})
        df.to_csv(file_path, mode='a', header=not pd.io.common.file_exists(file_path), index=False)
