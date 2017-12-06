import os
import sys
from datetime import datetime
import ctypes
import time

from HomebaseScraper.sub import CONSTANTS

import csv

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import *

user32 = ctypes.windll.user32

connie_id = '1494784'
joel_id = '631266'
ignacio_id = '348950'

table1 = None

def quit_on_error():
    input('Press enter to quit')
    quit(1)


def get_employee_data(employee_id, employee_name, start_day, end_day, month, year):
    URL = 'https://app.joinhomebase.com/timesheets#summary/{0}/{3}-{1}-{4}/{3}-{2}-{4}'.format(
        employee_id, start_day, end_day, month, year)
    driver.get(URL)  # redirects properly

    person_name = WebDriverWait(driver, 20).until(
        EC.visibility_of_any_elements_located((By.PARTIAL_LINK_TEXT, employee_name)))[0]

    table = person_name.find_elements_by_xpath('../../..')[0]
    row = table.find_element_by_tag_name("tr")  # list of one item
    cell = row.find_elements_by_tag_name('td')

    for i, area in enumerate(cell):
        if i == 5:
            final_hours = area.get_attribute('innerText').replace(' ', '').strip()

            return final_hours


def wait_for_id(element):
    return WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, element)))


def wait_for_name(element):
    return WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, element)))


class Information:
    def __init__(self, start_day, end_day):
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.os = sys.platform
        self.date = datetime.now()
        # we don't really need to worry about year since the site already gets you in the right year
        self.month = 11  # TODO: change this later
        self.day = self.get_date[1]
        self.year = 2017

        self.table1 = None
        self.table2 = None

        self.start_day = start_day
        self.end_day = end_day
        self.dimensions = self.get_window_dimensions

    @property
    def get_date(self) -> 'datetime.now()':
        """
        :return: array, [0] is month, [1] is day [2] is year
        """
        date = datetime.now().strftime('%m %d %Y')
        return date.split()

    @property
    def get_window_dimensions(self):
        return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

interval1 = 1
interval2 = 15
info = Information(interval1, interval2)  # these values will change

if 'win' not in info.os:
    # webdriver stuff is complicated with non-windows machines
    print('Your operating system ({}) is not supported.'.format(info.os))


driver = webdriver.Chrome('{}/chromedriver'.format(info.path))



#  kinda unnecessary
driver.set_window_size(info.dimensions[0], info.dimensions[1])
driver.set_window_position(0, 0)

driver.maximize_window()

driver.get('https://app.joinhomebase.com/accounts/sign_in')
email_area = None
password_area = None

try:
    email_area = wait_for_id("account_login")
    password_area = wait_for_id("account_password")
except selenium.common.exceptions.WebDriverException:
    print('The program timed out before it could find the login')
    quit_on_error()


email_area.send_keys(CONSTANTS.login_email)
password_area.send_keys(CONSTANTS.login_password)

password_area.send_keys(Keys.RETURN)

# ---- logged in after this point-----

try:
    reports_area = wait_for_id('dashboard')
    # this way we know that the page is loaded, dashboard is arbitrary
except Exception as e:
    print(e)

print('Logged in.')


joel_hours = get_employee_data(joel_id, "Joel", info.start_day, info.end_day, info.month, info.year)

connie_hours = get_employee_data(connie_id, "Connie", info.start_day, info.end_day, info.month, info.year)

print("Connie worked for " + connie_hours + " hours between the {} and {}th.".format(interval1, interval2))

print("Joel worked for " + joel_hours + " hours between {} and {}th.".format(interval1, interval2))


driver.close()
input('')
