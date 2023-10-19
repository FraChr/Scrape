import urllib.parse, urllib.error, urllib.request
from bs4 import BeautifulSoup
import ssl
import os

def url_input():
    url = input("Enter url - ")
    return url

def normalize_url(url):
    parsed_url = urllib.parse.urlparse(url)

    if parsed_url.scheme == 'http':
        parsed_url = parsed_url._replace(scheme='https')

    if not parsed_url.scheme:
        # Add 'https://' if scheme is missing
        url = 'https://' + url
        parsed_url = urllib.parse.urlparse(url)

    if not parsed_url.netloc.startswith('www.'):
        # Add 'www.' if not present in the netloc
        netloc = 'www.' + parsed_url.netloc
        parsed_url = parsed_url._replace(netloc=netloc)

    normalized_url = urllib.parse.urlunparse(parsed_url)
    return normalized_url

def img_scrape(soup):
    images = soup.find_all('img')
    image_urls = [item['src'] for item in images]
    return image_urls

def open_url(url):
    try:
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        ctx = ssl.create_default_context()
        reg = urllib.request.Request(url, headers=header)
        response = urllib.request.urlopen(reg, context=ctx)
        if response.status == 200:
            content_type = response.headers.get('Content-Type', '').lower()
            if content_type.startswith('image/'):
                image_data = response.read()
                return image_data
            else:
                html_data = response.read().decode()
                return html_data
    except urllib.error.URLError as e:
        print(f"Error: {e}")
    finally:
        response.close()

def prettify_html(html_code):
    soup = BeautifulSoup(html_code, 'html.parser')
    return soup.prettify()

def write_img(img_url, folder):
    try:
        image_data = open_url(img_url)
        if image_data:
            # Extract filename from url
            filename = os.path.basename(urllib.parse.urlparse(img_url).path)
            image_path = os.path.join(folder, filename)
            with open(image_path, 'wb') as image_file:
                image_file.write(image_data)
            print(f"Image {filename} saved as {image_path}")
            return image_path
    except Exception as e:
        print(f"Error saving image {img_url}: {e}")
    


def main():
    user = url_input()
    fixed_url = normalize_url(user)
    data = open_url(fixed_url)
    soup = BeautifulSoup(data, 'html.parser')
    image_urls = img_scrape(soup)

    folder = 'downloaded_images'

    if not os.path.exists(folder):
        os.makedirs(folder)

    for url in image_urls:
        if url:
            write_img(url, folder)
    
    print("Downloaded images saved in the output folder.")

    for url in image_urls:
        print(url)
    #pretty = prettify_html(data)
    #print(pretty)


if __name__=="__main__":
    main()