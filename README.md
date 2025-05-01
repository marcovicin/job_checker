Note: this version uses local Ollama even though it's not the best LLM available, because it's free and not too heavy to run on my computer. 
For more accurate result and a longer list of websites to monitor, it would be great to connect ChatGPT API, but it's not free.

Files description
1_scrape_pages —> From a list of career pages in a separate CSV, scrape and output txt with each website’s html.

2_extract_jobs_LLM —> From the txt use Ollama 3.2 to clean and create a new txt containing only extract jobs. 


Planned scripts to upload:
3_ standardize_jd —> Ollama will make errors in formatting, so this extra step will clean the output.

4_compare_new_old —> Ollama will compare "today" vs "today -1" versions of each job list for each page. And output a txt with the changes. 

5_send_email --> with smtplib  and  MIMEText (from email.mime.text) draft and send an email with the new jobs! Note: Store the gmail "app password" in a separate file, and don't share it. 
