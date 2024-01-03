import time
from diskcache import Cache
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.edge.options import Options
import pandas as pd

__SITE__URL = "https://www.airbnb.ca/s/Canada/homes?refinement_paths%5B%5D=%2Fhomes&flexible_trip_dates%5B%5D=april&flexible_trip_dates%5B%5D=august&flexible_trip_dates%5B%5D=december&flexible_trip_dates%5B%5D=february&flexible_trip_dates%5B%5D=january&flexible_trip_dates%5B%5D=july&flexible_trip_dates%5B%5D=june&flexible_trip_dates%5B%5D=march&flexible_trip_dates%5B%5D=may&flexible_trip_dates%5B%5D=november&flexible_trip_dates%5B%5D=october&flexible_trip_dates%5B%5D=september&flexible_trip_lengths%5B%5D=one_week&date_picker_type=flexible_dates&search_type=user_map_move&tab_id=home_tab&monthly_start_date=2023-10-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&source=structured_search_input_header&query=Canada&place_id=ChIJ2WrMN9MDDUsRpY9Doiq3aJk&category_tag=Tag%3A8173&search_mode=flex_destinations_search&location_search=MIN_MAP_BOUNDS&ne_lat=52.517666736180665&ne_lng=-67.12568672213581&sw_lat=44.88622206926421&sw_lng=-76.76888895377391&zoom=6.074441058706102&zoom_level=6.074441058706102&search_by_map=true"
__LISTING__CLASS = "cy5jw6o"


def extract_listings_links(driver, site_url, cache, target=__LISTING__CLASS, waiting_time=[5, 1]):
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
    divs = driver.find_elements(By.CSS_SELECTOR, 'div.' + target)
    listings = [div.find_element(By.TAG_NAME, 'a') for div in divs]
    listings_urls = [link.get_attribute('href') for link in listings]

    cache[site_url] = listings_urls
    # Returning the extract
    return listings_urls


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


def scrape_listing(driver, site_url, num_months=3):
    driver.get(site_url)
    wait = WebDriverWait(driver, 10)  # 10 seconds wait time
    time.sleep(5)

    title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.hpipapi'))).text

    review_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div._16e70jgn')))

    try:
        location = review_div.find_element(By.CSS_SELECTOR, 'h1.hpipapi').text
    except NoSuchElementException:
        location = "Not Found"

    try:
        avg_rating = driver.find_element(By.CSS_SELECTOR, 'span._12si43g').get_attribute('innerHTML')
    except NoSuchElementException:
        avg_rating = "Not Found"

    try:
        num_rating = driver.find_element(By.CSS_SELECTOR, 'span._bq6krt').get_attribute(
            'innerHTML')
    except NoSuchElementException:
        num_rating = "Not Found"

    try:
        accomodation_list = review_div.find_element(By.CSS_SELECTOR, 'ol.lgx66tx')
        accomodation_elements = accomodation_list.find_elements(By.CSS_SELECTOR, 'li')
        accomodation = [e.text for e in accomodation_elements]
    except NoSuchElementException:
        accomodation = "Not Found"

    try:
        host_name = review_div.find_element(By.CSS_SELECTOR, 'div.t1pxe1a4').get_attribute('innerText')
    except NoSuchElementException:
        host_name = "Not Found"





    counter = 0
    free = 0
    av_30 = 42
    av_60 = 420
    for _ in range(num_months):
        try:
            next_button = driver.find_element(By.CSS_SELECTOR,
                                          'button[aria-label="Move forward to switch to the next month."]')
            table = driver.find_element(By.CSS_SELECTOR, 'table._cvkwaj')
        except Exception:
            break  # Break the loop if elements are not found

        rows = table.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            columns = row.find_elements(By.TAG_NAME, 'td')
            for col in columns:
                label = col.get_attribute('aria-label')
                if label and "Unavailable" not in label:
                    free += 1
                counter += 1
                if counter == 30:
                    av_30 = free
                if counter == 60:
                    av_60 = free
                    break

        driver.execute_script("arguments[0].click();", next_button)
        print("Click!")
        wait.until(EC.staleness_of(table))  # Wait for the table to refresh

    try:
        price = driver.find_element(By.CSS_SELECTOR, 'span._tyxjp1').get_attribute('innerText')
    except NoSuchElementException:
        try:
            price = {
                'original_price': driver.find_element(By.CSS_SELECTOR,
                                                      'span._1ks8cgb').get_attribute('innerText'),
                'discounted_price': driver.find_element(By.CSS_SELECTOR,
                                                        'span._1y74zjx').get_attribute('innerText')
            }
        except NoSuchElementException:
            price = "Price not found"
    try:
        amenities_div = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div.b9672i7')))
        amenities_button = amenities_div.find_element(By.TAG_NAME, 'button')
        driver.execute_script("arguments[0].click();", amenities_button)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.twad414')))
        amenities_divs = driver.find_elements(By.CSS_SELECTOR, 'div.twad414')
        amenities = [div.text for div in amenities_divs]
    except NoSuchElementException:
        amenities = "Amenities Not Found"

    data_entry = {'title': title, 'location': location, 'avg_rating': avg_rating,
                  'num_rating': num_rating, 'accomodation': accomodation, 'host': host_name,
                  'price': price, 'amenities': amenities, 'av_30': av_30, 'av_60': av_60}

    print(data_entry)
    return data_entry


def main(n_listings = 5):
    data = []
    cache = Cache('./page_cache')
    # Setting up the options for the Edge browser.
    options = Options()
    #options.add_argument('--headless')  # Run the browser in headless mode (no GUI).
    options.add_argument(
        '--no-sandbox')  # Bypass OS-level security, sometimes necessary for running headless browsers.

    # Start a new Edge browser session.
    print("Starting new browser session...")
    driver = webdriver.Edge(options=options)

    links = extract_listings_links(driver, __SITE__URL, cache)
    print(len(links))
    for i in range(n_listings):
        data.append(scrape_listing(driver, links[i]))
    # Closing the browser session.
    driver.quit()

    df = pd.DataFrame(data)
    df.to_csv('./data/airbnb_scrape_1.csv', index=False)


if __name__ == "__main__":
    main(18)
