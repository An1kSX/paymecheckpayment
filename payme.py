from browser import driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import sqlite3
import time




try:
	db = sqlite3.connect('database.db', check_same_thread = False)
	sql = db.cursor()

except Exception as e:
	print(f'Error: {e}')



def new_user(user_id):
	try:
		sql.execute('SELECT * FROM users WHERE id = ?', (user_id, ))
		_user = sql.fetchone()
		if _user is None:
			sql.execute('INSERT INTO users VALUES (?, ?)', (user_id, None))
			db.commit()

	except Exception as e:
		print(e)


def check_payment(user_id, date):
	try:
		sql.execute('SELECT * FROM users WHERE id = ? and date_ = ?', (user_id, date))
		return sql.fetchone()

	except Exception as e:
		print(e)
		return None


def set_payment_date(user_id, date):
	try:
		sql.execute('UPDATE users SET date_ = ? WHERE id = ?', (date, user_id))
		db.commit()

	except Exception as e:
		print(e)



def payme(user_id, money):
	new_user(user_id)
################# Переходим в мониторинг платежей ###################
	try:
		driver.get('https://payme.uz/cabinet/history')

	except Exception as e:
		print(e)
		return -1

#####################################################################


############ Поступления за последние два дня #######################

	try:
		yesterday = datetime.now() - timedelta(1)
		yesterday = yesterday.strftime('%d.%m.%Y')

		WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text() = 'Фильтр']"))).click()

		WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, 'start'))).clear()
		driver.find_element(By.ID, 'start').send_keys(yesterday + Keys.RETURN)


		WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'operation'))).click()

		WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//option[text() = 'Поступления']"))).click()

		WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text() = 'Применить']"))).click()

	except Exception as e:
		print(e)
		return -1


#####################################################################


############# Проверяем наличие нужного поступления #################

	try:
		td = datetime.now()
		money = '{0:,}'.format(money).replace(',', ' ')
		time.sleep(5)
		for i in range(31):
			minutes = td + timedelta(minutes = -i)
			minutes = minutes.strftime("%H:%M")
			PATH = f"//span[text() = '{minutes}']/../..//span[text() = '{user_id}']/../../..//span[contains(text(), '{money}')]"

			try:
				driver.find_element(By.XPATH, PATH)
				td += timedelta(minutes = -i)
				td = td.strftime("%d.%m.%Y %H:%M")
				if check_payment(user_id, td) is None:
					set_payment_date(user_id, td)
					return 1

				return 0

			except:
				pass

		return 0

	except Exception as e:
		print(e)
		return -1


#####################################################################