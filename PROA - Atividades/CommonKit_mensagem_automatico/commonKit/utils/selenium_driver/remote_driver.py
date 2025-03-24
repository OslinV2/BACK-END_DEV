"""Este arquivo contém a definição de uma classe para manipulação do Selenium."""
import os

from selenium import webdriver


class SeleniumDriver:
    """
    Uma classe para manipulação do Selenium.

    Esta classe permite criar uma instância do WebDriver do Selenium para interagir com navegadores web.

    Attributes:
        download_directory_path (str): O caminho para o diretório de download. Se não fornecido,
            tenta recuperá-lo da variável de ambiente DOWNLOAD_DIRECTORY_PATH.
    """

    def __init__(self, download_directory_path: str="", local: bool=True) -> None:
        """
        Inicializa uma nova instância do SeleniumDriver.

        Args:
            download_directory_path (str, opcional): O caminho para o diretório de download. Se não fornecido,
                tenta recuperá-lo da variável de ambiente DOWNLOAD_DIRECTORY_PATH.
        """
        self.download_directory_path = download_directory_path
        self.local = local
        if not download_directory_path:
            self.download_directory_path = os.environ.get("DOWNLOAD_DIRECTORY_PATH", "")

    def create(self) -> webdriver.Remote:
        """
        Cria e retorna uma instância do WebDriver do Selenium configurada para downloads.

        Returns:
            webdriver.Remote: Uma instância do WebDriver do Selenium configurada para downloads.
        """
        if self.local:
            return self.create_local_driver()

        prefs = {'download.default_directory': self.download_directory_path}

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('ignore-certificate-errors')
        chrome_options.add_experimental_option('prefs', prefs)

        driver = webdriver.Remote(
            command_executor='http://chrome:4444',
            options=chrome_options
        )

        return driver

    def create_local_driver(self) -> webdriver.Chrome:
        """
        Cria e retorna uma instância local do WebDriver do Selenium configurada para downloads.

        Returns:
            webdriver.Remote: Uma instância do WebDriver do Selenium configurada para downloads.
        """

        prefs = {'download.default_directory': self.download_directory_path}

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('ignore-certificate-errors')
        chrome_options.add_experimental_option('prefs', prefs)

        driver = webdriver.Chrome(
            options=chrome_options
        )

        return driver
    