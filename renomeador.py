import os
import re
import tkinter as tk
from tkinter import filedialog

def reformat_date(filename):
    # Define the regex patterns to match dates in different formats
    patterns = [
        r'(\d{2})-(\d{2})-(\d{2})',                  # e.g., 01-02-21
        r'(\d{2})-(\d{2})-(\d{4})',                  # e.g., 01-02-2021
        r'(\d{4})-(\d{2})',                          # e.g., 2021-02
        r'(\d{2})-(\d{4})',                          # e.g., 01-2022
        r'(\d{4})(\d{2})(\d{2})',                    # e.g., 20240307
        r'(\d{4})(\d{2})',                           # e.g., 202202
        r'(\d{4}) (\d{1})',                          # e.g., 2021 2
        r'(\d{1,2})\s+(\d{4})',                      # e.g., 13 Sálario 2021 2
        r'(\d{4})\s+(\d{1,2})',                      # e.g., Sálario 2021 2
        r'_(\w{3})_(\d{4})',                         # e.g., _APR_2023
        r'(\w{3})_(\d{4})',                          # e.g., Abr_2021
        r'(\w{3})_(\d{2})',                          # e.g., Abr_20
        r'(\b\w{3,9}\b)\s+(\d{4})',                  # e.g., abril 2024, janeiro 2024,,,
        r'(\d{1,2})\s+parcela\s+do\s+13\s+(\b\w{3,9}\b)\s+(\d{4})',  # e.g., 2 parcela do 13 dezembro 2022
        r'(\d{1})-(\w{3,9})\s+(\d{4})',              # e.g., 1-JANEIRO 2021, 9-SETEMBRO 2023
        r'(\d{2})\s+(\w{3,9})\s+(\d{4})',            # e.g., 01 JANEIRO 2020, 08 AGOSTO 2022
        r'(\d{4})(\d{2})',                           # e.g., 202202, 202305
        r'(\w+)-(\d{2})-(\d{4})',                    # e.g., CONTRACHEQUE 11-2021
    ]

    # Mapping of month abbreviations and names to their numeric values
    month_map = {
        'JAN': '01', 'FEV': '02', 'MAR': '03', 'ABR': '04', 'MAI': '05', 'JUN': '06',
        'JUL': '07', 'AGO': '08', 'SET': '09', 'OUT': '10', 'NOV': '11', 'DEZ': '12',
        'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06',
        'JUL': '07', 'AUG': '08', 'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12',
        'JANEIRO': '01', 'FEVEREIRO': '02', 'MARÇO': '03', 'ABRIL': '04', 'MAIO': '05', 'JUNHO': '06',
        'JULHO': '07', 'AGOSTO': '08', 'SETEMBRO': '09', 'OUTUBRO': '10', 'NOVEMBRO': '11', 'DEZEMBRO': '12'
    }

    for pattern in patterns:
        match = re.search(pattern, filename, re.IGNORECASE)
        if match:
            if len(match.groups()) == 3:
                if pattern == r'(\w+)-(\d{2})-(\d{4})':  # Handle 'CONTRACHEQUE 11-2021'
                    month, year = match.groups()[1], match.groups()[2]
                else:
                    year, month, day = match.groups()
                    if len(year) == 2:
                        year = '20' + year
            elif len(match.groups()) == 2:
                group1, group2 = match.groups()
                if group1.isdigit() and len(group1) == 4:  # Year first
                    year, month = group1, group2.zfill(2)
                elif group2.isdigit() and len(group2) == 4:  # Year second
                    month, year = group1, group2
                    if month.upper() in month_map:
                        month = month_map[month.upper()]
                    else:
                        continue  # Skip if the month is not recognized
                elif group1.isdigit() and len(group1) == 2:  # Year second 2 digits
                    year, month = '20' + group2, group1
                elif len(group1) == 6 and group1.isdigit():  # Year and month concatenated
                    year, month = group1[:4], group1[4:6]
                else:
                    month, year = group1.upper(), group2
                    if month in month_map:
                        month = month_map[month]
                        if len(year) == 2:
                            year = '20' + year
                    else:
                        continue  # Skip if the month is not recognized
            elif len(match.groups()) == 3:  # Handle '2 parcela do 13 dezembro 2022' and '01 JANEIRO 2020'
                day, month, year = match.groups()
                if month.upper() in month_map:
                    month = month_map[month.upper()]
                else:
                    continue  # Skip if the month is not recognized
            else:
                year, month = match.groups()
            return f'{year}-{month}.pdf'
    return None  # Return None if no date is found

def rename_files(directory):
    for filename in os.listdir(directory):
        old_path = os.path.join(directory, filename)
        if os.path.isfile(old_path):  # Ensure it's a file, not a directory
            new_filename = reformat_date(filename)
            if new_filename:
                # Handle files with extra parts
                base_filename = new_filename
                suffix_counter = 1
                while os.path.exists(os.path.join(directory, new_filename)):
                    new_filename = f"{os.path.splitext(base_filename)[0]}-{suffix_counter}.pdf"
                    suffix_counter += 1
                
                new_path = os.path.join(directory, new_filename)
                os.rename(old_path, new_path)
                print(f'Renamed: {filename} -> {new_filename}')

def main():
    # Create a Tkinter root window and hide it
    root = tk.Tk()
    root.withdraw()

    # Open a file dialog to select a directory
    directory_path = filedialog.askdirectory(title="Select Directory")

    # If a directory was selected, proceed with renaming files
    if directory_path:
        rename_files(directory_path)
    else:
        print("No directory selected.")

if __name__ == "__main__":
    main()
