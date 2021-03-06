import csv
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# URLs for race data
url_race_head = "https://racing.hkjc.com/racing/information/English/Racing/LocalResults.aspx?RaceDate="
url_race_mid = "&Racecourse="
url_race_end = "&RaceNo="

# URLs for horse data
url_horse_list = "http://racing.hkjc.com/racing/information/English/Horse/SelectHorsebyChar.aspx?ordertype="

# XPATHs for race data
no_races_xpath = "//div[2]/table/tbody/tr/td/a"
type_xpath = "/html/body/div/div[4]/table/tbody/tr[2]/td[1]"
going_xpath = "/html/body/div/div[4]/table/tbody/tr[2]/td[3]"
course_xpath = "/html/body/div/div[4]/table/tbody/tr[3]/td[3]"
purse_xpath = "/html/body/div/div[4]/table/tbody/tr[4]/td[1]"
table_xpath = "//div[5]/table/tbody/tr/td"

# XPATHs for horse data
country_of_origin_age_xpath = "//div[1]/table[1]/tbody/tr/td[2]/table/tbody/tr[1]/td[3]"
color_sex_xpath = "//div[1]/table[1]/tbody/tr/td[2]/table/tbody/tr[2]/td[3]"
import_type_xpath = "//div[1]/table[1]/tbody/tr/td[2]/table/tbody/tr[3]/td[3]"
season_stakes_xpath = "//div[1]/table[1]/tbody/tr/td[2]/table/tbody/tr[4]/td[3]"
total_stakes_xpath = "//div[1]/table[1]/tbody/tr/td[2]/table/tbody/tr[5]/td[3]"
total_stakes_retired_xpath = "//div[1]/table[1]/tbody/tr/td[2]/table/tbody/tr[4]/td[3]"
no_of_123_starts_xpath = "//div[1]/table[1]/tbody/tr/td[2]/table/tbody/tr[6]/td[3]" 
no_of_123_starts_retired_xpath = "//div[1]/table[1]/tbody/tr/td[2]/table/tbody/tr[5]/td[3]"
no_of_starts_in_past_races_xpath = "//div[1]/table[1]/tbody/tr/td[2]/table/tbody/tr[7]/td[3]"
stable_loc_test_xpath = "//div[1]/table[1]/tbody/tr/td[2]/table/tbody/tr[8]/td[1]"
stable_loc_1_xpath = "//div[1]/table[1]/tbody/tr/td[2]/table/tbody/tr[8]/td[3]"
stable_loc_2_xpath = "//div[1]/table[1]/tbody/tr/td[2]/table/tbody/tr[9]/td[3]"
trainer_xpath = "//div[1]/table[1]/tbody/tr/td[3]/table/tbody/tr[1]/td[3]/a"
owner_xpath = "//div[1]/table[1]/tbody/tr/td[3]/table/tbody/tr[2]/td[3]/a"
owner_retired_xpath = "//div[1]/table[1]/tbody/tr/td[3]/table/tbody/tr[1]/td[3]/a"
current_rating_xpath = "//div[1]/table[1]/tbody/tr/td[3]/table/tbody/tr[3]/td[3]"
start_of_season_rating_xpath = "//div[1]/table[1]/tbody/tr/td[3]/table/tbody/tr[4]/td[3]"
last_rating_xpath = "//div[1]/table[1]/tbody/tr/td[3]/table/tbody/tr[2]/td[3]"
sire_xpath = "//div[1]/table[1]/tbody/tr/td[3]/table/tbody/tr[5]/td[3]"
sire_retired_xpath = "//div[1]/table[1]/tbody/tr/td[3]/table/tbody/tr[3]/td[3]"
dam_xpath = "//div[1]/table[1]/tbody/tr/td[3]/table/tbody/tr[6]/td[3]"
dam_retired_xpath = "//div[1]/table[1]/tbody/tr/td[3]/table/tbody/tr[4]/td[3]"
dam_sire_xpath = "//div[1]/table[1]/tbody/tr/td[3]/table/tbody/tr[7]/td[3]"
dam_sire_retired_xpath = "//div[1]/table[1]/tbody/tr/td[3]/table/tbody/tr[5]/td[3]"

# Setup web driver for automated data scraping
driver = webdriver.Chrome()
driver.set_page_load_timeout(30)
wait = WebDriverWait(driver, 10)

# DataFrame to keep track of horses
horse_df = pd.DataFrame({'Name': [], 'URL': [], 'Country': [], 'Age': [], 'Color': [], 'Sex': [], 
    'Import': [], 'Season Stakes': [], 'Total Stakes': [], 'No. 123 Starts': [], 'No. Starts In Past 10': [],
    'Stable Location': [], 'Trainer': [], 'Owner': [], 'Current Rating': [], 'SoS Rating': [], 'Sire': [],
    'Dam': [], 'Dams Sire': [], 'Retired': []})

'''
Function that checks if a XPATH input is valid and can be found

@param xpath: The xpath to be checked
@return: True if xpath is valid, false otherwise
'''
def verify(xpath):
  try:
      driver.find_element(By.XPATH, xpath)
  except NoSuchElementException:
      return False
  
  return True

'''
Function that scrapes data based on race date and location

@param race_date: The date of the race requested, inputted as a string
@param loc: Either ST or HV, inputted as a string
'''
def race_scrape(race_date, loc, writer_race, writer_horse):
    print("Scraping Date: " + race_date)
    url_full = url_race_head + race_date + url_race_mid + loc

    driver.get(url_full)
    driver.implicitly_wait(20)
    wait.until(EC.presence_of_element_located((By.XPATH, no_races_xpath)))
    num_races = driver.find_elements(By.XPATH, no_races_xpath)
    urls = []
    # race_df = pd.DataFrame({'Date': [], 'Loc.': [], 'Race No.': [], 'Type': [], 'Going': [], 
    #     'Course': [], 'Purse': [], 'Place': [], 'No.': [], 'Horse': [], 'Jockey': [], 'Trainer': [], 
    #     'Act. Wt.': [], 'Decl. Horse Wt.': [], 'Draw': [], 'LBW': [], 'Running Pos.': [], 
    #     'Finish Time': [], 'Win Odds': []})

    print("    Found: " + str(len(num_races)) + " races")
    for i in range(len(num_races)):
        urls.append(url_full + url_race_end + str(i + 1))

    for i in range(len(num_races)):
        # print(urls[i])
        driver.get(urls[i])
        driver.implicitly_wait(20)

        type = None
        going = None
        course = None
        purse = None

        if (verify(type_xpath)):
            temp_type = wait.until(EC.presence_of_element_located((By.XPATH, type_xpath)))
            type = (temp_type.text)
            # print(type)

        if (verify(going_xpath)):
            temp_going = wait.until(EC.presence_of_element_located((By.XPATH, going_xpath)))
            going = (temp_going.text)
            # print(going)

        if (verify(course_xpath)):
            temp_course = wait.until(EC.presence_of_element_located((By.XPATH, course_xpath)))
            course = (temp_course.text)
            # print(course)
        
        if (verify(purse_xpath)):
            temp_purse = wait.until(EC.presence_of_element_located((By.XPATH, purse_xpath)))
            purse = (temp_purse.text)
            # print(purse)

        if (verify(table_xpath)):
            temp_table = wait.until(EC.presence_of_all_elements_located((By.XPATH, table_xpath)))
            table = temp_table
            num_elements = len(table)
            
            if (num_elements % 12 == 0 and num_elements > 0):
                num_horses = int(num_elements / 12)

                for j in range(num_horses):
                    driver.get(urls[i])
                    driver.implicitly_wait(20)
                    temp_table = wait.until(EC.presence_of_all_elements_located((By.XPATH, table_xpath)))
                    table = temp_table
                    start_index = j * 12
                    pd_new_row = [race_date, loc, i + 1, type, going, course, purse] 
                    
                    for k in range(12):
                        if k != 8:
                            pd_new_row.append(table[start_index + k].text)
                        else:
                            pd_new_row.append('"' + table[start_index + k].text + '"')
                    
                    writer_race.writerow(pd_new_row)
                    
                    url_array = temp_table[start_index + 2].find_elements(By.TAG_NAME, 'a')
                    horse_url = url_array[0].get_attribute("href")

                    horse_scrape(horse_url, temp_table[start_index + 2].text, writer_horse)            

    return

'''
Function that scrapes data based on horse url and name. Adds values to horse_df if its 
entry does not exist in the dataframe.

@param horse_url: URL of the horse's webpage
@param horse_name: Name of the horse for string comparison with horse_df entries.
'''
def horse_scrape(horse_url, horse_name, writer_horse):
    # TODO: actually add it to horsedf
    if (horse_name in horse_df['Name']):
        print("We have it already!")
        return
    else:
        retrieve_name = None
        country_of_origin = None
        age = -1
        color = None
        sex = None
        import_type = None
        season_stakes = None
        total_stakes = None
        no_123_starts = None
        no_starts_in_10 = -1
        stable_loc = None
        trainer = None
        owner = None
        current_rating = -1
        sos_rating = -1
        sire = None
        dam = None
        dam_sire = None
        retired = False

        try:
            driver.get(horse_url)
            driver.implicitly_wait(20)
        except:
            print("WARNING: URL NOT FOUND. CHECK TIMEOUT.")
            print(horse_url)

        retrieve_name_xpath = "//div[1]/table[1]/tbody/tr/td[1]/table/tbody/tr[1]/td[1]"
        
        if (verify(retrieve_name_xpath)):
            wait.until(EC.presence_of_element_located((By.XPATH, retrieve_name_xpath)))
            retrieve_name = driver.find_element(By.XPATH, retrieve_name_xpath).text
        else:
            return

        if '(Retired)' in retrieve_name or '(Deregistered)' in retrieve_name:
            retired = True

        if (verify(country_of_origin_age_xpath)):
            wait.until(EC.presence_of_element_located((By.XPATH, country_of_origin_age_xpath)))
            country_age = driver.find_element(By.XPATH, country_of_origin_age_xpath).text

            tokens = country_age.split()

            if (len(tokens) == 1):
                country_of_origin = country_age
            elif (len(tokens) == 3):
                country_of_origin = tokens[0]
                age = int(tokens[2])

        if (verify(color_sex_xpath)):
            wait.until(EC.presence_of_element_located((By.XPATH, color_sex_xpath)))
            color_sex = driver.find_element(By.XPATH, color_sex_xpath).text

            tokens = color_sex.split()

            if (len(tokens) == 1):
                color = color_sex
            elif (len(tokens) == 3):
                color = tokens[0]
                sex = tokens[2]

        if (verify(import_type_xpath)):
            wait.until(EC.presence_of_element_located((By.XPATH, import_type_xpath)))
            import_type = driver.find_element(By.XPATH, import_type_xpath).text

        if not retired:
            if (verify(season_stakes_xpath)):
                wait.until(EC.presence_of_element_located((By.XPATH, season_stakes_xpath)))
                season_stakes = driver.find_element(By.XPATH, season_stakes_xpath).text

            if (verify(total_stakes_xpath)):
                wait.until(EC.presence_of_element_located((By.XPATH, total_stakes_xpath)))
                total_stakes = driver.find_element(By.XPATH, total_stakes_xpath).text

            if (verify(no_of_123_starts_xpath)):
                wait.until(EC.presence_of_element_located((By.XPATH, no_of_123_starts_xpath)))
                no_123_starts = driver.find_element(By.XPATH, no_of_123_starts_xpath).text

            if (verify(no_of_starts_in_past_races_xpath)):
                wait.until(EC.presence_of_element_located((By.XPATH, no_of_starts_in_past_races_xpath)))
                no_starts_in_10 = driver.find_element(By.XPATH, no_of_starts_in_past_races_xpath).text

            if (verify(stable_loc_test_xpath)):
                wait.until(EC.presence_of_element_located((By.XPATH, stable_loc_test_xpath)))
                stable_loc_test = driver.find_element(By.XPATH, stable_loc_test_xpath).text

                if "PP Pre-import races footage" in stable_loc_test:
                    stable_loc = driver.find_element(By.XPATH, stable_loc_2_xpath).text.replace('\n','')
                else:
                    stable_loc = driver.find_element(By.XPATH, stable_loc_1_xpath).text.replace('\n','')

            if (verify(trainer_xpath)):
                wait.until(EC.presence_of_element_located((By.XPATH, trainer_xpath)))
                trainer = driver.find_element(By.XPATH, trainer_xpath).text

            if (verify(owner_xpath)):
                wait.until(EC.presence_of_element_located((By.XPATH, owner_xpath)))
                owner = driver.find_element(By.XPATH, owner_xpath).text

            if (verify(current_rating_xpath)):
                wait.until(EC.presence_of_element_located((By.XPATH, current_rating_xpath)))

                try:
                    current_rating = int(driver.find_element(By.XPATH, current_rating_xpath).text)
                except:
                    current_rating = 0

            if (verify(start_of_season_rating_xpath)):
                wait.until(EC.presence_of_element_located((By.XPATH, start_of_season_rating_xpath)))
                
                try:
                    sos_rating = int(driver.find_element(By.XPATH, start_of_season_rating_xpath).text)
                except:
                    sos_rating = 0

            if (verify(sire_xpath)):
                wait.until(EC.presence_of_element_located((By.XPATH, sire_xpath)))
                sire = driver.find_element(By.XPATH, sire_xpath).text

            if (verify(dam_xpath)):
                wait.until(EC.presence_of_element_located((By.XPATH, dam_xpath)))
                dam = driver.find_element(By.XPATH, dam_xpath).text

            if (verify(dam_sire_xpath)):
                wait.until(EC.presence_of_element_located((By.XPATH, dam_sire_xpath)))
                dam_sire = driver.find_element(By.XPATH, dam_sire_xpath).text
        else:
            if (verify(total_stakes_retired_xpath)):
                wait.until(EC.presence_of_element_located((By.XPATH, total_stakes_retired_xpath)))
                total_stakes = driver.find_element(By.XPATH, total_stakes_retired_xpath).text

            if (verify(no_of_123_starts_retired_xpath)):
                wait.until(EC.presence_of_element_located((By.XPATH, no_of_123_starts_retired_xpath)))
                no_123_starts = driver.find_element(By.XPATH, no_of_123_starts_retired_xpath).text

            if (verify(owner_retired_xpath)):
                wait.until(EC.presence_of_element_located((By.XPATH, owner_retired_xpath)))
                owner = driver.find_element(By.XPATH, owner_retired_xpath).text

            if (verify(last_rating_xpath)):
                wait.until(EC.presence_of_element_located((By.XPATH, last_rating_xpath)))

                try:
                    current_rating = int(driver.find_element(By.XPATH, last_rating_xpath).text)
                except:
                    current_rating = 0

            if (verify(sire_retired_xpath)):
                wait.until(EC.presence_of_element_located((By.XPATH, sire_retired_xpath)))
                sire = driver.find_element(By.XPATH, sire_retired_xpath).text

            if (verify(dam_retired_xpath)):
                wait.until(EC.presence_of_element_located((By.XPATH, dam_retired_xpath)))
                dam = driver.find_element(By.XPATH, dam_retired_xpath).text

            if (verify(dam_sire_retired_xpath)):
                wait.until(EC.presence_of_element_located((By.XPATH, dam_sire_retired_xpath)))
                dam_sire = driver.find_element(By.XPATH, dam_sire_retired_xpath).text

        pd_new_row = [horse_name, horse_url, country_of_origin, age, color, sex, import_type, season_stakes, total_stakes, 
            no_123_starts, no_starts_in_10, stable_loc, trainer, owner, current_rating, sos_rating, sire, dam, dam_sire, retired]
        
        writer_horse.writerow(pd_new_row)
        
        print(pd_new_row)

if __name__ == "__main__":
    lines = []
    with open('races.txt') as f:
        lines = f.readlines()

    # name of csv file 
    filename_race = "race_data.csv"
    filename_horse = "horse_data.csv"
        
    # writing to csv file 
    with open(filename_race, 'w', newline="") as race_file:
        with open(filename_horse, 'w', newline="") as horse_file:
            fieldnames_race = ['Date', 'Loc.', 'Race No.', 'Type', 'Going',
            'Course', 'Purse', 'Place', 'No.', 'Horse', 'Jockey', 'Trainer', 
            'Act. Wt.', 'Decl. Horse Wt.', 'Draw', 'LBW', 'Running Pos.', 
            'Finish Time', 'Win Odds']
            fieldnames_horse = ['horse_name', 'horse_url', 'country_of_origin', 
            'age', 'color', 'sex', 'import_type', 'season_stakes', 'total_stakes', 
            'no_123_starts', 'no_starts_in_10', 'stable_loc', 'trainer', 'owner', 
            'current_rating', 'sos_rating', 'sire', 'dam', 'dam_sire', 'retired'] # TODO: header for horse data
            
            writer_race = csv.writer(race_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer_horse = csv.writer(horse_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer_race.writerow(fieldnames_race)
            writer_horse.writerow(fieldnames_horse)

            for line in lines[66:88]:
                tokens = line.split("\t")
                date = tokens[0].strip()
                loc = tokens[1].strip()

                race_scrape(date, loc, writer_race, writer_horse)

