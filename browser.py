from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time






service = Service()
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://payme.uz/login')
phone_number = ''                                             #НОМЕР ТЕЛЕФОНА
password = ''												  #ПАРОЛЬ










############## Вписываем данные аккаунта и логинимся ################


def run_browser():
	try:
		time.sleep(1)
		elem  = driver.find_element(By.ID,  'login')
		elem.send_keys(phone_number + Keys.RETURN)
		elem = driver.find_element(By.ID, 'password')
		elem.send_keys(password + Keys.RETURN)

		btn = driver.find_element(By.ID,  'login-submit')
		driver.execute_script("arguments[0].click();", btn)

		code = input('SMS CODE: ')

		elem = driver.find_element(By.ID, 'code')
		elem.send_keys(code + Keys.RETURN)


		btn = driver.find_element(By.ID,  'login-submit')
		driver.execute_script("arguments[0].click();", btn)

		btn = driver.find_element(By.XPATH, "//span[text() = 'Мониторинг платежей']")
		driver.execute_script("arguments[0].click();", btn)

		
		time.sleep(3)

	except Exception as e:
		run_browser()
		print(e)

	while True:
		driver.refresh()
		time.sleep(60)




#####################################################################