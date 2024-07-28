import os
import re
import tkinter as tk
from tkinter import filedialog

def load_patterns(patterns_file):
    with open(patterns_file, 'r') as file:
        patterns = [line.strip() for line in file if line.strip()]
    return patterns

def reformat_date(filename, patterns, month_map):
    for pattern in patterns:
        match = re.search(pattern, filename, re.IGNORECASE)
        if match:
            groups = match.groups()
            if len(groups) == 3 and groups[1].isdigit():
                day, month, year = groups
                if len(year) == 2:
                    year = '20' + year
            elif len(groups) == 2:
                group1, group2 = groups
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
            elif len(groups) == 3:  # Handle '2 parcela do 13 dezembro 2022' and '01 JANEIRO 2020'
                day, month, year = groups
                if month.upper() in month_map:
                    month = month_map[month.upper()]
                else:
                    continue  # Skip if the month is not recognized
            else:
                year, month = groups
            return f'{year}-{month}.pdf'
    return None  # Return None if no date is found

def rename_files(directory, patterns_file):
    patterns = load_patterns(patterns_file)
    month_map = {
        'JAN': '01', 'FEV': '02', 'MAR': '03', 'ABR': '04', 'MAI': '05', 'JUN': '06',
        'JUL': '07', 'AGO': '08', 'SET': '09', 'OUT': '10', 'NOV': '11', 'DEZ': '12',
        'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06',
        'JUL': '07', 'AUG': '08', 'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12',
        'JANEIRO': '01', 'FEVEREIRO': '02', 'MARÇO': '03', 'ABRIL': '04', 'MAIO': '05', 'JUNHO': '06',
        'JULHO': '07', 'AGOSTO': '08', 'SETEMBRO': '09', 'OUTUBRO': '10', 'NOVEMBRO': '11', 'DEZEMBRO': '12'
    }

    for filename in os.listdir(directory):
        old_path = os.path.join(directory, filename)
        if os.path.isfile(old_path):  # Ensure it's a file, not a directory
            new_filename = reformat_date(filename, patterns, month_map)
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
    root = tk.Tk()
    root.withdraw()

    patterns_file = filedialog.askopenfilename(title="Select Patterns File", filetypes=[("Text Files", "*.txt")])
    if not patterns_file:
        print("No patterns file selected.")
        return

    directory_path = filedialog.askdirectory(title="Select Directory")
    if not directory_path:
        print("No directory selected.")
        return

    rename_files(directory_path, patterns_file)

if __name__ == "__main__":
    main()
