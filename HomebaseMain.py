import os
import sys
from datetime import datetime
import ctypes
import time

from HomebaseScraper.sub import CONSTANTS


import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

user32 = ctypes.windll.user32

# don't think this is sensitive data as you have to be logged in to access it
connie_id = '1494784'
joel_id = '631266'
ignacio_id = '348950'


def quit_on_error():
    input('Press enter to quit')
    quit(1)


def get_employee_data(employee_id, employee_name, start_day, end_day, month, year):
    URL = 'https://app.joinhomebase.com/timesheets#summary/{0}/{3}-{1}-{4}/{3}-{2}-{4}'.format(
        employee_id, start_day, end_day, month, year)
    driver.get(URL)  # redirects properly

    # Selenium permanently caches all requests made using xpath which means we have to make
    # requests based on EMPLOYEE NAME and not just going through the tbody which makes the
    # next xpath request we sent to Selenium of tbody equal the previous employee's data.
    # That's why we're looking for employee name and going up to the parent instead.
    person_name = WebDriverWait(driver, 20).until(
        EC.visibility_of_any_elements_located((By.PARTIAL_LINK_TEXT, employee_name)))[0]

    # go up to tbody from child
    table = person_name.find_elements_by_xpath('../../..')[0]
    row = table.find_element_by_tag_name("tr")  # list of one item
    cell = row.find_elements_by_tag_name('td')

    for i, area in enumerate(cell):
        # employee work hours are the 5th cell by default, this might be an inconsistent way
        # for getting data though
        if i == 5:
            # Homebase's HTML sucks so it saves the values with a bunch of random whitespace
            # which we want to get rid of
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
        self.year = self.get_date[2]
        self.day = self.get_date[1]
        self.month = self.get_date[0]

        self.table1 = None
        self.table2 = None

        self.start_day = start_day
        self.end_day = end_day
        self.dimensions = self.get_window_dimensions

        self.email_area = None
        self.password_area = None

    @property
    def get_date(self) -> 'datetime.now()':
        """
        :return: array, [0] is month, [1] is day [2] is year
        """
        date = datetime.now().strftime('%m %d %Y')
        return date.split()

    # this is obsolete since we can just call fullscreen without screen dimensions
    @property
    def get_window_dimensions(self):
        return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


# get these values to be user inputs, we ideally just want a value interval of
# 1-15 and 15-30 since employees get paid bimonthly


interval1 = 1
interval2 = 15

# creating instance of Information
info = Information(interval1, interval2)

# debugging and date-related problems with the program
print("Today's date is {}/{}/{}.".format(info.month, info.day, info.year))

# webdriver stuff is complicated with non-windows machines
# it this program ends up working for windows we're going to add
# linux and macOS support which shouldn't be too complicated
if 'win' not in info.os:
    print('Your operating system ({}) is not supported.'.format(info.os))


driver = webdriver.Chrome('{}/chromedriver'.format(info.path))


driver.maximize_window()

driver.get('https://app.joinhomebase.com/accounts/sign_in')

# ---------------logging in--------------
try:
    info.email_area = wait_for_id("account_login")
    info.password_area = wait_for_id("account_password")
except selenium.common.exceptions.WebDriverException:
    # the program has a problem accessing Homebase, probably because of internet problems
    # we probably don't have to handle this error again later since a connection problem
    # would exit the program the first time
    print('The program timed out before it could find the login')
    quit_on_error()


info.email_area.send_keys(CONSTANTS.login_email)
info.password_area.send_keys(CONSTANTS.login_password)

info.password_area.send_keys(Keys.RETURN)  # pressing enter, obviously


# ---- logged in after this point-----

reports_area = wait_for_id('dashboard')
# this way we know that the page is loaded and we're logged in
# dashboard is an arbitrary element on the page that loads later than the other elements


print('Logged in.')

# make these requests be in a loop based on the amount of employee data that we want to grab
# so far it's just a placeholder
joel_hours = get_employee_data(joel_id, "Joel", info.start_day, info.end_day, info.month, info.year)
connie_hours = get_employee_data(connie_id, "Connie", info.start_day, info.end_day, info.month, info.year)

print("Joel worked for " + joel_hours + " hours between {} and {}th.".format(interval1, interval2))
print("Connie worked for " + connie_hours + " hours between the {} and {}th.".format(interval1, interval2))


driver.close()

# in case we don't convert to a GUI system we want the
# information to be visible before the terminal closes
input('')


