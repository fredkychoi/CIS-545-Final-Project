from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import string

url_head = "https://racing.hkjc.com/racing/information/English/Racing/LocalResults.aspx?RaceDate="
url_mid = "&Racecourse="
url_end = "&RaceNo="

race_name_xpath = "/html/body/div/div[4]/table/thead/tr/td[1]"
race_type_xpath = "/html/body/div/div[4]/table/tbody/tr[2]/td[1]"
race_going_xpath = "/html/body/div/div[4]/table/tbody/tr[2]/td[3]"
race_table_xpath = string.Template('''/html/body/div/div[5]/table/tbody/tr[$row]/td[$col]''')
no_races_xpath = "//div[2]/table/tbody/tr/td/a"

def race_scrape(race_date, course):
    driver = webdriver.Chrome()
    driver.set_page_load_timeout(30)
    wait = WebDriverWait(driver, 10)

    print("Scraping Date: " + race_date)
    url_full = url_head + race_date + url_mid + course

    driver.get(url_full)
    driver.implicitly_wait(2)
    wait.until(EC.presence_of_element_located((By.XPATH, no_races_xpath)))
    num_races = driver.find_elements(By.XPATH, no_races_xpath)
    urls = []

    print("    Found: " + str(len(num_races)) + " races")

    for i in range(len(num_races)):
        urls.append(url_full + url_end + str(i + 1))

    for url in urls:
        driver.get(url)
        driver.implicitly_wait(2)

        

    return

if __name__ == "__main__":
    race_scrape("2020/09/06", "ST")