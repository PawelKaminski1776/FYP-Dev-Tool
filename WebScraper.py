import requests
from bs4 import BeautifulSoup
import sys
import os


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python WebScraper.py <Num-Of-Images> <County>")
        sys.exit(1)

    num_of_images = int(sys.argv[1])
    county = sys.argv[2]

    headers = {'User-Agent': 'PostmanRuntime/7.29.0'}

    if not os.path.exists("property_images"):
        os.makedirs("property_images")

    def scrape_page(page_num):
        url = f"https://www.daft.ie/property-for-sale/{county}/houses?from={page_num}&pageSize=20"
        page_to_scrape = requests.get(url, headers=headers)

        if page_to_scrape.status_code != 200:
            print(f"Failed to retrieve page {page_num}. Status code: {page_to_scrape.status_code}")
            return

        soup = BeautifulSoup(page_to_scrape.text, "html.parser")
        listings = soup.findAll("img", draggable="false")

        for idx, listing in enumerate(listings):

            if idx >= num_of_images:
                break
            image_url = listing["src"]
            image_name = f"property_{page_num}_{idx}.jpg"
            download_image(image_url, image_name)

    def download_image(image_url, image_name):
        try:
            img_data = requests.get(image_url, headers=headers).content
            with open(f"property_images/{image_name}", 'wb') as handler:
                handler.write(img_data)
            print(f"Downloaded {image_name}")
        except Exception as e:
            print(f"Error downloading {image_name}: {e}")

    images_downloaded = 0
    page_num = 0
    while images_downloaded < num_of_images:
        scrape_page(page_num)
        images_downloaded += 20
        page_num += 20




