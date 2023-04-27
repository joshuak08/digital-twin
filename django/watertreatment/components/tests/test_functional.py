from selenium import webdriver
from selenium.webdriver import *
from components.models import *
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time

from selenium.webdriver.common.by import By


class TestHomePage(StaticLiveServerTestCase):
    host = "127.0.0.1"
    port = 8080

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")

        cls.driver = webdriver.Chrome("chromedriver.exe", options=options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()


    def test_home(self):
        response = self.driver.get(self.live_server_url)
        self.assertEqual(self.driver.current_url, "http://127.0.0.1:8080/")
        self.assertTemplateUsed(response, 'components/new-base.html')


    def test_home_types_redirect(self):
        self.driver.get(self.live_server_url)
        self.driver.find_element(By.XPATH, "/html/body/nav/ul/li[2]/a").click()
        self.assertEqual(self.driver.current_url, "http://127.0.0.1:8080/types/")

    def test_home_input_form_redirect(self):
        self.driver.get(self.live_server_url)
        self.driver.find_element(By.XPATH, "/html/body/nav/ul/li[3]/a").click()
        self.assertEqual(self.driver.current_url, "http://127.0.0.1:8080/input-form/")

    def test_home_model_redirect(self):
        self.driver.get(self.live_server_url)
        self.driver.find_element(By.XPATH, "/html/body/nav/ul/li[4]/a").click()
        self.assertEqual(self.driver.current_url, "http://127.0.0.1:8080/revit-model/")

    def test_home_simulation_redirect(self):
        self.driver.get(self.live_server_url)
        self.driver.find_element(By.XPATH, "/html/body/nav/ul/li[5]/a").click()
        self.assertEqual(self.driver.current_url, "http://127.0.0.1:8080/simulation/")

    def test_home_graph_redirect(self):
        self.driver.get(self.live_server_url)
        self.driver.find_element(By.XPATH, "/html/body/nav/ul/li[6]/a").click()
        self.assertEqual(self.driver.current_url, "http://127.0.0.1:8080/graph/")
