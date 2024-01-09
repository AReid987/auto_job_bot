from ai.ai_crew import AiCrew as AI
from utils.csv_formatter import *
from fuzzywuzzy import fuzz
import ipdb
import os
import pytest
from utils.logger import Logger
import random
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__, "-s", "--uc",
              "--demo", "--reuse-session", "--maximize")

# Instantiate logger
logger = Logger('sb_linkedin_bot', 'sb_linkedin_bot.log').get_logger()


class LinkedinBot(BaseCase):
    ###################################################################
    ########################## NUMBER 1 ###############################
    # Verify login page
    def verify_login_page(self):
        logger.info("\n Verifying login page... ")
        self.assert_element("input#username", timeout=6.25)
        logger.info("\n Verified login page. ")

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
                logger.error(
                    f"\n Failed to verify login page. {e} Exiting... ")

    ###################################################################
    ########################## NUMBER 2 ###############################
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

    # Log In
    @pytest.mark.run(order=2)
    def test_login(self):
        logger.debug("\n Test: login... ")
        try:
            self.login()
        except Exception as e:
            logger.error(f"\n Failed to login. Exiting... {e}")

    ###################################################################
    ########################## NUMBER 3 ###############################
    # Search for job by title
    def search_for_job(self, job_title):
        logger.info("\n Searching for job... ")
        # type job title and press enter
        self.type(
            'input[class="search-global-typeahead__input"]', f'{job_title}\n')
        self.sleep(10)

    @pytest.mark.flaky(reruns=2)
    @pytest.mark.run(order=3)
    def test_search_for_job(self):
        logger.debug("\n Test: search for job... ")
        try:
            self.search_for_job('Software Developer')
        except Exception as e:
            logger.error(f"\n Failed to search for job. {e} Exiting... ")

    ###################################################################
    ########################## NUMBER 4 ###############################
    # Click Jobs filter button
    def click_jobs_filter_button(self):
        logger.info("\n Clicking jobs filter button... ")
        self.click('button:contains("Jobs")', timeout=6.25)

    # Click Jobs filter button
    @pytest.mark.run(order=4)
    def test_click_jobs_filter_button(self):
        logger.debug("\n Test: click jobs filter button... ")
        try:
            self.click_jobs_filter_button()
        except Exception as e:
            logger.error(f"\n Failed to click jobs button. {e} Exiting... ")

    ###################################################################
    ########################## NUMBER 5 ###############################
    # Click Remote filter button
    def filter_remote_results(self):
        # Get initial number of search results
        logger.info("\n Getting initial number of search results... ")
        self.assert_element(
            'div.jobs-search-results-list__subtitle span', timeout=6.25)
        initial_results_num = self.find_element(
            'div.jobs-search-results-list__subtitle span', timeout=6.25).text
        logger.info(
            f"\n Initial number of search results: {initial_results_num}")
        # Click remote filter button
        logger.info("\n Clicking remote filter button... ")
        self.click('#searchFilter_workplaceType', timeout=6.25)
        # Click remote checkbox
        logger.info("\n Clicking remote checkbox")
        self.click("label[for='workplaceType-2']", timeout=6.25)
        # Click "show results" button
        logger.info("\n Clicking show results button")
        self.click(
            'div[data-basic-filter-parameter-name="workplaceType"] button[data-control-name="filter_show_results"]')
        # Wait randomly between 1 and 5 seconds
        wait_time = random.randint(1, 5)
        logger.info(f"\n Waiting for {wait_time} seconds... ")
        self.sleep(wait_time)
        # Wait for number of search results to change
        self.assert_element(
            'div.jobs-search-results-list__subtitle span', timeout=10)
        new_results_num = self.find_element(
            'div.jobs-search-results-list__subtitle span', timeout=20).text
        # Verify text changed
        self.assert_not_equal(new_results_num, initial_results_num,
                              "Search Results Number Text did not change")
        logger.info(f"\n Search Results Text has updated: {new_results_num}")

    # Click Remote filter button
    @pytest.mark.run(order=5)
    def test_filter_remote_results(self):
        logger.debug("\n Test: filter remote results.. ")
        try:
            self.filter_remote_results()
        except Exception as e:
            logger.error(
                f"\n Failed to filter remote results. {e} Exiting... ")

    ###################################################################
    ########################## NUMBER 6 ###############################
    # Scroll to bottom of Job Search Results
    def scroll_within_job_results(self):
        # Wait for search results container to be visible
        self.wait_for_element_visible(
            'div.jobs-search-results-list', timeout=6.25)
        job_results_container = self.find_element(
            'div.jobs-search-results-list')
        # Scroll to the bottom of the search results container
        logger.info("\n Scrolling to the bottom of Job Search Results... ")
        self.execute_script(
            "arguments[0].scroll({top: arguments[0].scrollHeight, behavior: 'smooth'})", job_results_container)

        # Wait randomly between 1 and 5 seconds
        wait_time = random.randint(1, 5)
        logger.info(f"\n Waiting for {wait_time} seconds... ")
        self.sleep(wait_time)

        job_results_container = self.find_element(
            'div.jobs-search-results-list', timeout=6.25)
        # Scroll back to the top of the search results container
        logger.info("\n Scrolling back to the top of Job Search Results... ")
        self.execute_script(
            "arguments[0].scroll({top: 0, behavior: 'smooth'})", job_results_container)
        # Wait randomly between 1 and 5 seconds
        wait_time = random.randint(1, 5)
        logger.info(f"\n Waiting for {wait_time} seconds... ")
        self.sleep(wait_time)

    # Scroll to load all of the search results
    @pytest.mark.run(order=6)
    def test_scroll_within_job_results(self):
        logger.debug("\n Test: scroll to bottom... ")
        try:
            self.scroll_within_job_results()
        except Exception as e:
            logger.error(f"\n Failed to complete scroll. {e} Exiting... ")

    ###################################################################
    ########################## NUMBER 7 ###############################

    ###################################################################
    ################### STANDARD APPLY LOGIC ##########################
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
        self.driver.close()

        # Switch to original tab
        self.switch_to_default_tab()
        logger.info("\n Switched to original tab.")

    ###################################################################
    ##################### EASY APPLY LOGIC ############################

    ###################################################################
    ############## CHECKING CSV FILE FOR MATCHES ######################

    # # Check CSV file for matches to form questions
    # def check_csv_matches(self, form_question):
    #     matched_response = ''
    #     # Iterate over processed csv file
    #     for prompt in [*processed_csv_data.keys()]:
    #         similarity = fuzz.token_set_ratio(prompt.lower(), form_question.lower())
    #         if similarity > 80:
    #             matched_response = processed_csv_data[prompt]

    #     return matched_response

    ###################################################################
    ################### HANDLING FORM FIELDS ##########################

    # Check for empty Radio button and make correct selection
    ###################### RADIO BUTTONS ##############################
    def handle_radio_button(self, field_set, radio_buttons):
        ipdb.set_trace()
        # Get the question
        prompt = field_set.text.split('\n')[0]
        # Check CSV for matching question
        # csv_check = self.check_csv_matches(prompt)
        csv_check = AI().run('qa_pairs.csv', prompt)
        ipdb.set_trace()
        # Use answer if match found
        if len(csv_check) > 0:
            answer = csv_check
            # radio_button.click('contains:answer')
            for radio_button in radio_buttons:
                if radio_button.get_attribute("value") == answer:
                    radio_button.click()
                    ipdb.set_trace()
        else:
            # If no match add question / answer choices to data sheet csv
            answers = [radio_button.get_attribute(
                'value') for radio_button in radio_buttons]
            write_to_trainer_sheet(prompt, answers)
            ipdb.set_trace()
        #
        # If not found Give the prompt to the AI to answer the question

    ######################## DROPDOWNS ################################
    # Check for empty dropdown and make correct selection
    def handle_dropdown(self, label, form_field):
        # Get the question
        prompt = label.text.split('\n')[0]
        # Check CSV for matching question
        csv_check = AI().run('qa_pairs.csv', prompt)
        ipdb.set_trace()
        # Use answer if match found
        if len(csv_check) > 0:
            answer = csv_check
        ipdb.set_trace()

    ########################### INPUTS ################################
    # Check for empty input and make correct selection
    def handle_input(self, label, form_field):
        prompt = label.text.split('\n')[0]
        # Check CSV for matching question
        csv_check = AI().run('qa_pairs.csv', prompt)
        logger.info(f"CSV Check: {csv_check}")
        ipdb.set_trace()
        # Use answer if match found
        # if len(csv_check) > 0:
        #     answer = csv_check
        #     # Write answer to trainer_sheet.csv
        #     write_to_trainer_sheet(prompt, answer)
        #     # Fill form field with answer
        #     ipdb.set_trace()
        #     form_field.send_keys(answer)
        # # If not found Give the prompt to the AI to answer the question
        # else:
        #     # If no match add question / answer choices to data sheet csv
        #     write_to_trainer_sheet(prompt, '<placeholder>')
        #     # Ask AI to fill form field with answer
        #     #answer = ask_ai_for_answer
        #     # LinkedinBot.add_to_global_prompts(prompt)
        #     # new_prompt = LinkedinBot.read_global_prompts()[-1]
        #     # main(new_prompt)
        #     #form_field.send_keys('')
        #     ipdb.set_trace()

    # Check for resume upload form
    def check_for_resume_upload(self):
        logger.info("\n Checking for resume upload form")
        try:
            self.find_element('div.ui-attachment.jobs-document-upload-redesign-card__container.jobs-document-upload-redesign-card__container--cursor-pointer.jobs-document-upload-redesign-card__container--selected.ui-attachment--pdf', timeout=6.25)
            logger.info("\n Resume upload form found")
            return True
        except:
            logger.info("\n No Resume upload form found")
            return False

    # Check form for empty fields
    # TODO : Refactor - separation of concerns
    def check_and_fill_form_fields(self):
        if not self.check_for_resume_upload():
            logger.info("\n Checking if form fields are filled...")
            # Select form field sections
            logger.info("\n Selecting form field sections...")
            form_sections = self.find_elements(
                'div.jobs-easy-apply-form-section__grouping')
            # Iterate over the form sections
            for form_section in form_sections:
                # Determine which type of form element
                try:
                    logger.info("\n Checking for radio buttons")
                    field_set = form_section.find_element(
                        'tag name', 'fieldset')
                    # Find and check radio buttons
                    radio_buttons = field_set.find_elements(
                        'css selector', 'input[type="radio"]')
                    # Iterate over radio buttons and check if any are selected
                    if not any(radio_button.is_selected() for radio_button in radio_buttons):
                        logger.info(
                            "\n Found an unselected radio button group")
                        self.handle_radio_button(field_set, radio_buttons)
                except Exception as e:
                    logger.info(f"\n Failed on checking radio buttons: {e}")
                    try:
                        logger.info("\n Checking for labels")
                        label = form_section.find_element('tag name', 'label')
                        form_field_id = label.get_attribute("for")
                        # Find label's corresponding element
                        logger.info("\n Finding label's corresponding field")
                        form_field = self.find_element(f"#{form_field_id}")
                        # Check if dropdown
                        if form_field.tag_name == 'select':
                            # Check if dropdown has a selection
                            logger.info(
                                "\n Found dropdown, checking for selection")
                            default_option = form_field.find_element(
                                'tag name', 'option')
                            if default_option.is_selected():
                                logger.info("\n Found an unselected dropdown")
                                dropdown_text = label.text.split("\n")[0]
                                # Make correct dropdown selection
                                self.handle_dropdown(label, form_field)
                                # TODO Logic to make correct dropdown selection
                        elif form_field.tag_name == 'input' or form_field.tag_name == 'textarea' or form_field.tag_name == 'email':
                            # Check if form field is empty
                            logger.info("\n Found text field")
                            field_value = form_field.get_attribute(
                                'value').strip()
                            if not field_value:
                                logger.info("\n Found an empty text field")
                                self.handle_input(label, form_field)
                                # TODO  Logic to input correct input field text
                    except:
                        logger.info("\n No label found")
        return True
    # Click Easy Apply button

    def click_easy_apply(self):
        logger.info("\n Clicking easy apply... ")
        self.click('button span:contains("Easy Apply")', timeout=6.25)

        # Wait randomly between 1 and 5 seconds
        wait_time = random.randint(1, 5)
        logger.info(f"\n Waiting for {wait_time} seconds... ")
        self.sleep(wait_time)
        # Until "Submit" button is present
        while not self.is_element_present('button:contains("Submit")'):
            try:
                # Check for empty form fields and input correct answer if found
                self.check_and_fill_form_fields()
                # Click "Next" button
                logger.info("\n Fields are filled.")
                # Check if 'Next' button is present
                if self.is_element_present('button:contains("Next")'):
                    logger.info("\n Clicking 'Next' Button")
                    self.click('button:contains("Next")', timeout=6.25)
                # Check if 'Review' button is present
                elif self.is_element_present('button:contains("Review")'):
                    logger.info("\n Clicking 'Review' Button")
                    self.click('button:contains("Review")', timeout=6.25)
            except Exception as e:
                logger.error(f"\n Failed to fill form fields: {e}")

        # If "Submit" button is present
        if self.is_element_present('button:contains("Submit")'):
            # Temporarily : quit without submitting application
            dismiss_button = self.find_element(
                'button.artdeco-button.artdeco-button--circle.artdeco-button--muted.artdeco-button--2.artdeco-button--tertiary.ember-view.artdeco-modal__dismiss')
            dismiss_button.click()
            # TODO: Submit application logic
    # Select Job Cards

    def select_job_cards(self):
        logger.info("\n Selecting Job Cards... ")
        # Select all the job cards
        job_cards = self.find_elements('div[data-view-name="job-card"]')
        logger.info(f"\n Found {len(job_cards)} job cards. ")

        # Iterate over the job cards
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
    # Apply to jobs

    @pytest.mark.run(order=7)
    def test_select_job_cards(self):
        logger.debug("\n Test: select job cards... ")
        try:
            self.select_job_cards()
        except Exception as e:
            logger.error(f"\n Failed to select job cards. {e} Exiting... ")

# TODO : Handle security checks

    # # Check for security check
    # def check_security(self):
    #     logger.info("\n Checking for security check... ")
    #     pass
    #     check for iframe
    #     if self.is_element_visible('iframe'):
    #         logger.info("\n Found iframe. ")
    #         self.switch_to_frame('iframe[title="Captcha Challenge"]')
    #         # look for verify button
    #         logger.info("\n Found security check. ")
    #         self.click('button:contains("Verify")', timeout=6.25)
    #         logger.info("\n Clicked security check button.")
    #     else:
    #         logger.info("\n No security check found. ")

    # # Check for security check
    # @pytest.mark.run(order=3)
    # def test_check_security(self):
    #     logger.debug("\n Test: check security... ")
    #     try:
    #         self.check_security()
    #     except Exception as e:
    #         logger.error("\n Failed to check security. {e} Exiting... ")

    # Search for job
