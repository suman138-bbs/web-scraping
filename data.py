import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def extract_data(div):
    company_name_div = div.find('div', class_='qBF1Pd fontHeadlineSmall') 
    company_name = company_name_div.text.strip() if company_name_div else "N/A"

    phone_number_span = div.find('span', class_='UsdlK') 
    phone_number = phone_number_span.text.strip() if phone_number_span else "N/A"

    website_anchor = div.find('a', class_='lcr4fd S9kvJb')  
    website = website_anchor['href'] if website_anchor else "N/A"

    ratings_span = div.find('span', class_='MW4etd')  
    ratings = ratings_span.text.strip() if ratings_span else "N/A"

    reviews_span = div.find('span', class_='UY7F9')  
    reviews = reviews_span.text.strip('()') if reviews_span else "N/A"

    address_span = div.find_all('span')[-1]  
    address = address_span.text.strip() if address_span else "N/A"

    maps_url = div.find('a', class_='hfpxzc')['href'] 
    latitude = maps_url.split('!3d')[1].split('!4d')[0] if maps_url else "N/A"
    longitude = maps_url.split('!4d')[1].split('!')[0] if maps_url else "N/A"

   
    plus_code, place_id, cid = "N/A", "N/A", "N/A"  

    
    additional_info_div = div.find('div', class_='W4Efsd')
    if additional_info_div:
        spans = additional_info_div.find_all('span', class_='e4rVHe fontBodyMedium')
        if len(spans) >= 3:
            plus_code, place_id, cid = [span.text.strip() for span in spans]

    return {
        "Company Name": company_name,
        "Phone Number": phone_number,
        "Website": website,
        "Ratings": ratings,
        "Reviews": reviews,
        "Latitude": latitude,
        "Longitude": longitude,
        "Address": address,
        "Google Maps URL": maps_url,
        "Plus Code": plus_code,
        "Place ID": place_id,
        "CID": cid
    }

driver = webdriver.Chrome()
url = "https://www.google.com/maps/search/pharmaceutical+industry+near+langar+house+hyderabad/@17.3913497,78.3847559,13z/data=!3m1!4b1?entry=ttu"
driver.get(url)
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "Nv2PK.tH5CWc.THOPZb")))
html = driver.page_source
driver.quit()

soup = BeautifulSoup(html, 'html.parser')

business_divs = soup.find_all('div', class_='Nv2PK tH5CWc THOPZb')


data = [extract_data(div) for div in business_divs]


df = pd.DataFrame(data)


df.to_excel("pharmaceutical_data2.xlsx", index=False)
