import urllib.error, urllib.parse, urllib.request
from bs4 import BeautifulSoup
import ssl
import os

class WebScraper:
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        self.ctx = ssl.create_default_context()

    def url_input(self):
        url = input("Enter URL > ")
        return url
    
    def normalize_url(self, url):
        parsed_url = urllib.parse.urlparse(url)
        
        if not parsed_url.scheme:
            # add https:// to url scheme if missing
            url = 'https://' + url
            parsed_url = urllib.parse.urlparse(url)

        if not parsed_url.netloc.startswith('www.'):
            # add 'www.' to netloc if missing
            server = 'www.' + parsed_url.netloc
            parsed_url = parsed_url._replace(netloc=server)

        propper_url = urllib.parse.urlunparse(parsed_url)
        return propper_url
    
    def open_url(self, url):
        try:
            reg = urllib.request.Request(url, headers=self.header)
            # response = urllib.request.urlopen(reg, context=self.ctx)
            with urllib.request.urlopen(reg, context=self.ctx) as response:
                if response.status == 200:
                    content_type = response.headers.get('Content-Type', '').lower()
                    if content_type.startswith('image/'):
                        image_data = response.read()
                        return image_data
                    else:
                        html_data = response.read().decode()
                        return html_data
        except urllib.error.URLError as e:
            print(f"Error {e}")
        except Exception as e:
            print(f"Error: {e}")
            
    def format_html(html_code):
        parsed_html = BeautifulSoup(html_code, 'html.parser')
        return parsed_html.prettify()
    
    def write_img(self, img_url, folder):
        try:
            image_data = self.open_url(img_url)
            if image_data:
                # Extract filename from URL
                filename = os.path.basename(urllib.parse.urlparse(img_url).path)
                image_path = os.path.join(folder, filename)
                with open(image_path, 'wb') as image_file:
                    image_file.write(image_data)
                print(f"Image {filename} saved as {image_path}")
                return image_path
        except Exception as e:
            print(f"Error saving image {img_url}: {e}")

    def download_images(self):
        user = self.url_input()
        fixed_url = self.normalize_url(user)
        data = self.open_url(fixed_url)
        soup = BeautifulSoup(data, 'html.parser')
        image_urls = self.image_scrape(soup)

        folder = input("Enter Folder Name > ")

        if not os.path.exists(folder):
            os.makedirs(folder)
        for url in image_urls:
            if url:
                self.write_img(url, folder)
        print("---------------------------------------------------------------------------------------\n")
        print(f"Downloaded images saved to {folder}.\n")
        print("---------------------------------------------------------------------------------------\n")

        for url in image_urls:
            print(url)

    @staticmethod
    def image_scrape(img):
        images = img.find_all('img')
        image_urls = [item['src'] for item in images]
        return image_urls
    

def main():
    scraper = WebScraper()
    scraper.download_images()

if __name__ == '__main__':
    main()