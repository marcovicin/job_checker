# extract_jobs_with_ollama.py
import os
import subprocess
from datetime import datetime

# Configuration
OLLAMA_PATH = "/usr/local/bin/ollama"
MODEL_NAME = "llama3.2:latest"

# Get today's date for folder names
today = datetime.now().strftime("%Y%m%d")
INPUT_FOLDER = today  # The folder created by the previous script
OUTPUT_FOLDER = f"{today}_LLM_extracted"  # New folder for outputs

# Create the output folder if it doesn't exist
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)
    print(f"Created output folder: {OUTPUT_FOLDER}")

def ask_ollama_for_jobs(text, model=MODEL_NAME):
    """Extract job postings using Ollama in a single step"""
    prompt = (       
        "You are a job listing extraction tool. Extract all job postings from the text below.\n\n"
        "For each job posting, format it EXACTLY as follows (with no deviations):\n"
        "Job title: [insert job title]\n"
        "Job description: [insert concise job description or NA]\n"
        "Posting date: [insert posting date or NA]\n"
        "Application deadline: [insert deadline or NA]\n\n"
        "Important instructions:\n"
        "1. Include ONLY the extracted job listings in your response\n"
        "2. Do not include any explanations, headers, or other text\n" 
        "3. If a field is missing, use 'NA' as the value\n"
        "4. Separate each job posting with exactly three blank lines\n"
        "5. Begin your response with the first job posting immediately\n\n"
        "Here's the content to extract from:\n\n"
        f"{text}"
    )
    
    try:
        result = subprocess.run(
            [OLLAMA_PATH, "run", model],
            input=prompt.encode(),
            stdout=subprocess.PIPE,
            timeout=90
        )
        return result.stdout.decode()
    except Exception as e:
        print(f"[OLLAMA ERROR] {e}")
        return None

def main():
    # Get all text files in today's input folder
    if not os.path.exists(INPUT_FOLDER):
        print(f"Input folder {INPUT_FOLDER} not found. Please run the scraper first.")
        return
    
    txt_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".txt")]
    
    if not txt_files:
        print(f"No text files found in {INPUT_FOLDER}.")
        return
    
    processed_count = 0
    
    # Process each file
    for filename in txt_files:
        input_path = os.path.join(INPUT_FOLDER, filename)
        output_filename = filename.replace(".txt", "_LLM.txt")
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        
        print(f"\n🔍 Analyzing: {input_path}")
        try:
            with open(input_path, "r", encoding="utf-8") as f:
                page_text = f.read()
                
            extracted_jobs = ask_ollama_for_jobs(page_text)
            if extracted_jobs:
                # Write the extracted jobs to an individual output file
                with open(output_path, "w", encoding="utf-8") as outfile:
                    outfile.write(extracted_jobs)
                print(f"Extracted job information saved to: {output_path}")
                processed_count += 1
            else:
                print("No jobs extracted")
                
        except Exception as e:
            print(f"[ERROR] Failed to process {input_path}: {e}")
    
    # Summary
    print(f"\n Processing complete. {processed_count} files processed.")

if __name__ == "__main__":
    main()
