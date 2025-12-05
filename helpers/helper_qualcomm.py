from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from defs import *
from helpers import Base
from datetime import datetime
from time import sleep
import re

MAX_DAYS = 30

class Qualcomm(Base):

  company = "qualcomm"

  job_list = []

  def get_jobs(self, url):
    self.driver.get(url)
    page_start = 0
    while True:
      try: 
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.show-more-positions"))
        )
        show_more = self.driver.find_element(By.CSS_SELECTOR, "button.show-more-positions")
        self.driver.execute_script("arguments[0].scrollIntoView();", show_more)
        sleep(0.5)
        show_more.click()
        sleep(0.5)
        print(page_start)
        page_start += 10
      except:
        break

    try:
      WebDriverWait(self.driver, 5).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, "div.job-card-container"))
      )
      jobs = self.driver.find_elements(By.CSS_SELECTOR, "div.job-card-container")
      print("Jobs found on this page: {}\n".format(len(jobs)))
      old_id = 0
      for job in jobs:
        title = job.find_element(By.CLASS_NAME, "job-card-title").text.strip()
        self.driver.execute_script("arguments[0].scrollIntoView();", job)
        sleep(0.3)
        job.click()
        try:
          WebDriverWait(self.driver, 15).until(
            lambda d: d.find_element(By.CSS_SELECTOR, "p.position-id-text").text != old_id
          )
          old_id = self.driver.find_element(By.CSS_SELECTOR, "p.position-id-text").text.strip()
        except:
          print("Failed to find job ID")
        link = self.driver.current_url
        clean_link = re.sub(r"query=[^&]*&", "", link)
        try:
          WebDriverWait(self.driver, 5).until(
              EC.presence_of_element_located((By.XPATH,"//h4[contains(text(),'Job Posting Date')]/following-sibling::div"))
          )
          date_str = self.driver.find_element(By.XPATH,"//h4[contains(text(),'Job Posting Date')]/following-sibling::div").text.strip()
          # Calc diff days between today and date_str format 2025-11-19
          date = datetime.strptime(date_str, "%Y-%m-%d").date()
          date_diff = (datetime.today().date() - date).days
          if date_diff > MAX_DAYS:
            continue
        except:
          date_str = "Date Not Found"
        self.job_list.append({"title": title, "link": clean_link, "date": date_str})
    except Exception as e:
      print("Error in fetching jobs")
    print("Total Jobs found on this page: {}\n".format(len(self.job_list)))
    return self.job_list
  def get_li_elements(self, link, qual_type):
    if qual_type == MIN_QUAL:
      quals = ["Minimum Qualifications".lower(),
              ]
    else:
      quals = ["Preferred Qualifications".lower(),
              ]
    conditions = " or ".join([
        f"contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{p}')" 
        for p in quals
    ])
    header_xpath = f".//*[self::h2 or self::h3 or self::b or self::div or self::p][{conditions}]"
    
    self.child_driver.get(link)
    try:
      WebDriverWait(self.child_driver, 5).until(
        EC.presence_of_element_located((By.XPATH,header_xpath))
      )
    except Exception as e:
      return []

    els = self.child_driver.find_elements(By.XPATH,header_xpath)
    qual_header = min(els, key=lambda e: len(e.get_attribute("outerHTML")))
    ul = qual_header.find_elements(By.XPATH, "./following::ul")
    if not ul:
      return []
    return ul[0].find_elements(By.TAG_NAME, "li")

  def print_date(self, job_index):
    dt = self.job_list[job_index]["date"]
    self.print("📅 Date Posted: {}".format(dt))
  
  def get_date(self, job_index):
    return self.job_list[job_index]["date"]
  
  @staticmethod
  def get_title_and_link(job):
    title = job["title"]
    link = job["link"]
    return (title, link)

  @staticmethod
  def get_filter_and_excludes():
    filters = ["Software Engineer",
              "Software Developer",
              "Backend Engineer"]
    
    exclude_titles = ["Senior",
                      "Staff",
                      "Mobile",
                      "Android",
                      "iOS",
                      "Manager",
                      "PhD",
                      "Front End"
                      ]
    
    exclude_descriptions = []
    for i in range(5,20):
      exclude_descriptions.append("{} years".format(i))
      exclude_descriptions.append("{}+ years".format(i))
      exclude_descriptions.append("{} or more years".format(i))
    
    # exclude_descriptions = []
    # exclude_titles = []
    
    return (filters, exclude_titles, exclude_descriptions)
  


  @staticmethod
  def get_base_url():
    return ["https://app.eightfold.ai/careers?query={}&location=United%20States&domain=qualcomm.com&sort_by=relevance&triggerGoButton=false"]
  
  @staticmethod
  def get_url(base_url, filter, page):
    return base_url.format(filter)
  
  @staticmethod
  def get_start_pageID():
    return 1
  
  @staticmethod
  def get_max_pages():
    return 1