import cloudscraper
from fake_useragent import UserAgent
from faker import Faker
import random
import os

# Create a UserAgent instance
ua = UserAgent()

# Create a Faker instance
fake = Faker()

# Generate random user details
username = fake.user_name()
fullname = fake.name()
domains = ["gmail.com", "yahoo.com", "yandex.com", "outlook.com"]
email = f"{username}{random.randint(0,99)}@{random.choice(domains)}"
phone = "25407" + ''.join([str(fake.random_int(0, 9)) for _ in range(6)])

# Referral URL
# ref_url = "https://e.vg/RNrYFmMjF?" #admin_real
ref_url = "https://e.vg/mSAqgyXKY?" #saumumueni

# Registration payload
register_payload = {
    "username": username,
    "fullname": fullname,
    "email": email,
    "phone": phone,
    "a": "a",
    "xrpAddr": "",
    "distTag": "",
    "password": "Matako",
    "repassword": "Matako",
    "checkbox": "on"
}

# Create a cloudscraper instance
scraper = cloudscraper.create_scraper()
scraper.headers.update({'User-Agent': ua.random})
ref_response = scraper.get(ref_url)

# Check if the referral GET request was successful
# clear the terminal
os.system("cls")
if ref_response.status_code == 200:
    print("Referral GET request successful")
    # Send the POST request to the registration URL using the same scraper session
    register_response = scraper.post("https://xrpspin.com/api.php?act=register", json=register_payload)
    # Print the response
    print(register_response.text)
else:
    print("Referral GET request failed")
    print(ref_response.text)
