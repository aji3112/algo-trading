import pync

def getCashDetails(driver):
    funds = driver.find_element_by_css_selector("#app > div.header > div > div.header-right > div.app-nav > a:nth-child(5)")
    funds.click()
    driver.implicitly_wait(50)
    availableCashField = driver.find_element_by_css_selector("#app > div.container.wrapper > div.container-right > div > div.margins > div.row > div:nth-child(1) > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > h1")
    availableCash = availableCashField.text
    return availableCash

