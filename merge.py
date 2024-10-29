import os
import pandas as pd

def merge_csv_files(input_folder, output_file):
    csv_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.csv')]
    
    # Read and concatenate all CSV files
    combined_csv = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)

    combined_csv = combined_csv.drop_duplicates()
    # Save the combined CSV to a new file
    combined_csv.to_csv(f"data/{output_file}", index=False)

def merge():
    output_filename = input("Enter the name for the merged CSV file (e.g., 'merged_CVs.csv'): ") or "b2b_leads.csv"
    if not output_filename.endswith('.csv'):
        output_filename += '.csv'
    input_folder = 'data' 
    merge_csv_files(input_folder, output_filename)
    print(f"All CSV files have been merged into {output_filename}")

if __name__ == "__main__":
    merge()