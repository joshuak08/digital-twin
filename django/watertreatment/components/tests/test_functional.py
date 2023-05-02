from selenium import webdriver
from selenium.webdriver import *
from components.models import *
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class TestHomePage(StaticLiveServerTestCase):
    host = "127.0.0.1"
    port = 8080

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--incognito")
        options.add_argument("--window-size=1920,1080")
        cls.driver = webdriver.Chrome("chromedriver.exe", options=options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()


    def test_home(self):
        self.driver.get(self.live_server_url)
        self.assertEqual(self.driver.current_url, "http://127.0.0.1:8080/")


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

    def test_home_read_more_redirect(self):
        self.driver.get(self.live_server_url)
        self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div/a").click()
        self.assertEqual(self.driver.current_url, "https://github.com/spe-uob/2022-WaterTreatmentDigitalTwin")

    def test_footer_company(self):
        self.driver.get(self.live_server_url)
        parentWindow = self.driver.current_window_handle
        self.clickAboutUs(parentWindow)
        self.clickOurServices(parentWindow)
        self.clickPrivacyPolicy(parentWindow)
        self.clickProgram(parentWindow)

    def clickAboutUs(self, parentWindow):
        element = self.driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[1]/ul/li[1]/a")
        self.newPage(parentWindow, element)
        self.assertEqual(self.driver.current_url, "https://www.nijhuisindustries.com/uk/about")
        self.backToHome(parentWindow)

    def clickOurServices(self, parentWindow):
        element = self.driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[1]/ul/li[2]/a")
        self.newPage(parentWindow, element)
        self.assertEqual(self.driver.current_url, "https://www.nijhuisindustries.com/uk/service")
        self.backToHome(parentWindow)

    def clickPrivacyPolicy(self, parentWindow):
        element = self.driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[1]/ul/li[3]/a")
        self.newPage(parentWindow, element)
        self.assertEqual(self.driver.current_url, "https://www.nijhuisindustries.com/uk/privacy")
        self.backToHome(parentWindow)
        
    def clickProgram(self, parentWindow):
        element = self.driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[1]/ul/li[4]/a")
        self.newPage(parentWindow, element)
        self.assertEqual(self.driver.current_url, "https://www.nijhuisindustries.com/uk")
        self.backToHome(parentWindow)

    def test_footer_help(self):
        self.driver.get(self.live_server_url)
        parentWindow = self.driver.current_window_handle
        self.clickNews(parentWindow)
        self.clickSolutions(parentWindow)
        self.clickContact(parentWindow)
        self.clickJoinUs(parentWindow)

    def clickNews(self, parentWindow):
        element = self.driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[2]/ul/li[1]/a")
        self.newPage(parentWindow, element)
        self.assertEqual(self.driver.current_url, "https://www.nijhuisindustries.com/uk/news")
        self.backToHome(parentWindow)

    def clickSolutions(self, parentWindow):
        element = self.driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[2]/ul/li[2]/a")
        self.newPage(parentWindow, element)
        self.assertEqual(self.driver.current_url, "https://www.nijhuisindustries.com/uk/solutions")
        self.backToHome(parentWindow)

    def clickContact(self, parentWindow):
        element = self.driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[2]/ul/li[3]/a")
        self.newPage(parentWindow, element)
        self.assertEqual(self.driver.current_url, "https://www.nijhuisindustries.com/uk/contact")
        self.backToHome(parentWindow)

    def clickJoinUs(self, parentWindow):
        element = self.driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[2]/ul/li[4]/a")
        self.newPage(parentWindow, element)
        self.assertEqual(self.driver.current_url, "https://www.nijhuisindustries.com/uk/careers")
        self.backToHome(parentWindow)

    def newPage(self, parentWindow, element):
        self.assertEqual(len(self.driver.window_handles), 1)
        self.driver.execute_script("arguments[0].click();", element)
        self.assertEqual(len(self.driver.window_handles), 2)
        for handle in self.driver.window_handles:
            if handle != parentWindow:
                self.driver.switch_to.window(handle)

    def backToHome(self, parentWindow):
        self.driver.close()
        self.driver.switch_to.window(parentWindow)
        self.assertEqual(self.driver.current_url, "http://127.0.0.1:8080/")

    def test_footer_social(self):
        self.driver.get(self.live_server_url)
        parentWindow = self.driver.current_window_handle
        self.clickFacebook(parentWindow)
        self.clickTwitter(parentWindow)
        # Can't test LinkedIn and Youtube due to annoying login and cookie consent urls
        self.clickGithub(parentWindow)

    def clickFacebook(self, parentWindow):
        element = self.driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[3]/div/a[1]")
        self.newPage(parentWindow, element)
        self.assertEqual(self.driver.current_url, "https://www.facebook.com/nijhuisindustries")
        self.backToHome(parentWindow)

    def clickTwitter(self, parentWindow):
        element = self.driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[3]/div/a[2]")
        self.newPage(parentWindow, element)
        self.assertEqual(self.driver.current_url, "https://twitter.com/NijhuisInd")
        self.backToHome(parentWindow)

    def clickGithub(self, parentWindow):
        element = self.driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[3]/div/a[5]")
        self.newPage(parentWindow, element)
        self.assertEqual(self.driver.current_url, "https://github.com/spe-uob/2022-WaterTreatmentDigitalTwin")
        self.backToHome(parentWindow)

    def testForms(self):
        self.driver.get(self.live_server_url + "/input-form/")
        tank0 = self.driver.find_element(By.ID, "id_tank0")
        tank1 = self.driver.find_element(By.ID, "id_tank1")
        tank2 = self.driver.find_element(By.ID, "id_tank2")
        tank3 = self.driver.find_element(By.ID, "id_tank3")
        average_flow = self.driver.find_element(By.ID, "id_average_flow")
        average_tss = self.driver.find_element(By.ID, "id_average_tss")
        sim_length = self.driver.find_element(By.ID, "id_sim_length")
        testing = self.driver.find_element(By.ID, "id_testing")
        submit = self.driver.find_element(By.ID, "submit_button")

        tank0.send_keys(1)
        tank1.send_keys(1)
        tank2.send_keys(1)
        tank3.send_keys(1)
        average_flow.send_keys(0.2)
        average_tss.send_keys(252)
        sim_length.send_keys(20)
        testing.send_keys("off")
        submit.click()

        self.assertEqual(self.driver.current_url, "http://127.0.0.1:8080/simulation/")
        self.driver.find_element(By.ID,"change-to-graph").click()
        self.assertEqual(self.driver.current_url, "http://127.0.0.1:8080/graph/")
        self.driver.find_element(By.ID,"change-to-simulation").click()
        self.assertEqual(self.driver.current_url, "http://127.0.0.1:8080/simulation/")

""" 
TODO: write tests for inputting forms, clicking submit then, changing from simulation to graphs 
"""