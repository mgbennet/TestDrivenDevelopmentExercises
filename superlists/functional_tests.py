from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        binary = FirefoxBinary("C:/Program Files (x86)/Mozilla Firefox/firefox.exe")
        self.browser = webdriver.Firefox(firefox_binary=binary)
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_list_and_retrieve_it_later(self):
        self.browser.get("http://localhost:8000")

        self.assertIn('To-Do', self.browser.title)
        self.fail("Finish the test!")


if __name__ == '__main__':
    unittest.main(warnings='ignore')