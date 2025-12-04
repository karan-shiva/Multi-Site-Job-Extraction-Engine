from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from defs import *
from helpers import Base
from time import sleep
import re

MAX_DAYS = 30

class Suse(Base):

  company = "SUSE"

  global_jobs = []

  def get_jobs(self, url):
    self.driver.get(url)
    job_list = []
    while True:
      WebDriverWait(self.driver, 5).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, '[data-automation-id="jobTitle"]'))
      )
      jobs = self.driver.find_elements(By.CSS_SELECTOR, '[data-automation-id="jobTitle"]')
      dates = self.driver.find_elements(By.CSS_SELECTOR, '[data-automation-id="postedOn"]')
      flag = True 
      for job_index, job in enumerate(jobs):
        title = job.text.strip()
        link = job.get_attribute("href")
        date = " ".join(dates[job_index].find_element(By.CSS_SELECTOR, 'dd').text.strip().split(" ")[1:])
        # Check if date is within 14 days with Format: Today, Yesterday, 2 Days Ago, 3 Days Ago, ... 30+ Days Ago
        if "Today" in date or "Yesterday" in date:
          pass
        else:
          days_ago = int(re.findall(r'(\d+)', date)[0])
          if days_ago > MAX_DAYS:
            flag = False
            break
        job_list.append({"title": title, "link": link, "date": date})
      if not flag:
        break
      try:
        next_btn = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((
              By.XPATH,
              '//nav[@aria-label="pagination"]//button[@data-uxi-widget-type="stepToNextButton" and @aria-label="next"]'
          )))
      except:
          break
      self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)
      WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(next_btn))
      next_btn.click()
      sleep(2)
    global global_jobs
    global_jobs = job_list
    return job_list
  
  def get_date(self, job_index):
    global global_jobs
    return global_jobs[job_index]["date"]
  
  def check_date(self, job_index):
    date = self.get_date(job_index)
    if "Today" in date or "Yesterday" in date:
      return True
    else:
      days_ago = int(re.findall(r'(\d+)', date)[0])
      if days_ago > 14:
        return False
    return True
  
  def print_date(self, job_index):
    date = self.get_date(job_index)
    self.print("📅 Date Posted: {}".format(date))
    return True
      

  def get_li_elements(self, link, qual_type):
    if qual_type == MIN_QUAL:
      quals = ["required qualification",
              ]
    else:
      quals = ["preferred skills and experience",
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
    for i in range(5,11):
      exclude_descriptions.append("{} years".format(i))
      exclude_descriptions.append("{}+ years".format(i))
      exclude_descriptions.append("{} or more years".format(i))
    
    # exclude_descriptions = []
    # exclude_titles = []
    
    return (filters, exclude_titles, exclude_descriptions)
  
  @staticmethod
  def get_url(base_url, filter, page):
    return base_url.format(filter)

  @staticmethod
  def get_base_url():
    return ["https://suse.wd3.myworkdayjobs.com/Jobsatsuse?q={}&locations=27c85e5cbe0d013ab8dd9a6d5700735a&locations=27c85e5cbe0d012ec626be7057000d66&locations=27c85e5cbe0d01b06d42bb7857009783&locations=27c85e5cbe0d01d3e27faa7857006f83&locations=27c85e5cbe0d01ff6ece707957003586"]