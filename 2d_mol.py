# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 15:53:42 2020

@author: ACascioli
"""

# %%

import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import pyautogui

from bs4 import BeautifulSoup
import urllib
import urllib.request


from pathlib import Path

import winsound

frequency = 2500  # Set Frequency To 2500 Hertz
duration = 500  # Set Duration To 1000 ms == 1 second

downloads = "C:\\Users\\ACascioli\\Downloads"


import os

path = os.path.dirname(os.path.abspath(__file__))
variables_path = path + "\\PythonVariables\\"
struct = path + "\\2D_mol_temp\\"
species_cas = np.load(variables_path + "cas.npy")
species = np.load(variables_path + "species.npy")
species_names = np.load(variables_path + "species_names.npy")
# empty = np.load(variables_path + 'empty.npy')

# %%

# Clean download folder
for files in os.listdir(downloads):
    if ".mol" in files:
        print("files removed:")
        print(files)
        os.remove(files)
        print("Processing...")

# To find button position
while True:
    time.sleep(2)
    print(pyautogui.position())

# %%

"""
2D-mol
"""

mol = 1
error = []

if mol == 1:
    driver = webdriver.Chrome(
        "C:\\Users\\ACascioli\\OneDrive - Scientific Network South Tyrol\\Python\\HTL\\Model\\Selenium_utils\\chromedriver"
    )
    driver.get("http://www.chemspider.com/")
    control = 0
    timeout = 5
    for i in range(len(species_cas)):
        # if species[i] == 'CH4':
        # break
        if i > 0 and control == 0:
            driver.execute_script("window.history.go(-1)")
        try:
            ID = "onetrust-accept-btn-handler"
            try:
                element_present = EC.presence_of_element_located((By.ID, ID))
                WebDriverWait(driver, timeout).until(element_present)
            except TimeoutException:
                print(i, "Timed out waiting for page to load")
            finally:
                print(i, "Page loaded")
            sel = "#onetrust-accept-btn-handler"
            CAS = driver.find_element_by_css_selector(sel)
        except NoSuchElementException:
            print("ciao")
            ID = "ctl00_ctl00_ContentSection_ContentPlaceHolder1_simpleSearch_simple_query"
            try:
                element_present = EC.presence_of_element_located((By.ID, ID))
                WebDriverWait(driver, timeout).until(element_present)
            except TimeoutException:
                print(i, "Timed out waiting for page to load")
            finally:
                print(i, "Page loaded")
            sel = "#ctl00_ctl00_ContentSection_ContentPlaceHolder1_simpleSearch_simple_query"
            CAS = driver.find_element_by_css_selector(sel)
        CAS.click()
        sel = (
            "#ctl00_ctl00_ContentSection_ContentPlaceHolder1_simpleSearch_simple_query"
        )
        CAS = driver.find_element_by_css_selector(sel)
        CAS.clear()
        CAS.send_keys(species_cas[i])
        # time.sleep(1)
        sel = "#ctl00_ctl00_ContentSection_ContentPlaceHolder1_simpleSearch_search_text_button"
        ID = "ctl00_ctl00_ContentSection_ContentPlaceHolder1_simpleSearch_search_text_button"
        try:
            element_present = EC.presence_of_element_located((By.ID, ID))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException:
            print(i, "Timed out waiting for page to load")
        finally:
            print(i, "Page loaded")
        search = driver.find_element_by_css_selector(sel)
        search.click()
        time.sleep(2)
        # pyautogui.scroll(-100)
        time.sleep(2)
        pyautogui.click(
            x=91,
            y=910,
            clicks=1,
            button="left",
        )
        time.sleep(2)
        pyautogui.moveTo(x=91, y=896)
        time.sleep(2)
        os.chdir(downloads)  # change dir
        files = sorted(filter(os.path.isfile, os.listdir(".")), key=os.path.getmtime)
        # print(files)
        file_name = struct + species_cas[i] + ".mol"
        if species_cas[i] + ".mol" in os.listdir(struct):
            os.remove(file_name)
        if ".mol" in files[-1]:
            os.rename(downloads + "\\" + files[-1], file_name)
            winsound.Beep(frequency, duration)
        else:
            print("No files .mol available...wait", i)
            time.sleep(3)
            if ".mol" in files[-1]:
                print("File arrived", i)
                os.rename(downloads + "\\" + files[-1], file_name)
                winsound.Beep(frequency, duration)
            else:
                print("Still no files .mol available...", i)
                error.append(i)
                continue
        # if i > 0 and control == 0:
        #     driver.execute_script("window.history.go(-1)")
        #     control = 0
        # if control == 1:
        #     driver.execute_script("window.history.go(-1)")
        #     control = 0

    driver.close()

# %%

# =============================================================================
# CHECK
# =============================================================================


maxlen = len(max(species_names, key=len))

check = 1
error = []
empty = []

if check == 1:
    driver = webdriver.Chrome(
        "C:\\Users\\ACascioli\\OneDrive - Scientific Network South Tyrol\\Python\\Selenium\\chromedriver"
    )
    driver.get(
        "http://ddbonline.ddbst.de/OnlinePropertyEstimation/OnlinePropertyEstimation.exe"
    )
    control = 0
    timeout = 5
    for i in range(len(species_cas)):
        if species[i] == "H2":
            continue
        if i > 0 and control == 0:
            driver.execute_script("window.history.go(-2)")
        ID = "ID1"
        try:
            element_present = EC.presence_of_element_located((By.ID, ID))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException:
            print(i, "Timed out waiting for page to load")
        finally:
            print(i, "Page loaded")
        sel = "#ID1"
        DBB = driver.find_element_by_css_selector(sel)
        DBB.click()
        ID = "ID5"
        try:
            element_present = EC.presence_of_element_located((By.ID, ID))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException:
            print(i, "Timed out waiting for page to load")
        finally:
            print(i, "Page loaded")
        sel = "#ID5"
        fileinput = driver.find_element_by_css_selector(sel)
        fileinput.send_keys(struct + species_cas[i] + ".mol")
        sel = "#ID8"
        search = driver.find_element_by_css_selector(sel)
        search.click()
        # check if name is the same
        sel = "#online-ddb-form > div:nth-child(2) > form > h3"
        form = driver.find_element_by_css_selector(sel).text
        # check if mol file is empty
        sel = "#online-ddb-form > div:nth-child(2) > form > table > tbody > tr:nth-child(7) > td:nth-child(2)"
        Pc = driver.find_element_by_css_selector(sel).text
        if Pc == "0":
            print("file for %s exists but is empty..." % species_names[i])
            empty.append(species_names[i])
        else:
            print(
                "%s\t%s\t%s\t\t%s"
                % (
                    species_names[i].ljust(maxlen, " "),
                    species_cas[i],
                    species[i],
                    form,
                )
            )
        time.sleep(1)
    np.save(variables_path + "empty.npy", empty)
    driver.close()
