from selenium.webdriver.common.by import By
from selenium import webdriver

def login():
    driver = webdriver.Chrome()
    driver.get('https://www.imdb.com/pt/?ref_=nv_home')   
    btn01 = driver.find_element(By.XPATH, "//a[@class='ipc-btn ipc-btn--single-padding ipc-btn--center-align-content ipc-btn--default-height ipc-btn--core-baseAlt ipc-btn--theme-baseAlt ipc-btn--button-radius ipc-btn--on-textPrimary ipc-text-button imdb-header__signin-text']").click()
    btn02 = driver.find_element(By.XPATH, "//span[@class='auth-sprite google-logo  retina ']").click()
    
login()
def extracao():
    
    