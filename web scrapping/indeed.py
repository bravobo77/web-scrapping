import requests

from bs4 import BeautifulSoup

LIMIT = 50 
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"

def get_last_page():
    result = requests.get(URL)
    #페이지1#
    soup = BeautifulSoup(result.text,"html.parser")
    #얼마나 페이지가 있는지, 데이터 탐색, 추출#
    pagination = soup.find("div",{"class":"pagination"})
    #div를 찾아서 clss명이 pagination인걸 html에서 찾은것#
    links = pagination.find_all("a")
    #거기에서 a링크를 찾아서 pages로 넣음#
    pages = [] 
    for link in links[:-1]:
        pages.append(int(link.string))
    #span을 추출하기 위해 loop를 써서 link 추출#
    max_page = pages[-1]
    #print(range(max_page))
    #range 여기에 넣은 수 만큼 배열을 만들어줌
    return max_page

def extract_job(html):
    title = html.find("div",{"class":"title"}).find("a")["title"]
  #일자리 제목
    company = html.find("span",{"class":"company"})
    if company : 
      company_anchor = company.find("a")
      if company_anchor is not None:
        company = str(company_anchor.string)
      else:
          company = str(company.string)
      company = company.strip()
    else:
      company = None
    location = html.find("div",{"class":"recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]
    
    return {
        "title": title,
        "company": company,
        "location": location,"link":f"https://www.indeed.com/viewjob?jk={job_id}"
    }
  
def extract_jobs(last_page):
  #last_page는 마지막 페이지 수이고 이걸 넘는 페이지 만들 기능
  jobs = []
  for page in range(last_page):
      #print(page)
    print(f"Scrapping Indeed Page {page}")
    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text,"html.parser")
    results = soup.find_all("div",{"class":"jobsearch-SerpJobCard"})
    for result in results:
        job = extract_job(result)
        jobs.append(job)
  return jobs

def get_jobs():
  last_page = get_last_page()
  jobs = extract_jobs(last_page)
  return jobs