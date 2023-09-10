import time
from diskcache import Cache
from html2text import HTML2Text
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
__SITE__URL = "https://www.airbnb.ca/s/Canada/homes?refinement_paths%5B%5D=%2Fhomes&flexible_trip_dates%5B%5D=april&flexible_trip_dates%5B%5D=august&flexible_trip_dates%5B%5D=december&flexible_trip_dates%5B%5D=february&flexible_trip_dates%5B%5D=january&flexible_trip_dates%5B%5D=july&flexible_trip_dates%5B%5D=june&flexible_trip_dates%5B%5D=march&flexible_trip_dates%5B%5D=may&flexible_trip_dates%5B%5D=november&flexible_trip_dates%5B%5D=october&flexible_trip_dates%5B%5D=september&flexible_trip_lengths%5B%5D=one_week&date_picker_type=flexible_dates&search_type=user_map_move&tab_id=home_tab&monthly_start_date=2023-10-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&source=structured_search_input_header&query=Canada&place_id=ChIJ2WrMN9MDDUsRpY9Doiq3aJk&category_tag=Tag%3A8173&search_mode=flex_destinations_search&location_search=MIN_MAP_BOUNDS&ne_lat=52.517666736180665&ne_lng=-67.12568672213581&sw_lat=44.88622206926421&sw_lng=-76.76888895377391&zoom=6.074441058706102&zoom_level=6.074441058706102&search_by_map=true"
__LISTING__CLASS = "cy5jw6o"



def extract_html_js(driver, site_url, cache, waiting_time=[5, 1]):
    """
    Extracts all divs of a particular class from a JS page using Selenium.
    """
    # Check if the URL is already in the cache
    if site_url in cache:
        print("Cache hit!")
        return cache[site_url]
    print("Cache miss!")
    # Navigating to the desired URL.
    driver.get(site_url)

    # Waiting for the page to load (or for certain scripts to run).
    time.sleep(waiting_time[0])
    print("Page loaded!")
    # Using Selenium to directly find all divs with the specified class.
    raw_html = driver.page_source
    cache[site_url] = raw_html

    # Returning the extract
    return raw_html


def extract_links(html, target):
    soup = BeautifulSoup(html, features='html.parser')
    # Find all div elements with the class name 'example-class'
    listings = soup.find_all('div', class_=target)
    links = [listing.find('a')['href'] for listing in listings]
    return links


def scrape_data(driver, link):


def main():
    cache = Cache('./page_cache')

    # Setting up the options for the Edge browser.
    options = Options()
    options.add_argument('--headless')  # Run the browser in headless mode (no GUI).
    options.add_argument(
        '--no-sandbox')  # Bypass OS-level security, sometimes necessary for running headless browsers.

    # Start a new Edge browser session.
    print("Starting new browser session...")
    driver = webdriver.Edge(options=options)

    html = extract_html_js(driver, __SITE__URL, cache)

    links = extract_links(html, __LISTING__CLASS)


    for link in links:
        scrape_data(driver, link)
    # Closing the browser session.
    driver.quit()


if __name__ == "__main__":
    h2t = HTML2Text()
    h2t.ignore_images = True
    h2t.mark_code = True
    h2t.skip_internal_links = True
    h2t.unicode_snob = True
    main()