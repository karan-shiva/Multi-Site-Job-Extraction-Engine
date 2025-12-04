from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from defs import *
from helpers import Base
from datetime import datetime

class Walmart(Base):

  company = "walmart"

  def get_jobs(self, url):
      self.driver.get(url)
      WebDriverWait(self.driver, 5).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, ".search__sort__option__label"))
      )
      date_label = self.driver.find_element(By.XPATH, "//label[@for='sortRadio1' and contains(text(), 'Date')]")
      self.driver.execute_script("arguments[0].click();", date_label)
      try:
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'li.search-result'))
        )
      except Exception as e:
        print("Error loading page")
        return []
      return self.driver.find_elements(By.CSS_SELECTOR, 'li.search-result')[:25]
  
  def check_date(self, job_index):
    date_str = self.driver.find_elements(By.CSS_SELECTOR,"span.job-listing__created")[job_index].text.strip()
    job_date = datetime.strptime(date_str, "%m/%d/%y")
    delta = datetime.now() - job_date
    if delta.days <= 14:
      return True
    return False
  
  def print_date(self, job_index):
    date_str = self.driver.find_elements(By.CSS_SELECTOR,"span.job-listing__created")[job_index]
    self.print(date_str.text.strip())
    return self.check_date(job_index)
    

  def get_qualifications(self, link, qual_type):
    self.child_driver.get(link)
    if qual_type == MIN_QUAL:
      header_xpath = (
      ".//b[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'minimum')]"
      )
    else:
      header_xpath = (
      ".//b[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'skills required')]"
      )
    
    try:
      WebDriverWait(self.child_driver, 5).until(
          EC.presence_of_element_located((By.XPATH, header_xpath))
      )
      qual_header = self.child_driver.find_element(By.XPATH, header_xpath)
      span = qual_header.find_element(By.XPATH, "following::span")
      return span.text.strip().split(";")
    except:
      if qual_type == MIN_QUAL:
        header_xpath = (
        ".//b[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'what you\'ll bring')]"
        )
      WebDriverWait(self.child_driver, 5).until(
          EC.presence_of_element_located((By.XPATH, header_xpath))
      )
      qual_header = self.child_driver.find_element(By.XPATH, header_xpath)
      ul = qual_header.find_element(By.XPATH, "following::ul")
      quals = []
      for li in ul.find_elements(By.TAG_NAME, "li"):
        quals.append(li.text.strip())
      return quals

  
  @staticmethod
  def get_title_and_link(job):
    title = job.find_element(By.CSS_SELECTOR, "a.job-listing__link").text.strip()
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
    
    return (filters, exclude_titles, exclude_descriptions)

  @staticmethod
  def get_base_url():
    return ["https://careers.walmart.com/results?q={}&page={}&sort=date&expand=department,brand,type,rate&jobCareerArea=all"]