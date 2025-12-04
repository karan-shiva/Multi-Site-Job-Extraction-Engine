
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from defs import *
from helpers.helper import Base
from types import SimpleNamespace

class Meta(Base):
  company = "meta"

  def get_jobs(self, url):
      self.driver.get(url)
      WebDriverWait(self.driver, 5).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, "a.x1ypdohk[target='_blank']"))
      )
      
      return self.driver.find_elements(By.CSS_SELECTOR, "a.x1ypdohk[target='_blank']")

  def get_li_elements(self, link, qual_type):
    qual = "Minimum Qualifications" if qual_type == MIN_QUAL else "Preferred Qualifications"

    self.child_driver.get(link)
    try:
      WebDriverWait(self.child_driver, 5).until(
            EC.presence_of_element_located((By.XPATH,".//div[contains(text(), '{}')]".format(qual)))
        )

      qual_header = self.child_driver.find_element(By.XPATH,".//div[contains(text(), '{}')]".format(qual))
      ul = qual_header.find_element(By.XPATH, "following::ul")
      return ul.find_elements(By.TAG_NAME, "li")
    except Exception as e:
      if qual_type == PREF_QUAL:
        return [SimpleNamespace(text="No Preferred Qualifications")]
      else:
        raise

  
  @staticmethod
  def get_title_and_link(job):
    title = job.text.strip().split("\n")[0].strip()
    link = job.get_attribute("href")
    return (title, link)

  @staticmethod
  def get_filter_and_excludes():
    filters = ["Software Engineer",
              "Software Developer",
              "University Grad"]
    
    exclude_titles = ["Senior",
                      "Staff",
                      "Mobile",
                      "Android",
                      "iOS",
                      "Manager",
                      "PhD",
                      "Front End",
                      "Electrical Engineer",
                      "Research Engineer",
                      "Research Scientist",
                      "QA Engineering Lead",
                      "Metrology Engineer",
                      "Image Sensor Validation Engineer",
                      "ASIC Engineer",
                      "Optical Engineer"
                      ]
    
    exclude_descriptions = ["Building large-scale infrastructure applications",
                            "Currently enrolled in a full-time, degree-seeking program and in the process of obtaining a Bachelors or Masters degree in",
                            "US Citizenship and the ability to obtain and maintain a United States Security Clearance"
                          ]
    for i in range(5,11):
      exclude_descriptions.append("{} years".format(i))
      exclude_descriptions.append("{}+ years".format(i))
      exclude_descriptions.append("{} or more years".format(i))
    
    return (filters, exclude_titles, exclude_descriptions)
  
  @staticmethod
  def get_max_pages():
    return 5

  @staticmethod
  def get_base_url():
    return ["https://www.metacareers.com/jobs?sort_by_new=true&offices[0]=Aiken%2C%20SC&offices[1]=Altoona%2C%20IA&offices[2]=Ashburn%2C%20VA&offices[3]=Atlanta%2C%20GA&offices[4]=Aurora%2C%20IL&offices[5]=Austin%2C%20TX&offices[6]=Bellevue%2C%20WA&offices[7]=Washington%2C%20DC&offices[8]=Boston%2C%20MA&offices[9]=Burlingame%2C%20CA&offices[10]=Cambridge%2C%20MA&offices[11]=Chandler%2C%20AZ&offices[12]=Cheyenne%2C%20WY&offices[13]=Chicago%2C%20IL&offices[14]=Crook%20County%2C%20OR&offices[15]=DeKalb%2C%20IL&offices[16]=Denver%2C%20CO&offices[17]=Detroit%2C%20MI&offices[18]=Durham%2C%20NC&offices[19]=Eagle%20Mountain%2C%20UT&offices[20]=Forest%20City%2C%20NC&offices[21]=Fort%20Worth%2C%20TX&offices[22]=Foster%20City%2C%20CA&offices[23]=Fremont%2C%20CA&offices[24]=Gallatin%2C%20TN&offices[25]=Garland%2C%20TX&offices[26]=Henrico%2C%20VA&offices[27]=Hillsboro%2C%20OR&offices[28]=Houston%2C%20TX&offices[29]=Huntsville%2C%20AL&offices[30]=Irvine%2C%20CA&offices[31]=Jeffersonville%2C%20IN&offices[32]=Kansas%20City%2C%20MO&offices[33]=Kuna%2C%20ID&offices[34]=Los%20Angeles%2C%20CA&offices[35]=Los%20Lunas%2C%20NM&offices[36]=Loudoun%20County%2C%20VA&offices[37]=Louisville%2C%20CO&offices[38]=Menlo%20Park%2C%20CA&offices[39]=Mesa%2C%20AZ&offices[40]=Miami%2C%20Florida&offices[41]=Montgomery%2C%20AL&offices[42]=Mountain%20View%2C%20CA&offices[43]=New%20Albany%2C%20OH&offices[44]=New%20York%2C%20NY&offices[45]=Newark%2C%20CA&offices[46]=Newark%2C%20OH&offices[47]=Newton%20County%2C%20GA&offices[48]=Northridge%2C%20CA&offices[49]=Papillion%2C%20NE&offices[50]=Pittsburgh%2C%20PA&offices[51]=Polk%20County%2C%20IA&offices[52]=Prineville%2C%20OR&offices[53]=Rayville%2C%20LA&offices[54]=Redmond%2C%20WA&offices[55]=Remote%2C%20UK&offices[56]=Remote%2C%20US&offices[57]=Rosemount%2C%20MN&offices[58]=Richmond%2C%20VA&offices[59]=Reston%2C%20VA&offices[60]=Salt%20Lake%2C%20UT&offices[61]=San%20Diego%2C%20CA&offices[62]=San%20Francisco%2C%20CA&offices[63]=San%20Mateo%2C%20CA&offices[64]=Sandston%2C%20VA&offices[65]=Santa%20Clara%2C%20CA&offices[66]=Sarpy%20County%2C%20NE&offices[67]=Sausalito%2C%20CA&offices[68]=Seattle%2C%20WA&offices[69]=Stanton%20Springs%2C%20GA&offices[70]=Sterling%2C%20VA&offices[71]=Sunnyvale%2C%20CA&offices[72]=Temple%2C%20TX&offices[73]=Utah%20County%2C%20UT&offices[74]=Valencia%2C%20NM&offices[75]=Vancouver%2C%20WA&q=%22{}%22&page={}"]