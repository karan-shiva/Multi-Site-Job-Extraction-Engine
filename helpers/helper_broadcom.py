from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from defs import *
from helpers import Base
from time import sleep
import re

class Broadcom(Base):

  company = "Broadcom"

  global_jobs = []

  def get_jobs(self, url):
    self.driver.get(url)
    job_list = []
    while True:
      WebDriverWait(self.driver, 5).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, '[data-automation-id="jobTitle"]'))
      )
      jobs = self.driver.find_elements(By.CSS_SELECTOR, '[data-automation-id="jobTitle"]')
      dates = self.driver.find_elements(By.CSS_SELECTOR, '[data-automation-id="postedOn"]')
      flag = True 
      for job_index, job in enumerate(jobs):
        title = job.text.strip()
        link = job.get_attribute("href")
        date = " ".join(dates[job_index].find_element(By.CSS_SELECTOR, 'dd').text.strip().split(" ")[1:])
        # Check if date is within 14 days with Format: Today, Yesterday, 2 Days Ago, 3 Days Ago, ... 30+ Days Ago
        if "Today" in date or "Yesterday" in date:
          pass
        else:
          days_ago = int(re.findall(r'(\d+)', date)[0])
          if days_ago > 14:
            flag = False
            break
        job_list.append({"title": title, "link": link, "date": date})
      if not flag:
        break
      try:
        next_btn = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((
              By.XPATH,
              '//nav[@aria-label="pagination"]//button[@data-uxi-widget-type="stepToNextButton" and @aria-label="next"]'
          )))
      except:
          break
      self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)
      WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(next_btn))
      next_btn.click()
      sleep(2)
    global global_jobs
    global_jobs = job_list
    return job_list
  
  def get_date(self, job_index):
    global global_jobs
    return global_jobs[job_index]["date"]
  
  def check_date(self, job_index):
    date = self.get_date(job_index)
    if "Today" in date or "Yesterday" in date:
      return True
    else:
      days_ago = int(re.findall(r'(\d+)', date)[0])
      if days_ago > 14:
        return False
    return True
  
  def print_date(self, job_index):
    date = self.get_date(job_index)
    self.print("📅 Date Posted: {}".format(date))
    return True
      

  def get_li_elements(self, link, qual_type):
    if qual_type == MIN_QUAL:
      quals = ["required qualification",
               "required skills",
               "Qualifications:".lower(),
               "Job Qualifications".lower(),
               "Job Requirements".lower(),
              ]
    else:
      quals = ["preferred skills and experience",
               "Additional Requirements:".lower(),
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

    els = self.child_driver.find_elements(By.XPATH, header_xpath)
    qual_header = min(els, key=lambda e: len(e.get_attribute("outerHTML")))
    ul = qual_header.find_element(By.XPATH, "./following::ul")
    return ul.find_elements(By.TAG_NAME, "li")

  
  @staticmethod
  def get_title_and_link(job):
    title = job["title"]
    link = job["link"]
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
                      "IC Validation Engineer",
                      "Mfg Support Ops",
                      "Mainframe Software, Technical Support Engineer",
                      "Test Development Engineer",
                      "R&D Software Engineer",
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
  def get_url(base_url, filter, page):
    return base_url.format(filter)

  @staticmethod
  def get_base_url():
    return ["https://broadcom.wd1.myworkdayjobs.com/External_Career?q={}&locations=877d747df719100213668b996bb60000&locations=877d747df7191002136680bc73dd0000&locations=877d747df719100213665b4fa1470000&locations=0dd627624e2e013c1b0b00dadcd9d20c&locations=bc19fd96cebf1069285cfef83d445107&locations=0dd627624e2e01ef94cee9d9dcd9be0c&locations=036f545a07811067f02d8e8d652ca59a&locations=12a17a8024ab0188b084e8699205dedc&locations=092b5fae35ea103936b2cf96c8937ee4&locations=877d747df7191002136629d4bc1f0000&locations=036f545a07811067f0a87f246cdca66f&locations=9c718cedc47410720f2bf064829fb76b&locations=0dd627624e2e0140aadb9fd9dcd9780c&locations=877d747df71910021365fa3b7dd40000&locations=df820e04c9924c84b5214f4d68b50fa9&locations=092b5fae35ea1039363a0cdcb5837e8b&locations=092b5fae35ea103937177f80adeb7f1f&locations=877d747df71910021365c0592d6f0000&locations=3d9f1a0214ac01439ca04708d2465801&locations=036f545a07811067ec96c1512ad3a036&locations=2a204116f85f0193baeeb7e2796b85c8&locations=f1900192220f010e8b06cc0dfeb6f74e&locations=2a204116f85f013c9e832787796b52c8&locations=877d747df719100213635c7f40d30000&locations=877d747df71910021363291521ae0000&locations=877d747df719100213623cd467ed0000&locations=877d747df71910021361d95ffda70000&locations=877d747df71910021363ae79396c0000&locations=092b5fae35ea103935df5e4c2e637d4f&locations=036f545a07811067f088b65977bba653"]
  
  @staticmethod
  def get_max_pages():
    return 0
  
  @staticmethod
  def get_start_pageID():
    return 0