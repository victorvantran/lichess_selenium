from locator import *
from element import BasePageElement

class SearchTextElement(BasePageElement):
    locator = "/faq"

class BasePage(object):
    def __init__(self, driver):
        self.driver = driver

class MainPage(BasePage):

    search_text_element = SearchTextElement()

    def is_title_match(self):
        return "lichess.org" in self.driver.title

    def click_sign_in_button(self):
        element = self.driver.find_element(*MainPageLocators.SIGN_IN_BUTTON)
        element.click()

class SearchResultPage(BasePage):

    def is_results_found(self):
        return "No results found." not in self.driver.page_source