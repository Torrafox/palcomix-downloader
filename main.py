import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
from pathlib import Path

# Headers to bypass anti-bot restrictions
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

# Function to get the comic title from the landing page
def get_comic_title(soup):
    title_tag = soup.find("title")
    if title_tag:
        title = title_tag.text.strip()
        title = re.sub(r"[^\w\s]", "", title)  # Remove special characters but keep spaces
        return title  # Keep spaces instead of replacing them
    return "Unknown Comic"

# Function to extract comic page URLs from the landing page
def get_comic_pages(base_url, soup):
    page_links = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if "imagepages" in href:  # Only collect links to image pages
            full_url = urljoin(base_url, href)
            page_links.append(full_url)
    return sorted(set(page_links))  # Remove duplicates and sort them

# Function to extract the full-sized image URL from a comic page
def get_full_image_url(comic_page_url):
    response = requests.get(comic_page_url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to access {comic_page_url}")
        return None, None

    soup = BeautifulSoup(response.text, "html.parser")

    # Find the correct <img> tag
    img_tag = soup.find("img", {"src": re.compile(r"\.\./images/.*\.(jpg|png|gif)$", re.IGNORECASE)})
    
    if img_tag and "src" in img_tag.attrs:
        img_url = urljoin(comic_page_url, img_tag["src"])  # Convert relative path to absolute URL
        filename = os.path.basename(urlparse(img_url).path)

        # Only accept images that contain numbers in their filename
        if re.search(r"\d", filename):
            return img_url, comic_page_url  # Return both image URL and the page URL for the referer
    return None, None

# Function to download images with proper headers and decode filenames
def download_image(img_url, referer, save_path):
    encoded_filename = os.path.basename(urlparse(img_url).path)
    decoded_filename = unquote(encoded_filename)  # Decode %20 to spaces, etc.
    img_path = save_path / decoded_filename

    # Set headers to bypass restrictions
    headers = {
        "User-Agent": HEADERS["User-Agent"],
        "Referer": referer,  # Set referer to the comic page
    }

    response = requests.get(img_url, headers=headers, stream=True)
    if response.status_code == 200:
        with open(img_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Downloaded: {decoded_filename}")
    else:
        print(f"Failed to download: {img_url} (status code {response.status_code})")

# Main function
def download_comic_images(landing_url):
    response = requests.get(landing_url, headers=HEADERS)
    if response.status_code != 200:
        print("Failed to access the landing page. Please check the URL.")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    comic_title = get_comic_title(soup)

    # Define the save path (with spaces)
    save_path = Path.home() / "Downloads" / comic_title
    save_path.mkdir(parents=True, exist_ok=True)
    print(f"Saving images to: {save_path}")

    # Get all comic page links
    comic_pages = get_comic_pages(landing_url, soup)
    if not comic_pages:
        print("No comic pages found. The site structure may have changed.")
        return

    # Process each comic page
    for page_url in comic_pages:
        full_img_url, referer = get_full_image_url(page_url)
        if full_img_url:
            download_image(full_img_url, referer, save_path)

    print("Download complete!")

if __name__ == "__main__":
    comic_url = input("Enter the Palcomix comic URL: ").strip()
    download_comic_images(comic_url)
