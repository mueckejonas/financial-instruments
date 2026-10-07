# %%
from edgar import Company, set_identity
import pandas as pd
import plotly.graph_objs as go
from google import genai
import json
from datetime import datetime
import os
from pathlib import Path
from IPython.utils import io
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import undetected_chromedriver as uc
from selenium import webdriver
import pymupdf
from google.genai import types
import pydantic
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from edgar import Company, set_identity
import pandas as pd
import plotly.graph_objs as go
from google import genai
import json
from datetime import datetime
import os
from pathlib import Path
from IPython.utils import io
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import undetected_chromedriver as uc
from selenium import webdriver
import pymupdf
from google.genai import types
import pydantic
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import math
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.svm import SVR
from sklearn.metrics import classification_report, confusion_matrix
import xgboost as xgb
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from IPython.display import display
import matplotlib.pyplot as plt
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from xgboost import XGBRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.inspection import permutation_importance
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix, classification_report, RocCurveDisplay
import streamlit as st
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.base import BaseEstimator, ClassifierMixin

# %%
class CompetitiveAdvantageItem(pydantic.BaseModel):
    Competitive_Advantage: str  # maps to your key name
    Grade: float
    Summary: str

# %%
class CompetitiveAdvantageDevelopment(pydantic.BaseModel):
    Competitive_Advantage: str  # maps to your key name
    Grade: float

# %%
def get_samsung_quarterly_reports():
    url = "https://www.samsung.com/global/ir/financial-information/audited-financial-statements/"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all('a')

    counter = 0


    for link in links:
        if ('_all.pdf' in link.get('href', [])) and (counter < 12):
            link_elements = link.get('href').split("/")
            link_name = link_elements[-1:][0]

            response = requests.get("https:"+link.get('href'))

            # Write content in pdf file
            pdf = open(link_name, 'wb')
            pdf.write(response.content)
            pdf.close()
            counter += 1

# %%
def get_tcehy_quarterly_reports():
    url = "https://www.tencent.com/en-us/investors/quarter-result.html"

    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all('a')

    counter = 0

    for link in links:
        if ('.pdf' in link.get('href', [])) and (counter < 12):
            if (link.text).strip() == "Earnings Releases":
                link_elements = link.get('href').split("/")
                link_name = link_elements[4]+"_"+link_elements[5]+"_"+link_elements[6]+"_"+"quarterly_reports"

                response = requests.get(link.get('href'))

                # Write content in pdf file
                pdf = open(link_name+".pdf", 'wb')
                pdf.write(response.content)
                pdf.close()
                counter += 1

# %%
def get_asml_quarterly_reports():
    url = "https://www.asml.com/en/investors/financial-results/"

    #https://www.asml.com/en/investors/financial-results/q1-2026

    years = [str(datetime.today().year), str(datetime.today().year-1), str(datetime.today().year-2), str(datetime.today().year-3)]
    quarters = ["q4", "q3", "q2", "q1"]

    for year in years:
        for quarter in quarters:
            response = requests.get(url+quarter+"-"+year)

            soup = BeautifulSoup(response.text, 'html.parser')

            links = soup.find_all('a')

            for link in links:
                if ("Financial-statements-US-GAAP-"+quarter.upper()+"-"+year+".pdf" in link.get('href', [])):
                    name = "Financial-statements-US-GAAP-"+quarter.upper()+"-"+year

                    response = requests.get(link.get('href'))

                    # Write content in pdf file
                    pdf = open(name+".pdf", 'wb')
                    pdf.write(response.content)
                    pdf.close()

# %%
def get_hynix_quarterly_reports():

    #pdf Download SK hynix FY2025 Q4

    years = [str(datetime.today().year), str(datetime.today().year-1), str(datetime.today().year-2), str(datetime.today().year-3)]
    quarters = ["Q4", "Q3", "Q2", "Q1"]

    options = Options()
    options.add_argument("--headless") # Run without a window

    driver = webdriver.Chrome(options=options)

    driver.get("https://www.skhynix.com/ir/UI-FR-IR06")

    time.sleep(60)

    links = driver.find_elements("xpath", "//a[@href]")

    for link in links:
        for year in years:
            for quarter in quarters:
                if "pdf Download SK hynix FY"+year+" "+quarter in link.text:
                    response = requests.get(link.get_attribute("href"))
                    name = "FY"+year+"_"+quarter+"_report"

                    # Write content in pdf file
                    pdf = open(name+".pdf", 'wb')
                    pdf.write(response.content)
                    pdf.close()
    
    dropdown_element = driver.find_element(By.ID, "yearChk")

    select = Select(dropdown_element)
    select.select_by_value("2024") 

    # 3. Find and click the 'Inquiry' button
    # The image shows it has a class 'btn_check'
    inquiry_button = driver.find_element(By.CLASS_NAME, "btn_check")
    inquiry_button.click()

    # 4. Wait for the list to refresh with 2024 data
    time.sleep(60)

    links = driver.find_elements("xpath", "//a[@href]")

    for link in links:
        for year in years:
            for quarter in quarters:
                if "pdf Download SK hynix FY"+year+" "+quarter in link.text:
                    response = requests.get(link.get_attribute("href"))
                    name = "FY"+year+"_"+quarter+"_report"

                    # Write content in pdf file
                    pdf = open(name+".pdf", 'wb')
                    pdf.write(response.content)
                    pdf.close()

    dropdown_element = driver.find_element(By.ID, "yearChk")

    select = Select(dropdown_element)
    select.select_by_value("2023") 

    # 3. Find and click the 'Inquiry' button
    # The image shows it has a class 'btn_check'
    inquiry_button = driver.find_element(By.CLASS_NAME, "btn_check")
    inquiry_button.click()

    # 4. Wait for the list to refresh with 2024 data
    time.sleep(60)

    links = driver.find_elements("xpath", "//a[@href]")

    for link in links:
        for year in years:
            for quarter in quarters:
                if "pdf Download SK hynix FY"+year+" "+quarter in link.text:
                    response = requests.get(link.get_attribute("href"))
                    name = "FY"+year+"_"+quarter+"_report"

                    # Write content in pdf file
                    pdf = open(name+".pdf", 'wb')
                    pdf.write(response.content)
                    pdf.close()
    driver.quit()

# %%
def get_alibaba_quarterly_reports():

    options = Options()
    options.add_argument("--headless=new") 
    options.add_argument("--window-size=1920,1200")

    driver = webdriver.Chrome(options=options)

    driver.get("https://www.alibabagroup.com/en-US/ir-financial-reports-quarterly-results")

    time.sleep(3)

    cookie_box = driver.find_element(By.CLASS_NAME, "accept-btn")
    cookie_box.click()

    links_high = driver.find_elements("xpath", "//a[@href]")

    for link_high in links_high:
        if "Press Releases" in link_high.text:

            response = requests.get(link_high.get_attribute("href"))

            soup = BeautifulSoup(response.text, 'html.parser')

            links_low = soup.find_all('a')

            for link_low in links_low:
                if (".pdf" in link_low.text):
                    name = link_low.text

                    response = requests.get(link_low.get('href'))

                    # Write content in pdf file
                    pdf = open(name, 'wb')
                    pdf.write(response.content)
                    pdf.close()

    dropdown_elements = driver.find_elements(By.CLASS_NAME, "quarterly-year-item")
    dropdown_elements[1].click()

    time.sleep(3)

    links_high = driver.find_elements("xpath", "//a[@href]")

    for link_high in links_high:
        if "Press Releases" in link_high.text:

            response = requests.get(link_high.get_attribute("href"))

            soup = BeautifulSoup(response.text, 'html.parser')

            links_low = soup.find_all('a')

            for link_low in links_low:
                if (".pdf" in link_low.text):
                    name = link_low.text

                    response = requests.get(link_low.get('href'))

                    # Write content in pdf file
                    pdf = open(name, 'wb')
                    pdf.write(response.content)
                    pdf.close()

    dropdown_elements[2].click()

    time.sleep(3)

    links_high = driver.find_elements("xpath", "//a[@href]")

    for link_high in links_high:
        if "Press Releases" in link_high.text:

            response = requests.get(link_high.get_attribute("href"))

            soup = BeautifulSoup(response.text, 'html.parser')

            links_low = soup.find_all('a')

            for link_low in links_low:
                if (".pdf" in link_low.text):
                    name = link_low.text

                    response = requests.get(link_low.get('href'))

                    # Write content in pdf file
                    pdf = open(name, 'wb')
                    pdf.write(response.content)
                    pdf.close()

    driver.quit()

# %%
def get_roche_quarterly_reports():
    url = "https://www.roche.com/investors/events/"

    #https://www.asml.com/en/investors/financial-results/q1-2026

    years = [str(datetime.today().year), str(datetime.today().year-1), str(datetime.today().year-2), str(datetime.today().year-3)]
    quarters = ["annual-results", "q3", "hy", "q1"]

    for year in years:
        for quarter in quarters:
            response = requests.get(url+quarter+"-"+year)

            soup = BeautifulSoup(response.text, 'html.parser')

            links = soup.find_all('a')

            for link in links:
                if ("Presentation with appendix" in link.text):
                    name = "Report-"+quarter.upper()+"-"+year

                    response = requests.get(link.get('href'))

                    # Write content in pdf file
                    pdf = open(name+".pdf", 'wb')
                    pdf.write(response.content)
                    pdf.close()

# %%
def get_hsbc_quarterly_reports():
   url = "https://www.hsbc.com/investors/results-and-announcements/all-reporting/group?page=1&take=40"

   years = [str(datetime.today().year), str(datetime.today().year-1), str(datetime.today().year-2), str(datetime.today().year-3)]
   reports = []
   for year in years:
       reports.append("-annual-report-and-accounts-"+year+".pdf")
       reports.append("-3q-"+year+"-earnings-release.pdf")
       reports.append("-interim-report-"+year+".pdf")
       reports.append("-1q-"+year+"-earnings-release.pdf")

   response = requests.get(url)

   soup = BeautifulSoup(response.text, 'html.parser')

   links = soup.find_all('a')

   for report in reports:
      for link in links:
            if (report in link.get("href")):
               name = report
               if os.path.exists(name):
                  continue

               response = requests.get("https://www.hsbc.com/"+link.get('href'))

               # Write content in pdf file
               pdf = open(name, 'wb')
               pdf.write(response.content)
               pdf.close()

# %%
def get_novartis_quarterly_reports():
   options = Options()
   options.add_argument("--headless=new") 
   options.add_argument("--window-size=1920,1200")

   driver = webdriver.Chrome(options=options)

   driver.get("https://www.novartis.com/investors/financial-data/quarterly-results")

   time.sleep(3)

   #cookie_boxes = driver.find_elements(By.CLASS_NAME, "nav-link")
   # cookie_boxes.click()

   links = driver.find_elements("xpath", "//a[@href]")

   counter = 0

   for link in links:
      if ("-interim-financial-report-en.pdf" in link.get_attribute("href")) and (counter < 12):
         name = link.get_attribute("href")[50:]

         response = requests.get(link.get_attribute("href"))

         # Write content in pdf file
         pdf = open(name, 'wb')
         pdf.write(response.content)
         pdf.close()
         counter += 1

   driver.quit()

# %%
def get_lvhm_quarterly_reports():
   options = Options()
   #options.add_argument("--headless") 

   driver = webdriver.Chrome(options=options)

   driver.get("https://www.lvmh.com/en/publications")

   time.sleep(3)

   cookie = driver.find_element(By.ID, "onetrust-accept-btn-handler")
   cookie.click()

   buttons = driver.find_elements(By.CLASS_NAME, "py-8")
   for button in buttons:
      try:
         if button.text == "PRESENTATIONS":
            button.click()
      except:
         nothing = "nothing happens"

   links = driver.find_elements("xpath", "//a[@href]")

   counter = 0

   for link in links:
      if ".pdf" in link.get_attribute("href") and (counter < 12):
         if not "esg" in link.get_attribute("href").lower() and not "-va" in link.get_attribute("href").lower():
            name = link.get_attribute("href")[50:].replace("/","")

            response = requests.get(link.get_attribute("href"))

            # Write content in pdf file
            pdf = open(name, 'wb')
            pdf.write(response.content)
            pdf.close()
            counter += 1

   driver.quit()

# %%
def get_toyota_quarterly_reports():    

    years = [str(datetime.today().year), str(datetime.today().year-1), str(datetime.today().year-2), str(datetime.today().year-3)]
    quarters = ["1q", "2q", "3q", "4q"]


    for year in years:
        for quarter in quarters:
            response = requests.get("https://global.toyota/pages/global_toyota/ir/financial-results/"+year+"_"+quarter+"_presentation_en.pdf")

            if not response.status_code == 404: 
                # Write content in pdf file
                pdf = open("Report_"+year+"_"+quarter+".pdf", 'wb')
                pdf.write(response.content)
                pdf.close()

# %%
def get_nestle_quarterly_reports():
    #https://www.nestle.com/media/mediaeventscalendar/allevents/2025-full-year-results

    years = [str(datetime.today().year), str(datetime.today().year-1), str(datetime.today().year-2), str(datetime.today().year-3)]
    quarters = ["three-month-sales", "half-year-results", "nine-month-sales", "full-year-results"]

    url = "https://www.nestle.com/media/mediaeventscalendar/allevents/"

    for year in years:
        for quarter in quarters:
            try:
                driver = uc.Chrome(headless=False,use_subprocess=False)
                #version_main=147 or new version_main=150
                driver.get(url+year+"-"+quarter)

                time.sleep(20)

                cookie = driver.find_element(By.ID, "onetrust-accept-btn-handler")
                cookie.click()

                time.sleep(2)

                links = driver.find_elements("xpath", "//a[@href]")

                for link in links:
                    if quarter in link.get_attribute("href") and "-en.pdf" in link.get_attribute("href"):
                        if link.get_attribute("href")[0] == "/":
                            response = requests.get("https://www.nestle.com/"+link.get_attribute("href"))
                        else:
                            response = requests.get(link.get_attribute("href"))
                        if not response.status_code == 404: 
                            # Write content in pdf file
                            pdf = open(year+"_"+quarter+"_Report.pdf", 'wb')
                            pdf.write(response.content)
                            pdf.close()
                driver.quit()
            except:
                driver = uc.Chrome(headless=False,use_subprocess=False)
                driver.get(url+year+"-"+quarter)

                time.sleep(20)

                cookie = driver.find_element(By.ID, "onetrust-accept-btn-handler")
                cookie.click()

                time.sleep(2)

                links = driver.find_elements("xpath", "//a[@href]")

                for link in links:
                    if quarter in link.get_attribute("href") and "-en.pdf" in link.get_attribute("href"):
                        if link.get_attribute("href")[0] == "/":
                            response = requests.get("https://www.nestle.com/"+link.get_attribute("href"))
                        else:
                            response = requests.get(link.get_attribute("href"))
                        if not response.status_code == 404: 
                            # Write content in pdf file
                            pdf = open(year+"_"+quarter+"_Report.pdf", 'wb')
                            pdf.write(response.content)
                            pdf.close()
                driver.quit()

# %%
def get_rbc_quarterly_reports():
    #https://www.rbc.com/investor-relations/financial-information.html
    years = [str(datetime.today().year), str(datetime.today().year-1), str(datetime.today().year-2), str(datetime.today().year-3)]
    quarters = ["q1","q2","q3","q4"]

    for year in years:
        for quarter in quarters:
             
             response = requests.get("https://www.rbc.com/investor-relations/_assets-custom/pdf/"+year+quarter+"release.pdf")
             if not response.status_code == 404: 
                        # Write content in pdf file
                        pdf = open(year+"_"+quarter+"_Report.pdf", 'wb')
                        pdf.write(response.content)
                        pdf.close()

# %%
def get_shell_quarterly_reports():
#https://www.shell.com/investors/results-and-reporting/quarterly-results.html#tab-2025
    years = [str(datetime.today().year), str(datetime.today().year-1), str(datetime.today().year-2), str(datetime.today().year-3)]

    for year in years:

        driver = uc.Chrome(headless=False,use_subprocess=False)
        driver.get("https://www.shell.com/investors/results-and-reporting/quarterly-results.html#tab-"+year)

        time.sleep(3)

        links = driver.find_elements("xpath", "//a[@href]")

        for link in links:
            if year+"-qra-document.pdf" in link.get_attribute("href"):
                response = requests.get(link.get_attribute("href"))
                if not response.status_code == 404: 
                    # Write content in pdf file
                    name = link.get_attribute("href").split("/")[-1]
                    pdf = open(name, 'wb')
                    pdf.write(response.content)
                    pdf.close()
        driver.quit()

# %%
def get_siemens_quarterly_reports():

    driver = uc.Chrome(headless=False,use_subprocess=False)
    driver.get("https://www.siemens.com/de-de/company/investor-relations/financial-results/")

    time.sleep(3)

    links = driver.find_elements("xpath", "//a[@href]")

    counter = 0 

    for link in links:
        if "-earnings-release-de.pdf" in link.get_attribute("href") and (counter < 12):
            response = requests.get(link.get_attribute("href"))
            if not response.status_code == 404: 
                # Write content in pdf file
                name = link.get_attribute("href").split("/")[-1]
                pdf = open(name, 'wb')
                pdf.write(response.content)
                pdf.close()
                counter += 1

    driver.quit()

# %%
def get_commbank_quarterly_reports():

    driver = uc.Chrome(headless=False,use_subprocess=False)
    driver.get("https://www.commbank.com.au/about-us/investors/results.html")

    time.sleep(3)

    links = driver.find_elements("xpath", "//a[@href]")


    for link in links:
        if "profit-announcement" in link.get_attribute("href").lower() or 'profit%20announcement' in link.get_attribute("href").lower():
            response = requests.get(link.get_attribute("href"))
            if not response.status_code == 404:
                # Write content in pdf file
                name = link.get_attribute("href").split("/")[-1]
                pdf = open(name, 'wb')
                pdf.write(response.content)
                pdf.close()

    driver.quit()

    driver = uc.Chrome(headless=False,use_subprocess=False)
    driver.get("https://www.commbank.com.au/about-us/investors/results/results-archive.html")

    time.sleep(3)

    links = driver.find_elements("xpath", "//a[@href]")

    counter = 0

    for link in links:
        if "profit-announcement" in link.get_attribute("href").lower() or 'profit%20announcement' in link.get_attribute("href").lower():
            if counter < 6:
                response = requests.get(link.get_attribute("href"))
                if not response.status_code == 404:
                    # Write content in pdf file
                    name = link.get_attribute("href").split("/")[-1]
                    pdf = open(name, 'wb')
                    pdf.write(response.content)
                    pdf.close()
                counter += 1

    driver.quit()

# %%
def get_sap_quarterly_reports():
    #https://www.sap.com/docs/download/investors/2026/sap-2026-q1-presentation.pdf

    years = [str(datetime.today().year), str(datetime.today().year-1), str(datetime.today().year-2), str(datetime.today().year-3)]
    quarters = ["q1", "q2", "q3", "q4"]

    for year in years:
        for quarter in quarters:
            download_path = os.getcwd()
            chrome_options = Options()
            prefs = {
                "download.default_directory": download_path,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "plugins.always_open_pdf_externally": True  # This forces the download instead of viewing
            }
            chrome_options.add_experimental_option("prefs", prefs)

            driver = webdriver.Chrome(options=chrome_options)
            driver.get("https://www.sap.com/docs/download/investors/"+year+"/sap-"+year+"-"+quarter+"-presentation.pdf")
            time.sleep(3)
            driver.quit()

# %%
def get_mitsubishi_quarterly_reports():
    #https://www.mitsubishicorp.com/jp/en/ir/library/earnings/fs2025.html
    years = [str(datetime.today().year), str(datetime.today().year-1), str(datetime.today().year-2), str(datetime.today().year-3)]

    for year in years:    
        driver = uc.Chrome(headless=False,use_subprocess=False)
        driver.get("https://www.mitsubishicorp.com/jp/en/ir/library/earnings/fs"+year+".html")

        time.sleep(3)

        links = driver.find_elements("xpath", "//a[@href]")

        counter = 0

        for link in links:
            if ("e.pdf" in link.get_attribute("href")) and ("earnings" in link.get_attribute("href")):
                link_elements = link.get_attribute("href").split("/")
                link_name = link_elements[-1:][0].split("?")[0]

                response = requests.get("https://www.mitsubishicorp.com/"+link.get_attribute("href"))

                # Write content in pdf file
                pdf = open(link_name, 'wb')
                pdf.write(response.content)
                pdf.close()
                counter += 1

        driver.quit()


# %%
def get_santander_quarterly_reports():
    options = Options()
    #options.add_argument("--headless")

    #https://www.santander.com/en/shareholders-and-investors/financial-and-economic-information/quarterly-results
    years = [str(datetime.today().year), str(datetime.today().year-1), str(datetime.today().year-2), str(datetime.today().year-3)]

    driver = webdriver.Chrome(options=options)

    driver.get("https://www.santander.com/en/shareholders-and-investors/financial-and-economic-information/quarterly-results")

    time.sleep(3)

    try:
        driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
    except:
        nothing = "nothing"

    for year in years:

        time.sleep(1)

        year_dropdown = driver.find_element(By.CSS_SELECTOR, ".dropdown__container--filter.anio .dropdown-toggle")
        year_dropdown.click()

        time.sleep(1)

        year_dropdown_select = driver.find_element(By.ID, year)
        year_dropdown_select.click()

        time.sleep(1)

        quarter_dropdown = driver.find_element(By.CSS_SELECTOR, ".dropdown__container--filter.trimes .dropdown-toggle")
        quarter_dropdown.click()

        time.sleep(1)

        quarter_dropdown_select = driver.find_element(By.ID, "all")
        quarter_dropdown_select.click()

        links = driver.find_elements("xpath", "//a[@href]")

        for link in links:
            if "-banco-santander-financial-report-en.pdf" in link.get_attribute("href"):
                    link_elements = link.get_attribute("href").split("/")
                    link_name = link_elements[-1:][0]

                    response = requests.get(link.get_attribute("href"))

                    # Write content in pdf file
                    pdf = open(link_name, 'wb')
                    pdf.write(response.content)
                    pdf.close()

    driver.quit()

# %%
def get_novonordisk_quarterly_reports():
#https://www.novonordisk.com/investors/financial-results.html
    options = Options()
    #options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)

    driver.get("https://www.novonordisk.com/investors/financial-results.html")

    links = driver.find_elements("xpath", "//a[@href]")

    counter = 0 

    for link in links:
        if counter < 12:
            if ("-investor-presentation" in link.get_attribute("href") and ".pdf" in link.get_attribute("href")) or "-2023-presentation.pdf" in link.get_attribute("href"):
                link_elements = link.get_attribute("href").split("/")
                link_name = link_elements[-1:][0]

                response = requests.get(link.get_attribute("href"))

                # Write content in pdf file
                pdf = open(link_name, 'wb')
                pdf.write(response.content)
                pdf.close()
                counter += 1

    driver.quit()

# %%
def get_canadatrust_quarterly_reports():
    #https://www.td.com/ca/en/about-td/for-investors/investor-relations/financial-information/financial-reports/quarterly-results/quarterly-results-2023

    years = [str(datetime.today().year-1), str(datetime.today().year-2), str(datetime.today().year-3)]

    driver = uc.Chrome(headless=False,use_subprocess=False)
    driver.get("https://www.td.com/ca/en/about-td/for-investors/investor-relations/financial-information/financial-reports/quarterly-results/")

    time.sleep(3)

    links = driver.find_elements("xpath", "//a[@href]")

    for link in links:
        if "-results-presentation" in link.get_attribute("href") and ".pdf" in link.get_attribute("href"):
            link_elements = link.get_attribute("href").split("/")
            link_name = link_elements[-1:][0]

            response = requests.get(link.get_attribute("href"))

            # Write content in pdf file
            pdf = open(link_name, 'wb')
            pdf.write(response.content)
            pdf.close()

    driver.quit()

    for year in years:
        driver = uc.Chrome(headless=False,use_subprocess=False)
        driver.get("https://www.td.com/ca/en/about-td/for-investors/investor-relations/financial-information/financial-reports/quarterly-results/quarterly-results-"+year)

        time.sleep(3)

        links = driver.find_elements("xpath", "//a[@href]")

        for link in links:
            if "-results-presentation" in link.get_attribute("href") and ".pdf" in link.get_attribute("href"):
                link_elements = link.get_attribute("href").split("/")
                link_name = link_elements[-1:][0]

                response = requests.get(link.get_attribute("href"))

                # Write content in pdf file
                pdf = open(link_name, 'wb')
                pdf.write(response.content)
                pdf.close()

        driver.quit()

# %%
def get_allianz_quarterly_reports():
#https://www.allianz.com/en/investor_relations/results-reports/results.html

    driver = uc.Chrome(headless=False,use_subprocess=False)
    driver.get("https://www.allianz.com/en/investor_relations/results-reports/results.html")

    time.sleep(3)

    cookie = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    cookie.click()

    time.sleep(1)

    links = driver.find_elements("xpath", "//a[@href]")

    counter = 0

    for link in links:
        if counter < 12:
            if ("earnings-release" in link.get_attribute("href") or "ir-release" in link.get_attribute("href")) and ".pdf" in link.get_attribute("href"):
                link_elements = link.get_attribute("href").split("/")
                link_name = link_elements[-1:][0]

                response = requests.get(link.get_attribute("href"))

                # Write content in pdf file
                pdf = open(link_name, 'wb')
                pdf.write(response.content)
                pdf.close()
                counter += 1

    driver.quit()

# %%
def get_tsmc_quarterly_reports():
    #https://investor.tsmc.com/english/quarterly-results/2025/q2

    years = [str(datetime.today().year), str(datetime.today().year-1), str(datetime.today().year-2), str(datetime.today().year-3)]
    quarters = ["q1", "q2", "q3", "q4"]

    for year in years:
        for quarter in quarters:
            driver = uc.Chrome(headless=False,use_subprocess=False)
            driver.get("https://investor.tsmc.com/english/quarterly-results/"+year+"/"+quarter)

            time.sleep(1)

            links = driver.find_elements("xpath", "//a[@href]")

            for link in links:
                if "FS.pdf" in link.get_attribute("href"):
                    download_path = os.getcwd()
                    chrome_options = Options()
                    prefs = {
                        "download.default_directory": download_path,
                        "download.prompt_for_download": False,
                        "download.directory_upgrade": True,
                        "plugins.always_open_pdf_externally": True  # This forces the download instead of viewing
                    }
                    chrome_options.add_experimental_option("prefs", prefs)

                    download_driver = webdriver.Chrome(options=chrome_options)
                    download_driver.get(link.get_attribute("href"))
                    time.sleep(3)
                    download_driver.quit()

            driver.quit()

# %%
def get_astrazenca_quarterly_reports():
    #https://www.astrazeneca.com/investor-relations/results-and-presentations.html#2026-0

    driver = uc.Chrome(headless=False,use_subprocess=False)
    driver.get("https://www.astrazeneca.com/investor-relations/results-and-presentations.html")

    time.sleep(3)

    links = driver.find_elements("xpath", "//a[@href]")

    counter = 0

    for link in links:
        if counter < 12:
            if "-results-presentation.pdf" in link.get_attribute("href"):
                download_path = os.getcwd()
                chrome_options = Options()
                prefs = {
                    "download.default_directory": download_path,
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "plugins.always_open_pdf_externally": True  # This forces the download instead of viewing
                }
                chrome_options.add_experimental_option("prefs", prefs)

                download_driver = webdriver.Chrome(options=chrome_options)
                download_driver.get(link.get_attribute("href"))
                time.sleep(3)
                download_driver.quit()
                counter += 1

    driver.quit()

# %%
def get_sony_quarterly_reports():
    #https://www.sony.com/en/SonyInfo/IR/library/presen/er/archive.html

    driver = uc.Chrome(headless=False,use_subprocess=False)
    driver.get("https://www.sony.com/en/SonyInfo/IR/library/presen/er/archive.html")

    time.sleep(3)

    links = driver.find_elements("xpath", "//a[@href]")

    counter = 0

    for link in links:
        if counter < 12:
            if "Financial Statements" in link.text:
                download_path = os.getcwd()
                chrome_options = Options()
                prefs = {
                    "download.default_directory": download_path,
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "plugins.always_open_pdf_externally": True  # This forces the download instead of viewing
                }
                chrome_options.add_experimental_option("prefs", prefs)

                download_driver = webdriver.Chrome(options=chrome_options)
                download_driver.get(link.get_attribute("href"))
                time.sleep(3)
                download_driver.quit()
                counter += 1

    driver.quit()

# %%
def get_shopify_quarterly_reports():
    #https://www.shopify.com/investors/quarterly-results

    years = [str(datetime.today().year), str(datetime.today().year-1), str(datetime.today().year-2), str(datetime.today().year-3)]

    driver = uc.Chrome(headless=False,use_subprocess=False)
    driver.get("https://www.shopify.com/investors/quarterly-results")

    time.sleep(3)

    for year in years:
        button = driver.find_element(By.ID, "year-tab-"+year)
        button.click()

        time.sleep(1)

        span_elements = driver.find_elements(By.XPATH, "//span[text()='Download 10-Q']")

        for span_element in span_elements:
            pdf_link_element = span_element.find_element(By.XPATH, "./following-sibling::div//a[.//p[text()='PDF']]")

            pdf_url = pdf_link_element.get_attribute("href")

            download_path = os.getcwd()
            download_chrome_options = Options()
            download_prefs = {
                "download.default_directory": download_path,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "plugins.always_open_pdf_externally": True  # This forces the download instead of viewing
            }
            download_chrome_options.add_experimental_option("prefs", download_prefs)

            download_driver = webdriver.Chrome(options=download_chrome_options)
            download_driver.get(pdf_url)
            time.sleep(1)
            download_driver.quit()

        span_elements = driver.find_elements(By.XPATH, "//span[text()='Download 10-K']")

        for span_element in span_elements:
            pdf_link_element = span_element.find_element(By.XPATH, "./following-sibling::div//a[.//p[text()='PDF']]")

            pdf_url = pdf_link_element.get_attribute("href")

            download_path = os.getcwd()
            download_chrome_options = Options()
            download_prefs = {
                "download.default_directory": download_path,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "plugins.always_open_pdf_externally": True  # This forces the download instead of viewing
            }
            download_chrome_options.add_experimental_option("prefs", download_prefs)

            download_driver = webdriver.Chrome(options=download_chrome_options)
            download_driver.get(pdf_url)
            time.sleep(1)
            download_driver.quit()

        time.sleep(1)

    driver.quit()

# %%
def get_quarterly_reports_texts_from_SEC(ticker):
    set_identity("Jonas Muecke mail@jonasmuecke.com")
    company = Company(ticker)

    all_filings = []

    if ticker == "BLK":
        BLK_New = "0002012383"
        BLK_Old = "0001364742"
        #Get new reports
        new_company = Company(BLK_New)

        #Get the Q filings
        Q_filings = new_company.get_filings(form="10-Q")
        counter = 0
        for i in Q_filings:
            if (i.form == "10-Q") and (counter < 12):
                all_filings.append(i)
                counter += 1

        #Get the K filings
        K_filings = new_company.get_filings(form="10-K")
        counter = 0
        for i in K_filings:
            if (i.form == "10-K") and (counter < 3):
                all_filings.append(i)
                counter += 1
        #Get old reports
        old_company = Company(BLK_Old)

        #Get the Q filings
        Q_filings = old_company.get_filings(form="10-Q")
        counter = 0
        for i in Q_filings:
            if (i.form == "10-Q") and (counter < 12):
                all_filings.append(i)
                counter += 1

        #Get the K filings
        K_filings = old_company.get_filings(form="10-K")
        counter = 0
        for i in K_filings:
            if (i.form == "10-K") and (counter < 3):
                all_filings.append(i)
                counter += 1
    else:
        #Get the Q filings
        Q_filings = company.get_filings(form="10-Q")
        counter = 0
        for i in Q_filings:
            if (i.form == "10-Q") and (counter < 12):
                all_filings.append(i)
                counter += 1

        #Get the K filings
        K_filings = company.get_filings(form="10-K")
        counter = 0
        for i in K_filings:
            if (i.form == "10-K") and (counter < 3):
                all_filings.append(i)
                counter += 1

    #Sort the Q and K filings by the publishing date
    def sort_func(filing):
        return datetime.strptime(filing.report_date, "%Y-%m-%d").date()
    
    all_filings.sort(key=sort_func)

    #Extract the text for all filings in the sorted list
    all_filings_texts = []

    for i in all_filings:
        with io.capture_output() as captured:
            all_filings_texts.append([ticker+"-"+i.report_date+"-"+i.form,i.text()])

    for i in all_filings_texts:
        with open(str(i[0])+".txt", "w", encoding="utf-8") as f:
            f.write(i[1])

# %%
def download_ticker_reports(ticker):
        directory_name_base = "Tickers"
        original_dir_base = os.getcwd()
        os.chdir(directory_name_base)
        time.sleep(12)
        directory_name = ticker
        Path(directory_name).mkdir(parents=True, exist_ok=True)
        original_dir = os.getcwd()
        os.chdir(directory_name)
        try:
                if ticker == "TSM":
                        get_tsmc_quarterly_reports()
                elif ticker == "005930.KS":
                        get_samsung_quarterly_reports()
                elif ticker == "TCEHY":
                        get_tcehy_quarterly_reports()
                elif ticker == "ASML":
                        get_asml_quarterly_reports()
                elif ticker == "000660.KS":
                        get_hynix_quarterly_reports()
                elif ticker == "9988.HK":
                        get_alibaba_quarterly_reports()
                elif ticker == "RHHBY":
                        get_roche_quarterly_reports()
                elif ticker == "HSBC":
                        get_hsbc_quarterly_reports()
                elif ticker == "AZN":
                        get_astrazenca_quarterly_reports()
                elif ticker == "NVS":
                        get_novartis_quarterly_reports()
                elif ticker == "MC.PA":
                        get_lvhm_quarterly_reports()
                elif ticker == "TM":
                        get_toyota_quarterly_reports()
                elif ticker == "NESN.SW":
                        get_nestle_quarterly_reports()
                elif ticker == "RY.TO":
                        get_rbc_quarterly_reports()
                elif ticker == "SHEL.L":
                        get_shell_quarterly_reports()
                elif ticker == "SIE.DE":
                        get_siemens_quarterly_reports()
                elif ticker == "CBA.AX":
                        get_commbank_quarterly_reports()
                elif ticker == "SAP.DE":
                        get_sap_quarterly_reports()
                elif ticker == "8306.T":
                        get_mitsubishi_quarterly_reports()
                elif ticker == "SAN.MC":  
                        get_santander_quarterly_reports()
                elif ticker == "NOVO-B.CO":
                        get_novonordisk_quarterly_reports()
                elif ticker == "TD.TO":
                        get_canadatrust_quarterly_reports()
                elif ticker == "ALV.DE":
                        get_allianz_quarterly_reports()
                elif ticker == "6758.T":
                        get_sony_quarterly_reports()
                elif ticker == "SHOP.TO":
                        get_shopify_quarterly_reports()
                else:
                        get_quarterly_reports_texts_from_SEC(ticker)
                print("Downloading files for "+ticker+" did worked!")
        except Exception as error:
                print("Downloading files for "+ticker+" did not worked! Because of" + str(error))
        os.chdir(original_dir) 
        os.chdir(original_dir_base)

# %%
def extract_quarterly_reports_date_from_prompt():
    return "You are an expert financial data extraction assistant. Your task is to analyze the attached text, which contains a single SEC financial report (such as Form 10-K or Form 10-Q), and find its official publishing, signing, or filing date. Instructions: Scan the text of the provided report to find the date it was officially completed, signed, or filed with the SEC. This is typically found near the signature block at the very end of the report, or on its cover page. Look specifically for the date next to the executive signatures (e.g., 'Date: May 26, 2023'). Do NOT confuse this with the 'quarterly period ended' date. Convert this date into the strict ISO format: YYYY-MM-DD. CRITICAL CONSTRAINT: You must output ONLY the raw date string in YYYY-MM-DD format. Do not include markdown code blocks, quotes, or any introductory text. For example, if the report's signature date is May 26, 2023, your exact response must be: 2023-05-26 Financial Report Text:"

# %%
def extract_scores_and_summaries_prompt():
    return "Here is your adjusted prompt. I have integrated the strict fallback logic instructing the model to output null for both the grading/calculation and the summary if the necessary data cannot be found in the text. You are an expert financial analyst. Your task is to analyze the provided financial reports for this Corporation and evaluate its competitive advantages. Scan the text to calculate or score the following 16 factors of competitive advantage based ONLY on the provided text. CRITICAL FALLBACK RULE: If the necessary financial statement line items, management commentary, or data points required to calculate or score any factor cannot be found anywhere in the provided annual or quarterly report text, you must explicitly assign a value of null to the 'Grade' key and state 'Information not available in the provided text' in the 'Summary' key. Do not attempt to guess or extrapolate from outside knowledge. For the 5 Quantitative Measures, mathematically calculate the exact decimal ratio from the provided financial statement line items (convert percentages to standard decimal format, e.g., 74.93% becomes 0.7493). For the 11 Qualitative Measures, evaluate management commentary, risk factors, or industry dynamics and assign an analyst scorecard rating as a float value on a scale from 1.0 (Worst/No Advantage) to 10.0 (Best/Absolute Moat). Provide a brief textual summary explanation within the JSON object justifying each calculation, rating, or null assignment. Map each factor to its respective 3-letter abbreviation as follows: Quantitative Measures (Calculate exact decimal values or return null): ROI (Return on Invested Capital) - Divide the companys after-tax operating profit by its total invested capital. GMD (Gross Margin) - Calculate Gross Profit Margin: Gross Profit divided by Total Revenue. Measures structural pricing power. RED (Revenue) - Evaluate top-line expansion velocity: Period-over-period or Year-over-year revenue change relative to baseline revenue. DER (Debt to Equity Ratio) - Calculate Leverage: Total Debt (Short-Term plus Long-Term Debt) divided by Total Shareholders' Equity. LQD (Liquidity Ratio) - Calculate Liquidity Cushion: (Cash & Cash Equivalents plus Marketable Securities) divided by Total Current Liabilities. Qualitative Measures (Assign an analyst scorecard float value from 1.0 to 10.0 or return null): RDI (Research & Development Intensity) - Evaluate commitment to staying ahead of technological obsolescence and software framework priority. CES (Cost Efficiency & Economies of Scale) - Grade structural operating leverage, cross-market architecture reuse, and dilution of corporate overhead. SBI (Strong Brand Identity) - Assess brand premium, corporate thought leadership in infrastructure, and ecosystem loyalty. IPP (Intellectual Property & Patents) - Grade patent portfolio depth, proprietary hardware/software footprint protection, and international IP risks. NEF (The Network Effects) - Evaluate developer ecosystem lock-in, platform dependencies, and developer community scaling. ARC (Exclusive Access to Resources or Distribution Channels) - Assess capacity lock-in, advanced packaging access, and the use of massive prepaids or obligations to dominate raw materials. TEP (Technology Edge & Proprietary Processes) - Grade core architecture introduction velocity, processing performance superiority, and interconnect breakthroughs. HSC (High Switching Costs) - Evaluate ecosystem stickiness, full-stack enterprise software integration friction, and platform dependency. UCC (Unique Company Culture & Top Talent) - Grade research and engineering talent density, talent acquisition trends, and low turnover resilience. ACS (Agility and Superior Customer Service) - Assess operational speed in adjusting to mask/yield issues, supply constraints, or circumventing export controls. NMS (Niche Market Specialization) - Evaluate success in cloning computing platforms into custom adjacent high-value ecosystems (e.g., automotive, healthcare, simulation). Strictly adhere to these rules: Provide your final output ONLY in a valid JSON array format containing exactly sixteen objects. Do not include any introductory text, markdown explanations, conversational text, or notes outside of the JSON block. Use the exact 3-letter abbreviations specified for the 'Competitive Advantage' key names. Include a 'Summary' key in each object detailing the rationale, math, or data omission for that specific metric. Expected Output Format: [ { 'Competitive Advantage': 'ROI', 'Grade': [Insert float decimal value OR null], 'Summary': '[Insert short summary explanation]' }, { 'Competitive Advantage': 'GMD', 'Grade': [Insert float decimal value OR null], 'Summary': '[Insert short summary explanation]' }, { 'Competitive Advantage': 'RED', 'Grade': [Insert float decimal value OR null], 'Summary': '[Insert short summary explanation]' }, { 'Competitive Advantage': 'DER', 'Grade': [Insert float decimal value OR null], 'Summary': '[Insert short summary explanation]' }, { 'Competitive Advantage': 'LQD', 'Grade': [Insert float decimal value OR null], 'Summary': '[Insert short summary explanation]' }, { 'Competitive Advantage': 'RDI', 'Grade': [Insert float score from 1.0 to 10.0 OR null], 'Summary': '[Insert short summary explanation]' }, { 'Competitive Advantage': 'CES', 'Grade': [Insert float score from 1.0 to 10.0 OR null], 'Summary': '[Insert short summary explanation]' }, { 'Competitive Advantage': 'SBI', 'Grade': [Insert float score from 1.0 to 10.0 OR null], 'Summary': '[Insert short summary explanation]' }, { 'Competitive Advantage': 'IPP', 'Grade': [Insert float score from 1.0 to 10.0 OR null], 'Summary': '[Insert short summary explanation]' }, { 'Competitive Advantage': 'NEF', 'Grade': [Insert float score from 1.0 to 10.0 OR null], 'Summary': '[Insert short summary explanation]' }, { 'Competitive Advantage': 'ARC', 'Grade': [Insert float score from 1.0 to 10.0 OR null], 'Summary': '[Insert short summary explanation]' }, { 'Competitive Advantage': 'TEP', 'Grade': [Insert float score from 1.0 to 10.0 OR null], 'Summary': '[Insert short summary explanation]' }, { 'Competitive Advantage': 'HSC', 'Grade': [Insert float score from 1.0 to 10.0 OR null], 'Summary': '[Insert short summary explanation]' }, { 'Competitive Advantage': 'UCC', 'Grade': [Insert float score from 1.0 to 10.0 OR null], 'Summary': '[Insert short summary explanation]' }, { 'Competitive Advantage': 'ACS', 'Grade': [Insert float score from 1.0 to 10.0 OR null], 'Summary': '[Insert short summary explanation]' }, { 'Competitive Advantage': 'NMS', 'Grade': [Insert float score from 1.0 to 10.0 OR null], 'Summary': '[Insert short summary explanation]' } ] Output Requirements: Return ONLY a valid, raw JSON array of objects. Do NOT wrap the JSON in markdown code blocks (e.g., do not use json ... ). Do NOT include any intro text, preamble, trailing notes, or comments. Here is the document text to analyze:"

# %%
def extract_ticker_reports(ticker):
    client = genai.Client(api_key="AIzaSyC68Ue0q-YMeAj0UEotciPbeoSofnOkZQ4")

    directory_name_base = "Tickers"
    original_dir_base = os.getcwd()
    os.chdir(directory_name_base)
    directory_name = ticker
    original_dir = os.getcwd()
    os.chdir(directory_name)
    try:
        text_prompt = extract_scores_and_summaries_prompt()
        filename_prompt = extract_quarterly_reports_date_from_prompt()
        files = [f for f in os.listdir() if f.endswith((".pdf", ".txt"))]
        for i in range(0,len(files)):
            time.sleep(10)
            loop_error = True
            counter = 0
            while loop_error:
                try:
                    if ".pdf" in files[0]:
                        text = ""
                        doc = pymupdf.open(files[i])
                        for page in doc:
                            text += page.get_text()
                        # gemini-2.5-flash-lite Try this one first because it is the most affordable
                        # gemini-3.1-flash-lite Maybe also us this but not sure yet
                        filename_response = client.models.generate_content(
                        model="gemini-2.5-flash-lite", contents=filename_prompt+text
                        )
                        dataframe_response = client.models.generate_content(
                        model="gemini-2.5-flash-lite", contents=text_prompt+text,
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json",
                            response_schema=list[CompetitiveAdvantageItem],
                        )
                        )
                        df = pd.DataFrame(json.loads(dataframe_response.text))
                        df.to_csv(filename_response.text+"_static.csv")
                    elif ".txt" in files[0]:
                        text = ""
                        with open(files[i], "r", encoding="utf-8") as f:
                            text = f.read()
                        
                        # filename_tokens = client.models.count_tokens(
                        #     model="gemini-2.5-flash-lite", contents=text_prompt+text
                        # ).total_tokens
                        #print(filename_tokens)
                        filename_response = client.models.generate_content(
                        model="gemini-2.5-flash-lite", contents=filename_prompt+text
                        )
                        dataframe_response = client.models.generate_content(
                        model="gemini-2.5-flash-lite", contents=text_prompt+text,
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json",
                            response_schema=list[CompetitiveAdvantageItem],
                        )
                        )
                        df = pd.DataFrame(json.loads(dataframe_response.text))
                        df.to_csv(filename_response.text+"_static.csv")
                    loop_error = False
                except Exception as error:
                    print("Creating Dataframes for "+ticker+" did not worked! Because of "+str(error)+" I am trying again!")
                    if counter > 3:
                        loop_error = False
                    else:
                        if getattr(error, 'code', None) != 503:
                            print(getattr(error, 'code', None))
                            counter += 1
                            time.sleep(5)
        print("Creating Dataframes for "+ticker+" did worked!")
    except Exception as error:
        print("Creating Dataframes for "+ticker+" did not worked! Because of "+str(error))
    os.chdir(original_dir)
    os.chdir(original_dir_base)

# %%
def grade_development_reports():
    return "You are an expert financial analyst. Your task is to analyze the historical track record of competitive advantage scores and summaries provided for this Corporation across multiple periods, and evaluate the development and trajectory of its competitive advantages over time. Scan the historical data up until the final period provided. For all 16 factors of competitive advantage (both the quantitative financial ratios and the qualitative dimensions), assign a Development Trajectory Score as a float value on a scale from 1.0 to 10.0 based ONLY on the provided track record: 1.0 to 4.9: Deteriorating / Weakening (The competitive advantage or financial stability is eroding over time). 5.0: Flat / Stable / Stagnant (No meaningful shift in momentum, performance, or competitive positioning). 5.1 to 10.0: Strengthening / Accelerating (The competitive moat is deepening, or financial performance metrics are structural improving). Map each factor to its respective 3-letter abbreviation as follows: Quantitative Measures (Evaluate the trend/trajectory of the calculated decimal ratios): ROI (Return on Invested Capital Development) GMD (Gross Margin Development) RED (Revenue Development) DER (Debt to Equity Ratio Development) LQD (Liquidity Ratio Development) Qualitative Measures (Evaluate the trend/trajectory of the scorecard ratings and supporting commentary): RDI (Research & Development Intensity Development) CES (Cost Efficiency & Economies of Scale Development) SBI (Strong Brand Identity Development) IPP (Intellectual Property & Patents Development) NEF (The Network Effects Development) ARC (Exclusive Access to Resources or Distribution Channels Development) TEP (Technology Edge & Proprietary Processes Development) HSC (High Switching Costs Development) UCC (Unique Company Culture & Top Talent Development) ACS (Agility and Superior Customer Service Development) NMS (Niche Market Specialization Development) Strictly adhere to these rules: Provide your final output ONLY in a valid JSON array format containing exactly sixteen objects. Do not include any introductory text, markdown explanations, conversational text, or notes outside of the JSON block. Use the exact 3-letter abbreviations specified for the 'Competitive Advantage' key names. For the 'Grade' key, output the assigned float score from 1.0 to 10.0 representing the development trajectory. Expected Output Format: [ { 'Competitive Advantage': 'ROI', 'Grade': [Insert float score from 1.0 to 10.0] }, { 'Competitive Advantage': 'GMD', 'Grade': [Insert float score from 1.0 to 10.0] }, { 'Competitive Advantage': 'RED', 'Grade': [Insert float score from 1.0 to 10.0] }, { 'Competitive Advantage': 'DER', 'Grade': [Insert float score from 1.0 to 10.0] }, { 'Competitive Advantage': 'LQD', 'Grade': [Insert float score from 1.0 to 10.0] }, { 'Competitive Advantage': 'RDI', 'Grade': [Insert float score from 1.0 to 10.0] }, { 'Competitive Advantage': 'CES', 'Grade': [Insert float score from 1.0 to 10.0] }, { 'Competitive Advantage': 'SBI', 'Grade': [Insert float score from 1.0 to 10.0] }, { 'Competitive Advantage': 'IPP', 'Grade': [Insert float score from 1.0 to 10.0] }, { 'Competitive Advantage': 'NEF', 'Grade': [Insert float score from 1.0 to 10.0] }, { 'Competitive Advantage': 'ARC', 'Grade': [Insert float score from 1.0 to 10.0] }, { 'Competitive Advantage': 'TEP', 'Grade': [Insert float score from 1.0 to 10.0] }, { 'Competitive Advantage': 'HSC', 'Grade': [Insert float score from 1.0 to 10.0] }, { 'Competitive Advantage': 'UCC', 'Grade': [Insert float score from 1.0 to 10.0] }, { 'Competitive Advantage': 'ACS', 'Grade': [Insert float score from 1.0 to 10.0] }, { 'Competitive Advantage': 'NMS', 'Grade': [Insert float score from 1.0 to 10.0] } ] Output Requirements: Return ONLY a valid, raw JSON array of objects. Do NOT wrap the JSON in markdown code blocks (e.g., do not use json ... ). Do NOT include any intro text, preamble, trailing notes, or comments. Here is the historical track record data containing previous factor ratings and summaries to analyze:"

# %%
def development_grading_ticker_reports(ticker):
    client = genai.Client(api_key="AIzaSyC68Ue0q-YMeAj0UEotciPbeoSofnOkZQ4")

    directory_name_base = "Tickers"
    original_dir_base = os.getcwd()
    os.chdir(directory_name_base)
    directory_name = ticker
    original_dir = os.getcwd()
    os.chdir(directory_name)
    try:
        text_prompt = grade_development_reports()
        files = [f for f in os.listdir() if f.endswith(("_static.csv"))]
        for i in range(0,len(files)):
            time.sleep(10)
            loop_error = True
            counter = 0
            while loop_error:
                try:
                    text = ""
                    for j in range(0,i):
                        df = pd.read_csv(files[j])
                        df_string = df.to_string()
                        text += " Factor Ratings and summaries for the quarter/annual report:"+files[j]
                        text += df_string
                    dataframe_response = client.models.generate_content(
                    model="gemini-2.5-flash-lite", contents=text_prompt+text,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=list[CompetitiveAdvantageDevelopment],
                    )
                    )
                    df = pd.DataFrame(json.loads(dataframe_response.text))
                    df.to_csv(files[i].replace("_static.csv","_dynamic.csv"))
                    loop_error = False
                except Exception as error:
                    print("Creating Dataframes for "+ticker+" did not worked! Because of "+str(error)+" I am trying again!")
                    if counter > 3:
                        loop_error = False
                    else:
                        if getattr(error, 'code', None) != 503:
                            print(getattr(error, 'code', None))
                            counter += 1
                            time.sleep(5)
        print("Creating Dataframes for "+ticker+" did worked!")
    except Exception as error:
        print("Creating Dataframes for "+ticker+" did not worked! Because of "+str(error))
    os.chdir(original_dir)
    os.chdir(original_dir_base)

# %%
def get_sharp_ratio(ticker, date):
    #NVDA
    #2025-02-21
    n_days = 63
    rf_annual = 0.00

    start = pd.to_datetime(date)
    download_end = start + pd.Timedelta(days=int(n_days * 1.5))

    df = yf.download(ticker, start=start, end=download_end, auto_adjust=True, progress=False)

    window = df.iloc[:n_days + 1]
    close = window["Close"].squeeze()

    rets = close.pct_change().dropna()
    rf_daily = rf_annual / 252
    excess = rets - rf_daily

    sharpe = excess.mean() / excess.std(ddof=1)
    return sharpe

# %%
def create_sharpe_ratios(ticker):
    directory_name_base = "Tickers"
    original_dir_base = os.getcwd()
    os.chdir(directory_name_base)
    original_dir = os.getcwd()
    os.chdir(ticker)
    records = []
    try:
        files = os.listdir()
        for file in files:
            if file.endswith("_dynamic.csv") and file != f"{ticker}_sharp_ratios.csv":
                df = pd.read_csv(file)
                sharpe_ratio = get_sharp_ratio(ticker, file.replace("_dynamic.csv",""))
                records.append({"Company": ticker, "date": file.replace("_dynamic.csv",""), "sharpe_ratio": sharpe_ratio,"ROI": df["Grade"][0],"GMD": df["Grade"][1],"RED": df["Grade"][2],"DER": df["Grade"][3],"LQD": df["Grade"][4],"RDI": df["Grade"][5],"CES": df["Grade"][6],"SBI": df["Grade"][7],"IPP": df["Grade"][8],"NEF": df["Grade"][9],"ARC": df["Grade"][10],"TEP": df["Grade"][11],"HSC": df["Grade"][12],"UCC": df["Grade"][13],"ACS": df["Grade"][14],"NMS": df["Grade"][15]})
        df = pd.DataFrame(records, columns=["Company", "date", "sharpe_ratio", "ROI", "GMD", "RED", "DER", "LQD", "RDI", "CES", "SBI", "IPP", "NEF","ARC","TEP","HSC","UCC","ACS","NMS"])
        df.to_csv(ticker+"_sharp_ratios.csv", index=False)
        print("Creating Sharpe Ratios for "+ticker+" did worked!")
    except Exception as error:
        print("Creating Sharp Ratios for "+ticker+" did not worked! Because of "+str(error))
    os.chdir(original_dir)
    os.chdir(original_dir_base)


# %%
def create_sharp_ratios_all_tickers(tickers):
    for i in tickers:
        download_ticker_reports(i)
        extract_ticker_reports(i)
        development_grading_ticker_reports(i)
        create_sharpe_ratios(i)

# %%
def create_all_data_file():
    directory_name_base = "Tickers"
    original_dir_base = os.getcwd()
    os.chdir(directory_name_base)
    folders = os.listdir()
    records = []
    for i in folders:
        original_dir = os.getcwd()
        os.chdir(i)
        files = os.listdir()
        for file in files:
                if file == f"{i}_sharp_ratios.csv":
                    df = pd.read_csv(file)
                    records.append(df)
        os.chdir(original_dir)
    os.chdir(original_dir_base)
    combined = pd.concat(records, ignore_index=True)
    exclude = ["date", "Company", "sharpe_ratio"]
    for col in combined.columns:
        if col not in exclude:
            combined = combined[(combined[col] >= 0) & (combined[col] <= 10)]
    combined.to_csv("Total_sharp_ratios.csv", index=False)

# %%
# =====================================================================
# STREAMLIT INTERFACE  —  "Signal Desk" design across the whole app
# ---------------------------------------------------------------------
# Drop-in replacement for everything below your last pipeline function.
# The Tickers page, Data preview page and sidebar now share the Model
# page's design system (ink-navy heroes, mint-teal accent, mono data
# type, stat cards, numbered sections). ALL computations, widgets and
# behavior are unchanged — only presentation was touched.
#
# Run with:  streamlit run <your_file>.py
# =====================================================================

ALL_TICKERS = [
    "NVDA", "AAPL", "MSFT", "AMZN", "GOOGL", "TSM", "AVGO", "GOOG", "TSLA",
    "META", "BRK-B", "WMT", "005930.KS", "LLY", "JPM", "XOM", "TCEHY", "ASML",
    "JNJ", "000660.KS", "V", "MU", "ORCL", "MA", "AMD", "COST", "NFLX", "BAC",
    "CAT", "ABBV", "CVX", "HD", "PG", "CSCO", "INTC", "9988.HK", "PLTR",
    "LRCX", "RHHBY", "KO", "GE", "HSBC", "AZN", "AMAT", "MS", "UNH", "NVS",
    "MRK", "MC.PA", "TM", "GS", "GEV", "RTX", "NESN.SW", "WFC", "RY.TO",
    "SHEL.L", "PM", "IBM", "KLAC", "C", "AXP", "LIN", "SIE.DE", "MCD",
    "CBA.AX", "PEP", "SAP.DE", "8306.T", "TXN", "TMO", "VZ", "AMGN", "NEE",
    "DIS", "SAN.MC", "APH", "T", "NOVO-B.CO", "TJX", "BA", "TD.TO", "ALV.DE",
    "BLK", "SHOP.TO", "ABT", "CRM", "ISRG", "APP", "SCHW", "UBER", "QCOM",
    "SPGI", "6758.T", "ACN", "INTU", "NOW", "BKNG",
]

ALL_FEATURES = ["ROI", "GMD", "RED", "DER", "LQD", "RDI", "CES", "SBI",
                "IPP", "NEF", "ARC", "TEP", "HSC", "UCC", "ACS", "NMS"]

FEATURE_LABELS = {
    "ROI": "Return on Invested Capital", "GMD": "Gross Margin",
    "RED": "Revenue Development", "DER": "Debt to Equity Ratio",
    "LQD": "Liquidity Ratio", "RDI": "R&D Intensity",
    "CES": "Cost Efficiency & Economies of Scale", "SBI": "Strong Brand Identity",
    "IPP": "Intellectual Property & Patents", "NEF": "Network Effects",
    "ARC": "Exclusive Access to Resources / Distribution",
    "TEP": "Technology Edge & Proprietary Processes",
    "HSC": "High Switching Costs", "UCC": "Unique Culture & Top Talent",
    "ACS": "Agility & Superior Customer Service",
    "NMS": "Niche Market Specialization",
}


# =====================================================================
# APP-WIDE DESIGN SYSTEM — "Signal Desk"
# ---------------------------------------------------------------------
# Ink-navy heroes and stat cards, mint-teal signal accent, periwinkle
# model accent, mono type for every number. Space Grotesk carries
# headings, IBM Plex Mono carries data. All helpers below are
# presentation-only; the numbers they show are computed exactly as
# before.
# =====================================================================

_INK = "#0B1220"
_MUTED = "#5B6B84"
_SIGNAL = "#2DD4BF"      # mint teal  — the app's signature accent
_VIOLET = "#818CF8"      # periwinkle — model identity
_AMBER = "#FBBF24"
_LONG = "#34D399"
_SHORT = "#F87171"

_MODEL_COLOR = {
    "random_forest": _SIGNAL, "xgboost": _VIOLET, "svr": _AMBER,
    "random_forest_clf": _SIGNAL, "xgboost_clf": _VIOLET, "svc_clf": _AMBER,
    "ensemble": "#E879F9", "ensemble_clf": "#E879F9",
}

_APP_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

/* ---------------- global chrome ---------------- */
[data-testid="stAppViewContainer"]{background:#F6F8FB;}
h1,h2,h3{font-family:'Space Grotesk',sans-serif!important;color:#0B1220;letter-spacing:-.01em;}

/* ---------------- sidebar ---------------- */
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0B1220 0%,#0F1D38 70%,#0E2430 100%);border-right:1px solid rgba(45,212,191,.18);}
[data-testid="stSidebar"] p,[data-testid="stSidebar"] label,[data-testid="stSidebar"] span{color:#C9D4E6;}
[data-testid="stSidebar"] .stRadio label p{font-family:'Space Grotesk',sans-serif;font-size:.95rem;font-weight:500;}
.sb-brand{padding:4px 0 14px;border-bottom:1px solid rgba(143,160,188,.25);margin-bottom:14px;}
.sb-eyebrow{font-family:'IBM Plex Mono',monospace;font-size:.6rem;letter-spacing:.3em;color:#2DD4BF;text-transform:uppercase;}
.sb-title{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:1.12rem;color:#E7ECF5;margin-top:5px;line-height:1.25;}
.sb-label{font-family:'IBM Plex Mono',monospace;font-size:.6rem;letter-spacing:.26em;color:#7C8CA8;text-transform:uppercase;margin:18px 0 4px;}
.sb-steps{display:flex;flex-direction:column;gap:6px;margin-top:8px;padding-bottom:10px;}
.sb-step{font-family:'IBM Plex Mono',monospace;font-size:.68rem;color:#8FA0BC;letter-spacing:.04em;}
.sb-step b{color:#2DD4BF;font-weight:600;margin-right:8px;}

/* ---------------- buttons ---------------- */
.stButton>button{border-radius:10px;font-family:'Space Grotesk',sans-serif;font-weight:600;border:1px solid #D5DCE8;background:#FFFFFF;color:#0B1220;}
.stButton>button:hover{border-color:#2DD4BF;color:#0B1220;}
.stButton>button[kind="primary"]{background:#2DD4BF;color:#0B1220;border:none;}
.stButton>button[kind="primary"]:hover{background:#25BBA8;color:#0B1220;}

/* ---------------- multiselect tags ---------------- */
span[data-baseweb="tag"]{background:#EAF7F5!important;border:1px solid #BFEDE6!important;border-radius:8px!important;}
span[data-baseweb="tag"] span{color:#0B1220!important;font-family:'IBM Plex Mono',monospace;font-size:.72rem;}

/* ---------------- hero ---------------- */
.mdl-hero{background:linear-gradient(135deg,#0B1220 0%,#111E38 55%,#0E2A32 100%);border:1px solid rgba(45,212,191,.22);border-radius:18px;padding:32px 36px 26px;color:#E7ECF5;margin-bottom:10px;}
.mdl-eyebrow{font-family:'IBM Plex Mono',monospace;font-size:.7rem;letter-spacing:.3em;color:#2DD4BF;text-transform:uppercase;}
.mdl-title{font-family:'Space Grotesk',sans-serif;font-size:2.15rem;font-weight:700;line-height:1.08;margin:.4rem 0 .45rem;}
.mdl-title em{font-style:normal;color:#2DD4BF;}
.mdl-sub{color:#98A6BE;font-size:.93rem;max-width:64ch;line-height:1.55;}
.mdl-rail{display:flex;flex-wrap:wrap;gap:7px;margin-top:20px;}
.mdl-step{font-family:'IBM Plex Mono',monospace;font-size:.68rem;letter-spacing:.07em;color:#8FA0BC;border:1px solid rgba(143,160,188,.35);border-radius:999px;padding:4px 11px;white-space:nowrap;}
.mdl-step b{color:#2DD4BF;font-weight:600;margin-right:6px;}

/* ---------------- sections ---------------- */
.mdl-sec{display:flex;align-items:baseline;gap:13px;margin:2.4rem 0 .15rem;}
.mdl-sec-num{font-family:'IBM Plex Mono',monospace;background:#2DD4BF;color:#0B1220;border-radius:8px;padding:2px 9px;font-size:.78rem;font-weight:600;}
.mdl-sec-title{font-family:'Space Grotesk',sans-serif;font-size:1.28rem;font-weight:700;color:#0B1220;letter-spacing:-.01em;}
.mdl-sec-desc{color:#5B6B84;font-size:.87rem;line-height:1.55;margin:4px 0 16px 46px;max-width:80ch;border-left:2px solid #E3E8F0;padding-left:12px;}

/* ---------------- stat cards ---------------- */
.mdl-stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(165px,1fr));gap:12px;margin:4px 0 10px;}
.mdl-card{background:#0E1526;border:1px solid rgba(129,140,248,.18);border-radius:14px;padding:15px 17px 13px;}
.mdl-card .lbl{font-family:'IBM Plex Mono',monospace;font-size:.64rem;letter-spacing:.18em;text-transform:uppercase;color:#7C8CA8;}
.mdl-card .val{font-family:'IBM Plex Mono',monospace;font-size:1.55rem;font-weight:600;color:#E7ECF5;margin-top:5px;line-height:1.1;}
.mdl-card .note{font-size:.72rem;color:#7C8CA8;margin-top:5px;}
.mdl-card.pos .val{color:#34D399;} .mdl-card.neg .val{color:#F87171;} .mdl-card.sig .val{color:#2DD4BF;}

/* ---------------- report cards ---------------- */
.mdl-report{background:#FFFFFF;border:1px solid #E3E8F0;border-radius:14px;padding:14px 18px 12px;margin-bottom:10px;box-shadow:0 1px 2px rgba(11,18,32,.04);}
.mdl-report .name{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:.95rem;color:#0B1220;display:flex;align-items:center;gap:8px;}
.mdl-dot{width:9px;height:9px;border-radius:3px;display:inline-block;}
.mdl-report .rows{display:flex;flex-wrap:wrap;gap:6px 26px;margin-top:9px;}
.mdl-report .kv{font-family:'IBM Plex Mono',monospace;font-size:.78rem;color:#5B6B84;}
.mdl-report .kv b{color:#0B1220;font-weight:600;}
.mdl-badge{display:inline-block;font-family:'IBM Plex Mono',monospace;font-size:.66rem;letter-spacing:.1em;border-radius:999px;padding:3px 10px;margin-top:10px;}
.mdl-badge.warn{background:#FEF3C7;color:#92400E;border:1px solid #FDE68A;}
.mdl-badge.bad{background:#FEE2E2;color:#991B1B;border:1px solid #FECACA;}
.mdl-badge.ok{background:#D1FAE5;color:#065F46;border:1px solid #A7F3D0;}

/* ---------------- chips ---------------- */
.mdl-chips{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 4px;}
.mdl-chip{font-family:'IBM Plex Mono',monospace;font-size:.72rem;background:#F1F4F9;border:1px solid #E3E8F0;border-radius:8px;padding:3px 9px;color:#33415C;}
.mdl-chip b{color:#0B1220;}

/* ---------------- verdict banner ---------------- */
.mdl-verdict{border-radius:18px;padding:26px 30px;margin:10px 0 14px;color:#E7ECF5;}
.mdl-verdict.pos{background:linear-gradient(120deg,#062C22,#0B1220 70%);border:1px solid rgba(52,211,153,.35);}
.mdl-verdict.neg{background:linear-gradient(120deg,#3A0F14,#0B1220 70%);border:1px solid rgba(248,113,113,.35);}
.mdl-verdict .lbl{font-family:'IBM Plex Mono',monospace;font-size:.68rem;letter-spacing:.26em;text-transform:uppercase;color:#8FA0BC;}
.mdl-verdict .big{font-family:'IBM Plex Mono',monospace;font-size:2.6rem;font-weight:600;line-height:1.05;margin:.35rem 0 .2rem;}
.mdl-verdict.pos .big{color:#34D399;} .mdl-verdict.neg .big{color:#F87171;}
.mdl-verdict .note{color:#98A6BE;font-size:.83rem;max-width:70ch;}
</style>
"""


def _mdl_html(s):
    """Render HTML without markdown treating indentation as code."""
    st.markdown("".join(line.strip() for line in s.splitlines()),
                unsafe_allow_html=True)


def _mdl_page_hero(eyebrow, title_html, sub_html, steps):
    """Shared ink-navy hero used by every page."""
    rail = "".join(f"<span class='mdl-step'><b>{i+1:02d}</b>{s}</span>"
                   for i, s in enumerate(steps))
    _mdl_html(f"""
    <div class='mdl-hero'>
      <div class='mdl-eyebrow'>{eyebrow}</div>
      <div class='mdl-title'>{title_html}</div>
      <div class='mdl-sub'>{sub_html}</div>
      <div class='mdl-rail'>{rail}</div>
    </div>""")


def _mdl_hero(n_features, split_variable):
    _mdl_page_hero(
        "Model Lab · Competitive Moats → Risk-Adjusted Returns",
        "Can moat grades predict the <em>next quarter's Sharpe?</em>",
        f"""Random Forest, XGBoost and SVR are tuned on a leak-free chronological
        split of {n_features} competitive-advantage trajectory grades, blended into an
        equal-weighted ensemble, then backtested long/short on every company's newest report.
        Current split quantile: <span style="color:#2DD4BF;font-family:'IBM Plex Mono',monospace;">{split_variable:.2f}</span>.""",
        ["Split", "Tune", "Fit", "Diagnose", "Explain",
         "Classify", "Ensemble", "Backtest"])


def _mdl_section(num, title, desc):
    badge = f"{num:02d}" if isinstance(num, int) else num
    _mdl_html(f"""
    <div class='mdl-sec'><span class='mdl-sec-num'>{badge}</span>
    <span class='mdl-sec-title'>{title}</span></div>
    <div class='mdl-sec-desc'>{desc}</div>""")


def _mdl_stats(items):
    """items: list of (label, value, note, tone) — tone in '', 'pos', 'neg', 'sig'."""
    cards = "".join(
        f"<div class='mdl-card {tone}'><div class='lbl'>{lbl}</div>"
        f"<div class='val'>{val}</div><div class='note'>{note}</div></div>"
        for lbl, val, note, tone in items)
    _mdl_html(f"<div class='mdl-stats'>{cards}</div>")


def _mdl_param_chips(params):
    chips = "".join(f"<span class='mdl-chip'>{k.replace('svr__','')}: <b>{v}</b></span>"
                    for k, v in params.items())
    _mdl_html(f"<div class='mdl-chips'>{chips}</div>")


def _mdl_report_card(name, rows, badge=None):
    """rows: list of 'Label|value' strings. badge: (text, cls) or None."""
    color = _MODEL_COLOR.get(name, _VIOLET)
    kvs = "".join(f"<span class='kv'>{r.split('|')[0]} <b>{r.split('|')[1]}</b></span>"
                  for r in rows)
    badge_html = (f"<div><span class='mdl-badge {badge[1]}'>{badge[0]}</span></div>"
                  if badge else "")
    _mdl_html(f"""
    <div class='mdl-report'>
      <div class='name'><span class='mdl-dot' style='background:{color};'></span>{name}</div>
      <div class='rows'>{kvs}</div>{badge_html}
    </div>""")


def _mdl_polish(fig, *axes):
    """Consistent chart chrome (presentation only)."""
    fig.patch.set_facecolor("white")
    for ax in axes:
        ax.set_facecolor("white")
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color("#C9D2E0")
        ax.tick_params(colors=_MUTED, labelsize=9)
        ax.xaxis.label.set_color(_MUTED)
        ax.yaxis.label.set_color(_MUTED)
        ax.title.set_color(_INK)
        ax.title.set_fontweight("bold")
        ax.title.set_fontsize(11)
        ax.set_axisbelow(True)
        ax.grid(True, color="#EEF1F7", linewidth=0.8)
    fig.tight_layout()


_CM_CMAP = None
def _mdl_cmap():
    global _CM_CMAP
    if _CM_CMAP is None:
        _CM_CMAP = sns.light_palette(_VIOLET, as_cmap=True)
    return _CM_CMAP


# ---------------------------------------------------------------------
# Web-adapted twin of all_data_preview()
# Same data, same tables, same pair-plot logic — only presentation
# (hero + numbered sections + formatted columns) changed.
# ---------------------------------------------------------------------
def all_data_preview_web():
    df = pd.read_csv("Total_sharp_ratios.csv")

    _mdl_page_hero(
        "Dataset · Moat Grades × Realized Sharpe",
        "The combined panel, <em>at a glance</em>",
        f"""{len(df)} report observations across {df['Company'].nunique()} companies.
        Each row is one quarterly/annual report: the 16 development-trajectory grades
        plus the realized 63-day Sharpe ratio after the report date.""",
        ["Panel", "Correlation", "Pair plot"])

    _mdl_stats([
        ("Observations", f"{len(df):,}", "one row per report", "sig"),
        ("Companies", f"{df['Company'].nunique()}", "in the combined file", ""),
        ("Grade columns", f"{len(ALL_FEATURES)}", "moat trajectory factors", ""),
        ("Target", "Sharpe", "realized 63-day, post-report", ""),
    ])

    _mdl_section(1, "Combined dataset (Total_sharp_ratios.csv)",
                 "Every <ticker>_sharp_ratios.csv merged into one panel and filtered to "
                 "grades in (0, 10]. This is the exact table the Model page trains on.")
    st.dataframe(df, width="stretch")

    corr_df = df.drop("date", axis=1)
    corr_df = corr_df.drop("Company", axis=1)
    corr = corr_df.corr()

    _mdl_section(2, "Correlation with the Sharpe ratio",
                 "Pearson correlation of every competitive-advantage grade with the realized "
                 "Sharpe ratio, sorted descending. This is a first, purely linear look at "
                 "which factors move together with subsequent risk-adjusted returns.")
    st.dataframe(
        corr["sharpe_ratio"].sort_values(ascending=False).rename("corr"),
        width="stretch",
        column_config={"corr": st.column_config.NumberColumn(
            "Correlation", format="%.4f")},
    )

    _mdl_section(3, "Pair plot",
                 "Scatter matrix of all numeric columns (same plot as in the notebook). "
                 "With 17 variables this is a large figure and takes a moment to render, "
                 "so it is off by default.")
    if st.checkbox("Render pair plot (slow)", value=False):
        with st.spinner("Building pair plot..."):
            sns.set_palette("Pastel1")
            g = sns.pairplot(corr_df)
            g.fig.suptitle("Pair Plot for DataFrame", y=1.02)
            st.pyplot(g.fig)
            plt.close(g.fig)


# ---------------------------------------------------------------------
# Web-adapted twin of train_models_all_data()
# Same split logic, same grids, same models, same metrics, same
# backtest — only the presentation layer changed. The pipeline is
# split into small stage functions for readability; each stage's
# computation is verbatim from the original.
# ---------------------------------------------------------------------

def _stage_split(split_variable, feature_variables):
    df = pd.read_csv("Total_sharp_ratios.csv")
    df["date"] = pd.to_datetime(df["date"])
    panel_df = df.sort_values("date")

    last_report_idx = panel_df.groupby("Company")["date"].idxmax()
    backtest = panel_df.loc[last_report_idx]

    remaining = panel_df.drop(index=last_report_idx)

    train_end = remaining["date"].quantile(split_variable)

    train = remaining[remaining["date"] <= train_end]
    test = remaining[(remaining["date"] > train_end)]

    feature_cols = feature_variables
    X_train, y_train = train[feature_cols], train["sharpe_ratio"]
    X_test, y_test = test[feature_cols], test["sharpe_ratio"]
    X_backtest, y_backtest = backtest[feature_cols], backtest["sharpe_ratio"]

    _mdl_section(1, "Data split",
                 "Time-based split: the newest report of every company is held out as the "
                 "backtest universe; the remaining reports are split chronologically at the "
                 "chosen quantile into train and test. This avoids look-ahead bias.")
    _mdl_stats([
        ("Train samples", f"{len(X_train):,}",
         f"reports ≤ {train_end.date()}", "sig"),
        ("Test samples", f"{len(X_test):,}",
         f"reports > {train_end.date()}", ""),
        ("Backtest samples", f"{len(X_backtest):,}",
         "newest report per company", ""),
        ("Features", f"{len(feature_cols)}", "moat trajectory grades", ""),
    ])
    return (backtest, feature_cols, X_train, y_train, X_test, y_test,
            X_backtest, y_backtest)


def _stage_tuning(X_train, y_train):
    _mdl_section(2, "Hyperparameter tuning",
                 "GridSearchCV with a 5-fold TimeSeriesSplit tunes each model on the training "
                 "set only, scored by R². The best parameters found are then used to fit the "
                 "final models.")
    tscv = TimeSeriesSplit(n_splits=5)

    with st.status("Tuning Random Forest…", expanded=False) as status:
        rfg_param_grid = {"max_depth": [2, 3, 4],
                          "min_samples_leaf": [5, 10, 20],
                          "n_estimators": [100, 200, 300]}
        rfg_grid = GridSearchCV(RandomForestRegressor(random_state=42),
                                rfg_param_grid, cv=tscv, scoring="r2")
        rfg_grid.fit(X_train, y_train)
        rfg_best_params = rfg_grid.best_params_
        status.update(label="Random Forest tuned", state="complete")
    _mdl_html("<div class='mdl-chips'><span class='mdl-chip'><b>Random Forest</b></span></div>")
    _mdl_param_chips(rfg_best_params)

    with st.status("Tuning XGBoost…", expanded=False) as status:
        xgb_param_grid = {
            "max_depth": [2, 3, 4],
            "learning_rate": [0.01, 0.03, 0.05, 0.1],
            "n_estimators": [100, 200, 300],
            "reg_alpha": [0, 0.5, 1.0],
            "reg_lambda": [1.0, 2.0, 5.0],
        }
        xgb_grid = GridSearchCV(XGBRegressor(random_state=42),
                                xgb_param_grid, cv=tscv, scoring="r2",
                                n_jobs=-1)
        xgb_grid.fit(X_train, y_train)
        xgb_best_params = xgb_grid.best_params_
        status.update(label="XGBoost tuned", state="complete")
    _mdl_html("<div class='mdl-chips'><span class='mdl-chip'><b>XGBoost</b></span></div>")
    _mdl_param_chips(xgb_best_params)

    with st.status("Tuning SVR…", expanded=False) as status:
        svr_pipeline = make_pipeline(StandardScaler(), SVR(kernel="rbf"))
        svr_param_grid = {
            "svr__C": [0.01, 0.1, 1.0, 10.0],
            "svr__epsilon": [0.01, 0.05, 0.1, 0.2],
            "svr__gamma": ["scale", "auto", 0.01, 0.1],
        }
        svr_grid = GridSearchCV(svr_pipeline, svr_param_grid, cv=tscv,
                                scoring="r2", n_jobs=-1)
        svr_grid.fit(X_train, y_train)
        svr_best_params = svr_grid.best_params_
        status.update(label="SVR tuned", state="complete")
    _mdl_html("<div class='mdl-chips'><span class='mdl-chip'><b>SVR</b></span></div>")
    _mdl_param_chips(svr_best_params)

    return rfg_best_params, xgb_best_params, svr_best_params


def _bias_variance_report_web(model, X_train, y_train, X_test, y_test, name=""):
    # Mean Squared Error: Average squared difference between actual and
    # predicted values, lower values indicate better predictions.
    # R-squared: Indicates how much variance in the target variable is
    # explained by the model, values close to 1 show a strong fit.
    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)
    train_mse = mean_squared_error(y_train, train_pred)
    test_mse = mean_squared_error(y_test, test_pred)
    train_r2 = r2_score(y_train, train_pred)
    test_r2 = r2_score(y_test, test_pred)

    badge = None
    if test_mse > 1.5 * train_mse:
        badge = ("HIGH VARIANCE · OVERFITTING", "warn")
    elif train_mse > 0.5:  # threshold depends on your scale
        badge = ("HIGH BIAS · UNDERFITTING", "bad")

    _mdl_report_card(name if name else "model", [
        f"Train MSE|{train_mse:.4f}", f"Test MSE|{test_mse:.4f}",
        f"Train R²|{train_r2:.4f}", f"Test R²|{test_r2:.4f}",
    ], badge=badge)
    return train_mse, test_mse


def train_models_all_data_web(split_variable=0.7, feature_variables=None):
    if feature_variables is None:
        feature_variables = list(ALL_FEATURES)

    # ---------------- 1 · Split dataset ----------------
    (backtest, feature_cols, X_train, y_train, X_test, y_test,
     X_backtest, y_backtest) = _stage_split(split_variable, feature_variables)

    # ---------------- 2 · Find parameters ----------------
    rfg_best_params, xgb_best_params, svr_best_params = \
        _stage_tuning(X_train, y_train)

    # ---------------- Train the models ----------------
    models = {
        "random_forest": RandomForestRegressor(
            n_estimators=rfg_best_params["n_estimators"],
            max_depth=rfg_best_params["max_depth"],
            min_samples_leaf=rfg_best_params["min_samples_leaf"],
            max_features="sqrt", random_state=42
        ),
        "xgboost": XGBRegressor(
            n_estimators=xgb_best_params["n_estimators"],
            max_depth=xgb_best_params["max_depth"],
            learning_rate=xgb_best_params["learning_rate"],
            reg_alpha=xgb_best_params["reg_alpha"],
            reg_lambda=xgb_best_params["reg_lambda"],
            subsample=0.7, colsample_bytree=0.7,
            random_state=42
        ),
        "svr": make_pipeline(StandardScaler(),
                             SVR(kernel="rbf", C=svr_best_params["svr__C"],
                                 epsilon=svr_best_params["svr__epsilon"]))
    }
    fitted = {}
    with st.spinner("Fitting final regressors..."):
        for name, model in models.items():
            model.fit(X_train, y_train)
            fitted[name] = model

    # ---------------- 3 · Bias-variance diagnostics ----------------
    _mdl_section(3, "Bias–variance diagnostics (regression)",
                 "MSE is the average squared prediction error (lower is better); R² is the "
                 "share of Sharpe-ratio variance the model explains. A test MSE far above the "
                 "train MSE signals overfitting; a high train MSE signals underfitting.")

    results = {}
    for name, model in fitted.items():
        train_mse, test_mse = _bias_variance_report_web(
            model, X_train, y_train, X_test, y_test, name=name)
        results[name] = (train_mse, test_mse)

    names = list(results.keys())
    train_mse = [v[0] for v in results.values()]
    test_mse = [v[1] for v in results.values()]

    x = np.arange(len(names))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(x - width / 2, train_mse, width, label="Train MSE",
           color=_SIGNAL, edgecolor="none")
    ax.bar(x + width / 2, test_mse, width, label="Test MSE",
           color=_VIOLET, edgecolor="none")
    ax.set_xticks(x)
    ax.set_xticklabels(names)
    ax.set_ylabel("MSE")
    ax.set_title("Bias–Variance Diagnostic: Train vs Test Error by Model")
    ax.legend(frameon=False)
    _mdl_polish(fig, ax)
    st.pyplot(fig)
    plt.close(fig)

    # ---------------- 4 · Feature importance ----------------
    _mdl_section(4, "Feature importance",
                 "Which competitive-advantage grades each tree model relies on most when "
                 "predicting the Sharpe ratio (impurity-based importance), followed by "
                 "model-agnostic permutation importance on the test set.")

    c1, c2 = st.columns(2)
    with c1:
        importances = fitted["random_forest"].feature_importances_
        fig, ax = plt.subplots(figsize=(6, 5))
        pd.Series(importances, index=feature_cols).sort_values().plot(
            kind="barh", ax=ax, color=_SIGNAL)
        ax.set_title("Random Forest Feature Importance")
        _mdl_polish(fig, ax)
        st.pyplot(fig)
        plt.close(fig)
    with c2:
        importances_xgb = fitted["xgboost"].feature_importances_
        fig, ax = plt.subplots(figsize=(6, 5))
        pd.Series(importances_xgb, index=feature_cols).sort_values().plot(
            kind="barh", ax=ax, color=_VIOLET)
        ax.set_title("XGBoost Feature Importance")
        _mdl_polish(fig, ax)
        st.pyplot(fig)
        plt.close(fig)

    st.caption("Permutation importance on the TEST set: how much R² drops "
               "when a feature's values are shuffled. This is model-agnostic "
               "and measures true out-of-sample relevance.")
    with st.spinner("Computing permutation importances..."):
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        for ax, (name, model) in zip(axes, fitted.items()):
            perm = permutation_importance(model, X_test, y_test,
                                          n_repeats=30, random_state=42,
                                          scoring="r2")
            pd.Series(perm.importances_mean,
                      index=feature_cols).sort_values().plot(
                kind="barh", ax=ax, color=_MODEL_COLOR.get(name, _VIOLET))
            ax.set_title(f"{name} — Permutation Importance")
        _mdl_polish(fig, *axes)
        st.pyplot(fig)
        plt.close(fig)

    # ---------------- 5 · Classification ----------------
    _mdl_section(5, "Classification: outperform vs underperform",
                 "The Sharpe ratio is binarized at the training-set median and three "
                 "classifiers predict whether a report leads to above- or below-median "
                 "performance. Reported: accuracy, AUC, confusion matrix and per-class "
                 "precision/recall.")

    threshold = y_train.median()

    y_train_binary = (y_train > threshold).astype(int)
    y_test_binary = (y_test > threshold).astype(int)

    # --- Train classifiers, mirroring the regressor setup ---
    clf_models = {
        "random_forest_clf": RandomForestClassifier(
            n_estimators=300, max_depth=3, min_samples_leaf=10,
            max_features="sqrt", random_state=42
        ),
        "xgboost_clf": XGBClassifier(
            n_estimators=150, max_depth=3, learning_rate=0.03,
            reg_alpha=0.5, reg_lambda=2.0, subsample=0.7,
            colsample_bytree=0.7,
            random_state=42, eval_metric="logloss"
        ),
        "svc_clf": make_pipeline(StandardScaler(),
                                 SVC(kernel="rbf", C=1.0, probability=True)),
    }

    fitted_clf = {}
    with st.spinner("Fitting classifiers..."):
        for name, model in clf_models.items():
            model.fit(X_train, y_train_binary)
            fitted_clf[name] = model

    # --- Report accuracy, AUC, confusion matrix for each ---
    for name, model in fitted_clf.items():
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]

        acc = accuracy_score(y_test_binary, y_pred)
        auc = roc_auc_score(y_test_binary, y_proba)
        cm = confusion_matrix(y_test_binary, y_pred)

        _mdl_report_card(name, [
            f"Accuracy|{acc:.4f}", f"AUC|{auc:.4f}",
            f"TN / FP|{cm[0][0]} / {cm[0][1]}",
            f"FN / TP|{cm[1][0]} / {cm[1][1]}",
        ])
        with st.expander(f"Per-class precision / recall — {name}"):
            st.code(classification_report(
                y_test_binary, y_pred,
                target_names=["Underperform", "Outperform"]), language=None)

    # --- Visualize ROC curves together ---
    st.caption("ROC curves: the further above the grey diagonal (random "
               "guessing), the better the classifier separates out- from "
               "underperformers.")
    c1, c2 = st.columns([2, 3])
    with c1:
        fig, ax = plt.subplots(figsize=(6, 6))
        for name, model in fitted_clf.items():
            RocCurveDisplay.from_estimator(
                model, X_test, y_test_binary, ax=ax, name=name,
                curve_kwargs={"color": _MODEL_COLOR.get(name, _VIOLET), "linewidth": 2})
        ax.plot([0, 1], [0, 1], linestyle="--", color="gray")
        ax.set_title("ROC Curves")
        ax.legend(frameon=False, fontsize=8)
        _mdl_polish(fig, ax)
        st.pyplot(fig)
        plt.close(fig)

    # --- Visualize confusion matrices as heatmaps ---
    with c2:
        fig, axes = plt.subplots(1, len(fitted_clf), figsize=(15, 4.4))
        for ax, (name, model) in zip(axes, fitted_clf.items()):
            cm = confusion_matrix(y_test_binary, model.predict(X_test))
            sns.heatmap(cm, annot=True, fmt="d", cmap=_mdl_cmap(), ax=ax,
                        cbar=False, annot_kws={"family": "monospace"},
                        xticklabels=["Under", "Out"],
                        yticklabels=["Under", "Out"])
            ax.set_title(name)
            ax.title.set_color(_INK)
            ax.title.set_fontweight("bold")
            ax.title.set_fontsize(10)
            ax.tick_params(colors=_MUTED, labelsize=9)
        fig.patch.set_facecolor("white")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # ---------------- 6 · Ensembles ----------------
    _mdl_section(6, "Equal-weighted ensembles",
                 "The three regressors (and classifiers) are averaged into a simple "
                 "equal-weighted ensemble, which usually smooths out individual model errors.")
    
    class SimpleEnsemble(RegressorMixin, BaseEstimator):
        def __init__(self, models: dict, weights: dict | None = None):
            self.models = models
            self.weights = weights or {k: 1 / len(models) for k in models}

        def fit(self, X, y=None):
            return self

        def predict(self, X):
            preds = np.zeros(len(X))
            for name, model in self.models.items():
                preds += self.weights[name] * model.predict(X)
            return preds

    ensemble = SimpleEnsemble(fitted)  # equal-weighted; or set weights from test-set performance
    _bias_variance_report_web(ensemble, X_train, y_train, X_test, y_test,
                              name="ensemble")

    with st.spinner("Computing ensemble permutation importance..."):
        perm_result = permutation_importance(
            ensemble, X_test, y_test,
            n_repeats=30, random_state=42, scoring="r2"
        )

    perm_importance_ensemble = pd.Series(
        perm_result.importances_mean, index=feature_cols).sort_values()

    fig, ax = plt.subplots(figsize=(8, 5.5))
    perm_importance_ensemble.plot(kind="barh", ax=ax,
                                  color=_MODEL_COLOR["ensemble"])
    ax.set_title("Ensemble — Permutation Importance")
    ax.set_xlabel("Mean decrease in R² when feature is shuffled")
    _mdl_polish(fig, ax)
    st.pyplot(fig)
    plt.close(fig)

    class SimpleEnsembleClassifier(ClassifierMixin, BaseEstimator):
        def __init__(self, models: dict, weights: dict | None = None):
            self.models = models
            self.weights = weights or {k: 1 / len(models) for k in models}
            self.classes_ = np.array([0, 1])

        def fit(self, X, y=None):
            self.is_fitted_ = True
            return self

        def predict_proba(self, X):
            proba = np.zeros(len(X))
            for name, model in self.models.items():
                proba += self.weights[name] * model.predict_proba(X)[:, 1]
            return np.column_stack([1 - proba, proba])

        def predict(self, X):
            return (self.predict_proba(X)[:, 1] > 0.5).astype(int)

    ensemble_clf = SimpleEnsembleClassifier(fitted_clf)

    # --- Report accuracy, AUC, confusion matrix for the ensemble only ---
    y_pred = ensemble_clf.predict(X_test)
    y_proba = ensemble_clf.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test_binary, y_pred)
    auc = roc_auc_score(y_test_binary, y_proba)
    cm = confusion_matrix(y_test_binary, y_pred)

    _mdl_report_card("ensemble_clf", [
        f"Accuracy|{acc:.4f}", f"AUC|{auc:.4f}",
        f"TN / FP|{cm[0][0]} / {cm[0][1]}",
        f"FN / TP|{cm[1][0]} / {cm[1][1]}",
    ])
    with st.expander("Per-class precision / recall — ensemble_clf"):
        st.code(classification_report(
            y_test_binary, y_pred,
            target_names=["Underperform", "Outperform"]), language=None)

    c1, c2 = st.columns(2)
    with c1:
        # --- ROC curve for the ensemble only ---
        fig, ax = plt.subplots(figsize=(6, 6))
        RocCurveDisplay.from_estimator(
            ensemble_clf, X_test, y_test_binary, ax=ax, name="ensemble_clf",
            curve_kwargs={"color": _MODEL_COLOR.get(name, _VIOLET), "linewidth": 2})
        ax.plot([0, 1], [0, 1], linestyle="--", color="gray")
        ax.set_title("ROC Curve — Ensemble")
        ax.legend(frameon=False, fontsize=8)
        _mdl_polish(fig, ax)
        st.pyplot(fig)
        plt.close(fig)
    with c2:
        # --- Confusion matrix heatmap for the ensemble only ---
        fig, ax = plt.subplots(figsize=(5, 4.6))
        sns.heatmap(cm, annot=True, fmt="d", cmap=_mdl_cmap(), ax=ax,
                    cbar=False, annot_kws={"family": "monospace"},
                    xticklabels=["Under", "Out"],
                    yticklabels=["Under", "Out"])
        ax.set_title("Confusion Matrix — Ensemble")
        ax.title.set_color(_INK)
        ax.title.set_fontweight("bold")
        ax.tick_params(colors=_MUTED)
        fig.patch.set_facecolor("white")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # ---------------- 7 · Backtest ----------------
    _mdl_section(7, "Backtest on the latest reports",
                 "The ensemble scores the held-out newest report of every company. Top/bottom "
                 "10 by predicted score form an equal-weighted long/short portfolio, evaluated "
                 "on the realized Sharpe ratio after those reports.")

    backtest_universe = backtest.copy()
    backtest_universe["predicted_score"] = ensemble.predict(
        backtest_universe[feature_cols])

    top10 = backtest_universe.nlargest(10, "predicted_score")[
        ["Company", "predicted_score", "date"]]
    bottom10 = backtest_universe.nsmallest(10, "predicted_score")[
        ["Company", "predicted_score", "date"]]

    col_cfg = {
        "Company": st.column_config.TextColumn("Company"),
        "predicted_score": st.column_config.NumberColumn(
            "Predicted score", format="%.4f"),
        "date": st.column_config.DateColumn("Report date"),
    }
    c1, c2 = st.columns(2)
    with c1:
        _mdl_html("<div class='mdl-chips'><span class='mdl-chip' "
                  "style='border-color:#A7F3D0;background:#ECFDF5;color:#065F46;'>"
                  "▲ LONG LEG · Top 10 predicted</span></div>")
        st.dataframe(top10, width="stretch", hide_index=True,
                     column_config=col_cfg)
    with c2:
        _mdl_html("<div class='mdl-chips'><span class='mdl-chip' "
                  "style='border-color:#FECACA;background:#FEF2F2;color:#991B1B;'>"
                  "▼ SHORT LEG · Bottom 10 predicted</span></div>")
        st.dataframe(bottom10, width="stretch", hide_index=True,
                     column_config=col_cfg)

    # backtest_universe already has: predicted_score AND the actual
    # realized sharpe_ratio
    top10 = backtest_universe.nlargest(10, "predicted_score")
    bottom10 = backtest_universe.nsmallest(10, "predicted_score")

    # --- Equally-weighted long/short portfolio ---
    long_leg_return = top10["sharpe_ratio"].mean()
    short_leg_return = bottom10["sharpe_ratio"].mean()

    # assume a simple transaction cost assumption, e.g. 10 bps per leg round-trip
    txn_cost = 0.001  # 10 bps = 0.10% = 0.001, adjust to your assumption
    long_short_return = (long_leg_return - short_leg_return) - 2 * txn_cost

    tone = "pos" if long_short_return > 0 else "neg"
    _mdl_html(f"""
    <div class='mdl-verdict {tone}'>
      <div class='lbl'>Long/Short portfolio · net of 2×10bps costs</div>
      <div class='big'>{long_short_return:+.4f}</div>
      <div class='note'>Equal-weighted long leg minus short leg on realized 63-day Sharpe
      ratios after each company's newest report.</div>
    </div>""")

    _mdl_stats([
        ("Long leg avg Sharpe", f"{long_leg_return:.4f}",
         f"std {top10['sharpe_ratio'].std():.4f}", "pos"),
        ("Short leg avg Sharpe", f"{short_leg_return:.4f}",
         f"std {bottom10['sharpe_ratio'].std():.4f}", "neg"),
        ("Long − Short (net)", f"{long_short_return:.4f}",
         "after 2 × 10 bps costs", tone),
    ])

    # --- Was the model actually right? Compare rank correlation between
    # predicted and realized ---
    from scipy.stats import spearmanr
    rho, pval = spearmanr(backtest_universe["predicted_score"],
                          backtest_universe["sharpe_ratio"])
    st.caption("Spearman rank correlation between predicted score and "
               "realized Sharpe: >0 means higher-ranked companies really "
               "did perform better; p-value tests whether that ranking "
               "skill could be chance.")
    _mdl_stats([
        ("Spearman ρ", f"{rho:.4f}", "predicted vs realized rank", "sig"),
        ("p-value", f"{pval:.4f}", "chance of this ranking skill", ""),
    ])

    c1, c2 = st.columns([3, 2])
    with c1:
        # --- Visualize: did higher predicted score = higher realized outcome? ---
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.scatterplot(data=backtest_universe, x="predicted_score",
                        y="sharpe_ratio", ax=ax, color=_VIOLET, s=55,
                        edgecolor=_INK, linewidth=0.4, alpha=0.85)
        ax.axhline(0, color="gray", linestyle="--")
        ax.set_title("Predicted score vs realized Sharpe ratio (backtest set)")
        ax.set_xlabel("Predicted score")
        ax.set_ylabel("Realized Sharpe ratio")
        _mdl_polish(fig, ax)
        st.pyplot(fig)
        plt.close(fig)
    with c2:
        # --- Bar chart comparing the two legs ---
        comparison = pd.DataFrame({
            "Leg": ["Long (Top 10)", "Short (Bottom 10)"],
            "Avg Realized Sharpe": [long_leg_return, short_leg_return]
        })
        fig, ax = plt.subplots(figsize=(5.5, 6))
        sns.barplot(data=comparison, x="Leg", y="Avg Realized Sharpe",
                    ax=ax, palette=[_LONG, _SHORT], hue="Leg", legend=False)
        ax.axhline(0, color="#C9D2E0", linewidth=1)
        ax.set_title("Backtest: Long vs Short leg performance")
        _mdl_polish(fig, ax)
        st.pyplot(fig)
        plt.close(fig)

    st.success("Regression pipeline finished.")


# ---------------------------------------------------------------------
# Helpers for the Tickers page  (logic UNCHANGED)
# ---------------------------------------------------------------------
def ticker_folder_status():
    """Scan the Tickers/ folder and summarize the processing state of
    every ticker (reports downloaded, static/dynamic gradings, sharpe file)."""
    rows = []
    base = "Tickers"
    existing = set(os.listdir(base)) if os.path.isdir(base) else set()
    for t in sorted(ALL_TICKERS):
        row = {"Ticker": t, "Folder": t in existing, "Reports": 0,
               "Static CSVs": 0, "Dynamic CSVs": 0, "Sharpe file": False}
        if t in existing:
            files = os.listdir(os.path.join(base, t))
            row["Reports"] = sum(f.endswith((".pdf", ".txt")) for f in files)
            row["Static CSVs"] = sum(f.endswith("_static.csv") for f in files)
            row["Dynamic CSVs"] = sum(f.endswith("_dynamic.csv") for f in files)
            row["Sharpe file"] = f"{t}_sharp_ratios.csv" in files
        rows.append(row)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------
# App layout
# ---------------------------------------------------------------------
st.set_page_config(page_title="Competitive Advantage Analyzer",
                   layout="wide")
st.markdown(_APP_CSS, unsafe_allow_html=True)

with st.sidebar:
    _mdl_html("""
    <div class='sb-brand'>
      <div class='sb-eyebrow'>Signal Desk</div>
      <div class='sb-title'>Competitive Advantage Analyzer</div>
    </div>
    <div class='sb-label'>Navigate</div>""")
    page = st.radio("Pages", ["Tickers", "Data preview", "Model"],
                    label_visibility="collapsed")
    _mdl_html("""
    <div class='sb-label'>Pipeline</div>
    <div class='sb-steps'>
      <div class='sb-step'><b>01</b>Download reports</div>
      <div class='sb-step'><b>02</b>Extract grades</div>
      <div class='sb-step'><b>03</b>Development grading</div>
      <div class='sb-step'><b>04</b>Sharpe ratios</div>
      <div class='sb-step'><b>05</b>Combined file</div>
      <div class='sb-step'><b>06</b>Model</div>
    </div>""")

# =========================== TICKERS PAGE ============================
if page == "Tickers":
    status = ticker_folder_status()

    _mdl_page_hero(
        "Universe · Pipeline Operations",
        f"{len(ALL_TICKERS)} tickers, <em>one pipeline</em>",
        "All companies in the universe and the processing state of their folder "
        "under Tickers/. Run any pipeline step for selected tickers from here.",
        ["Download", "Extract", "Grade", "Sharpe", "Combine"])

    sharpe_ready = int(status["Sharpe file"].sum())
    _mdl_stats([
        ("Tickers in universe", f"{len(ALL_TICKERS)}", "companies tracked", "sig"),
        ("Folders present", f"{int(status['Folder'].sum())}",
         "under Tickers/", ""),
        ("Sharpe files ready", f"{sharpe_ready}",
         "fully processed tickers", "pos" if sharpe_ready else ""),
        ("Coverage", f"{sharpe_ready / len(ALL_TICKERS):.0%}",
         "of the universe model-ready", ""),
    ])

    _mdl_section("◆", "Universe status",
                 "Per-ticker processing state: downloaded reports, static and dynamic "
                 "grading CSVs, and whether the final Sharpe file exists.")
    st.dataframe(
        status, width="stretch", hide_index=True,
        column_config={
            "Ticker": st.column_config.TextColumn("Ticker"),
            "Folder": st.column_config.CheckboxColumn("Folder", disabled=True),
            "Reports": st.column_config.NumberColumn("Reports"),
            "Static CSVs": st.column_config.NumberColumn("Static CSVs"),
            "Dynamic CSVs": st.column_config.NumberColumn("Dynamic CSVs"),
            "Sharpe file": st.column_config.CheckboxColumn("Sharpe file",
                                                           disabled=True),
        })

    _mdl_section("▶", "Run pipeline steps",
                 "Pick tickers, then launch a single step or the full pipeline for each "
                 "of them. Detailed logs stream to the terminal.")
    selected = st.multiselect("Tickers to process", ALL_TICKERS,
                              default=[])

    c1, c2, c3, c4, c5 = st.columns(5)
    run_download = c1.button("Download reports")
    run_extract = c2.button("Extract grades")
    run_dynamic = c3.button("Development grading")
    run_sharpe = c4.button("Sharpe ratios")
    run_full = c5.button("Full pipeline", type="primary")

    if any([run_download, run_extract, run_dynamic, run_sharpe, run_full]):
        if not selected:
            st.warning("Select at least one ticker first.")
        else:
            Path("Tickers").mkdir(parents=True, exist_ok=True)
            for t in selected:
                with st.spinner(f"Processing {t}..."):
                    if run_full:
                        create_sharp_ratios_all_tickers([t])
                    else:
                        if run_download:
                            download_ticker_reports(t)
                        if run_extract:
                            extract_ticker_reports(t)
                        if run_dynamic:
                            development_grading_ticker_reports(t)
                        if run_sharpe:
                            create_sharpe_ratios(t)
                st.success(f"{t} done (see terminal for detailed logs).")
            st.rerun()

    _mdl_section("∑", "Combined dataset",
                 "Merges every <ticker>_sharp_ratios.csv into Total_sharp_ratios.csv "
                 "and filters grades to (0, 10].")
    if st.button("Build Total_sharp_ratios.csv"):
        with st.spinner("Combining all sharpe-ratio files..."):
            create_all_data_file()
        st.success("Total_sharp_ratios.csv written.")

# ========================= DATA PREVIEW PAGE =========================
elif page == "Data preview":
    if not os.path.exists("Total_sharp_ratios.csv"):
        _mdl_page_hero(
            "Dataset · Moat Grades × Realized Sharpe",
            "The combined panel, <em>at a glance</em>",
            "Inspect the merged panel of competitive-advantage grades and realized "
            "63-day Sharpe ratios once it has been built.",
            ["Panel", "Correlation", "Pair plot"])
        st.warning("Total_sharp_ratios.csv not found. Build it on the "
                   "Tickers page first.")
    else:
        all_data_preview_web()

# ============================ MODEL PAGE =============================
elif page == "Model":
    if not os.path.exists("Total_sharp_ratios.csv"):
        _mdl_hero(len(ALL_FEATURES), 0.70)
        st.warning("Total_sharp_ratios.csv not found. Build it on the "
                   "Tickers page first.")
    else:
        # Hero slot is created first so it renders on top, but is filled
        # after the widgets exist so it reflects the live configuration.
        hero_slot = st.container()

        # ---- Configuration panel ----
        with st.container(border=True):
            _mdl_html("""
            <div class='mdl-sec' style='margin-top:.2rem;'>
              <span class='mdl-sec-num'>⚙</span>
              <span class='mdl-sec-title'>Configuration</span>
            </div>
            <div class='mdl-sec-desc'>Set the chronological train/test split and pick which
            competitive-advantage factors feed the models, then launch the full regression,
            classification and backtest run.</div>""")

            c1, c2 = st.columns([1, 2])
            with c1:
                split_variable = st.slider(
                    "Train share of the chronological split (quantile)",
                    min_value=0.50, max_value=0.95, value=0.70, step=0.05,
                    help="Reports up to this date-quantile go to training, the "
                         "rest to testing. The newest report per company is always "
                         "reserved for the backtest.")
            with c2:
                feature_variables = st.multiselect(
                    "Competitive advantages used as features",
                    options=ALL_FEATURES, default=ALL_FEATURES,
                    format_func=lambda f: f"{f} — {FEATURE_LABELS[f]}")

            _mdl_html(f"""
            <div class='mdl-chips'>
              <span class='mdl-chip'>split <b>{split_variable:.2f}</b></span>
              <span class='mdl-chip'>features <b>{len(feature_variables)} / {len(ALL_FEATURES)}</b></span>
              <span class='mdl-chip'>models <b>RF · XGB · SVR + ensemble</b></span>
              <span class='mdl-chip'>horizon <b>63-day Sharpe</b></span>
            </div>""")

            run = st.button("Run regression", type="primary",
                            width="stretch")

        with hero_slot:
            _mdl_hero(len(feature_variables) if feature_variables
                      else len(ALL_FEATURES), split_variable)

        if run:
            if not feature_variables:
                st.warning("Select at least one feature.")
            else:
                train_models_all_data_web(split_variable, feature_variables)