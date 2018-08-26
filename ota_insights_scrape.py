#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ota_insights_scrape.py
#  
#  Copyright 2018 Paul <paul@Paul-jc>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

"""
This program is to scrape files from the website OTA Insights in order to process in bulk with the 
intention of concatinating them using my other program OTA-data-compiler.
It will prompt for username and password (input feedback hidden from password).

To use this program change line 153 to your default download location and the desired folder to store 
processed files on line 135.

Future development will include developing a GUI for date and offset as well as including the ability 
to run multiple offsets in one functions. Also dynamicallly select download location and where files 
will be saved once processed.

Later development will also integrate the OTA-data-compiler program into the same GUI for downloading
and processing of all files in one program.

Eventually this will also include a machine learning process and price recommendation facility.
"""

import os
import time
import getpass
from random import randint
from selenium import webdriver
from pyvirtualdisplay import Display
from datetime import timedelta, date
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options


# Prompt user for username and password, using getpass to hide password
user_username = input("Please enter username: ")
user_password = getpass.getpass("Please enter password: ")
# As a quick solution to recieving user input, will taking each element seperately for now
user_start_year = input("Please enter start date year as 'yyyy': ")
user_start_month = input("Please enter start date month as 'mm': ")
user_start_day = input("Please enter start date day as 'dd': ")
user_end_year = input("Please enter end date year as 'yyyy': ")
user_end_month = input("Please enter end date month as 'mm': ")
user_end_day = input("Please enter end date day as 'dd': ")
offset_select = input("Please enter offset 0 or multiples of 30: ")

# Use chrome to navigate and download files individually
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")

# Set download setting so that user is not prompted to accept the download each time
options = Options()
options.add_experimental_option("prefs", {
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})

# This protocol will add periodic pauses into the program to stop putting too much traffic through the website 
# and possibly either negatively impact other users experience or cause website to block user
def throttle(f):
    r = f % 18
    if r == 0:
        print("pausing 15 seconds")
        time.sleep(15)
    r = f % 45
    if r == 0:
        print("throttling 3 minutes")
        time.sleep(180)

# Used to navigate to the login page and use previously saved username and password to log into user account
def login_page(i):
    driver.get("https://app.otainsight.com/hotel/72204/rates?compsetId=1&los=1&otaId=bookingdotcom")
    time.sleep(i)
    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")
    username.send_keys(user_username)
    password.send_keys(user_password)
    driver.find_element_by_id("loginbutton").click()

# Problems were encounted with delay in the buttons loading, this waits 2 seconds, tries to click botton 
# waits 3 more seconds if not present then tries again. If still not successful it will trow error containing date of files being downloaded at the time
def check_button(*args):
    time.sleep(2)
    try:
        driver.find_element_by_class_name('export-button').click()
        
    except(NoSuchElementException):
        try:
            time.sleep(3)
            driver.find_eilement_by_class_name('export-button').click
        except(NoSuchElementException):
            print("Error found while exporting " + str(date))
            sys.exit(1)
        else:
            pass
    else:
        pass

# This delays random intervals to emulate true user behaviour and navigates to the url given before going to the check_button protocol to download the file
def download(d):
    driver.get(d)
    delay = randint(10,18)
    time.sleep(delay)
    check_button()

# This protocol checks the file has been downloaded and repeats if nessesary
def check_for_file (fname):
    time.sleep(2)
    while not os.path.isfile(fname):
        time.sleep(2)
        print("file delay")

# This will first check that the file has downloaded using check_for_file before renaming it
def rename_file (oldfile, date, offset):
    time.sleep(3)
    rename = "/home/user/Downloads/OTA_Insights/Report" + str(date) + "_" + offset + "days.xlsx"
    os.rename(oldfile, rename)

#another_day = timedelta(days = 1)

# To iterate over dates during iterations
from datetime import timedelta, date
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

# Implement start and end date
start_date = date(int(user_start_year), int(user_start_month), int(user_start_day))
end_date = date(int(user_end_year), int(user_end_month), int(user_end_day)+1)


def url_creation(offset):
    #impliement 0 day iteration - need to seperate single date from input
    oldfile = "/home/user/Downloads/Report.xlsx"
    file_number = 1
    for single_date in daterange(start_date, end_date):
        d = str(single_date.day).rjust(2, '0')
        m = str(single_date.month).rjust(2, '0')
        y = str(single_date.year)
        if offset == 0:
            url = "https://app.otainsight.com/hotel/72204/rates/detail?cancellable=false&compsetId=1&date="+y+"-"+m+"-"+d+"&los=1&month="+y+"-"+m+"&otaId=bookingdotcom&view=table"
        else:
            url = "https://app.otainsight.com/hotel/72204/rates/detail?cancellable=false&compsetId=1&date="+y+"-"+m+"-"+d+"&los=1&offset="+offset+"&otaId=bookingdotcom&view=table"
        
        print(str(single_date) + " download started")   #    *** FIX change date string to dd-mm-yyyy format ***
        if single_date == start_date:
            login_page(5)
        else:
            pass
        delay = randint(10,16)
        time.sleep(delay)
        throttle(file_number)
        download(url)
        check_for_file(oldfile)
        rename_file(oldfile,single_date,offset)
        file_number += 1
    print("Complete " + str(start_date) + " to " + str(end_date) + " " + str(offset) + "days offset - " + str(file_number) + " files")   #    *** FIX - change date string to dd-mm-yyyy format, also needs to be original selection rather than incremented by 1 on end date***


url_creation(offset_select)
