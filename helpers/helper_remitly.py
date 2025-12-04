from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from defs import *
from helpers import Base
from datetime import datetime

class Remitly(Base):

  company = "remitly"

  def get_jobs(self, url):
      self.driver.get(url)
    
      WebDriverWait(self.driver, 5).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, "div.jobTitle"))
      )

      
      return self.driver.find_elements(By.CSS_SELECTOR, "div.jobTitle")

  def get_li_elements(self, link, qual_type):
    self.child_driver.get(link)
    WebDriverWait(self.child_driver, 5).until(
      EC.presence_of_element_located((By.XPATH,".//p[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'you will:')]"))
    )
    if qual_type == MIN_QUAL:
      qual_header = self.child_driver.find_element(By.XPATH,".//p[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'you will:')]")
    else:
      qual_header = self.child_driver.find_element(By.XPATH,".//p[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'you have:')]")
    ul = qual_header.find_element(By.XPATH, "following::ul")
    return ul.find_elements(By.TAG_NAME, "li")
  
  def check_date(self, job_index):
    dt = self.driver.find_element(By.CSS_SELECTOR, "div.joblist-posdate").text.strip()
    given_date = datetime.strptime(dt, "%m/%d/%Y")
    if (datetime.today() - given_date).days > 500:
      return False
    return True
  
  def print_date(self, job_index):
    dt = self.driver.find_element(By.CSS_SELECTOR, "div.joblist-posdate").text.strip()
    self.print("📅 Date Posted: {}".format(dt))
    given_date = datetime.strptime(dt, "%m/%d/%Y")
    if (datetime.today() - given_date).days > 5:
      return False
    return True

  
  @staticmethod
  def get_title_and_link(job):
    title = job.find_elements(By.CSS_SELECTOR, "a")[0].text.strip()
    link = job.find_elements(By.CSS_SELECTOR, "a")[0].get_attribute("href")
    return (title, link)

  @staticmethod
  def get_filter_and_excludes():
    filters = ["Software Engineer",
              "Software Developer"]
    
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
    
    return (filters, exclude_titles, exclude_descriptions)

  @staticmethod
  def get_base_url():
    return ["https://careers.remitly.com/job-search-results/?keyword={}&compliment=United%20States%20of%20America&pg={}"]