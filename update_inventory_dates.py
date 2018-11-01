from selenium import webdriver
from time import sleep
import datetime
import os

driver = webdriver.Chrome()
BASE = 'https://apps.commercehub.com/account/login'
username = os.environ['CHUB_username']
password = os.environ['CHUB_password']
now = datetime.datetime.now()

if now.weekday() == 4:
    input_date = now + datetime.timedelta(days=3)
else:
    input_date = now + datetime.timedelta(days=1)

next_update_day = input_date.strftime('%m/%d/%Y')

def update_product_inventory():
    date_fields = driver.find_elements_by_xpath('//input[contains(@id, "nextAvailDate")]')

    for date_field in date_fields:
        date_field.clear()
        date_field.send_keys(next_update_day)


driver.get(BASE)
driver.maximize_window()

###################
# Login
###################
driver.find_element_by_id('username').send_keys(username)
driver.find_element_by_id('password').send_keys(password)
driver.find_element_by_name('submit').click()

###################
# Navigate to page
###################
sleep(1)
driver.find_element_by_id('chub-navi-my-apps-trigger').click()
sleep(1)
driver.find_element_by_id('chub-navi-feature-link-application.orderstream.production').click()
sleep(3)
driver.get('https://dsm.commercehub.com/dsm/gotoUpdateInventory.do')
driver.find_element_by_id('nonibl').click()
driver.find_element_by_id('noniblsubmit').click()

#####################
# Update inventory for all products
#####################
while True:
    sleep(.5)
    update_product_inventory()
    try:
        driver.find_element_by_link_text('Next').click()
    except:
        break

###################
# Submit Order
###################
driver.find_element_by_id('submitButton').click()
driver.quit()
