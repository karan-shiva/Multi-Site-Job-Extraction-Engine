from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from defs import *
from helpers import Base
from datetime import datetime

MAX_DAYS = 14

class Visa(Base):

  company = "visa"

  def get_jobs(self, url):
      self.driver.get(url)
      
      WebDriverWait(self.driver, 5).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, "li.vs-underline"))
      )

      return self.driver.find_elements(By.CSS_SELECTOR, "li.vs-underline")

  def get_li_elements(self, link, qual_type):
    if qual_type == MIN_QUAL:
      quals = ["Basic Qualifications".lower(),
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
  
  def get_date(self):
    date = self.child_driver.find_element(By.XPATH, ".//p[strong[contains(text(), 'Date :')]]").text.strip().replace("Date :", "").strip()
    return date
  
  def print_date(self, job_index):
    date_str = self.get_date()
    self.print("📅 Date Posted: {}".format(date_str))

  def check_date(self, job_index):
    date_str = self.get_date()
    date = datetime.strptime(date_str, "%b %d, %Y").date()
    diff = (datetime.today().date() - date).days
    return diff <= MAX_DAYS

  
  @staticmethod
  def get_title_and_link(job):
    title = job.find_element(By.CSS_SELECTOR, "a").text.strip()
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
  def get_base_url():
    return ["https://corporate.visa.com/en/jobs/?q={}&cities=Ashburn&cities=Atlanta&cities=Austin&cities=Bellevue&cities=Foster%20City&cities=Highlands%20Ranch&cities=Lehi&cities=Miami&cities=New%20York&cities=San%20Francisco&cities=Union%20City&cities=Washington&sortProperty=createdOn&sortOrder=DESC"]
  
  def get_url(self, base_url, filter, page):
    return base_url.format(filter)