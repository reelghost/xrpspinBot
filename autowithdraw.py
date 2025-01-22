import cloudscraper
import csv
from time import sleep
from fake_useragent import UserAgent

# Function to handle login and withdrawal for a single account
def process_account(username):
    ua = UserAgent()
    login_payload = {
        "username": username,
        "password": "Matako"
    }
    auto_payload = {
        "password": "Matako",
    }
    # Create a cloudscraper instance
    scraper = cloudscraper.create_scraper()
    scraper.headers.update({'User-Agent': ua.random})

    try:
        login_response = scraper.post("https://xrpspin.com/api.php?act=login", json=login_payload)
        if login_response.status_code == 200:
            print(f"Login successful for {username}")
            withdraw_response = scraper.post("https://xrpspin.com/api.php?act=activeAutoWithdraw", json=auto_payload)
            print(f"{username}: {withdraw_response.json().get('parameters', 'None')}")
        else:
            print(f"Login failed for {username}: {login_response.text}")
    except Exception as e:
        print(f"Error processing account {username}: {e}")

# Read accounts.csv and process each account
def main():
    process_account("josehall86@yahoo.com")

if __name__ == "__main__":
    main()
