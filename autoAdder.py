from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
from dotenv import load_dotenv

load_dotenv()


places_list = [
    "bảo tàng chứng tích chiến tranh saigon",
    "chợ bến thành saigon",
    "nhà thờ đức bà saigon",
    "địa đạo củ chi saigon",
    "tòa nhà bitexco saigon",
    "nhà hát lớn saigon",
    "chùa ngọc hoàng saigon",
    "dinh độc lập saigon",
    "bảo tàng thành phố hồ chí minh saigon",
    "nhà thờ tân định saigon",
    "phố đi bộ nguyễn huệ saigon",
    "bến bạch đằng saigon",
    "công viên nước đầm sen saigon",
    "khu du lịch suối tiên saigon",
    "bảo tàng lịch sử việt nam saigon",
    "thảo cầm viên saigon",
    "tour đồng bằng sông cửu long saigon",
    "căn hộ cà phê saigon",
    "chùa bà thiên hậu saigon",
    "chợ lớn (khu phố tàu) saigon"


]

user_data_dir = r"/Users/danvu/Library/Application Support/Google/Chrome/Default"
profile_directory = "Default"

def handle_login(driver, username, password):
    """Handles login process if required."""
    try:
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='email' or @type='text']"))
        )
        username_field.send_keys(username)
        print("Entered username.")

        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' or @type='button']"))
        )
        next_button.click()
        print("Clicked next after username.")

        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
        )
        password_field.send_keys(password)
        print("Entered password.")

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' or @type='button']"))
        )
        login_button.click()
        print("Logged in successfully.")

    except Exception as e:
        print(f"Error during login: {str(e)}")
        input("Please complete the login process manually and press Enter to continue...")

def generate_google_maps_link(place):
    """Generate a Google Maps link for a search term."""
    base_url = "https://www.google.com/maps/search/?api=1&query="
    return f"{base_url}{place.replace(' ', '+')}"

def save_places_as_links(places_list):
    locations = []
    for place in places_list:
        link = generate_google_maps_link(place)
        locations.append(link)
    return locations
    

def main():
    # Load environment variables for credentials
    username = os.getenv("MAPS_USERNAME")
    password = os.getenv("MAPS_PASSWORD")

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"profile-directory={profile_directory}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    locations = save_places_as_links(places_list)
    try:
        print("Opening Google Maps...")
        driver.get("https://www.google.com/maps")
        time.sleep(5)

        try:
            sign_in_element = driver.find_element(By.XPATH, '//*[@aria-label="Sign in"]')
            print("Sign in element exists. Proceeding with login.")
            sign_in_element.click()
            handle_login(driver, username, password)
        except Exception as e:
            print("Sign in element does not exist. Skipping login attempt.")

        for i, location in enumerate(locations, 1):
            try:
                print(f"Processing location {i}/{len(locations)}")
                driver.get(location)

                if "captcha" in driver.page_source.lower():
                    print("Captcha detected! Please resolve it manually.")
                    input("Press Enter once you have resolved the captcha...")

                save_button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Save']"))
                )
                save_button.click()

                travel_plans_button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'MMWRwe') and contains(@class, 'fxNQSd') and @data-index='2']"))
                )
                travel_plans_button.click()

                print(f"Successfully saved location {i} to Travel Plans.")
                time.sleep(3)

            except Exception as e:
                print(f"Error processing location {i}: {str(e)}")
                user_input = input("Do you want to retry this location? (yes/no): ").strip().lower()
                if user_input == "yes":
                    driver.get(location)
                else:
                    print("Skipping to the next location...")
                    continue

        print("All locations have been processed.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    main()
