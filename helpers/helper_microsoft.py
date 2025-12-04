from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
from defs import *
from helpers import Base
from urllib.parse import quote

class Microsoft(Base):

  company = "microsoft"

  def get_jobs(self, url):
      self.driver.get(url)
      WebDriverWait(self.driver, 5).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, "h2.MZGzlrn8gfgSs8TZHhv2"))
      )
      
      return self.driver.find_elements(By.CSS_SELECTOR, "h2.MZGzlrn8gfgSs8TZHhv2")

  def get_li_elements(self, link, qual_type):
    self.child_driver.get(link)
    WebDriverWait(self.child_driver, 5).until(
      EC.presence_of_element_located((By.XPATH,".//p[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'required') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'minimum')] | .//strong[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'required') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'minimum')]"))
    )

    if qual_type == MIN_QUAL:
      qual_header = self.child_driver.find_element(By.XPATH,".//p[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'required') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'minimum')] | .//strong[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'required') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'minimum')]")
    else:
      qual_header = self.child_driver.find_element(By.XPATH,".//p[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'preferred')] | .//strong[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'preferred')]")

    ul = qual_header.find_element(By.XPATH, "following::ul")
    return ul.find_elements(By.TAG_NAME, "li")


  def print_date(self, job_index):
    try:
      date_posted = self.child_driver.find_element(By.XPATH, ".//div[contains(text(), 'Date posted')]")
      date = date_posted.find_element(By.XPATH, "./following-sibling::div").text.strip()
      self.print(date)
      given_date = datetime.strptime(date,"%b %d, %Y")
      today = datetime.today()
      if (today - given_date).days > 5:
        return False
      return True
    except:
      print("ERROR fetching Date")
      # self.print("ERROR: fetching Date\n")
      # self.print("Link: {}".format(self.link))
      self.print("No Date")
      return True
  
  def check_date(self, job_index):
    try:
      date_posted = self.child_driver.find_element(By.XPATH, ".//div[contains(text(), 'Date posted')]")
      date = date_posted.find_element(By.XPATH, "./following-sibling::div").text.strip()
      given_date = datetime.strptime(date,"%b %d, %Y")
      today = datetime.today()
      if (today - given_date).days > 5:
        return False
      return True
    except:
      # print("ERROR fetching Date")
      # self.print("ERROR: fetching Date\n")
      # self.print("Link: {}".format(self.link))
      return True
  
  @staticmethod
  def get_title_and_link(job):
    title = job.text.strip()
    ancestor = job.find_element(By.XPATH, "./ancestor::div[contains(@aria-label, 'Job item')]")
    job_id = ancestor.get_attribute("aria-label").split()[-1]
    link = "https://jobs.careers.microsoft.com/global/en/job/{}/{}".format(job_id, quote(title))
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
                      "Front End",
                      "Principal",
                      "Sr Software",
                      "Sr. Software",
                      "Data Analyst",
                      " CTJ ",
                      "Electrical Engineer",
                      "Security Engineer",
                      "Quality Engineer",
                      "Network Security Service Engineer",
                      "Cloud Solution Architect",
                      "Researcher Intern",
                      "Partner Technical Advisor",
                      "Service Engineer",
                      "Research Intern"
                      ]
    
    exclude_descriptions = ["2+ years of experience in mobile app development"]
    for i in range(5,11):
      exclude_descriptions.append("{} years".format(i))
      exclude_descriptions.append("{}+ years".format(i))
      exclude_descriptions.append("{} or more years".format(i))
    
    return (filters, exclude_titles, exclude_descriptions)

  @staticmethod
  def get_base_url():
    return ["https://jobs.careers.microsoft.com/global/en/search?q=%22{}%22&lc=United%20States&l=en_us&pg={}&pgSz=20&o=Recent"]