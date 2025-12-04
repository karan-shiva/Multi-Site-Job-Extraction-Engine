from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from defs import *
from helpers import Base

class Oracle(Base):

  company = "oracle"

  def get_jobs(self, url):
      self.driver.get(url)
      WebDriverWait(self.driver, 30).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, "div.job-tile"))
      )
      
      return self.driver.find_elements(By.CSS_SELECTOR, "div.job-tile")

  def get_qualifications(self, link, qual_type):
    return []

  
  @staticmethod
  def get_title_and_link(job):
    title = job.find_element(By.CSS_SELECTOR, "span.job-tile__title").text.strip()
    link = job.find_element(By.CSS_SELECTOR, "a.job-grid-item__link").get_attribute("href")
    return (title, link)

  @staticmethod
  def get_filter_and_excludes():
    filters = ["Software Engineer"]
    
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
    
    exclude_descriptions = []
    exclude_titles = []
    
    return (filters, exclude_titles, exclude_descriptions)

  @staticmethod
  def get_base_url():
    return ["https://careers.oracle.com/en/sites/jobsearch/jobs?keyword={}&lastSelectedFacet=AttributeChar6&location=United+States&locationId=300000000149325&mode=location&selectedFlexFieldsFacets=%22AttributeChar6%7C0+to+2%2B+years%22"]
  
  @staticmethod
  def get_max_pages():
    return 1
  
  @staticmethod
  def get_url(base_url, filter, page):
    return base_url.format(filter)