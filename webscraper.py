from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from helpers import Apple, Meta, Google, Remitly, Microsoft, Amazon, Oracle, PaloAlto, Paypal, Walmart, Adobe, Broadcom, IBM, Intel, Nvidia, RedHat, Suse, Visa, Qualcomm, ByteDance
from defs import *
from urllib.parse import quote
from datetime import datetime
import traceback

def print_job_titles_and_links(company: Qualcomm, jobs):
  for i, job in enumerate(jobs):
    title, link = company.get_title_and_link(job)
    # print("{}. Title: {}, Link: {}, Date: {}".format(i+1, title, link, company.get_date(i)))
    print("{}. Title: {}, Link: {}".format(i+1, title, link))

def check_and_get_quals(company: Broadcom, link, exclude_description, qual_type):
  quals = company.get_qualifications(link, qual_type)
  desc = []
  for qual in quals:
    desc.append(qual)
    if any(desc in qual for desc in exclude_description):
      return (True, desc)
  return (False, desc)

def output_jobs(company: Broadcom, filter, exclude_titles, exclude_descriptions):
  link_set = set(company.get_link())
  base_urls = company.get_base_url()
  quals = company.get_quals()

  company.print("\n✅ Filtered Job Titles with filter: {}: \n".format(filter))

  for i, base_url in enumerate(base_urls):
    total_jobs = 0
    total_filtered_jobs = 0
    page = company.get_start_pageID()
    counter = 1
    date_counter = 1
    date_check = True

    company.print("🔗 BASE_URL {}\n".format(i+1))
    while True:
      desc_dict = {}

      # print(page)
      if page > company.get_max_pages():
        break
      # print("Fetching page starting at: {}\n\n".format(page))
      url = company.get_url(base_url, filter, page)
      # print(url)
      try:
        jobs = company.get_jobs(url)
      except Exception as e:
        company.print(f"Verify URL: {url}")
        company.print("")
        # for i, job in enumerate(company.job_list):
        #   print("{} : {}".format(i+1,job))
        # print("Error type:", type(e).__name__)
        break

      if not jobs:
        break

      # print("Page: {}".format(page))
      print_job_titles_and_links(company, jobs)

      for j, job in enumerate(jobs):
        try:
          title, link = company.get_title_and_link(job)
        except Exception as e:
              company.print(f"ERROR: url: {url}")
              company.print("")
              print("ERROR in getting Title/Link Company: {}\n".format(company.company))
              print("Error : {}".format(e))
              return
        company.set_link(link)
        total_jobs += 1
        if title and company.check_link(link, link_set, j):
          total_filtered_jobs += 1
          company.print_link(link, j)
          company.add_link(link, link_set, j)
          if not any(ex in title for ex in exclude_titles):
            flag = True
            flag_error = False
            for qual in quals:
              try:
                descs = []
                flag, descs = check_and_get_quals(company, link, exclude_descriptions, qual)
              except Exception as e:
                company.print(f"ERROR title: {title}")
                company.print(f"ERROR: link: {link}")
                company.print(f"ERROR: url: {url}")
                company.print(f"ERROR: qual_type: {qual}")
                company.print("")
                print("ERROR SEEN")
                print("Error type:", type(e).__name__)
                # traceback.print_exc()
                # exit()
                flag_error = True
                break
              if flag:
                company.print_exclude_desc(title, link, descs)
                break
              if flag_error:
                break
              desc_dict[qual] = descs
            
            if flag or flag_error:
              # company.add_link(link, link_set, j)
              # link_set.add(link)
              continue

            company.print("{}) ({}) {}".format(counter, date_counter, title))
            company.print_date(j)
            company.print(link)

            for qual in quals:
              company.print("{}: ".format(qual))
              for desc in desc_dict[qual]:
                company.print("* {}".format(desc))
              company.print("")

            company.print("-"*110+"\n")
            counter += 1

            if not company.check_date(j):
              date_check = False
              break
          # if not date_check:
          #   break
          elif any(ex in title for ex in exclude_titles):
            company.print_exlucde_title(title)
        date_counter += 1
            
      page += company.get_page_increement()
      if not date_check:
        break
    print("{} Total jobs: {} / {} / {}".format(company.company.upper(),counter-1, total_filtered_jobs, total_jobs))
   

def run_script(company: Walmart):
  try:

    child_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=company.get_child_options())
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=company.get_parent_options())

    company.set_drivers(driver, child_driver)
    
    filters, exclude_titles, exclude_descriptions = company.get_filter_and_excludes()

    company.reset_files()
    company.print_link_data(datetime.today().strftime("%B %d, %Y %H:%M:%S"))

    for filter in filters:
      output_jobs(company, quote(filter), exclude_titles, exclude_descriptions)
    print()

  finally:
    if driver:
      driver.quit()
    if child_driver:
      child_driver.quit()







if __name__ == "__main__":
  run_script(Adobe())
  run_script(Amazon())
  run_script(Apple())
  run_script(Broadcom())
  run_script(ByteDance())
  run_script(Google())
  run_script(IBM())
  run_script(Intel())
  run_script(Meta())
  run_script(Microsoft())
  run_script(Nvidia())
  run_script(Paypal())
  run_script(Qualcomm())
  run_script(RedHat())
  run_script(Suse())
  run_script(Visa())
  run_script(Oracle())
  run_script(Remitly())
  
  
  
