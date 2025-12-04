from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from defs import *
from helpers import Base

class IBM(Base):

  company = "IBM"

  def get_jobs(self, url):
      self.driver.get(url)
      WebDriverWait(self.driver, 5).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, "div.bx--card-group__cards__col"))
      )
      
      return self.driver.find_elements(By.CSS_SELECTOR, "div.bx--card-group__cards__col")

  def get_li_elements(self, link, qual_type):
    if qual_type == MIN_QUAL:
      quals = ["Required technical and professional expertise".lower(),
              ]
    else:
      quals = ["Preferred technical and professional experience".lower(),
              ]
    conditions = " or ".join([
        f"contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{p}')" 
        for p in quals
    ])
    header_xpath = f".//*[self::h2 or self::h3 or self::div or self::p][{conditions}]"
    
    self.child_driver.get(link)
    try:
      WebDriverWait(self.child_driver, 5).until(
        EC.presence_of_element_located((By.XPATH,header_xpath))
      )
    except Exception as e:
      return []

    els = self.child_driver.find_elements(By.XPATH,header_xpath)
    qual_header = min(els, key=lambda e: len(e.get_attribute("outerHTML")))
    ul = qual_header.find_element(By.XPATH, "./following::ul")
    return ul.find_elements(By.TAG_NAME, "li")
  
  def get_date(self, job_index):
    date_posted = self.child_driver.find_element(By.XPATH, ".//div[contains(text(), 'Date posted')]")
    return date_posted.find_element(By.XPATH, "./following-sibling::div").text.strip()
  
  def check_date(self, job_index):
    date = self.get_date(job_index)
    from datetime import datetime
    given_date = datetime.strptime(date,"%d-%b-%Y")
    today = datetime.today()
    if (today - given_date).days > 14:
      return False
    return True

  def print_date(self, job_index):
    date = self.get_date(job_index)
    print(date)
    self.print(date)
  
  @staticmethod
  def get_title_and_link(job):
    title = job.find_element(By.CSS_SELECTOR, "div.bx--card__heading").text.strip()
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
                      "Technical Sales Engineer",
                      
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
    return ["https://www.ibm.com/careers/search?field_keyword_05[0]=United%20States&q={}&sort=dcdate_desc&p={}"]