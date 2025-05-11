This repo contains two job checker attempts I'm using. 
Option 1--> job_checker_simple.ipynb  | very simple, connected to a gsheet that I'm using to keep track of the career websites I want to check. it detects ANY change in such websites.
Option 2--> 1_scrape_pages.py + 2_extract_jobs_LLM.py + (upcoming)  | more complex, use Ollama 3.2 locally to detect which position have been added. Work in progress. 


DETAILS ON OPTION 2:
Note: this version uses local Ollama. Even though it's not the best LLM available (may 2025), it is free and not too heavy to run on my computer. 
For more accurate results and with a longer list of websites to monitor, it would be great to connect ChatGPT API or similar, but they are not free.



Files description
1_scrape_pages —> From a list of career pages in a separate CSV, scrape and output txt with each website’s html.
2_extract_jobs_LLM —> Run Ollama 3.2 on each txt to clean and create a new txt containing only extract jobs. 

Planned scripts to upload:
3_ standardize_jd —> Ollama will make errors in formatting, so this extra step will clean the output.

4_compare_new_old —> Ollama will compare "today" vs "today -1" versions of each job list for each page. And output a txt with the changes. 

5_send_email --> with smtplib  and  MIMEText (from email.mime.text) draft and send an email with the new jobs! Note: Store the gmail "app password" (different than the normal email password) in a separate file, and be careful not to share it. 
