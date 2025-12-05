from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from defs import *
from helpers import Base

class ByteDance(Base):

  company = "bytedance"

  def get_jobs(self, url):
      self.driver.get(url)
      WebDriverWait(self.driver, 5).until(
          EC.presence_of_element_located((By.XPATH, "//a[@href and count(@*) = 1]"))
      )

      return self.driver.find_elements(By.XPATH, "//a[@href and count(@*) = 1]")

  def get_qualifications(self, link, qual_type):
    self.child_driver.get(link)
    try:
      WebDriverWait(self.child_driver, 5).until(
          EC.presence_of_element_located((By.XPATH, "//p[contains(@class, 'bd-title') and contains(normalize-space(.), 'Qualifications')]"))
      )
      qual_text = self.child_driver.find_element(By.XPATH, "//p[contains(@class, 'bd-title') and contains(normalize-space(.), 'Qualifications')]").find_element(By.XPATH, "./following-sibling::p").text.strip()
      return [qual_text]
    except Exception as e:
      return []

  
  @staticmethod
  def get_title_and_link(job):
    title = job.find_element(By.CSS_SELECTOR, "span.font-bold").text.strip()
    link = job.get_attribute("href")
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
    return ["https://joinbytedance.com/search?keyword={}&recruitment_id_list=&job_category_id_list=&subject_id_list=&location_code_list=CT_1000001%2CCT_247%2CCT_100764%2CCT_94%2CCT_114%2CCT_223%2CCT_203%2CCT_75%2CCT_1103355%2CCT_157&limit=12&offset={}"]
  
  @staticmethod
  def get_start_pageID():
    return 0
  
  @staticmethod
  def get_page_increement():
    return 12
  
  @staticmethod
  def get_quals():
    return [MIN_QUAL]