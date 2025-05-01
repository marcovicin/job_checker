import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import csv

# Read career websites from CSV file
def read_urls_from_csv(csv_file):
    urls = []
    try:
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            # Skip header row
            next(reader, None)
            # Read URLs from column A (index 0)
            for row in reader:
                if row and row[0].strip():  # Check if the cell has content
                    urls.append(row[0].strip())
        print(f"Loaded {len(urls)} URLs from {csv_file}")
        return urls
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []


# Create a folder with today's date (format: YYYYMMDD)
today = datetime.now().strftime("%Y%m%d")
STORAGE_FOLDER = today

# Create the folder if it doesn't exist yet
if not os.path.exists(STORAGE_FOLDER):
    os.makedirs(STORAGE_FOLDER)
    print(f"Created folder for today: {STORAGE_FOLDER}")
else:
    print(f"Folder {STORAGE_FOLDER} already exists")

def get_filename(url):
    """Generate a simple filename from the URL"""
    # Extract domain name for the filename
    domain = url.split("//")[1].split("/")[0].replace(".", "_")
    return os.path.join(STORAGE_FOLDER, f"{domain}.txt")

def fetch_page_text(url):
    """Fetch the page content and extract the text"""
    try:
        print(f"Fetching: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()
    except Exception as e:
        print(f"[ERROR] Could not fetch {url}: {e}")
        return None

# CSV file containing the list of career websites
CSV_FILE = "list_career_pages.csv"

# Get URLs from CSV file
career_urls = read_urls_from_csv(CSV_FILE)

if not career_urls:
    print("No URLs found in the CSV file or file could not be read. Exiting.")
    exit()

# Track how many sites were processed
processed_count = 0
skipped_count = 0

# Process each career site
for url in career_urls:
    filename = get_filename(url)
    
    # Skip if we already downloaded this site today
    if os.path.exists(filename):
        print(f"Already downloaded today: {url}")
        skipped_count += 1
        continue
    
    # Fetch the content
    content = fetch_page_text(url)
    if not content:
        continue
    
    # Save the content to a file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Saved: {filename}")
    processed_count += 1

# Summary
print(f"\nDaily scraping complete - {processed_count} sites downloaded, {skipped_count} sites skipped")