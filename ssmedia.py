# Author:   Christian Wiegman | equationunequal
# Website:  http://www.newskin.nl
# Purpose:  Download all media files from a Squarespace website using the sitemap.xml
# License:  http://unlicense.org

# Imports
import requests
import os
import xml.etree.ElementTree as ET

# Function to download media files
def download_media(url, headers):
    media_file_name = url.split('/')[-1]  # Extracting filename from URL
    media_file_path = os.path.join("media", media_file_name)
    media_file = requests.get(url, headers=headers)
    if media_file.status_code == 200:
        with open(media_file_path, 'wb') as f:
            f.write(media_file.content)
        print(f"Downloaded: {media_file_name}")
    else:
        print(f"Failed to download: {media_file_name}")

# Function to parse sitemap.xml and extract URLs recursively
def parse_sitemap_recursive(node, urls):
    try:
        if 'url' in node.tag:  # Check if current node is a URL node
            image_elements = node.findall('.//image:loc', namespaces={'image': 'http://www.google.com/schemas/sitemap-image/1.1'})
            for image_element in image_elements:
                url = image_element.text
                urls.append(url)
    except AttributeError:
        pass
    for child in node:
        parse_sitemap_recursive(child, urls)

# Function to parse sitemap.xml and extract URLs
def parse_sitemap(sitemap_url):
    response = requests.get(sitemap_url, headers=headers)
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        urls = []
        parse_sitemap_recursive(root, urls)
        return urls
    else:
        print("Failed to fetch sitemap.xml")
        return []

# Set the URL of the Squarespace site
site_url = input("Enter the URL of the Squarespace site: ")

# Create media directory if it does not exist
if not os.path.exists('media'):
   os.makedirs('media')

# Add http:// if needed
if site_url.startswith("http://") == False and site_url.startswith("https://") == False:
    site_url = "http://" + site_url

if site_url.endswith("/") == False:
    site_url = site_url + "/"

sitemap_url = site_url + "sitemap.xml"

# Spoof headers, required for some sites
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

print(f"Scanning site: {site_url}")

# Parse sitemap and filter media URLs
urls = parse_sitemap(sitemap_url)
media_urls = [url for url in urls if any(ext in url for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.mp4', '.mov', '.avi'])]

# Download media files
for url in media_urls:
    download_media(url, headers)

# Version History
# 2024-03-23: 1.0