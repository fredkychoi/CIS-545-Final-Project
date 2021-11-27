import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

url_head = "https://racing.hkjc.com/racing/information/English/Racing/LocalResults.aspx?RaceDate="
url_mid = "&Racecourse="
url_end = "&RaceNo="

no_races_xpath = "//div[2]/table/tbody/tr/td/a"
type_xpath = "/html/body/div/div[4]/table/tbody/tr[2]/td[1]"
going_xpath = "/html/body/div/div[4]/table/tbody/tr[2]/td[3]"
course_xpath = "/html/body/div/div[4]/table/tbody/tr[3]/td[3]"
purse_xpath = "/html/body/div/div[4]/table/tbody/tr[4]/td[1]"
table_xpath = "//div[5]/table/tbody/tr/td"

driver = webdriver.Chrome()
driver.set_page_load_timeout(30)
wait = WebDriverWait(driver, 10)

def verify(xpath):
  try:
      driver.find_element(By.XPATH, xpath)
  except NoSuchElementException:
      return False
  
  return True

def race_scrape(race_date, loc):
    print("Scraping Date: " + race_date)
    url_full = url_head + race_date + url_mid + loc

    driver.get(url_full)
    driver.implicitly_wait(20)
    wait.until(EC.presence_of_element_located((By.XPATH, no_races_xpath)))
    num_races = driver.find_elements(By.XPATH, no_races_xpath)
    urls = []
    race_df = pd.DataFrame({'Date': [], 'Loc.': [], 'Race No.': [], 'Type': [], 'Going': [], 
        'Course': [], 'Purse': [], 'Place': [], 'No.': [], 'Horse': [], 'Jockey': [], 'Trainer': [], 
        'Act. Wt.': [], 'Decl. Horse Wt.': [], 'Draw': [], 'LBW': [], 'Running Pos.': [], 
        'Finish Time': [], 'Win Odds': []})

    print("    Found: " + str(len(num_races)) + " races")

    for i in range(len(num_races)):
        urls.append(url_full + url_end + str(i + 1))

    for i in range(len(num_races)):
        print(urls[i])
        driver.get(urls[i])
        driver.implicitly_wait(20)

        type = ""
        going = ""
        course = ""
        purse = ""

        if (verify(type_xpath)):
            temp_type = wait.until(EC.presence_of_element_located((By.XPATH, type_xpath)))
            type = (temp_type.text)
            print(type)

        if (verify(going_xpath)):
            temp_going = wait.until(EC.presence_of_element_located((By.XPATH, going_xpath)))
            going = (temp_going.text)
            print(going)

        if (verify(course_xpath)):
            temp_course = wait.until(EC.presence_of_element_located((By.XPATH, course_xpath)))
            course = (temp_course.text)
            print(course)
        
        if (verify(purse_xpath)):
            temp_purse = wait.until(EC.presence_of_element_located((By.XPATH, purse_xpath)))
            purse = (temp_purse.text)
            print(purse)

        if (verify(table_xpath)):
            temp_table = wait.until(EC.presence_of_all_elements_located((By.XPATH, table_xpath)))
            table = temp_table
            num_elements = len(table)
            
            if (num_elements % 12 == 0 and num_elements > 0):
                num_horses = int(num_elements / 12)

                for j in range(num_horses):
                    start_index = j * 12
                    pd_new_row = [race_date, loc, i + 1, type, going, course, purse] 
                    
                    for k in range(12):
                        pd_new_row.append(table[start_index + k].text)

                    print(pd_new_row)

    return

if __name__ == "__main__":
    race_scrape("2020/09/06", "ST")