import random
from seleniumbase import BaseCase
# import Keys
from selenium.webdriver.common.keys import Keys
BaseCase.main(__name__, __file__, "-s", "--uc", "--demo", "--reuse-session", "--maximize")
from logger import Logger
import pytest
import os

# Instantiate logger
logger = Logger('sb_linkedin_bot', 'sb_linkedin_bot.log').get_logger()

class LinkedinBot(BaseCase):
    # Verify login page
    def verify_login_page(self):
        logger.info("\n Verifying login page... ")
        self.assert_element("input#username", timeout=6.25)
        logger.info("\n Verified login page. ")

    # Login
    def login(self):
        logger.info("\n Logging in... ")
        # type username
        logger.info("\n Typing username ")
        self.type('input#username', os.getenv('LINKEDIN_USERNAME'))
        # type password
        logger.info("\n Typing password ")
        self.type('input#password', os.getenv('LINKEDIN_PASSWORD'))

        # click login button
        logger.info("\n Clicking login button ")
        self.click('button:contains("Sign in")', timeout=6.25)

    # Check for security check
    def check_security(self):
        logger.info("\n Checking for security check... ")
        # check for iframe
        if self.is_element_visible('iframe'):
            logger.info("\n Found iframe. ")
            self.switch_to_frame('iframe[title="Captcha Challenge"]')
            # look for verify button
            logger.info("\n Found security check. ")
            self.click('button:contains("Verify")', timeout=6.25)
            logger.info("\n Clicked security check button.")
        else:
            logger.info("\n No security check found. ")


    # Search for job by title
    def search_for_job(self, job_title):
        logger.info("\n Searching for job... ")
        # type job title and press enter
        self.type('input[class="search-global-typeahead__input"]', f'{job_title}\n')
        self.sleep(10)

    # Click Jobs filter button
    def click_jobs_filter_button(self):
        logger.info("\n Clicking jobs filter button... ")
        self.click('button:contains("Jobs")', timeout=6.25)

    # Click Remote filter button
    def filter_remote_results(self):
        # Get initial number of search results
        logger.info("\n Getting initial number of search results... ")
        self.assert_element('div.jobs-search-results-list__subtitle span', timeout=6.25)
        initial_results_num = self.find_element('div.jobs-search-results-list__subtitle span', timeout=6.25).text
        logger.info(f"\n Initial number of search results: {initial_results_num}")
        # Click remote filter button
        logger.info("\n Clicking remote filter button... ")
        self.click('#searchFilter_workplaceType', timeout=6.25)
        # Click remote checkbox
        logger.info("\n Clicking remote checkbox")
        self.click("label[for='workplaceType-2']", timeout=6.25)
        # Click "show results" button
        logger.info("\n Clicking show results button")
        self.click('div[data-basic-filter-parameter-name="workplaceType"] button[data-control-name="filter_show_results"]')
        # Wait randomly between 1 and 5 seconds
        wait_time = random.randint(1, 5)
        logger.info(f"\n Waiting for {wait_time} seconds... ")
        self.sleep(wait_time)
        # Wait for number of search results to change
        self.assert_element('div.jobs-search-results-list__subtitle span', timeout=10)
        new_results_num = self.find_element('div.jobs-search-results-list__subtitle span', timeout=20).text
        # Verify text changed
        self.assert_not_equal(new_results_num, initial_results_num, "Search Results Number Text did not change")
        logger.info(f"\n Search Results Text has updated: {new_results_num}")

    # Scroll to bottom of Job Search Results
    def scroll_within_job_results(self):
        # Wait for search results container to be visible
        self.wait_for_element_visible('div.jobs-search-results-list', timeout=6.25)
        job_results_container = self.find_element('div.jobs-search-results-list')
        # Scroll to the bottom of the search results container
        logger.info("\n Scrolling to the bottom of Job Search Results... ")
        self.execute_script(
        "arguments[0].scroll({top: arguments[0].scrollHeight, behavior: 'smooth'})", job_results_container)


        # Wait randomly between 1 and 5 seconds
        wait_time = random.randint(1, 5)
        logger.info(f"\n Waiting for {wait_time} seconds... ")
        self.sleep(wait_time)

        job_results_container = self.find_element('div.jobs-search-results-list', timeout=6.25)
        # Scroll back to the top of the search results container
        logger.info("\n Scrolling back to the top of Job Search Results... ")
        self.execute_script(
        "arguments[0].scroll({top: 0, behavior: 'smooth'})", job_results_container)
        # Wait randomly between 1 and 5 seconds
        wait_time = random.randint(1, 5)
        logger.info(f"\n Waiting for {wait_time} seconds... ")
        self.sleep(wait_time)

    # Capture questions and corresponding form element
    def extract_label_element_pairs(self):
        # Check for regular form label / input pairs
        # Execute current logic if found
        # Check for resume upload page
        #ember792 > div > div:nth-child(2) > form > div > div > div > div.mt2 > div
        # Write resume upload logic
        # Alternate checking on each page until "Review button is found"
        # Click "Review" button
        # Click "submit button"


        # Find all labels within the form
        logger.info("\n Finding all labels within the easy apply form... ")
        form_labels = self.find_elements('div.jobs-easy-apply-content div form label')

        questions_dictionary = {}
        logger.info("\n Creating Questions Dictionary")
        for label in form_labels:
            label_text = label.text.strip().lower()
            logger.info(f"\n Found label: {label_text}")
            # Attempt to find the corresponding form element
            # Strategy 1: Check for "for" attribute in label
            if label.get_attribute("for"):
                element_id = label.get_attribute("for")
                element = self.find_element(f'#{element_id}')
                logger.info(f"\n Found corresponding element: {element.tag_name} with ID: {element_id}")
            # Strategy 2: Find input/select/textarea within the same parent
            else:
                parent_element = label.find_element_by_xpath("..")
                element = parent_element.find_element_by_xpath(".//input | .//select | .//textarea")
                logger.info(f"\n Found corresponding element: {element.tag_name} with ID: {element.id}")
            # Check if the element exists
            if element:
                questions_dictionary[label_text] = element.tag_name
        logger.info(f"\n Extracted questions dictionary: {questions_dictionary}")
        return questions_dictionary

    def click_apply(self):
        logger.info("\n Clicking apply... ")
        self.click('button span:contains("Apply")', timeout=6.25)

        # Wait randomly between 1 and 5 seconds
        wait_time = random.randint(1, 5)
        logger.info(f"\n Waiting for {wait_time} seconds... ")
        self.sleep(wait_time)

        # Switch to new tab with SeleniumBase
        self.switch_to_newest_tab()
        logger.info("\n Switched to new tab. ")

        # Close Tab with SeleniumBase
        logger.info("\n Closing tab... ")
        self.send_keys('body', Keys.COMMAND + 'w')

        # Switch to original tab
        self.switch_to_default_tab()
        logger.info("\n Switched to original tab. ")

    # Click Easy Apply button
    def click_easy_apply(self):
        logger.info("\n Clicking easy apply... ")
        self.click('button span:contains("Easy Apply")', timeout=6.25)

        # Wait randomly between 1 and 5 seconds
        wait_time = random.randint(1, 5)
        logger.info(f"\n Waiting for {wait_time} seconds... ")
        self.sleep(wait_time)
        # Create label / tag dictionary and click 'Next' button until 'Review' button is present
        while not self.is_element_present('button:contains("Review")'):
            self.extract_label_element_pairs()
            # Click "Next" button
            logger.info("\n Clicking next... ")
            # Check if 'Next' button is present
            if self.is_element_present('button:contains("Next")'):
                logger.info("\n Clicking 'Next' Button")
                self.click('button:contains("Next")', timeout=6.25)
            # Check if 'Review' button is present
            elif self.is_element_present():
                logger.info("\n Clicking 'Review' Button")
                self.click('button:contains("Review")', timeout=6.25)

    # Select Job Cards
    def select_job_cards(self):
        logger.info("\n Selecting Job Cards... ")
        job_cards = self.find_elements('div[data-view-name="job-card"]')
        logger.info(f"\n Found {len(job_cards)} job cards. ")

        for job_card in job_cards:
            logger.info(f"\n Clicking job card... {job_card} ")
            job_card.click()

            # Find "Apply" or "Easy Apply" button
            apply_button = self.find_element('button span:contains("Apply")')
            logger.info(f"\n Found apply button: {apply_button.text}")
            if apply_button.text == "Apply":
                self.click_apply()
            elif apply_button.text == "Easy Apply":
                self.click_easy_apply()

            # Wait randomly between 1 and 5 seconds
            wait_time = random.randint(1, 5)
            logger.info(f"\n Waiting for {wait_time} seconds... ")
    # Navigate to LinkedIn
    # Retry 3 times if verifying login fails
    @pytest.mark.flaky(reruns=3)
    @pytest.mark.run(order=1)
    def test_verify_login(self):
        logger.debug("\n Test: verify login... ")
        # get undetectable driver
        if not (self.undetectable):
            logger.info("\n Getting undetectable driver... ")
            self.get_new_driver(undetectable=True)
        # Navigate to LinkedIn
        logger.info("\n Navigating to LinkedIn... ")
        self.driver.get("https://www.linkedin.com/login")
        try:
            # Verify login page opened
            logger.info("\n Trying to verify login page... ")
            self.verify_login_page()
        except Exception:
            # If login page not loaded, clear all cookies and try again
            self.clear_all_cookies()
            self.get_new_driver(undetectable=True)
            self.driver.get("https://www.linkedin.com/login")
            try:
                # Verify login page opened
                logger.debug("\n Trying to verify login page... ")
                self.verify_login_page()
            except Exception as e:
                logger.error(f"\n Failed to verify login page. {e} Exiting... ")

    # Log In
    @pytest.mark.run(order=2)
    def test_login(self):
        logger.debug("\n Test: login... ")
        try:
            self.login()
        except Exception:
            logger.error("\n Failed to login. Exiting... ")

    # Check for security check
    @pytest.mark.run(order=3)
    def test_check_security(self):
        logger.debug("\n Test: check security... ")
        try:
            self.check_security()
        except Exception as e:
            logger.error("\n Failed to check security. {e} Exiting... ")

    # Search for job
    @pytest.mark.flaky(reruns=2)
    @pytest.mark.run(order=4)
    def test_search_for_job(self):
        logger.debug("\n Test: search for job... ")
        try:
            self.search_for_job('Software Developer')
        except Exception as e:
            logger.error(f"\n Failed to search for job. {e} Exiting... ")

    # Click Jobs filter button
    @pytest.mark.run(order=5)
    def test_click_jobs_filter_button(self):
        logger.debug("\n Test: click jobs filter button... ")
        try:
            self.click_jobs_filter_button()
        except Exception as e:
            logger.error(f"\n Failed to click jobs button. {e} Exiting... ")

    # Click Remote filter button
    @pytest.mark.run(order=6)
    def test_filter_remote_results(self):
        logger.debug("\n Test: filter remote results.. ")
        try:
            self.filter_remote_results()
        except Exception as e:
            logger.error(f"\n Failed to filter remote results. {e} Exiting... ")

    # Scroll to bottom of search results
    @pytest.mark.run(order=7)
    def test_scroll_within_job_results(self):
        logger.debug("\n Test: scroll to bottom... ")
        try:
            self.scroll_within_job_results()
        except Exception as e:
            logger.error(f"\n Failed to complete scroll. {e} Exiting... ")

    # Select Job Cards
    @pytest.mark.run(order=8)
    def test_select_job_cards(self):
        logger.debug("\n Test: select job cards... ")
        try:
            self.select_job_cards()
        except Exception as e:
            logger.error(f"\n Failed to select job cards. {e} Exiting... ")

# Until all job cards have been clicked

  # Click Job Card
    # If Job Card does not say "easy apply"
      # Click apply button
      # Switch to new tab
      # Fill out application
      # Close tab
      # Switch back to original tab
    # Else if Job Card says "easy apply"
      # Click easy apply button
      # While button does not say "Review"
        # Fill out form fields
        # Click "Next" button
    # Click "Review" button

# Click Next Page button

