from urllib import response
from dotenv import load_dotenv
from logger import Logger
from custom_web_driver import CustomWebDriver
from selenium.webdriver.support.ui import WebDriverWait
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from cached_element import CachedElement
# import pandas as pd
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.action_chains import ActionChains


# # Make environment variables available
# load_dotenv()

# # instantiate logger
# logger = Logger('linkedin_logger', 'linkedin_bot.log').get_logger()

# # Instantiate Chrome web driver
# chrome_driver = CustomWebDriver().get_driver()

# # Declare wait variable
# wait = WebDriverWait(chrome_driver, 20)

# # Print webElement attributes
# def print_element_details(element):
#     # Retrieve basic information
#     tag_name = element.tag_name
#     text = element.text
#     attributes_to_retrieve = ['id', 'class', 'name', 'href', 'src', 'alt', 'title', 'type', 'value', 'data-*', 'aria-*', 'innerHTML', 'outerHTML']  # Add more attributes as needed

#     # Function to safely get attribute
#     def safe_get_attribute(elem, attr):
#         try:
#             return elem.get_attribute(attr)
#         except:
#             return None

#     # Retrieve and store attributes
#     attributes = {attr: safe_get_attribute(element, attr) for attr in attributes_to_retrieve}

#     # Print the details
#     logger.info(f"Tag Name: {tag_name}")
#     logger.info(f"Text: {text}")
#     for attr, value in attributes.items():
#         if value:
#             logger.info(f"{attr.capitalize()}: {value}")

# # Log into LinkedIn
# def login_to_linkedin():
#     logger.info('Navigating to LinkedIn login page')
#     with chrome_driver:
#         chrome_driver.get('https://www.linkedin.com/login')
#         username = os.getenv('LINKEDIN_USERNAME')
#         password = os.getenv('LINKEDIN_PASSWORD')

#         wait.until(EC.visibility_of_element_located((By.ID, 'username')))

#         logger.info('Filling in login form')
#         username_input = chrome_driver.find_element(By.ID, 'username')
#         username_input.send_keys(username)

#         password_input = chrome_driver.find_element(By.ID, 'password')
#         password_input.send_keys(password)

#         logger.info('Submitting login form')
#         password_input.submit()

# # Search for a job title and apply remote filter
# def search_job_and_apply_filters(job_title):
#     # Search for job title
#     logger.info(f'Searching for job title: {job_title}')
#     search_bar = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'search-global-typeahead__input')))
#     search_bar.send_keys(job_title)
#     search_bar.send_keys(Keys.ENTER)

#     # Select jobs filter button
#     logger.info('Selecting jobs filter button')
#     jobs_button = wait.until(EC.visibility_of_element_located(
#         (By.CSS_SELECTOR, 'button.artdeco-pill.artdeco-pill--slate.artdeco-pill--choice.artdeco-pill--2.search-reusables__filter-pill-button.search-reusables__filter-pill-button')))
#     logger.debug('Clicking jobs filter button')
#     # Click jobs filter button
#     jobs_button.click()

#     # Wait for results
#     logger.info('Waiting for search results to load')
#     wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'jobs-search-results-list')))

#     # Cache old results
#     old_results_cache = CachedElement(chrome_driver, (By.CLASS_NAME, 'jobs-search-results-list'))
#     # Get old results
#     old_results = old_results_cache.get()

#     # Wait for remote filter
#     wait.until(EC.element_to_be_clickable((By.ID, 'searchFilter_workplaceType')))

#     # Select remote filter
#     remote_button = wait.until(EC.visibility_of_element_located((By.ID, 'searchFilter_workplaceType')))
#     logger.debug('Clicking remote filter button')
#     # Click remote filter
#     remote_button.click()

#     # Select remote checkbox
#     remote_checkbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='workplaceType-2']")))
#     logger.debug('Clicking remote checkbox option')
#     # Click remote checkbox
#     remote_checkbox.click()

#     # Select Show Results button
#     wait.until(
#         EC.element_to_be_clickable(
#             (By.CSS_SELECTOR, '[data-basic-filter-parameter-name="workplaceType"] [data-control-name="filter_show_results"]')))

#     # Cache Show Results button
#     show_results_button_cache = CachedElement(
#         chrome_driver, (By.CSS_SELECTOR, '[data-basic-filter-parameter-name="workplaceType"] [data-control-name="filter_show_results"]'))

#     # Get Show Results button
#     show_results_button = show_results_button_cache.get()
#     # Print the attributes
#     print_element_details(show_results_button)
#     # Click Show Results button
#     logger.debug('Clicking Show Results button')
#     show_results_button.click()

#     # Wait for the old results to disappear
#     wait.until(EC.staleness_of(old_results))

# # load the job results
# def load_jobs():
#     # Wait for the job results to load
#     logger.info('Waiting for job results to load')
#     wait.until(
#         EC.presence_of_element_located((By.CLASS_NAME, 'jobs-search-results-list'))
#     )
#     # cache the job results
#     logger.info('Caching job results')
#     new_results_cache = CachedElement(chrome_driver, (By.CLASS_NAME, 'jobs-search-results-list'))

#     # Get the job results container
#     job_results_container = new_results_cache.get()

#     # Wait for at least one job card to appear in new results
#     wait.until(
#         EC.presence_of_element_located(
#             (By.XPATH, '//div[@data-view-name="job-card"]')))

#     print_element_details(job_results_container)

# # Log in to LinkedIn
# try:
#     login_to_linkedin()

# # Log any errors
# except Exception as e:
#     logger.error(f"An error occurred while logging in: {e}", exc_info=True)

# # Search for job and apply filters
# try:
#     search_job_and_apply_filters('Software Developer')

# # Log any errors
# except Exception as e:
#     logger.error(f"An error occurred while searching for a job title: {e}", exc_info=True)

# # Load job results
# try:
#     load_jobs()
# except Exception as e:
#     logger.error(f"An error occurred while waiting for search results: {e}", exc_info=True)
#     chrome_driver.quit()





# # wait for all job cards to reload
# logger.info('Waiting for all job cards to reload')
# wait.until(
#     EC.visibility_of_all_elements_located(
#         (By.XPATH, '//div[@data-view-name="job-card"]'))
# )

# job_results_container = driver.find_element(By.CLASS_NAME, 'jobs-search-results-list')

# # get initial number of job_cards
# num_cards = len(job_results_container.find_elements(By.XPATH, '//div[@data-view-name="job-card"]'))
# logger.info(f'Initial number of job cards: {num_cards}')

# # loop until all job cards are loaded
# logger.info('Looping until all job cards are loaded')
# while True:
#     # scroll to the bottom of the job results container
#     logger.info('Scrolling to the bottom of the job results container')
#     driver.execute_script(
#         "arguments[0].scroll({top: arguments[0].scrollHeight, behavior: 'smooth'})", job_results_container)

#     # wait for results to load after scrolling
#     wait.until(
#         EC.visibility_of_element_located((By.CLASS_NAME, "jobs-search-results-list"))
#     )

#     # get current number of job_cards
#     current_num_cards = len(job_results_container.find_elements(By.XPATH, '//div[@data-view-name="job-card"]'))
#     logger.info(f'Current number of job cards: {current_num_cards}')

#     # if all job cards are loaded, break the loop
#     if current_num_cards > num_cards:
#         logger.info('All job cards are loaded')
#         logger.info(f'Number of job cards: {current_num_cards}')
#         break
#     else:
#         logger.info('Not all job cards are loaded')
#         num_cards = current_num_cards

# application_data = []

# def find_elements_with_click_events():
#     # execute JavaScript to find elements with click events
#     script = """
#         const clickableElements = []
#         const elements = document.querySelectorAll('*');
#         for (let i = 0; i < elements.length; i++) {
#             let clickEvent = elements[i].onclick;
#             if (clickEvent !== null) {
#                 clickableElements.push(elements[i]);
#             }
#             return clickableElements;
#         }
#     """
#     return driver.execute_script(script)

# def is_partial_match(text, keywords):
#     return any(keyword.lower() in text.lower() for keyword in keywords)

# # check if element or nested element contains a keyword
# def is_apply_element(element):
#     keywords = ["apply", "application", "role", "resume", "join"]
#     return is_partial_match(element.text, keywords) or is_partial_match(element.get_attribute("innerText"), keywords)

# # find all clickable elements on the page
# def find_apply_elements():
#     clickable_elements_xpath = driver.find_elements(By.XPATH, "//a | //button | //input")

#     # Find all elements that contain the word "apply
#     clickable_elements_text = driver.find_elements(By.XPATH, '//*[contains(translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "apply")]')

#     # Find all elements with JavaScript click events
#     # clickable_elements_events = find_elements_with_click_events()

#     # Find all clickable elements using CSS selector
#     clickable_elements_css = driver.find_elements(By.CSS_SELECTOR, '[href*="apply"], [onclick*="apply"], [value*="apply"], [type="submit"], [type="button"], [data-apply*="true"], [aria-apply*="true"]')

#     all_clickable_elements = clickable_elements_xpath + clickable_elements_text  + clickable_elements_css

#     # filter clickable elements that contain the word "apply"
#     apply_elements = [element for element in all_clickable_elements if is_apply_element(element)]

#     logger.info(f"Found {len(apply_elements)} apply elements")
#     logger.info(f'{[apply_element.get_attribute("outerHTML") for apply_element in apply_elements]}')


#     return apply_elements
# # submit application functions
# def apply(apply_button):
#     tabs_before_click = driver.window_handles
#     apply_button.click()

#     # wait for new tab to open
#     wait.until(EC.number_of_windows_to_be(len(tabs_before_click) + 1))

#     # switch to new tab

#     tabs_before_click = driver.window_handles
#     apply_button.click()

#     wait.until(EC.number_of_windows_to_be(len(tabs_before_click) + 1))

#     new_tab = [
#         tab for tab in driver.window_handles if tab not in tabs_before_click][0]
#     driver.switch_to.window(new_tab)

#     tabs_after_click = driver.window_handles

#     # find button that contains the text 'apply' (case insensitive)
#     try:
#         find_apply_elements()

#         logger.info("external apply button found")

#         # check if clicking the button opens another new tab
#         tabs_after_external_click = driver.window_handles

#         if len(tabs_after_external_click) > len(tabs_after_click):
#             # if another new tab is opened after clicking, switch to it
#             new_tab_after_external_click = [
#                 tab for tab in tabs_after_external_click if tab not in tabs_after_click][0]

#             driver.switch_to.window(new_tab_after_external_click)

#             logger.info("Another new tab opened after external apply button clicked")
#             # then, look for form element
#             # if form element is found,
#             # select labels and corresponding form fields
#             # group into data structure and store for analysis
#             # else return text 'No application form found'
#         else:
#             # elif another new tab is not opened after clicking,
#             # then, look for form element
#             # select labels and corresponding form fields
#             # group into data structure and store for analysis
#             logger.info("No new tab opened after external apply button clicked")
#         # else return text 'No application form found'
#     except NoSuchElementException:
#         logger.info("No external apply button found")

#         # elif no apply button is found,
#         # then, look for form element
#         # select labels and corresponding form fields
#         # group into data structure and store for analysis
#         # else return text 'No application form found'

#     wait.until(EC.presence_of_element_located((By.ID, 'username')))
#     # form submission logic to be added after analysis


# def easy_apply(apply_button):
#     # click apply_button with JavaScript
#     script = """
#         arguments[0].click();
#     """
#     driver.execute_script(script, apply_button)

#     wait.until(EC.presence_of_element_located(
#         (By.XPATH, '//div[@class="jobs-easy-apply-content"]')))

#     # init dictionary to store label and corresponding form field pairs
#     form_data = {}

#     while True:
#         # check for parent div
#         parent_div = None
#         try:
#             parent_div = driver.find_element(
#                 By.XPATH, '//div[@class="jobs-easy-apply-content"]')
#             logger.info("Found parent div:")
#             logger.info(parent_div)
#         except NoSuchElementException:
#             pass

#         # if additional questions (parent div is found)
#         if parent_div:
#             # find sibling div containers of label / form field
#             sibling_divs = parent_div.find_elements(
#                 By.CSS_SELECTOR, 'div.jobs-easy-apply-form-section__grouping')

#             logger.info("Found sibling divs:")
#             logger.info(sibling_divs)
#             # Iterate to select labels and corresponding form fields
#             for sibling_div in sibling_divs:
#                 logger.info("Found sibling div:")
#                 logger.info(sibling_div)
#                 # find label text
#                 label_text = sibling_div.find_element(
#                     By.XPATH, '//label//[not contains(@class, "visually-hidden))"]//*[@class]').text.strip()

#                 # find form field following sibling
#                 next_form_field = sibling_div.find_element(
#                     By.XPATH, './/label/following-sibling::*')

#                 # get the tag name of the form field
#                 element_type = next_form_field.tag_name

#                 # store the pair in the dictionary
#                 form_data[label_text] = element_type

#             # check for "Next" button
#             next_button = None
#             try:
#                 next_button = driver.find_element(
#                     By.XPATH, '//*[contains(translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "next")]')
#             except NoSuchElementException:
#                 pass

#             # if "Next" button is found click it
#             if next_button:
#                 next_button.click()
#                 wait.until(EC.presence_of_element_located(
#                     (By.XPATH, '//div[@class="jobs-easy-apply-content"]')))
#             else:
#                 break
#         else:
#             # If no parent div is found, check for "review" button
#             review_button = None
#             try:
#                 review_button = driver.find_element(
#                     By.XPATH, '//*[contains(translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "review")]')
#             except NoSuchElementException:
#                 pass

#             # if "review" button is found click it
#             if review_button:
#                 review_button.click()
#                 wait.until(EC.presence_of_element_located(
#                     (By.XPATH, '//div[@class="jobs-easy-apply-content"]')))
#             else:
#                 break
#         logger.info(form_data)
#         return form_data

#     # for submission logic to be added after analysis

# # wait until all job cards are visible
# wait.until(EC.visibility_of_all_elements_located(
#     (By.XPATH, '//div[@data-view-name="job-card"]')
# ))

# # select all job cards
# job_cards = driver.find_elements(By.XPATH, '//div[@data-view-name="job-card"]')
# logger.info(f'Found {len(job_cards)} job cards')
# # collect job data
# job_data = []

# # extract data from job cards
# logger.info('Extracting data from job cards')
# for job_card in job_cards:
#     wait.until(EC.element_to_be_clickable(
#         (By.XPATH, '//div[@data-view-name="job-card"]')))

#     logger.info(f'clicking job card {job_card}')
#     # use JavaScript to click the job_card directly
#     driver.execute_script(
#         "arguments[0].click();", job_card
#     )

#     job_title = job_card.find_element(
#         By.CSS_SELECTOR, 'a.disabled.ember-view.job-card-container__link.job-card-list__title').text.strip()

#     logger.info(f'Job Title: {job_title}')

#     company = job_card.find_element(
#         By.CSS_SELECTOR, 'span.job-card-container__primary-description').text.strip()

#     try:
#         salary = job_card.find_element(
#             By.CSS_SELECTOR, '.mt1.t-sans.t-12.t-black--light.t-normal.t-roman.artdeco-entity-lockup__metadata.ember-view ul li').text.strip()
#     except NoSuchElementException:
#         salary = 'None provided'

#     # link

#     job_data.append(
#         {'job_title': job_title, 'company': company, 'salary': salary})

#     # find apply button
#     apply_button = driver.find_element(
#         By.CSS_SELECTOR, 'div.jobs-s-apply.jobs-s-apply--fadein.inline-flex.mr2')
#     # get button text
#     button_text = apply_button.find_element(
#         By.CSS_SELECTOR, 'span.artdeco-button__text').text.strip()

#     if button_text == 'Apply':
#         logger.info('clicking Apply')
#         apply(apply_button)
#         # wait.until(EC.staleness_of(apply_button))
#     elif button_text == 'Easy Apply':
#         easy_apply(apply_button)
#         logger.info('clicking Easy Apply')
#         # wait.until(EC.staleness_of(apply_button))



# # print collected job data
# df = pd.DataFrame(job_data)
# logger.info(df)

# # # get HTML of current page
# # html = driver.page_source

# # # create beautiful soup object
# # soup = BeautifulSoup(html, 'html.parser')