import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re
import json

driver = webdriver.Chrome()
# URL of the problems list

def get_xpath(element):
    """
    Generate XPath for a given WebElement in Selenium WebDriver.
    """
    n = len(element.find_elements(By.XPATH, "./ancestor::*"))
    path = ""
    current = element

    for i in range(n, 0, -1):
        tag = current.tag_name
        lvl = len(current.find_elements(By.XPATH, f"./preceding-sibling::{tag}")) + 1
        path = f"/{tag}[{lvl}]{path}"
        current = current.find_element(By.XPATH, "./parent::*")

    return "/" + current.tag_name + path


url = "https://www.techiedelight.com/data-structures-and-algorithms-problems/"

# Function to fetch the webpage content
def fetch_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Failed to retrieve page: {e}")
        return None

# Function to extract links from the main problems page
def extract_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    ol_element = soup.select_one('ol')
    links = []
    
    if ol_element:
        for li in ol_element.find_all('li'):
            a_tag = li.find('a')
            if a_tag and 'href' in a_tag.attrs:
                links.append(a_tag['href'])
    else:
        print("Failed to find <ol> element")
    
    return links

# Function to extract problem details from a problem page
def extract_problem_details(problem_url):
    # define usin selenium
    problem_solution={}
    page_content = fetch_page(problem_url)
    if not page_content:
        return None
    
    soup = BeautifulSoup(page_content, 'html.parser')
    
    # Extract problem title
    problem_title = soup.select_one('article > div > div:nth-of-type(2) > div:nth-of-type(3) > h1').text.strip()
    
    # Extract problem description
    problem_description = soup.select_one('article > div > div:nth-of-type(2) > div:nth-of-type(4) > div:nth-of-type(1) > p:nth-of-type(1)').text.strip()

    problem_solution["problem"]=problem_title
    problem_solution["problem_description"]=problem_description

    driver.get(problem_url)
    try:
        consent_button = driver.find_element(By.XPATH, '/html/body/div[2]/div/button')
        consent_button.click()
    except:
        print("Consent button not found or already clicked")
    buttons = driver.find_elements(By.CLASS_NAME, 'responsive-tabs__list__item')
    lan_counter={}
    for button in buttons:
        button.click()
        button_xpath = get_xpath(button)
        lan=button.text
        if lan in problem_solution:
            if lan in lan_counter:
                lan_counter[lan] += 1
            else:
                lan_counter[lan] = 2  # Start with -2 suffix if the first one exists
            lan = f"{lan}-{lan_counter[lan]}"
        index = button_xpath.find('/ul[1]/li[')
        prefix =  button_xpath[:index]
        suffix_match = re.search(r'/ul\[1\]/li\[(\d+)\]', button_xpath)
        if suffix_match:
            suffix = suffix_match.group(1)
        else:
            suffix = None
        reference_x=prefix+'/div['+str(suffix)+']'+'/div/div[2]/div/table/tbody/tr/td[2]/div/div[1]'
        # Find the next sibling div with class 'c-line' after the clicked button
        reference_div = button.find_element(By.XPATH, reference_x)
        
        # Find the parent element of the reference div
        parent_element = reference_div.find_element(By.XPATH, './..')

        # Find all sibling div elements
        sibling_divs = parent_element.find_elements(By.XPATH, './div')

        # Iterate over sibling divs, concatenate text of all spans, and print it
        for div in sibling_divs:
            span_texts = []
            spans = div.find_elements(By.TAG_NAME, 'span')
            for span in spans:
                span_texts.append(span.text)
            concatenated_text = " ".join(span_texts)
            code=concatenated_text.strip()
            if lan:
                if lan in problem_solution:
                    problem_solution[lan]+=code
                else:
                    problem_solution[lan]=code
            else:
                continue
    return problem_solution

# Fetch and parse the main problems page
main_page_content = fetch_page(url)
if main_page_content:
    problem_links = extract_links(main_page_content)
    for link in problem_links:
        problem_details = extract_problem_details(link)
        if problem_details:
            with open('output.json', 'a') as f:
                json.dump(problem_details, f)  # Write dictionary as JSON
                f.write(',')
    
driver.quit()