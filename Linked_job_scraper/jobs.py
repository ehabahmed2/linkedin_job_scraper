# importing modules
from bs4 import BeautifulSoup
import pandas as pd
import requests


# Get the title of the job
required_job = input("Job required: ")
country = input("Enter required job place: ")
num_pages = int(input("Enter number of pages(1 page = 60 results | max 3 pages): "))
file_path = input("Enter the full file path here: ")

# check that user didn't enter more than 3 pages
while num_pages > 3:
    print("maximum 3 pages")
    num_pages = int(input("Enter number of pages(1 page = 60 results | max 3): "))

# search and parse the page
url = f"https://www.linkedin.com/jobs/search?keywords={required_job}&location={country}&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"
response = requests.get(url)
src = response.content
soup = BeautifulSoup(src, "lxml")


#empty lists to contain the details
job_titles = []
company_names = []
work_locations = []
post_dates = []
active_jobs = []
links = []
details = []


# Get the job titles
def job_details(page_num):
    container = soup.find("ul", {"class": "jobs-search__results-list"})
    if container:
        job_lists = container.find_all("li")
        for job_card in job_lists:
            job_title = job_card.find("h3", {"class": "base-search-card__title"})
            job_titles.append(job_title.text.strip() if job_title else "N/A")
            company_name = job_card.find("h4", {"class": "base-search-card__subtitle"})
            company_names.append(company_name.text.strip() if company_name else "N/A")
            
            work_location = job_card.find("span", class_="job-search-card__location")
            work_locations.append(work_location.text.strip() if work_location else "N/A")
            
            post_date = job_card.find("time")
            post_dates.append(post_date.text.strip() if post_date else "N/A")
            
            is_job_active = job_card.find("span", class_="job-posting-benefits__text")
            active_jobs.append(is_job_active.text.strip() if is_job_active else "N/A")
            
            job_link = job_card.find("a", class_="base-card__full-link").attrs['href']
            links.append(job_link)
    else:
        print("No job listings found or unable to fetch the page content.")

for page_num in range(num_pages):
    job_details(page_num)



# Loop through each link to get the details of the job
def get_details():
    for link in links:
        response = requests.get(link)
        src = response.content
        soup_page_two = BeautifulSoup(src, "lxml")
        # details_container = soup_page_two.find("div", {"class": "core-section-container__content break-words"})
        details_container = soup_page_two.find("div", {"class": "show-more-less-html__markup"})
        if details_container:
            info = details_container.find_all(['strong', 'li', 'p'])
            job_detail = " ".join([p.text.strip() for p in info])
            details.append(job_detail)

get_details()



#handling error with lenght
max_length = max(len(job_titles), len(company_names), len(work_locations), len(post_dates), len(active_jobs), len(links), len(details))

def fill_list(lst, max_length):
    return lst + [None] * (max_length - len(lst))
print(max_length)
job_titles = fill_list(job_titles, max_length)
company_names = fill_list(company_names, max_length)
work_locations = fill_list(work_locations, max_length)
post_dates = fill_list(post_dates, max_length)
active_jobs = fill_list(active_jobs, max_length)
links = fill_list(links, max_length)
details = fill_list(details, max_length)
#end of error handling


# Adding the data to excel
df = pd.DataFrame({
    "Job Title": job_titles,
    "Company Name": company_names,
    "Work Location": work_locations,
    "Active jobs": active_jobs,
    "Post date": post_dates,
    "Links": links,
    "Details of the job": details,
})
# df.to_csv(r"F:\VS projects\.vscode\scraping\jobs scraping\JobList.csv" , index=False)
df.to_csv(rf"{file_path}JobList.csv" , index=False)
print("Done, File saved succefully :)")
