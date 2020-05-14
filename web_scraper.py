from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time


options = webdriver.ChromeOptions()

# make the window open in the background
options.add_argument('headless')

# initialize the driver
driver = webdriver.Chrome(chrome_options=options)


def scrape_calcmaps(url):
    driver.get(url)
    time.sleep(2)
    building_specs = driver.find_element_by_id("status")
    print(building_specs.text)

    # Scrape the area from the returned HTML
    building_specs = building_specs.text.split()
    building_area = building_specs[1] + " " + building_specs[2]
    print(building_area)

    driver.quit()
    return building_area


def scrape_googlesolar(address):
    driver.get("https://www.google.com/get/sunroof")

    # Enter address information into web page
    input = driver.find_element_by_id("input-0")
    input.send_keys(address)
    time.sleep(1)  # Form requires a second to auto-populate
    input.send_keys(Keys.ENTER)

    # Allow page to load
    time.sleep(3)

    # An array containing all our solar information we want to return
    solar_specs = {}

    # Grab and append each piece of information we want
    info_from_site = driver.find_element_by_class_name("panel-facts").text
    info_from_site = info_from_site.split()

    # Get sunlight per year
    sunlight_per_year = info_from_site[0] + ' ' + info_from_site[1]
    solar_specs.update({'sunlight_per_year': sunlight_per_year})

    # Get area for solar
    area_for_panels = info_from_site[14] + ' ' + info_from_site[15] + ' ' + info_from_site[16]
    solar_specs.update({'area_for_panels': area_for_panels})

    # Get solar savings
    info_from_site = driver.find_element_by_class_name("panel-estimate-savings")
    savings_with_solar = info_from_site.text
    solar_specs.update({'savings_with_solar': savings_with_solar})

    # Get solar roof cost
    info_from_site = driver.find_element_by_class_name("cost-cell-value")
    solar_roof_cost = info_from_site.text
    solar_specs.update({'cost_of_solar': solar_roof_cost})

    return solar_specs


def scrape_nerdwallet(address):
    url_builder = "https://www.nerdwallet.com/home/home-value/my-home/"

    address_info = address.split(',')

    # Replace spaces with '%20' for url
    city_split = address_info[1].replace(" ", "%20")
    url_builder += city_split + "/"

    state_zip_split = address_info[2].split(" ")
    url_builder += state_zip_split[0] + "/"
    url_builder += state_zip_split[1] + "/"

    url_builder += address_info[0].replace(" ", "%20")

    driver.get(url_builder)

    # Allow page to load
    time.sleep(3)

    home_value = driver.find_element_by_class_name("_3gDX3._1wVT-._3ZdB_")

    return home_value.get_attribute('innerHTML')