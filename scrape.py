from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
os.system("clear")
cwd = os.getcwd()

#Variables
url:str = "https://hprera.nic.in/PublicDashboard"
location_to_chrome_driver:str = f"{cwd}/chromedriver"
no_of_records_to_fetch:int = 6
wait_timeout:int = 20

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set the path to chromedriver
service = Service(location_to_chrome_driver)

# Initialize the driver
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(url)

try:
    print("Scraping please wait.\n")
    # Wait until the loading text is no longer present
    wait = WebDriverWait(driver,wait_timeout)
    wait.until_not(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "div#content-tab_project_main"), "Loading"))

    list_of_reg_projects = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div#tab_project_main-filtered-data .col-lg-6"))
    )
    count_of_active_projects = len(list_of_reg_projects)
    print(f"Total Projects: {count_of_active_projects}")
    print(f"Displaying Data for first {no_of_records_to_fetch} records only.")
    
    #print the demo for first record
    start_time = time.time()
    for i in range(0,no_of_records_to_fetch):
        print("\n-----------------------------------------------------")
        # print(count_of_active_projects[i].text)
        rerano = list_of_reg_projects[i].find_element(By.CSS_SELECTOR, "a[onclick^='tab_project_main_ApplicationPreview']")
        rerano = str(rerano.text)

        #Click on the rerano
        element = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, rerano)))
        element.click()

        #Wait for the data to load
        wait = WebDriverWait(driver,wait_timeout)
        wait.until_not(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "div#content-tab_project_main"), "Loading"))

        #fetch all table content
        builder_data = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#project-menu-html")))  
        # print(builder_data.text)

        name_element = builder_data.find_element(By.XPATH, ".//tr[td[text()='Name']]/td[2]")
        gstin_element = builder_data.find_element(By.XPATH, ".//tr[td[text()='GSTIN No.']]/td[2]")
        panno_element = builder_data.find_element(By.XPATH, ".//tr[td[text()='PAN No.']]/td[2]")
        address_element = builder_data.find_element(By.XPATH, ".//tr[td[text()='Permanent Address']]/td[2]")
        print(f"Record No. {i+1}")
        print(f"RERA No.: {rerano}")
        print(f"Name: {name_element.text}")
        print(f"GSTIN No.: {gstin_element.text.replace(' GST Certificate', '')}")
        print(f"PAN No.: {panno_element.text.replace(' PAN Card', '')}")
        print(f"Permanent Address: {address_element.text.replace(' Address Proof', '')}")

        #Simulate closing of Modal
        close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.close[data-dismiss='modal']")))
        close_button.click()
    time_taken = time.time()-start_time
    print("\n-----------------------------------------")    
    print("SCRAPING COMPLETED")
    print(f"Total time taken: {time_taken:.0f} s")

#Exit the driver
finally:
    driver.quit()
