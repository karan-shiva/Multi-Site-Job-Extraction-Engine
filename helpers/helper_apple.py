from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
from defs import *
from helpers import Base

class Apple(Base):

  company = "apple"

  def get_jobs(self, url):
      self.driver.get(url)
      WebDriverWait(self.driver, 5).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, "a.link-inline"))
      )
      
      return self.driver.find_elements(By.CSS_SELECTOR, "a.link-inline")
  
  def get_li_elements(self, link, qual_type):
    qual = "Minimum Qualifications" if qual_type == MIN_QUAL else "Preferred Qualifications"
    
    self.child_driver.get(link)
    WebDriverWait(self.child_driver, 5).until(
          EC.presence_of_element_located((By.XPATH,".//h2[contains(text(), '{}')]".format(qual)))
      )
    
    qual_header = self.child_driver.find_element(By.XPATH,".//h2[contains(text(), '{}')]".format(qual))
    ul = qual_header.find_element(By.XPATH, "following::ul")
    return ul.find_elements(By.TAG_NAME, "li")
  
  def check_date(self, job_index):
    date = self.child_driver.find_element(By.CSS_SELECTOR,"time")
    dt = date.get_attribute("datetime")
    given_date = datetime.strptime(dt,"%Y-%m-%d")
    today = datetime.today()
    if (today - given_date).days > 7:
      return False
    return True
  
  def print_date(self, job_index):
    date = self.child_driver.find_element(By.CSS_SELECTOR,"time").text.strip()
    self.print("📅 Date Posted: {}".format(date))
    dt = date.get_attribute("datetime")
    given_date = datetime.strptime(dt,"%Y-%m-%d")
    today = datetime.today()
    if (today - given_date).days > 5:
      return False
    return True

  @staticmethod
  def get_title_and_link(job):
    title = " ".join(job.get_attribute("aria-label").split()[:-1])
    link = job.get_attribute("href")
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
                  "Sr. Software",
                  "Solutions Architect",
                  "Software Development Engineer in Test",
                  "Sr Software",
                  "UI Software Engineer",
                  "Graphics Rendering",
                  "UI Solutions",
                  "UI Software Engineer",
                  "Software Engineer in Test",
                  "Cellular Platform Software Engineer",
                  "Wi-Fi",
                  "Graphics",
                  "Software Developer in Test",
                  "Wireless",
                  "VR Software Engineer",
                  "AR Software Engineer"
                  ]
    
    exclude_descriptions = [
                            "3+ years of software engineering experience with strong programming skills in Objective-C and/or Swift",
                            "2+ years proven experience shipping high quality, tested code on iOS and / or macOS",
                            "3+ years of professional iOS or macOS",
                            "2+ years experience building scalable web applications",
                            "2D and 3D graphics",
                            "experience in Cellular",
                            "Knowledge of real-time audio",
                            "3+ years Industry experience in Cocoa",
                            "Exposure to image processing technologies",
                            "experience in Layer 2, Layer 3"]
    
    #Optional
    # exclude_descriptions.append("Proficiency in full-stack")
    
    for i in range(5,20):
      exclude_descriptions.append("{} years".format(i))
      exclude_descriptions.append("{}+ years".format(i))
      exclude_descriptions.append("{} or more years".format(i))
      exclude_descriptions.append("{} year".format(i))
      exclude_descriptions.append("{}+ year".format(i))
      exclude_descriptions.append("{} or more year".format(i))
    
    # exclude_descriptions = []
    # exclude_titles = []
    
    return (filters, exclude_titles, exclude_descriptions)

  @staticmethod
  def get_base_url():
    return ["https://jobs.apple.com/en-us/search?search=%22{}%22&sort=newest&location=united-states-USA&page={}&team=machine-learning-infrastructure-MLAI-MLI+apps-and-frameworks-SFTWR-AF+cloud-and-infrastructure-SFTWR-CLD+core-operating-systems-SFTWR-COS+devops-and-site-reliability-SFTWR-DSR+engineering-project-management-SFTWR-EPM+information-systems-and-technology-SFTWR-ISTECH+machine-learning-and-ai-SFTWR-MCHLN+security-and-privacy-SFTWR-SEC+software-quality-automation-and-tools-SFTWR-SQAT+wireless-software-SFTWR-WSFT"]