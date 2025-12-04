from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from defs import *
from helpers import Base
from datetime import datetime

class Amazon(Base):

  company = "amazon"

  def get_jobs(self, url):
      self.driver.get(url)

      WebDriverWait(self.driver, 5).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, "a.job-link"))
      )

      return self.driver.find_elements(By.CSS_SELECTOR, "a.job-link")

  def get_qualifications(self, link, qual_type):
    qual = "BASIC QUALIFICATIONS" if qual_type == MIN_QUAL else "PREFERRED QUALIFICATIONS"
    qual = qual.lower()
    
    self.child_driver.get(link)
    # print(link)
    WebDriverWait(self.child_driver, 5).until(
      EC.presence_of_element_located((By.XPATH,".//h2[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{}')]".format(qual)))
    )

    qual_header = self.child_driver.find_element(By.XPATH,".//h2[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{}')]".format(qual))
    p = qual_header.find_element(By.XPATH, "./following-sibling::p")
    p = p.text.replace("Amazon is an equal opportunity employer and does not discriminate on the basis of protected veteran status, disability, or other legally protected status.","").\
            replace("Our inclusive culture empowers Amazonians to deliver the best results for our customers. If you have a disability and need a workplace accommodation or adjustment during the application and hiring process, including support for the interview or onboarding process, please visit","").\
            replace("https://amazon.jobs/content/en/how-we-hire/accommodations","").\
            replace("for more information. If the country/region you’re applying in isn’t listed, please contact your Recruiting Partner.","").\
            replace("https://www.aboutamazon.com/workplace/employee-benefits","").\
            replace(". This position will remain posted until filled. Applicants should apply via our internal or external career site.","").\
            replace("Los Angeles County applicants: Job duties for this position include: work safely and cooperatively with other employees, supervisors, and staff; adhere to standards of excellence despite stressful conditions; communicate effectively and respectfully with employees, supervisors, and staff to ensure exceptional customer service; and follow all federal, state, and local laws and Company policies. Criminal history may have a direct, adverse, and negative relationship with some of the material job duties of this position. These include the duties and responsibilities listed above, as well as the abilities to adhere to company policies, exercise sound judgment, effectively manage stress and work safely and respectfully with others, exhibit trustworthiness and professionalism, and safeguard business operations and the Company’s reputation. Pursuant to the Los Angeles County Fair Chance Ordinance, we will consider for employment qualified applicants with arrest and conviction records.", "")
    return [p[:p.find("Our compensation reflects the cost")].strip()]
  
  def get_date(self, job_index):
    date = self.driver.find_elements(By.CSS_SELECTOR, "span.posting-date")[job_index]
    update = date.find_element(By.XPATH, "./following-sibling::p").text.strip()
    return (date.text.strip(), update)
  
  def check_update(self, update: str):
    time = update.split(" ")[-3:-1]
    try:
      res =  time[1].find("hour") != -1 or (time[1].find("day") != -1 and int(time[0]) < 2)
    except:
      print("ERROR: Update = {}".format(update))
      exit(-1)
    if res:
      pass
    return res
    
  
  def add_link(self, link, link_set, job_index):
    date, _ = self.get_date(job_index)
    link_set.add((link, date))
  
  def check_link(self, link, link_set, job_index):
    # date, update = self.get_date(job_index)
    return (link not in link_set)
  
  def get_link(self):
    try: 
      with open("{}/{}-link.txt".format(self.company, self.company), "r") as f:
        lines = f.read().split("\n")
        a = [line.split("KARAN")[0] for line in lines]
        return a
    except:
      return []
    
  def print_link(self, link, job_index):
    date, _ = self.get_date(job_index)
    return super().print_link_data("KARAN".join([link, date]))

  def print_date(self, job_index):
    date, update = self.get_date(job_index)
    self.print("\n".join([date, update,""]))
    # dt = " ".join(date.text.strip().split(" ")[1:])
    # given_date = datetime.strptime(dt,"%B %d, %Y")
    # today = datetime.today()
    # if (today - given_date).days > 30:
    #   return False
    return True
  
  @staticmethod
  def get_title_and_link(job):
    title = job.text.strip()
    link = job.get_attribute("href")
    return (title, link)

  @staticmethod
  def get_filter_and_excludes():
    filters = ["Software Engineer",
              "Software Developer",
              "2025"]
    
    exclude_titles = ["Senior",
                      "Staff",
                      "Mobile",
                      "Android",
                      "iOS",
                      "Manager",
                      "PhD",
                      "Front End",
                      "Analyst",
                      "Co-op",
                      "Business Intelligence Engineer",
                      "Flow Lead, Central Flow",
                      "Data Center Technician",
                      "Customs Brokerage Specialist",
                      "Interim Ship Clerk"
                      ]
    
    exclude_descriptions = ["Coding experience in either iOS or Android",
                            "Must be enrolled in a full-time degree program at time of application and returning to school after the internship"
                            ]
    for i in range(5,11):
      exclude_descriptions.append("{} years".format(i))
      exclude_descriptions.append("{}+ years".format(i))
      exclude_descriptions.append("{} or more years".format(i))
    
    return (filters, exclude_titles, exclude_descriptions)

  @staticmethod
  def get_base_url():
    return [
            "https://www.amazon.jobs/en/search?base_query=%22{}%22&offset={}&result_limit=10&sort=recent&distanceType=Mi&radius=80km&industry_experience=less_than_1_year&latitude=38.89036&longitude=-77.03196&loc_group_id=&loc_query=United%20States&city=&country=USA&region=&county=&query_options=&",
            "https://www.amazon.jobs/en/search?base_query=%22{}%22&offset={}&result_limit=10&sort=recent&distanceType=Mi&radius=80km&industry_experience=one_to_three_years&latitude=38.89036&longitude=-77.03196&loc_group_id=&loc_query=United%20States&city=&country=USA&region=&county=&query_options=&"
            ]
  
  @staticmethod
  def get_start_pageID():
    return 0
  
  @staticmethod
  def get_page_increement():
    return 10
  
  @staticmethod
  def get_max_pages():
    return 20