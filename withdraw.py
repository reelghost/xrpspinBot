import cloudscraper
import csv
from time import sleep
from fake_useragent import UserAgent

# Function to handle login and withdrawal for a single account
def process_account(username, tag):
    ua = UserAgent()
    login_payload = {
        "username": username,
        "password": "Matako"
    }
    withdraw_payload = {
        "confirm": 0,
        "payout_value": 0.000025,
        "password": "matako",
        "xrpAddr": "rHcXrn8joXL2Qe7BaMnhB5VRuj1XKEmUW6",
        "distTag": tag
    }

    # Create a cloudscraper instance
    scraper = cloudscraper.create_scraper()
    scraper.headers.update({'User-Agent': ua.random})

    try:
        login_response = scraper.post("https://xrpspin.com/api.php?act=login", json=login_payload)
        if login_response.status_code == 200:
            print(f"Login successful for {username}")
            withdraw_response = scraper.post("https://xrpspin.com/api.php?act=withdrawXrp", json=withdraw_payload)
            response_message = withdraw_response.json().get('parameters', 'None')[1]
            print(f"{username}: {response_message}")
        else:
            response_message = "Login failed"
            print(f"Login failed for {username}: {login_response.text}")
    except Exception as e:
        print(f"Error processing account {username}: {e}")
    return response_message

# Read accounts.csv and process each account
def main():
    while True:
        try:
            with open("accounts.csv", "r") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    username = row.get("username")
                    tag = row.get("tag")

                    if username and tag:
                        process_account(username, tag)
                    else:
                        print(f"Invalid data in row: {row}")
                    sleep(1)  # Wait 5 seconds between processing accounts

        except FileNotFoundError:
            print("Error: accounts.csv not found.")
        except Exception as e:
            print(f"Error reading accounts.csv: {e}")

        # if resp_msg == 'Incorrect destination tag':
        #     sleep(1 + (1 * (1 if __import__('random').randint(0, 1) else 0)))
        # elif resp_msg == 'Login failed':
        #     sleep(1 + (1 * (1 if __import__('random').randint(0, 1) else 0)))
        # else:
        print("Waiting for 5-6 minutes before next loop...")
        sleep(300 + (60 * (1 if __import__('random').randint(0, 1) else 0)))  # Wait 5-6 minutes

if __name__ == "__main__":
    main()
