from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import ssl
import logging
import os

ssl._create_default_https_context = ssl._create_unverified_context

# Set up the WebDriver 
import undetected_chromedriver as uc  # for bot check prevention, this driver is used (pip install undetected_chromedriver)
driver = uc.Chrome()

# Configure logging
log_file = "automation.log"  # Specify the log file name
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=log_file,
                    filemode='w')  # 'w' to overwrite log file each run, 'a' to append

logger = logging.getLogger()

# Create a directory for screenshots
screenshot_dir = "screenshots"
os.makedirs(screenshot_dir, exist_ok=True)

def take_screenshot(step_name):
    screenshot_path = os.path.join(screenshot_dir, f"{step_name}.png")
    driver.save_screenshot(screenshot_path)
    logger.info(f"Screenshot saved: {screenshot_path}")

try: 
    # Maximize the browser window
    driver.maximize_window()
    
    # Navigate to the Expedia website
    driver.get("https://www.expedia.co.in/")
    logger.info(f"URL: {driver.current_url}")
    logger.info(f"Title: {driver.title}")
    take_screenshot("Expedia_Home")
    time.sleep(2)  # Wait for the page to load

    # Click on "Flights"
    flights_tab = driver.find_element(By.XPATH, "//a[.//span[text()='Flights']]")
    flights_tab.click()
    logger.info("'Flights' button clicked")
    take_screenshot("Flights_Tab")
    time.sleep(2)  # Wait for the flights tab to open

    # Click the button for the "Leaving from" input
    button = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[1]/div[2]/div[1]/div[4]/div/div[1]/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div/div[1]/div/div[1]/div/div/div[2]/div[1]/button")
    button.click()
    logger.info("Clicked 'leaving from' text box")
    take_screenshot("Leaving_From_Click")
    time.sleep(2)

    # Enter "Kolkata" into the departure input field
    input_field = driver.find_element(By.XPATH, "//input[@placeholder='Leaving from']")
    input_field.send_keys("Kolkata")
    input_field.send_keys(Keys.RETURN)
    logger.info("'Kolkata' typed in departure")
    take_screenshot("Kolkata_Departure")
    time.sleep(2)

    # Enter "Hyderabad" into the destination input field
    button = driver.find_element(By.XPATH, "//*[@id='FlightSearchForm_ROUND_TRIP']/div/div[1]/div/div[2]/div/div/div[2]/div[1]/button")
    button.click()
    time.sleep(2)
    input_field = driver.find_element(By.XPATH, "//input[@placeholder='Going to']")
    input_field.send_keys("Hyderabad")
    input_field.send_keys(Keys.RETURN)
    logger.info("'Hyderabad' typed in destination")
    take_screenshot("Hyderabad_Destination")
    time.sleep(2)

    # Click on the departure date picker(calendar)
    departure_date = driver.find_element(By.XPATH, "//button[@data-testid='uitk-date-selector-input1-default']")
    departure_date.click()
    logger.info("Clicked on 'Calendar'")
    take_screenshot("Calendar_Click")
    time.sleep(2)
    
    # Select the date "September 8"
    calendar_table = driver.find_element(By.XPATH, "//table[@aria-label='September 2024']")
    rows = calendar_table.find_elements(By.TAG_NAME, 'tr')

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        for cell in cells:
            date_elements = cell.find_elements(By.CLASS_NAME, 'uitk-date-number')
            if date_elements and date_elements[0].text == "8":
                cell.find_element(By.TAG_NAME, 'div').click()
                break
        else:
            continue
        break

    logger.info("Selected date 'September 8'")
    take_screenshot("Date_Selected")
    time.sleep(2)

    # Click on the "Done" button
    done_button = driver.find_element(By.XPATH, "//footer//button[@data-stid='apply-date-selector']")
    done_button.click()
    logger.info("Clicked on 'Done' button")
    take_screenshot("Done_Click")
    time.sleep(2)

    # Click on the "Travellers" button
    traveler_selector_button = driver.find_element(By.XPATH, '//*[@id="FlightSearchForm_ROUND_TRIP"]/div/div[3]/div/div[1]/button')
    traveler_selector_button.click()
    logger.info("Clicked on 'Travellers' button")
    take_screenshot("Travellers_Click")
    time.sleep(2)

    # Click the "+" button until the value reaches 2
    increase_button = driver.find_element(By.XPATH, "//button[@class='uitk-layout-flex-item uitk-step-input-touch-target'][2]")
    for _ in range(1):
        increase_button.click()
        time.sleep(1)  # Wait for the value to update
    logger.info("Selected 2 Adults")
    take_screenshot("2_Adults_Selected")

    # Click on the "Done" button in the traveler section
    travellers_done_button = driver.find_element(By.XPATH, "//div[@class='uitk-layout-flex uitk-layout-flex-justify-content-flex-end uitk-spacing uitk-spacing-padding-blockstart-four uitk-spacing-padding-blockend-three']/button[@id='travelers_selector_done_button']")
    travellers_done_button.click()
    logger.info("'Travellers Done' button clicked")
    take_screenshot("Travellers_Done_Click")
    time.sleep(2)

    # Click on the SEARCH Button
    search_button = driver.find_element(By.XPATH, '//*[@id="search_button"]')
    search_button.click()
    logger.info("'Search' button clicked")
    take_screenshot("Search_Click")
    time.sleep(2)

    # Click on the first flight available
    first_flight = driver.find_element(By.XPATH, "(//li[@data-test-id='offer-listing'])[1]")
    first_flight.click()
    logger.info("Clicked on the first flight available")
    take_screenshot("First_Flight_Click")
    time.sleep(5)

except Exception as e:
    logger.error(f"An error occurred: {e}")

finally:
    driver.quit()
    logger.info("Browser closed")
