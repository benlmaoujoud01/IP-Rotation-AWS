import requests
from requests_ip_rotator import ApiGateway
import feedparser
from datetime import datetime
import time
from urllib.parse import urlparse

def fetch_rss_feeds(feed_urls, requests_per_url=100, max_retries=3, delay_between_requests=1):

    gateways = {}
    session = requests.Session()
    
    headers = {
            """You can add more user agent..."""
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    session.headers.update(headers)
    
    def get_domain(url):
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"
    
    def setup_gateway(url):
        domain = get_domain(url)
        if domain not in gateways:
            gateway = ApiGateway(
                domain,
            )
            gateway.start()
            gateways[domain] = gateway
            session.mount(domain, gateway)
    
    def fetch_single_feed(url, request_number):
        """Fetch a single feed with IP rotation"""
        setup_gateway(url) 
        
        for attempt in range(max_retries):
            try:
                print(f"\nRequest {request_number + 1}/100 for URL: {url}")
                

                if "ipify.org" in url:
                    ip_response = session.get(url, timeout=10)
                    print(f"Current IP: {ip_response.text}")
                
                response = session.get(url, timeout=10)
                response.raise_for_status()
                
                feed = feedparser.parse(response.content)
                print(f"Status: {response.status_code}")
                print(f"Number of entries: {len(feed.entries)}")
                # change this to print your results
                for entry in feed.entries:
                    print(entry.somethign)
                
                return True
                
            except requests.RequestException as e:
                print(f"Attempt {attempt + 1} failed for {url} (Request {request_number + 1}): {str(e)}")
                if attempt == max_retries - 1:
                    print(f"Max retries reached for {url} (Request {request_number + 1})")
                time.sleep(delay_between_requests * (attempt + 1))
                
            except Exception as e:
                print(f"Error processing {url} (Request {request_number + 1}): {str(e)}")
                break
                
        return False

    try:
        for url in feed_urls:
            print(f"\n=== Starting {requests_per_url} requests for: {url} ===")
            successful_requests = 0
            failed_requests = 0
            
            for request_num in range(requests_per_url):
                success = fetch_single_feed(url, request_num)
                if success:
                    successful_requests += 1
                else:
                    failed_requests += 1
                
                time.sleep(delay_between_requests)
            
            print(f"\n=== Summary for {url} ===")
            print(f"Successful requests: {successful_requests}")
            print(f"Failed requests: {failed_requests}")
            print("=" * 50)
            
    finally:
        for gateway in gateways.values():
            try:
                gateway.shutdown()
            except:
                pass
        session.close()

feed_urls = [
  "past your urls"
]

if __name__ == "__main__":
    fetch_rss_feeds(feed_urls)
