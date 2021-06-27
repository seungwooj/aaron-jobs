import requests
from bs4 import BeautifulSoup


def extract_last_page(url):
  result = requests.get(url)
  soup = BeautifulSoup(result.text, 'html.parser')
  pages = soup.find('div', {'class': 's-pagination'}).find_all('a')
  last_page = pages[-2].get_text(strip=True)
  return int(last_page)


def extract_job(html):
  title = html.find('h2', {'class': 'fs-body3'}).find('a')['title']
  company, location = html.find('h3', 
  {'class': 'fs-body1'}).find_all('span', recursive=False)
  company = company.get_text(strip=True)
  location = location.get_text(strip=True)
  job_id = html['data-jobid']

  return {
    'title': title,
    'company': company,
    'location': location,
    'link': f"https://stackoverflow.com/jobs/{job_id}/"
    }


def extract_jobs(last_page, url):
  jobs = []
  for page in range(last_page):
    print(f"Scraping Stackoverflow: page {page+1}")
    result = requests.get(f"{url}&pg={page+1}")
    soup = BeautifulSoup(result.text, 'html.parser')
    results = soup.find_all('div', {'class': '-job'})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs


def return_jobs(word):
  url = f"https://stackoverflow.com/jobs?q={word}&sort=i"
  last_page = extract_last_page(url)
  jobs = extract_jobs(last_page, url)
  return jobs


