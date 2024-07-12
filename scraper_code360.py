# /html/body/div[4]
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
import re
from selenium.webdriver.support import expected_conditions as EC
import json
# Specify the path to your chromedriver executable
driver_path = 'E:\Desktop\chromedriver.exe'
import pickle

filename = "output2.pkl"

with open(filename, "rb") as file:
    loaded_array = pickle.load(file)
# Create a ChromeService object with the driver path
service = ChromeService(executable_path=driver_path)

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver,50)
wait2 = WebDriverWait(driver,5)
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
    diffculty=driver.find_element(By.CLASS_NAME,'difficulty-level').text
    # time_taken=driver.find_element(By.CLASS_NAME,'avg-time').text
    # time_taken = int(re.search(r'\d+', time_taken).group())
    # if not(time_taken):
    #     time_taken=5
    
    if diffculty.lower!='easy':
        problem_details['difficulty']=diffculty
        # Problem Statements
        problem_statement = driver.find_element(By.CSS_SELECTOR, '#mat-tab-content-0-0 > div > div.problem-details.pt-12.px-8.ng-star-inserted > div > ninjas-problems-ui-problem-details-tab > div > ninjas-problems-ui-problem-details-tab-description > div > div.problem-main-statement.ng-star-inserted > div').text
        problem_details['problem_statement'] = problem_statement
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
            jints=driver.find_element(By.CLASS_NAME,'hints-box-container')
            jint=1
        except:
            jint=0
        try:
            if jint:
                approach_button = driver.find_element(By.XPATH, '/html/body/codingninjas-root/codingninjas-publicsection-app/div[1]/div/div[2]/codingninjas-problems/mat-sidenav-container/mat-sidenav-content/codingninjas-problem-offerings-panel/div/codingninjas-problem-classroom-v2/div/div[1]/span/as-split/as-split-area[1]/ninjas-problems-ui-problem-left-panel/div/mat-tab-group/div/mat-tab-body[3]/div/div[2]/div/ninjas-problems-ui-solution-details-tab/div/div/ninjas-problems-ui-hints-and-solutions/div/div[2]/ninjas-problems-ui-approaches-box/div/div[2]/ninjas-problems-ui-solution-locked-content[1]/div/div[2]/button')
            else:
                approach_button = driver.find_element(By.XPATH, '/html/body/codingninjas-root/codingninjas-publicsection-app/div[1]/div/div[2]/codingninjas-problems/mat-sidenav-container/mat-sidenav-content/codingninjas-problem-offerings-panel/div/codingninjas-problem-classroom-v2/div/div[1]/span/as-split/as-split-area[1]/ninjas-problems-ui-problem-left-panel/div/mat-tab-group/div/mat-tab-body[3]/div/div[2]/div/ninjas-problems-ui-solution-details-tab/div/div/ninjas-problems-ui-hints-and-solutions/div/div[1]/ninjas-problems-ui-approaches-box/div/div[2]/ninjas-problems-ui-solution-locked-content[1]/div/div[2]/button')
            if approach_button:
                 print('app')
                 approach_button.click()
                 time.sleep(1)
        except Exception as e:
            print('Approach already seen')

        edit=driver.find_element(By.CLASS_NAME,'suggest-edit')
        driver.execute_script("arguments[0].scrollIntoView(true); window.scrollBy(0, 20);", edit)

        
        try:
            if jint:
                solution_button = driver.find_element(By.XPATH, '/html/body/codingninjas-root/codingninjas-publicsection-app/div[1]/div/div[2]/codingninjas-problems/mat-sidenav-container/mat-sidenav-content/codingninjas-problem-offerings-panel/div/codingninjas-problem-classroom-v2/div/div[1]/span/as-split/as-split-area[1]/ninjas-problems-ui-problem-left-panel/div/mat-tab-group/div/mat-tab-body[3]/div/div[2]/div/ninjas-problems-ui-solution-details-tab/div/div/ninjas-problems-ui-hints-and-solutions/div/div[3]/ninjas-problems-ui-approaches-box/div/div[3]/ninjas-problems-ui-unlocked-approach-content/div/mat-tab-group/div/mat-tab-body[1]/div/div/ninjas-problems-ui-solution-locked-content/div/div[2]/button/span/span/span[2]')
            else:
                solution_button = driver.find_element(By.XPATH, '/html/body/codingninjas-root/codingninjas-publicsection-app/div[1]/div/div[2]/codingninjas-problems/mat-sidenav-container/mat-sidenav-content/codingninjas-problem-offerings-panel/div/codingninjas-problem-classroom-v2/div/div[1]/span/as-split/as-split-area[1]/ninjas-problems-ui-problem-left-panel/div/mat-tab-group/div/mat-tab-body[3]/div/div[2]/div/ninjas-problems-ui-solution-details-tab/div/div/ninjas-problems-ui-hints-and-solutions/div/div[1]/ninjas-problems-ui-approaches-box/div/div[2]/ninjas-problems-ui-solution-locked-content[2]/div/div[2]/button/span/span')
            
            if solution_button:
                driver.execute_script("arguments[0].scrollIntoView(true); window.scrollBy(0, 20);", solution_button)

                print('soln')
                solution_button.click()
        except Exception as e:
            print('Solution already seen')

        approach_div='/html/body/codingninjas-root/codingninjas-publicsection-app/div[1]/div/div[2]/codingninjas-problems/mat-sidenav-container/mat-sidenav-content/codingninjas-problem-offerings-panel/div/codingninjas-problem-classroom-v2/div/div[1]/span/as-split/as-split-area[1]/ninjas-problems-ui-problem-left-panel/div/mat-tab-group/div/mat-tab-body[3]/div/div[2]/div/ninjas-problems-ui-solution-details-tab/div/div/ninjas-problems-ui-hints-and-solutions/div/div[3]/ninjas-problems-ui-approaches-box/div/div[3]/ninjas-problems-ui-unlocked-approach-content/div/mat-tab-group/mat-tab-header/div/div/div/div[1]'
        if not(jint):
            approach_div='/html/body/codingninjas-root/codingninjas-publicsection-app/div[1]/div/div[2]/codingninjas-problems/mat-sidenav-container/mat-sidenav-content/codingninjas-problem-offerings-panel/div/codingninjas-problem-classroom-v2/div/div[1]/span/as-split/as-split-area[1]/ninjas-problems-ui-problem-left-panel/div/mat-tab-group/div/mat-tab-body[3]/div/div[2]/div/ninjas-problems-ui-solution-details-tab/div/div/ninjas-problems-ui-hints-and-solutions/div/div[2]/ninjas-problems-ui-approaches-box/div/div[3]/ninjas-problems-ui-unlocked-approach-content/div/mat-tab-group/mat-tab-header/div/div/div/div[1]'
        reference_div = wait.until(EC.presence_of_element_located((By.XPATH,approach_div )))
        
        # Find the parent element of the reference div
        parent_element = reference_div.find_element(By.XPATH, './..')

        # Find all sibling div elements
        sibling_divs = parent_element.find_elements(By.XPATH, './div')
        print(len(sibling_divs))
        approaches={}
        for num,z in enumerate(sibling_divs):
            i=None
            butt=f'/html/body/codingninjas-root/codingninjas-publicsection-app/div[1]/div/div[2]/codingninjas-problems/mat-sidenav-container/mat-sidenav-content/codingninjas-problem-offerings-panel/div/codingninjas-problem-classroom-v2/div/div[1]/span/as-split/as-split-area[1]/ninjas-problems-ui-problem-left-panel/div/mat-tab-group/div/mat-tab-body[3]/div/div[2]/div/ninjas-problems-ui-solution-details-tab/div/div/ninjas-problems-ui-hints-and-solutions/div/div[3]/ninjas-problems-ui-approaches-box/div/div[3]/ninjas-problems-ui-unlocked-approach-content/div/mat-tab-group/mat-tab-header/div/div/div/div[{str(num+1)}]'
            if not(jint):
                butt=f'/html/body/codingninjas-root/codingninjas-publicsection-app/div[1]/div/div[2]/codingninjas-problems/mat-sidenav-container/mat-sidenav-content/codingninjas-problem-offerings-panel/div/codingninjas-problem-classroom-v2/div/div[1]/span/as-split/as-split-area[1]/ninjas-problems-ui-problem-left-panel/div/mat-tab-group/div/mat-tab-body[3]/div/div[2]/div/ninjas-problems-ui-solution-details-tab/div/div/ninjas-problems-ui-hints-and-solutions/div/div[2]/ninjas-problems-ui-approaches-box/div/div[3]/ninjas-problems-ui-unlocked-approach-content/div/mat-tab-group/mat-tab-header/div/div/div/div[{str(num+1)}]'
            butt=wait.until(EC.presence_of_element_located((By.XPATH,butt)))
            butt.click()
            approach_text=driver.find_element(By.CLASS_NAME,'heading')
            approach_text=approach_text.text
            approach_text=approach_text.split('\n')[0]
            lan=f'/html/body/codingninjas-root/codingninjas-publicsection-app/div[1]/div/div[2]/codingninjas-problems/mat-sidenav-container/mat-sidenav-content/codingninjas-problem-offerings-panel/div/codingninjas-problem-classroom-v2/div/div[1]/span/as-split/as-split-area[1]/ninjas-problems-ui-problem-left-panel/div/mat-tab-group/div/mat-tab-body[3]/div/div[2]/div/ninjas-problems-ui-solution-details-tab/div/div/ninjas-problems-ui-hints-and-solutions/div/div[3]/ninjas-problems-ui-approaches-box/div/div[3]/ninjas-problems-ui-unlocked-approach-content/div/mat-tab-group/div/mat-tab-body[{str(num+1)}]/div/div/div[2]/div[2]/shared-ui-problem-languages/mat-select'
            if not(jint):
                lan=f'/html/body/codingninjas-root/codingninjas-publicsection-app/div[1]/div/div[2]/codingninjas-problems/mat-sidenav-container/mat-sidenav-content/codingninjas-problem-offerings-panel/div/codingninjas-problem-classroom-v2/div/div[1]/span/as-split/as-split-area[1]/ninjas-problems-ui-problem-left-panel/div/mat-tab-group/div/mat-tab-body[3]/div/div[2]/div/ninjas-problems-ui-solution-details-tab/div/div/ninjas-problems-ui-hints-and-solutions/div/div[2]/ninjas-problems-ui-approaches-box/div/div[3]/ninjas-problems-ui-unlocked-approach-content/div/mat-tab-group/div/mat-tab-body[{str(num+1)}]/div/div/div[2]/div[2]/shared-ui-problem-languages/mat-select'
            lan=wait.until(EC.presence_of_element_located((By.XPATH,lan)))
            code_text=wait.until(EC.presence_of_element_located((By.CLASS_NAME,"code-text")))
            driver.execute_script("arguments[0].scrollIntoView(true); window.scrollBy(0, 50);",  code_text)

            lan.click()
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    lan_option = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'lang-option')))
                    for i in lan_option:
                        i.click()
                        lan_text = lan.text  # Assuming you meant to get text from `i`, not `lan`
                        solution = wait.until(EC.presence_of_element_located((By.ID, 'coding'))).text
                        approaches[lan_text] = solution
                        lan.click()  # Assuming you meant to re-click the same element to close it or similar

                    lan_option[0].click()
                    break  # Break out of the retry loop if successful
                except Exception as e:
                    if attempt == max_retries - 1:  # Last attempt
                        raise Exception("Failed after multiple retries") from e
                    time.sleep(15)  # Wait before retrying

            problem_details[approach_text]=approaches
                    
                   

            
    return problem_details

def concatenate_texts(text1, text2, text3):
    return text1 + "\n" + text2 + "\n" + text3

# Main script
homepage_url = "https://www.naukri.com/code360/home"
driver = fetch_page(homepage_url)
if driver:
    # Wait for user to log in
    time.sleep(30)
    # List of problem links to iterate over
    loaded_array=loaded_array[101:]
    for link in loaded_array:
                details=None
                print(f'Startin for {link}')
                retries=0
                while True:
                    try:
                        details = extract_problem_details(driver, link)
                        break
                    except:
                        if retries>=3:
                            break
                        retries+=1
                        continue
                if details:
                    with open('code_360_striver.json', 'a') as f:
                        json.dump(details, f)  # Write dictionary as JSON
                        f.write(',')
                        print(f'Done for {link}')
                else:
                    continue
    driver.quit()
