from selenium.webdriver.common.by import By
from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://www.imdb.com/chart/top/?ref_=nv_mv_250')
nomes = driver.find_elements(By.XPATH, '//div[@class="ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-3713cfda-2 fSzZES cli-title with-margin"]')

for nome in nomes:
    print(nome.text)
driver.close()