from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from defs import *
from helpers import Base

ALPHA_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHA_LOWER = "abcdefghijklmnopqrstuvwxyz"
MAX_DAYS = 14 

class Paypal(Base):

  company = "paypal"

  def get_jobs(self, url):
      self.driver.get(url)
      WebDriverWait(self.driver, 5).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="job-listing"]'))
      )
      return self.driver.find_elements(By.CSS_SELECTOR, '[data-test-id="job-listing"]')[:10]
      

  def get_li_elements(self, link, qual_type):
    if qual_type == MIN_QUAL:
      quals = ["What you need to bring:".lower(),
               "Expected Qualifications:".lower(),
               "Minimum Qualifications:".lower(),
              ]
    else:
      quals = ["Preferred Qualifications:".lower(),
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
  
  def get_date(self, job_index):
    date = self.driver.find_elements(By.CSS_SELECTOR,"div.subData-13Lm1")[job_index].text.strip()
    return date
  
  def print_date(self, job_index):
    date = self.get_date(job_index)
    self.print("📅 Date Posted: {}".format(date))
    return True

  def check_date(self, job_index):
    date = self.get_date(job_index).lower()
    if "month" in date:
      return False
    days = date.split(" ")[1]
    if days == "a":
      return True
    num_days = int(days)
    if num_days > MAX_DAYS:
      return False
    return True

  
  @staticmethod
  def get_title_and_link(job):
    title = job.find_element(By.CSS_SELECTOR, "div.title-1aNJK").text.strip()
    link = job.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
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
                      "Front End",
                      "Sr Software",
                      ]
    
    exclude_descriptions = []
    for i in range(5,11):
      exclude_descriptions.append("{} years".format(i))
      exclude_descriptions.append("{}+ years".format(i))
      exclude_descriptions.append("{} or more years".format(i))
    
    return (filters, exclude_titles, exclude_descriptions)

  @staticmethod
  def get_base_url():
    return ["https://paypal.eightfold.ai/careers?query={}&start={}&location=United+States+of+America&pid=274915942384&sort_by=timestamp&filter_include_remote=1"]
  
  @staticmethod
  def get_start_pageID():
    return 0
  
  @staticmethod
  def get_page_increement():
    return 10