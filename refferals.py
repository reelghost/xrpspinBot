import cloudscraper
from faker import Faker
import random
import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

class SequentialProxyRegistrar:
    def __init__(self):
        self.fake = Faker()
        self.proxy_sources = [
            "https://www.sslproxies.org/",
            "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies",
            "https://raw.githubusercontent.com/fyvri/fresh-proxy-list/main/http.txt"
        ]
        self.stats = {
            'tested': 0,
            'valid': 0,
            'success': 0,
            'failed': 0
        }

    def fetch_proxies(self):
        proxies = set()
        for url in self.proxy_sources:
            try:
                response = requests.get(url, timeout=15)
                if "sslproxies" in url:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    table = soup.find('table', {'class': 'table table-striped table-bordered'})
                    for row in table.tbody.find_all('tr'):
                        cols = row.find_all('td')
                        if cols[6].text == 'yes':
                            proxies.add(f"{cols[0].text}:{cols[1].text}")
                else:
                    proxies.update([line.strip() for line in response.text.split('\n') if ':' in line])
            except Exception as e:
                print(f"Proxy source error ({url}): {str(e)}")
        return list(proxies)

    def _test_proxy(self, proxy):
        try:
            with cloudscraper.create_scraper() as scraper:
                response = scraper.get(
                    'https://httpbin.org/ip',
                    proxies={'http': f'http://{proxy}', 'https': f'http://{proxy}'},
                    timeout=20
                )
                return proxy if response.status_code == 200 else None
        except:
            return None

    def _register_with_proxy(self, proxy):
        try:
            identity = {
                'username': self.fake.user_name() + str(random.randint(100, 999)),
                'fullname': self.fake.name(),
                'email': f"{self.fake.user_name()}{random.randint(0,99)}@{random.choice(['gmail.com', 'yahoo.com'])}",
                'phone': f"2541{random.randint(1000000, 9999999)}",
                'password': "Matako",
                'repassword': "Matako",
                'checkbox': 'on'
            }

            with cloudscraper.create_scraper() as scraper:
                scraper.proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
                scraper.headers.update({
                    'User-Agent': self.fake.user_agent(),
                    'Accept-Language': 'en-US,en;q=0.9'
                })

                # Get referral URL
                ref_response = scraper.get("https://e.vg/ZPHHMVxdn?", timeout=25)
                if ref_response.status_code != 200:
                    return False

                # Submit registration
                reg_response = scraper.post(
                    'https://xrpspin.com/api.php?act=register',
                    json=identity,
                    timeout=30
                )
                print(reg_response.text)
                return reg_response.status_code == 200
        except:
            return False

    def process_proxies(self):
        raw_proxies = self.fetch_proxies()
        print(f"Found {len(raw_proxies)} proxies, starting sequential processing...")

        with ThreadPoolExecutor(max_workers=20) as executor:
            # Test proxies in parallel
            test_futures = {executor.submit(self._test_proxy, proxy): proxy for proxy in raw_proxies}
            
            # Process results as they become available
            for future in as_completed(test_futures):
                proxy = test_futures[future]
                self.stats['tested'] += 1
                
                try:
                    valid_proxy = future.result()
                    if valid_proxy:
                        self.stats['valid'] += 1
                        print(f"Testing {valid_proxy} | Starting registration...")
                        
                        # Immediate registration in main thread
                        success = self._register_with_proxy(valid_proxy)
                        
                        if success:
                            self.stats['success'] += 1
                            print(f"✅ Success with {valid_proxy}")
                        else:
                            self.stats['failed'] += 1
                            print(f"❌ Failed with {valid_proxy}")
                except Exception as e:
                    print(f"Error processing {proxy}: {str(e)}")

        # Final report
        print("\n📊 Processing Complete")
        print(f"Tested: {self.stats['tested']}")
        print(f"Valid: {self.stats['valid']}")
        print(f"Success: {self.stats['success']}")
        print(f"Failed: {self.stats['failed']}")

if __name__ == '__main__':
    registrar = SequentialProxyRegistrar()
    registrar.process_proxies()