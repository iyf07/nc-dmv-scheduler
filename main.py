from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from datetime import date
from selenium import webdriver
from selenium.common.exceptions import *
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import re

# Create Flask application
app = Flask(__name__)


@app.route('/home.html')
def renderHome():
    return render_template('home.html')


@app.route('/form.html')
def renderForm():
    return render_template('form.html')


@app.route('/result', methods=["post"])
def renderResult():

    # Retrive information from the user
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    phone = request.form.get('phone')
    zipcode = request.form.get('zipcode')
    distance = request.form.get('distance')
    email = request.form.get('email')
    dateafter = date.fromisoformat(request.form.get('dateafter'))
    datebefore = date.fromisoformat(request.form.get('datebefore'))
    days = request.form.getlist('day')
    appointment = request.form.get('appointment')
    timerange = request.form.getlist('time')
    textcheck = request.form.get('textcheck')
    emailcheck = request.form.get('emailcheck')

    # Main function
    main(firstname, lastname, phone, zipcode, distance, email, dateafter, datebefore, appointment, days, timerange,
         textcheck, emailcheck)


# Change the format of dates in order to search for all the matching dates
def dateconvert(_date):
    datetemp = date.fromisoformat('2021-07-02')
    interval = _date - datetemp
    datetempvalue = 16251840
    datevalue = (datetempvalue + interval.days * 864) * 100000
    return datevalue


# Get user's available dates with constraint of weekdays, date before, and date after
def getdate(dateafter, datebefore, days):
    datea = dateconvert(dateafter)
    dateb = dateconvert(datebefore) + 86400000
    uncleanedlist = []
    cleanedlist = []
    for _date in range(datea, dateb, 86400000):
        uncleanedlist.append(_date)
    for day in days:
        for _date in uncleanedlist:
            if (int(_date) - (1625184000000 - 86400000 * int(day))) % (86400000 * 7) == 0:
                cleanedlist.append(_date)
    cleanedlist.sort()
    return cleanedlist


# Get user's available time
def gettime(timerange):
    timeframe = []
    for _time in timerange:
        for i in range(4):
            temp = 420 + int(_time) * 60 + i * 15
            timeframe.append(temp)
    return timeframe


# Simulate a click on the home page to the schedule appointment page
# Enter the zipcode of the user and sort all the locations by distance
def webclick(driver, zipcode, appointment):
    url = "https://skiptheline.ncdot.gov/Webapp"

    # Go to the home page
    driver.get(url)
    driver.find_element_by_xpath("//button[@class='btn btn-CustomActions-darkblue btn-block']").click()
    driver.find_elements_by_xpath("//button[@class='submit btn btn-CustomObjects heightButtonsAppType btn-block']")[
        int(appointment)].click()


    # Enter the zipcode
    driver.find_element_by_id("ZipCode").send_keys(zipcode)

    # Click the button of sorting locations by distance whenever the button is available to click
    while True:
        try:
            driver.find_element_by_xpath("//i[@class='glyphicon glyphicon-search']").click()
            break
        except ElementClickInterceptedException:
            pass


# Get all the locations with a distance constraint
def scrapelocations(driver, distance):
    # Set up beautifulsoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all the elements inside the div tags
    source = soup.findAll('div')

    # Scrape the name and distance of all the locations
    resulttemp = re.findall(r'centerDiv">\n([\w\W]+?) Miles</span>', str(source))
    locationlist = []

    # Iterate through the name and distance of all the location
    for i in resulttemp:
        i = i.strip()
        location = re.findall(r'^([\w ]*)\n', i)[0]
        miles = re.findall(r'\d+\.*\d*$', i)[0]

        # Add the location name to the list if it is not in the list and the distance meets user's requirement
        if int(float(miles)) <= int(distance) and location not in locationlist:
            locationlist.append(location)
    return locationlist


# Search for the dates and time to find the available time for user
def searchdate(driver, locations, datelist, timelist):
    # After iterating through the location list, interate again until find an available date and time which will return true to end this function
    while True:

        # Iterate through the location list
        for locationnumber in range(len(locations)):
            driver.find_elements_by_xpath("//button[@class='btn btn-danger btn-block']")[locationnumber].click()
            driver.find_element_by_id("Date").click()

            # Times clicking the button of next month
            nexttimes = 0
            dateopen = []
            while True:
                try:

                    # If there is no available date in three months, break this indefinite iteration and search for the next location
                    if nexttimes == 3:
                        driver.back()
                        break

                    # Open dates have class name "day"
                    # Find all the open date elements in current month
                    dateopenelements = driver.find_elements_by_xpath("//td[@class='day']")

                    # Get the date of the elements, convert them to int, and store them in dateopen list
                    for _date in dateopenelements:
                        dateopen.append(int(_date.get_attribute('data-date')))

                    # Iterate through the dateopen list
                    for _date in dateopen:

                        # If an element in the dateopen list matches with user's available dates, click the date
                        if _date in datelist:
                            datexpath = f"//td[@class='day'][@data-date={_date}]"
                            driver.find_element_by_xpath(datexpath).click()

                            # Check the available time of this date
                            if searchtime(driver, timelist):

                                # Return true if find a matching open time
                                return True

                            # if not find an available time, try the next date
                            else:
                                driver.find_element_by_id("Date").click()

                    # If there is no available date in this month, click to the next month
                    driver.find_element_by_class_name("next").click()
                    nexttimes += 1

                # If there is no open date in this month
                except NoSuchElementException:
                    nexttimes += 1

                    # Try click to the next month
                    try:
                        driver.find_element_by_class_name("next").click()

                    # If cannot click to the next month (the only reason is that this location is temporarily closed)
                    except NoSuchElementException:
                        # Break the loop and try the next location
                        driver.back()
                        break


# Check the available time of this date
def searchtime(driver, timelist):
    # Click the time block
    driver.find_element_by_id("Time").click()

    # Iterate through user's available time slots
    for _time in timelist:

        # Try click user's time slot
        try:
            timexpath = f"//option[@value={_time}]"
            driver.find_element_by_xpath(timexpath).click()

            # Return true if find an open time
            return True

        # If the time slot is not open, search for the next available time slot of user
        except NoSuchElementException:
            continue

    # After iterating over user's aviable time slots, if there is no matching open time, return false
    return False


def enterinfo(driver, firstname, lastname, phone, email, textcheck, emailcheck):

    # Enter the personal information and simulate to click to finish the registration
    driver.find_element_by_id("Validate").click()
    driver.find_element_by_id("TelNumber1").send_keys(phone)
    driver.find_element_by_id("FirstName").send_keys(firstname)
    driver.find_element_by_id("LastName").send_keys(lastname)
    driver.find_element_by_id("EMail").send_keys(email)
    driver.find_element_by_id("Conf_EMail").send_keys(email)
    if textcheck == "true":
        driver.find_element_by_id("2").click()
    if emailcheck == "true":
        driver.find_element_by_id("1").click()
    driver.find_element_by_id("Validate").click()

    # COMMENT OUT THIS LINE IF YOU WANT TO TEST THE PROGRAM INSTEAD OF SCHEDULLING AN APPOINTMENT
    # UNCOMMENT THE CODE ONLY WHEN YOU WANT TO SCHEDULE AN APPOINTMENT
    # driver.find_element_by_id("Validate").click()


def main(firstname, lastname, phone, zipcode, distance, email, dateafter, datebefore, appointment, days, timerange,
         textcheck, emailcheck):
    datelist = getdate(dateafter, datebefore, days)
    timelist = gettime(timerange)

    # Set up the driver
    option = webdriver.ChromeOptions()

    # COMMENT OUT THESE TWO LINES TO RUN WEBDRIVER WITH OPENING BROWSER
    # option.add_argument('headless')

    driver = webdriver.Chrome(ChromeDriverManager().install(), options = option)

    webclick(driver, zipcode, appointment)
    locations = scrapelocations(driver, distance)

    # If find an available date and time, the personal information will be entered to finish the registration
    if searchdate(driver, locations, datelist, timelist):
        enterinfo(driver, firstname, lastname, phone, email, textcheck, emailcheck)

if __name__ == '__main__':
    app.run(debug=True)
