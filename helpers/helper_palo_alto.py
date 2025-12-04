from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from defs import *
from helpers import Base

class PaloAlto(Base):

  company = "palo alto networks"

  def get_jobs(self, url):
      self.driver.get(url)

      WebDriverWait(self.driver, 5).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, "h3.QJPWVe"))
      )

      
      return self.driver.find_elements(By.CSS_SELECTOR, "div[jscontroller='snXUJb']")

  def get_li_elements(self, link, qual_type):
    qual = "Minimum qualifications" if qual_type == MIN_QUAL else "Preferred qualifications"
    
    self.child_driver.get(link)
    WebDriverWait(self.child_driver, 5).until(
      EC.presence_of_element_located((By.XPATH,".//h4[contains(text(), '{}')]".format(qual)))
    )

    qual_header = self.child_driver.find_element(By.XPATH,".//h4[contains(text(), '{}')]".format(qual))
    ul = qual_header.find_element(By.XPATH, "./following-sibling::ul")
    return ul.find_elements(By.TAG_NAME, "li")

  
  @staticmethod
  def get_title_and_link(job):
    title = job.find_elements(By.CSS_SELECTOR, "h2.section29__search-results-job-title")[0].text.strip()
    link = job.find_elements(By.CSS_SELECTOR, "a.section29__search-results-link")[0].get_attribute("href")
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
    
    exclude_descriptions = []
    exclude_titles = []
    
    return (filters, exclude_titles, exclude_descriptions)

  @staticmethod
  def get_base_url():
    return ["https://jobs.paloaltonetworks.com/en/search-jobs/{}/United%20States/47263/1/2/6252001/39x76/-98x5/50/2"]
  
  @staticmethod
  def get_url(base_url, filter, page):
    return base_url.format(filter)