from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

url = 'https://www.indeed.com/jobs?q=data+engineer&l=United+States'

response = requests.get(url) 
data = response.text
soup = BeautifulSoup(data, 'html.parser')
jobs = soup.find_all('div',{'class':'jobsearch-SerpJobCard'})
  
for job in jobs:
    title = job.find('a',{'class':'jobtitle'}).text
    link1 = job.find('a',{'class':'jobtitle'}).get('href')
    link = 'https://www.indeed.com' + link1
    
    #for each JOB's webpage, you need to connect to the link first:
    job_response = requests.get(link)
    job_data = job_response.text
    job_soup = BeautifulSoup(job_data, 'html.parser')
    
    job_description_tag = job_soup.find('div',{'id':'jobDescriptionText'})
    job_description = job_description_tag.text if job_description_tag else "N/A"
    
    print('Job Title:', title, '\nLink:', link, '\nJob Description:', job_description, '\n---')