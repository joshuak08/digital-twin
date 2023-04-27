from selenium import webdriver
from selenium.webdriver import *
from components.models import *
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time

from selenium.webdriver.common.by import By


class TestHomePage(StaticLiveServerTestCase):
    host = "127.0.0.1"
    port = 8000

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")

        cls.driver = webdriver.Chrome("chromedriver.exe", options=options)

    # def setUp(self):
    #     options = webdriver.ChromeOptions()
    #     # options.add_argument("--headless")
    #     options.add_argument("--window-size=1920,1080")
    #     print(options.capabilities)
    #     self.browser = Chrome('chromedriver.exe', options=options)
    #     self.browser.service.port = 8000

        # self.live_server_url = "http://127.0.0.1/8000"
        # print('setup: ' + self.browser.current_url)

    #
    # @classmethod
    # def tearDownClass(cls):
    #     cls.browser.close()
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()


    def test_home_page(self):
        self.driver.get(self.live_server_url)
        alert = self.driver.find_element(By.CLASS_NAME, "logo")

        # alert = self.browser.find_element_by_class_name("logo")
        self.assertEqual(
            alert.find_element(By.TAG_NAME, 'p').text,
            'WATER TREATMENT DIGITAL TWIN'
        )

        self.driver.get(self.live_server_url + '/input-form/')
        time.sleep(2)
        # print(self.driver.current_url)

    def test_lol(self):
        # print("second test")
        self.assertEqual(self.driver.current_url, "http://127.0.0.1:8000/input-form/")
