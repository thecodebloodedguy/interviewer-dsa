from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
import re
from selenium.webdriver.support import expected_conditions as EC
import json
import pickle

# Specify the path to your chromedriver executable
driver_path = 'E:\Desktop\chromedriver.exe'

# Load array from pickle file
filename = "output2.pkl"
with open(filename, "rb") as file:
    loaded_array = pickle.load(file)

# Create a ChromeService object with the driver path
service = ChromeService(executable_path=driver_path)

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 50)
wait2 = WebDriverWait(driver, 5)

def fetch_page(url):
    try:
        driver.get(url)
        return driver
    except Exception as e:
        print(f"Failed to retrieve page: {e}")
        return None

def extract_problem_details(driver, url):
    problem_details = {}

    driver.get(url)
    time.sleep(5)  # Adjust the sleep time as needed to ensure the page loads completely
    difficulty = driver.find_element(By.CLASS_NAME, 'difficulty-level').text

    if difficulty.lower() != 'easy':
        problem_details['difficulty'] = difficulty

        # Problem Statements
        problem_statement = driver.find_element(By.CSS_SELECTOR, '#mat-tab-content-0-0 > div > div.problem-details.pt-12.px-8.ng-star-inserted > div > ninjas-problems-ui-problem-details-tab > div > ninjas-problems-ui-problem-details-tab-description > div > div.problem-main-statement.ng-star-inserted > div').text
        problem_title = driver.find_element(By.CLASS_NAME, 'problem-title zen-typo-subtitle-small').text  # New code to extract problem title
        problem_details['problem_statement'] = problem_statement
        problem_details['problem_title'] = problem_title  # New code to add problem title to details

        problem_detail = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/codingninjas-root/codingninjas-publicsection-app/div[1]/div/div[2]/codingninjas-problems/mat-sidenav-container/mat-sidenav-content/codingninjas-problem-offerings-panel/div/codingninjas-problem-classroom-v2/div/div[1]/span/as-split/as-split-area[1]/ninjas-problems-ui-problem-left-panel/div/mat-tab-group/div/mat-tab-body[1]/div/div[2]/div/ninjas-problems-ui-problem-details-tab/div/ninjas-problems-ui-problem-details-tab-description/div/div[3]/div[1]/div[1]")))
        driver.execute_script("arguments[0].scrollIntoView(true); window.scrollBy(0, 20);", problem_detail)
        problem_detail.click()
        problem_detail_text = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/codingninjas-root/codingninjas-publicsection-app/div[1]/div/div[2]/codingninjas-problems/mat-sidenav-container/mat-sidenav-content/codingninjas-problem-offerings-panel/div/codingninjas-problem-classroom-v2/div/div[1]/span/as-split/as-split-area[1]/ninjas-problems-ui-problem-left-panel/div/mat-tab-group/div/mat-tab-body[1]/div/div[2]/div/ninjas-problems-ui-problem-details-tab/div/ninjas-problems-ui-problem-details-tab-description/div/div[3]")))
        problem_detail_text = problem_detail_text.text
        problem_details['problem_details'] = problem_detail_text
        input_output_text = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/codingninjas-root/codingninjas-publicsection-app/div[1]/div/div[2]/codingninjas-problems/mat-sidenav-container/mat-sidenav-content/codingninjas-problem-offerings-panel/div/codingninjas-problem-classroom-v2/div/div[1]/span/as-split/as-split-area[1]/ninjas-problems-ui-problem-left-panel/div/mat-tab-group/div/mat-tab-body[1]/div/div[2]/div/ninjas-problems-ui-problem-details-tab/div/ninjas-problems-ui-problem-details-tab-description/div/div[4]')))
        input_output_text = input_output_text.text
        try:
            input_output_text2 = wait2.until(EC.presence_of_element_located((By.XPATH, '/html/body/codingninjas-root/codingninjas-publicsection-app/div[1]/div/div[2]/codingninjas-problems/mat-sidenav-container/mat-sidenav-content/codingninjas-problem-offerings-panel/div/codingninjas-problem-classroom-v2/div/div[1]/span/as-split/as-split-area[1]/ninjas-problems-ui-problem-left-panel/div/mat-tab-group/div/mat-tab-body[1]/div/div[2]/div/ninjas-problems-ui-problem-details-tab/div/ninjas-problems-ui-problem-details-tab-description/div/div[5]')))
            input_output_text2 = input_output_text2.text
        except:
            input_output_text2 = ''
        try:
            input_output_text3 = wait2.until(EC.presence_of_element_located((By.XPATH, '/html/body/codingninjas-root/codingninjas-publicsection-app/div[1]/div/div[2]/codingninjas-problems/mat-sidenav-container/mat-sidenav-content/codingninjas-problem-offerings-panel/div/codingninjas-problem-classroom-v2/div/div[1]/span/as-split/as-split-area[1]/ninjas-problems-ui-problem-left-panel/div/mat-tab-group/div/mat-tab-body[1]/div/div[2]/div/ninjas-problems-ui-problem-details-tab/div/ninjas-problems-ui-problem-details-tab-description/div/div[6]')))
            input_output_text3 = input_output_text3.text
        except:
            input_output_text3 = ''
        problem_details['input_output'] = input_output_text + '\n' + input_output_text2 + '\n' + input_output_text3

        # Solutions
        solution_tab_button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/codingninjas-root/codingninjas-publicsection-app/div[1]/div/div[2]/codingninjas-problems/mat-sidenav-container/mat-sidenav-content/codingninjas-problem-offerings-panel/div/codingninjas-problem-classroom-v2/div/div[1]/span/as-split/as-split-area[1]/ninjas-problems-ui-problem-left-panel/div/mat-tab-group/mat-tab-header/div/div/div/div[3]/span[2]/span/div/div")))
        solution_tab_button.click()
        try:
            jints = driver.find_element(By.CLASS_NAME, 'hints-box-container')
            jint = 1
        except:
            jint = 0
        try:
            if jint:
                approach_button = driver.find_element(By.XPATH, '/html/body/codingninjas-root/codingninjas-publicsection-app/div[1]/div/div[2]/codingninjas-problems/mat-sidenav-container/mat-sidenav-content/codingninjas-problem-offerings-panel/div/codingninjas-problem-classroom-v2/div/div[1]/span/as-split/as-split-area[1]/ninjas-problems-ui-problem-left-panel/div/mat-tab-group/div/mat-tab-body[3]/div/div[2]/div/ninjas-problems-ui-solution-details-tab/div/div/ninjas-problems-ui-hints-and-solutions/div/div[2]/ninjas-problems-ui-approaches-box/div/div[2]/ninjas-problems-ui-solution-locked-content[1]/div/div[2]/button')
            else:
                approach_button = driver.find_element(By.XPATH, '/html/body/codingninjas-root/codingninjas-publicsection-app/div[1]/div/div[2]/codingninjas-problems/mat-sidenav-container/mat-sidenav-content/codingninjas-problem-offerings-panel/div/codingninjas-problem-classroom-v2/div/div[1]/span/as-split/as-split-area[1]/ninjas-problems-ui-problem-left-panel/div/mat-tab-group/div/mat-tab-body[3]/div/div[2]/div/ninjas-problems-ui-solution-details-tab/div/div[1]/ninjas-problems-ui-approaches-box/div/div[2]/ninjas-problems-ui-solution-locked-content[1]/div/div[2]/button')
            if approach_button:
                print('app')
                approach_button.click()
                time.sleep(1)
        except Exception as e:
            print('Approach already seen')

        edit = driver.find_element(By.CLASS_NAME, 'suggest-edit')
        driver.execute_script("arguments[0].scrollIntoView(true); window.scrollBy(0, 20);", edit)

        try:
            if jint:
                solution_button = driver.find_element(By.XPATH, '/html/body/codingninjas-root/codingninjas-publicsection-app/div[1]/div/div[2]/codingninjas-problems/mat-sidenav-container/mat-sidenav-content/codingninjas-problem-offerings-panel/div/codingninjas-problem-classroom-v2/div/div[1]/span/as-split/as-split-area[1]/ninjas-problems-ui-problem-left-panel/div/mat-tab-group/div/mat-tab-body[3]/div/div[2]/div/ninjas-problems-ui-solution-details-tab/div/div/ninjas-problems-ui-hints-and-solutions/div/div[2]/ninjas-problems-ui-approaches-box/div/div[2]/ninjas-problems-ui-solution-locked-content[2]/div/div[2]/button')
            else:
                solution_button = driver.find_element(By.XPATH, '/html/body/codingninjas-root/codingninjas-publicsection-app/div[1]/div/div[2]/codingninjas-problems/mat-sidenav-container/mat-sidenav-content/codingninjas-problem-offerings-panel/div/codingninjas-problem-classroom-v2/div/div[1]/span/as-split/as-split-area[1]/ninjas-problems-ui-problem-left-panel/div/mat-tab-group/div/mat-tab-body[3]/div/div[2]/div/ninjas-problems-ui-solution-details-tab/div/div[1]/ninjas-problems-ui-approaches-box/div/div[2]/ninjas-problems-ui-solution-locked-content[2]/div/div[2]/button')
            if solution_button:
                print('sol')
                solution_button.click()
                time.sleep(1)
        except Exception as e:
            print('Solution already seen')
        try:
            if jint:
                code_tab_button = driver.find_element(By.XPATH, '/html/body/codingninjas-root/codingninjas-publicsection-app/div[1]/div/div[2]/codingninjas-problems/mat-sidenav-container/mat-sidenav-content/codingninjas-problem-offerings-panel/div/codingninjas-problem-classroom-v2/div/div[1]/span/as-split/as-split-area[1]/ninjas-problems-ui-problem-left-panel/div/mat-tab-group/div/mat-tab-body[3]/div/div[2]/div/ninjas-problems-ui-solution-details-tab/div/div/ninjas-problems-ui-hints-and-solutions/div/div[2]/ninjas-problems-ui-approaches-box/div/div[2]/ninjas-problems-ui-solution-locked-content[3]/div/div[2]/button')
            else:
                code_tab_button = driver.find_element(By.XPATH, '/html/body/codingninjas-root/codingninjas-publicsection-app/div[1]/div/div[2]/codingninjas-problems/mat-sidenav-container/mat-sidenav-content/codingninjas-problem-offerings-panel/div/codingninjas-problem-classroom-v2/div/div[1]/span/as-split/as-split-area[1]/ninjas-problems-ui-problem-left-panel/div/mat-tab-group/div/mat-tab-body[3]/div/div[2]/div/ninjas-problems-ui-solution-details-tab/div/div[1]/ninjas-problems-ui-approaches-box/div/div[2]/ninjas-problems-ui-solution-locked-content[3]/div/div[2]/button')
            if code_tab_button:
                print('code')
                code_tab_button.click()
                time.sleep(1)
        except Exception as e:
            print('Code already seen')

        try:
            code_elements = driver.find_elements(By.CSS_SELECTOR, ".solution-content .code-wrapper code")
            solution_codes = [code_element.text for code_element in code_elements]
            problem_details['solution_codes'] = solution_codes
        except Exception as e:
            print(f"Failed to extract code: {e}")
    return problem_details

# Iterate over each problem statement URL and extract details
all_problem_details = []

for url in loaded_array:
    problem_details = extract_problem_details(driver, url)
    if problem_details:
        all_problem_details.append(problem_details)

# Save all problem details to a JSON file
json_filename = "problem_details.json"
with open(json_filename, "w") as json_file:
    json.dump(all_problem_details, json_file, indent=4)

# Quit the driver after all URLs have been processed
driver.quit()

print(f"Problem details saved to {json_filename}")
