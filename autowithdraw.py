import cloudscraper
from bs4 import BeautifulSoup
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
            # get how many refferals available
            referrals_response = scraper.get("https://xrpspin.com/referrals.php")
            ref_page = BeautifulSoup(referrals_response.text, 'html.parser')
            ref_link = ref_page.find("input", {"id": "myurl"}).get("value").split(" ")[0]
            ref_count = ref_page.find('div', class_='project').find("h3").text.split(':')[-1].strip()
            # if ref_count 0 is a multiple of 10
            if int(ref_count) % 10 == 0 and int(ref_count) != 0:
                print(f"{username}: {ref_count} referrals")
                # withdraw
                withdraw_response = scraper.post("https://xrpspin.com/api.php?act=activeAutoWithdraw", data=auto_payload)
                print(f"{username}: {withdraw_response.json().get('parameters', 'None')}")
            else:
                print(f"{ref_link}: {ref_count} referrals")
        else:
            print(f"Login failed for {username}: {login_response.text}")
    except Exception as e:
        print(f"Error processing account {username}: {e}")



if __name__ == "__main__":
    process_account("saumumueni")
