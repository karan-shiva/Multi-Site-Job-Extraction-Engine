from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from defs import *
from helpers import Base
from time import sleep

class Intel(Base):

  company = "intel"

  def get_jobs(self, url):
      self.driver.get(url)
      job_list = []
      while True:
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-automation-id="jobTitle"]'))
        )
        jobs = self.driver.find_elements(By.CSS_SELECTOR, '[data-automation-id="jobTitle"]')
        for job in jobs:
          title = job.text.strip().split("\n")[0]
          link = job.get_attribute("href")
          job_list.append({"title": title, "link": link})
        try:
          next_btn = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "button[data-uxi-element-id='next'][aria-label='next']"))
          )
        except:
          break
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)
        self.driver.execute_script("arguments[0].click();", next_btn)
        sleep(2)
      
      return job_list

  def get_li_elements(self, link, qual_type):
    if qual_type == MIN_QUAL:
      quals = ["minimum qualification",
              ]
    else:
      quals = ["preferred qualification",
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
    ul = qual_header.find_element(By.XPATH, "./following::ul")
    return ul.find_elements(By.TAG_NAME, "li")

  
  @staticmethod
  def get_title_and_link(job):
    title = job['title']
    link = job['link']
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
    return ["https://intel.wd1.myworkdayjobs.com/en-US/External?q={}&locations=1e4a4eb3adf101cc4e292078bf8199d0&locations=1e4a4eb3adf101fa2a777d76bf8116cf&locations=1e4a4eb3adf1016541777876bf8111cf&locations=0741efd9f02e01994a3c9ca2ae078199&locations=da6b8032b879100204a63a809f6c0000&locations=1e4a4eb3adf1011246675c76bf81f8ce&locations=1e4a4eb3adf10118b1dfe877bf8162d0&locations=1e4a4eb3adf10129d05fe377bf815dd0&locations=1e4a4eb3adf1018c4bf78f77bf8112d0&locations=1e4a4eb3adf101b8aec18a77bf810dd0"]
  
  def get_url(self, base_url, filter, page):
    return base_url.format(filter)
  
  def get_start_pageID(self):
    return 1
  
  def get_max_pages(self):
    return 1

  def get_date(self, job_index):
    return self.child_driver.find_element(By.XPATH, "//dt[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'posted on')]").find_element(By.XPATH, "following-sibling::dd").text.strip()

  def print_date(self, job_index):
    date = self.get_date(job_index)
    self.print("📅 Date Posted: {}".format(date))
    
  def check_date(self, job_index):
    date = self.get_date(job_index)
    if "today" in date.lower() or "yesterday" in date.lower():
      return True
    days = date.split(" ")[1]
    if "+" in days:
      return False
    days_ago = int(days)
    if days_ago <= 3:
      return True
    return False