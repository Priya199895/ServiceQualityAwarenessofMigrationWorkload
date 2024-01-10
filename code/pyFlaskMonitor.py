import requests
import time

def hit_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        print(f"Successfully hit {url} - Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error hitting {url}: {e}")

if __name__ == "__main__":
    url_to_hit = "http://localhost:5000/download"#"http://192.168.202.153:5000/download"#  # Replace with the URL you want to hit

    while True:
        print("hitting url")
        hit_url(url_to_hit)
        time.sleep(15)  # Sleep for 1 minute before the next request
