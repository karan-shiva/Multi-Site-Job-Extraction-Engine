from types import SimpleNamespace
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from defs import *
from helpers import Base
from datetime import datetime
from time import sleep
from selenium.webdriver.chrome.options import Options

DAY_LIMIT = 3

class Adobe(Base):

  company = "adobe"

  job_list = []
  job_set = set()

  def get_jobs(self, url):
      self.driver.get(url)
      # Apply country filter for United States of America
      country_button = WebDriverWait(self.driver, 5).until(
        EC.element_to_be_clickable((By.ID, "CountryAccordion"))
      )
      if country_button.get_attribute("aria-expanded") == "false":
          country_button.click()
      country_search = WebDriverWait(self.driver, 5).until(
        EC.visibility_of_element_located((By.ID, "facetInput_1"))
      )
      country_search.clear()
      country_search.send_keys("United States of America")
      us_checkbox = WebDriverWait(self.driver, 5).until(
        EC.presence_of_element_located((
            By.XPATH,
            "//input[@type='checkbox' and @data-ph-at-id='facet-checkbox' "
            "and @data-ph-at-facetkey='facet-country' "
            "and @data-ph-at-text='United States of America']"
        ))
      )
      self.driver.execute_script("arguments[0].click();", us_checkbox)
      sleep(2) 

      # Sort by Most Recent
      sort_el = WebDriverWait(self.driver, 5).until(
          EC.presence_of_element_located((By.ID, "sortselect"))
      )
      select = Select(sort_el)
      select.select_by_visible_text("Most recent")
      WebDriverWait(self.driver, 5).until(lambda d: Select(d.find_element(By.ID, "sortselect")).first_selected_option.text.strip() == "Most recent")
      sleep(2)
      # page = 1
      while True:
        # print("Page: {}\n".format(page))
        # page += 1
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li.jobs-list-item"))
        )
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)  # let JS hydrate rows
        self.driver.execute_script("window.scrollTo(0, 0);")
        sleep(0.5)
        jobs = self.driver.find_elements(By.CSS_SELECTOR, "li.jobs-list-item")
        for job in jobs:
          title = job.find_element(By.CSS_SELECTOR, "a").text.strip()
          link = job.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
          try:
            date = job.find_element(By.CSS_SELECTOR, "span.job-postdate").text.strip().split("\n")[-1]
            given_date = datetime.strptime(date,"%m/%d/%Y")
            today = datetime.today()
            if (today - given_date).days > DAY_LIMIT:
              # print("Total Jobs fetched: {}\n".format(len(self.job_list)))
              self.driver.quit()
              return self.job_list
          except:
            date = "No Date"
          if (title, link, date) in self.job_set:
            print("Duplicate Job Found")
          else:
            self.job_set.add((title, link, date))
            self.job_list.append({"title": title, "link": link, "date": date})
        
        # print("Jobs fetched so far: {}\n".format(len(self.job_list)))

        next_buttons = self.driver.find_elements(By.XPATH, "//a[@data-ph-at-id='pagination-next-link']")
        if next_buttons:
          next_button = next_buttons[0]
          first_job = jobs[0]
          self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
          self.driver.execute_script("arguments[0].click();", next_button)
          WebDriverWait(self.driver, 20).until(EC.staleness_of(first_job))
        else:
          # print("Total Jobs fetched: {}\n".format(len(self.job_list)))
          self.driver.quit()
          return self.job_list

  def get_li_elements(self, link, qual_type):
    if qual_type == MIN_QUAL:
      quals = ["ideal candidate will have",
              "what you need to succeed",
              "what you will need to success",
              "Key Attributes for Success".lower(),
              "What You Bring".lower(),
              "To be successful in this position, you will possess:".lower(),
              "What’s Needed for Success".lower(),
              "What You’ll Need to Succeed".lower(),
              "To excel in this position, you should:".lower(),
              "What you’ll bring:".lower(),
              "Requirements:".lower(),
              ]
    else:
      quals = ["nice to have",
               "Additional requirements:".lower()]
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
      els = self.child_driver.find_elements(By.XPATH,header_xpath)
      qual_header = min(els, key=lambda e: len(e.get_attribute("outerHTML")))
      ul = qual_header.find_element(By.XPATH, "./following::ul")
      return ul.find_elements(By.TAG_NAME, "li")
    except Exception as e:
        return []

  def get_title_and_link(self, job):
    title = job["title"]
    link = job["link"]
    # print("TITLE: {}".format(title))
    # print("LINK: {}".format(link))
    # print("DATE: {}\n".format(job["date"]))
    return (title, link)

  @staticmethod
  def get_filter_and_excludes():
    filters = ["Software Engineer"
              # "Software Developer",
              # "Backend Engineer"
              ]
    
    exclude_titles = ["Senior",
                      "Staff",
                      "Mobile",
                      "Android",
                      "iOS",
                      "Manager",
                      "PhD",
                      "Front End",
                      "Director",
                      "Legal Counsel",
                      "Head of Customer Engagement",
                      "Solutions Consultant",
                      "Business Development Executive",
                      "Support Pricing Specialist",
                      "Strategic Pursuit Specialist",
                      "Sr. Administrative Assistant",
                      ]
    
    exclude_descriptions = ["Currently enrolled full time and pursuing a Bachelor’s degree",
                            "Currently enrolled full time and pursuing a Bachelor’s or Master’s degree",
                            "required graduating between December 2025 – June 2026"
                            ]
    for i in range(5,20):
      exclude_descriptions.append("{} years".format(i))
      exclude_descriptions.append("{}+ years".format(i))
      exclude_descriptions.append("{} or more years".format(i))
    
    # exclude_descriptions = []
    # exclude_titles = []
    
    return (filters, exclude_titles, exclude_descriptions)

  def print_date(self, job_index):
    dt = self.job_list[job_index]["date"]
    self.print("📅 Date Posted: {}".format(dt))

  @staticmethod
  def get_base_url():
    return ["https://careers.adobe.com/us/en/search-results?keywords={}"]
  
  @staticmethod
  def get_url(base_url, filter, page):
    # print("URL PAGE: {}".format(base_url.format(filter)))
    return base_url.format(filter)

  @staticmethod
  def get_start_pageID():
    return 1
  
  @staticmethod
  def get_page_increement():
    return 1
  
  @staticmethod
  def get_max_pages():
    return 1
  
  @staticmethod
  def get_parent_options():
    options = Options()
    options.add_argument("--disable-gpu")   # Optional: improves compatibility
    options.add_argument("--window-size=1920,1080")  # Optional: needed for some rendering
    return options