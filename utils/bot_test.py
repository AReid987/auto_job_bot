from seleniumbase import BaseCase
BaseCase.main(__name__, __file__, "--uc", "-s")
from utils.logger import Logger

# Instantiate logger
logger = Logger('bot_test', 'bot_test.log').get_logger()

class BotTest(BaseCase):
  def verify_success(self):
        self.assert_text("OH YEAH, you passed!", "h1", timeout=6.25)
        self.post_message("Selenium wasn't detected!", duration=2.8)
        logger.info("\n Success! Website did not detect Selenium! ")

  def fail_me(self):
        self.fail('Selenium was detected! Try using: "pytest --uc"')

  def test_browser_is_undetected(self):
      if not (self.undetectable):
          self.get_new_driver(undetectable=True)
      self.driver.get("https://nowsecure.nl/#relax")
      try:
          logger.info("\n Trying to verify success...")
          self.verify_success()
      except Exception:
          self.clear_all_cookies()
          self.get_new_driver(undetectable=True)
          self.driver.get("https://nowsecure.nl/#relax")
          try:
              self.verify_success()
          except Exception:
              if self.is_element_visible('iframe[src*="challenge"]'):
                  with self.frame_switch('iframe[src*="challenge"]'):
                      self.click("span.mark")
              else:
                  self.fail_me()
              try:
                  self.verify_success()
              except Exception:
                  self.fail_me()



