# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 11:47:41 2020

@author: ACascioli
"""

import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

import os
path = (os.path.dirname(os.path.abspath(__file__)))
variables_path = path + '\\PythonVariables\\'
struct = path + '\\2D_mol_temp\\'
species_cas = np.load(variables_path + 'cas.npy')
species = np.load(variables_path + 'species.npy')

stop = list(species).index('CH4')

vn = str(np.load(variables_path + 'variables_name.npy'))


print(len(species))
# name = 'Tc_' + vn
# print(name)

# %%

crit = 1

if crit == 1:
    timeout = 5
    driver = webdriver.Chrome('C:\\Users\\ACascioli\\OneDrive - Scientific Network South Tyrol\\Python\\HTL\\Model\\Selenium_utils\\chromedriver')
    driver.get("http://ddbonline.ddbst.de/OnlinePropertyEstimation/OnlinePropertyEstimation.exe")
    sel = '#ID4'
    DBB = driver.find_element_by_css_selector(sel)
    DBB.click()
    Tc = []
    Pc = []
    Gj0 = []
    control = 0
    for i in range(0,len(species_cas)):
        if i == stop:
            break
        print(i)
        if species_cas[i] == '7732-18-5':
            Tc.append(647.096)
            Pc.append(22060)
            Gj0.append(-237.14)
            continue
        if species_cas[i] == '7783-06-4':
            Tc.append(373.40)
            Pc.append(8970)
            Gj0.append(-33.4)
            continue
        if species_cas[i] == '7664-41-7':
            Tc.append(405.40)
            Pc.append(11300)
            Gj0.append(-26.57) # acqueous
            continue
        if species_cas[i] == '630-08-0':
            Tc.append(134.45)
            Pc.append(3521.04)
            Gj0.append(-137.16)
            continue
        if species_cas[i] == '124-38-9':
            Tc.append(304.35)
            Pc.append(7382.50)
            Gj0.append(-394.39)
            continue
        if species_cas[i] == '74-82-8':
            Tc.append(199.70)
            Pc.append(5760.00)
            Gj0.append(50.6)
            continue
        if species_cas[i] == '1333-74-0':
            Tc.append(33.18)
            Pc.append(1300.00)
            Gj0.append(0)
            continue
        if species_cas[i] == '494-99-5':
            Tc.append(693.63)
            Pc.append(3035.62)
            Gj0.append(-91.95)
            continue
        if species_cas[i] == '17059-52-8':
            Tc.append(709.16)
            Pc.append(3950.57)
            Gj0.append(130.35)
            continue
        if species_cas[i] == '2634-45-9':
            Tc.append(947.951)
            Pc.append(963.87)
            Gj0.append(-15.57)
            continue


        if i > 0 and control == 0:
            driver.execute_script("window.history.go(-2)")
            control = 0
            time.sleep(1)
        if control == 1:
            driver.execute_script("window.history.go(-1)")
            control = 0
            time.sleep(1)
        sel = '#online-ddb-form > div:nth-child(2) > form > table > tbody > tr:nth-child(2) > td > table > tbody:nth-child(2) > tr:nth-child(3) > td:nth-child(2) > input[type=text]'
        CAS = driver.find_element_by_css_selector(sel)
        CAS.clear()
        CAS.send_keys(species_cas[i])
        time.sleep(1)
        sel = '#online-ddb-form > div:nth-child(2) > form > table > tbody > tr:nth-child(2) > td > table > tbody:nth-child(2) > tr:nth-child(3) > td:nth-child(3) > input[type=submit]'
        search = driver.find_element_by_css_selector(sel)
        try:
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, sel))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        search.click()
        sel = '#online-ddb-form > div:nth-child(2) > form > table > tbody > tr:nth-child(3) > td'
        if driver.find_element_by_css_selector(sel).text == 'No component found for specified CAS registry number.':
            print('No component found for CAS number:', species_cas[i])
            # driver.get_screenshot_as_file('C:\\Users\\ACascioli\\OneDrive - Scientific Network South Tyrol\\Python\\Selenium\\google.png')
            control = 1
            driver1 = webdriver.Chrome('C:\\Users\\ACascioli\\OneDrive - Scientific Network South Tyrol\\Python\\Selenium\\chromedriver')
            driver1.get("https://www.chemeo.com/")
            sel = '#home > form > table > tbody > tr:nth-child(1) > td > input[type=text]:nth-child(1)'
            CAS = driver1.find_element_by_css_selector(sel)
            CAS.clear()
            CAS.send_keys(species_cas[i])
            sel = '#home > form > table > tbody > tr:nth-child(1) > td > input[type=submit]:nth-child(2)'
            search = driver1.find_element_by_css_selector(sel)
            search.click()
            sel1 = '#details-content > table:nth-child(2) > tbody > tr:nth-child(9) > td.r'
            sel2 = '#details-content > table:nth-child(2) > tbody > tr:nth-child(7) > td.r'
            sel3 = '#details-content > table:nth-child(2) > tbody > tr:nth-child(2) > td.r'
            stT = driver1.find_element_by_css_selector(sel1).text
            temp = []
            if ' ' in stT:
                for char in stT:
                    # print(char)
                    if char == ' ':
                        break
                    else:
                        temp.append(char)
                temp = [''.join(temp)]
                Tc.append(np.float(temp[0]))
            else:
                Tc.append(np.float(driver1.find_element_by_css_selector(sel1).text))
            stP = driver1.find_element_by_css_selector(sel2).text
            temp = []
            if ' ' in stP:
                for char in stP:
                    # print(char)
                    if char == ' ':
                        break
                    else:
                        temp.append(char)
                temp = [''.join(temp)]
                Pc.append(np.float(temp[0]))
            else:
                Pc.append(np.float(driver1.find_element_by_css_selector(sel2).text))
            stG = driver1.find_element_by_css_selector(sel3).text
            temp = []
            if ' ' in stG:
                for char in stG:
                    # print(char)
                    if char == ' ':
                        break
                    else:
                        temp.append(char)
                temp = [''.join(temp)]
                Gj0.append(np.float(temp[0]))
            else:
                Gj0.append(np.float(driver1.find_element_by_css_selector(sel3).text))
            driver1.quit()
            continue

# %%
        # time.sleep(1)
        sel = '#ID8'
        calculate = driver.find_element_by_css_selector(sel)
        try:
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, sel))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        calculate.click()
        # time.sleep(1)
        sel1 = '#online-ddb-form > div:nth-child(2) > form > table:nth-child(6) > tbody > tr:nth-child(8) > td:nth-child(2)'
        sel2 = '#online-ddb-form > div:nth-child(2) > form > table:nth-child(6) > tbody > tr:nth-child(7) > td:nth-child(2)'
        sel3 = '#online-ddb-form > div:nth-child(2) > form > table:nth-child(6) > tbody > tr:nth-child(3) > td:nth-child(2)'
        if driver.find_element_by_css_selector(sel1).text == '0' or driver.find_element_by_css_selector(sel2).text == '0':
                # driver.get_screenshot_as_file('C:\\Users\\ACascioli\\OneDrive - Scientific Network South Tyrol\\Python\\Selenium\\google.png')
                print('ciao')
                control = 1
                driver1 = webdriver.Chrome('C:\\Users\\ACascioli\\OneDrive - Scientific Network South Tyrol\\Python\\Selenium\\chromedriver')
                driver1.get("https://www.chemeo.com/")
                sel = '#home > form > table > tbody > tr:nth-child(1) > td > input[type=text]:nth-child(1)'
                CAS = driver1.find_element_by_css_selector(sel)
                CAS.clear()
                CAS.send_keys(species_cas[i])
                sel = '#home > form > table > tbody > tr:nth-child(1) > td > input[type=submit]:nth-child(2)'
                search = driver1.find_element_by_css_selector(sel)
                search.click()
                sel1 = '#details-content > table:nth-child(2) > tbody > tr:nth-child(9) > td.r'
                sel2 = '#details-content > table:nth-child(2) > tbody > tr:nth-child(7) > td.r'
                sel3 = '#details-content > table:nth-child(2) > tbody > tr:nth-child(2) > td.r'
                stT = driver1.find_element_by_css_selector(sel1).text
                temp = []
                if ' ' in stT:
                    for char in stT:
                        # print(char)
                        if char == ' ':
                            break
                        else:
                            temp.append(char)
                    temp = [''.join(temp)]
                    Tc.append(np.float(temp[0]))
                else:
                    Tc.append(np.float(driver1.find_element_by_css_selector(sel1).text))
                stP = driver1.find_element_by_css_selector(sel2).text
                temp = []
                if ' ' in stP:
                    for char in stP:
                        # print(char)
                        if char == ' ':
                            break
                        else:
                            temp.append(char)
                    temp = [''.join(temp)]
                    Pc.append(np.float(temp[0]))
                else:
                    Pc.append(np.float(driver1.find_element_by_css_selector(sel2).text))
                stG = driver1.find_element_by_css_selector(sel3).text
                temp = []
                if ' ' in stG:
                    for char in stG:
                        # print(char)
                        if char == ' ':
                            break
                        else:
                            temp.append(char)
                    temp = [''.join(temp)]
                    Gj0.append(np.float(temp[0]))
                else:
                    Gj0.append(np.float(driver1.find_element_by_css_selector(sel3).text))
                driver1.quit()
        else:
                Tc.append(np.float(driver.find_element_by_css_selector(sel1).text))
                Pc.append(np.float(driver.find_element_by_css_selector(sel2).text))
                Gj0.append(np.float(driver.find_element_by_css_selector(sel3).text))
    driver.quit()
    np.save(variables_path + 'Tc_'+vn+'.npy', Tc)
    np.save(variables_path + 'Pc_'+vn+'.npy', Pc)
    np.save(variables_path + 'Gj0_'+vn+'.npy', Gj0)
    print('Tc', Tc)
    print('Pc', Pc)
    print('G0', Gj0)
    # box.submit()
