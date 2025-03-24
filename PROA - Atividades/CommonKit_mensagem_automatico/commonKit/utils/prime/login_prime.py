import time as t

from os import environ
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException, WebDriverException

from ..criptador import decypher
from ..email_handler import EmailHandler
from ..microsoft.msal_auth import MSALAuth



def login(driver:webdriver.Chrome) -> str:
    """
    Realiza o login no Prime.

    Essa função recebe como parâmetro o driver do Chrome e realiza o login no Prime utilizando as credenciais de usuário e senha.

    Parâmetros:
    - driver (webdriver.Chrome): O driver do Chrome utilizado para a automação.

    Retorna:
    - str: Uma string indicando o resultado do login. Pode ser "OK" em caso de sucesso ou "Falha" em caso de falha.

    Raises:
    - WebDriverException: Exceção lançada em caso de erro no WebDriver.

    """
    try:
        user = str(decypher(environ.get('PRIME_LOGIN')))
        password = str(decypher(environ.get('PRIME_PASSWORD')))
        driver.maximize_window()
        driver.find_element(By.XPATH, "//input[@type='text'][@name='USUARIO']").send_keys(user)
        driver.find_element(By.XPATH, "//input[@type='password']").send_keys(password)
        driver.find_element(By.XPATH, "//img[@name='login_botao']").click()
        t.sleep(10)
        codigo = EmailHandler(MSALAuth()).get_code()
        driver.find_element(By.XPATH, "//input[@name='TOKEN']").send_keys(codigo)
        t.sleep(1)       # aguardando 1 segundo para o site carregar
        driver.find_element(By.XPATH, "//img[@name='login_botao']").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//img[@src='BarraSup05.jpg']")))

        if existe_alerta(driver):
            aceita_alerta(driver)
            return "Falha"
        return "OK"

    except WebDriverException as e:
        print(e)
        driver.quit()
    return "Falha"

def existe_alerta(driver: webdriver.Chrome) -> bool:
    """
    Verifica se existe um alerta presente na página.

    Args:
        driver (webdriver.Chrome): O objeto do driver do Chrome.

    Returns:
        bool: True se um alerta estiver presente, False caso contrário.
    """
    try:
        alert = Alert(driver)
        if alert.text is not None:
            return True
        return False
    except NoAlertPresentException:
        print("sem alerta")
        return False

def aceita_alerta(driver:webdriver.Chrome) -> None:
    """
    Aceita o diálogo de alerta na página da web.

    Args:
        driver (webdriver.Chrome): A instância do WebDriver do Chrome.
    
    Returns:
        None
    """
    alert = Alert(driver)
    alert.accept()
