from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        binary = FirefoxBinary("C:/Program Files (x86)/Mozilla Firefox/firefox.exe")
        self.browser = webdriver.Firefox(firefox_binary=binary)
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    @contextmanager
    def wait_for_page_load(self, timeout=30):
        old_page = self.browser.find_element_by_tag_name("html")
        yield WebDriverWait(self.browser, timeout).until(
            EC.staleness_of(old_page)
        )

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_list_and_retrieve_it_later(self):
        self.browser.get("http://localhost:8000")

        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", header_text)

        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(
            inputbox.get_attribute("placeholder"),
            "Enter a to-do item"
        )
        inputbox.send_keys("Buy peacock feathers")
        inputbox.send_keys(Keys.ENTER)

        with self.wait_for_page_load(timeout=10):
            self.check_for_row_in_list_table("1: Buy peacock feathers")

        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)

        with self.wait_for_page_load(timeout=10):
            self.check_for_row_in_list_table("1: Buy peacock feathers")
            self.check_for_row_in_list_table("2: Use peacock feathers to make a fly")

        self.fail("Finish the test!")


if __name__ == '__main__':
    unittest.main(warnings='ignore')