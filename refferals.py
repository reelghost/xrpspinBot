import cloudscraper
from faker import Faker
import random
import os
import argparse

# Create a Faker instance
fake = Faker()

# Generate random user details
username = fake.user_name()
fullname = fake.name()
domains = ["gmail.com", "yahoo.com", "yandex.com", "outlook.com"]
email = f"{username}{random.randint(0,99)}@{random.choice(domains)}"
phone = "25407" + ''.join([str(fake.random_int(0, 9)) for _ in range(6)])

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Process referral URL.')
parser.add_argument('-r', '--refurl', type=str, required=True, help='Referral URL')
args = parser.parse_args()

# Registration payload
register_payload = {
    "username": username,
    "fullname": fullname,
    "email": email,
    "phone": phone,
    "a": "b",
    "xrpAddr": "",
    "distTag": "",
    "password": "Matako",
    "repassword": "Matako",
    "checkbox": "on"
}

# Create a cloudscraper instance with proxy
scraper = cloudscraper.create_scraper()

# Send the GET request to the referral URL
ref_response = scraper.get(args.refurl)
if ref_response.status_code == 200:
    print("Referral GET request successful")
    # Send the POST request to the registration URL using the same scraper session
    register_response = scraper.post("https://xrpspin.com/api.php?act=register", json=register_payload)
    # Print the response
    print(register_response.text)
else:
    print("Referral GET request failed")
    print(ref_response.text)

# running examlple
# python refferals.py -r https://e.vg/RNrYFmMjF?
