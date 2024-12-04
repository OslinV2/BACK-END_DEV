import requests
import shutil
from win32com.client import Dispatch
from zipfile import ZipFile
import glob
import os

caminho = f"{os.environ['userprofile']}\\Desktop\\WebDriver"

def get_version_via_com(filename):
    parser = Dispatch("Scripting.FileSystemObject")
    try:
        version = parser.GetFileVersion(filename)
    except Exception:
        return None
    return version

def update():
    os.remove(fr'{caminho}\chromedriver.exe')
    baixado = False
    versao = get_version_via_com('C:\Program Files\Google\Chrome\Application\chrome.exe')
    versoes = requests.get('https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json').json()
    while not baixado:
        for i in versoes['versions']:
            if i['version'] == versao:
                binario = requests.get(i['downloads']['chromedriver'][4]['url'], stream=True)
                with open(rf'{caminho}\\chromedriver.zip', 'wb') as driver:
                    shutil.copyfileobj(binario.raw, driver)
                baixado = True
                break
        print('Versão não encontrada, realizando downgrade')
        print(versao)
        versaoADiminuir = versao.split('.')
        print(versaoADiminuir)
        versaoADiminuir[-1] = int(versaoADiminuir[-1])
        versaoADiminuir[-1] -= 1
        versaoADiminuir[-1] = str(versaoADiminuir[-1])
        versao = ".".join(versaoADiminuir)
        
    with ZipFile(rf'{caminho}\\chromedriver.zip', 'r') as zipado:
        zipado.extract(rf'chromedriver-win64/chromedriver.exe', rf'{caminho}\\driver')
    zipado.close()
    driverFinal = glob.glob(rf'{caminho}\\driver\**\*.exe')
    os.rename(driverFinal[-1], rf'{caminho}\\chromedriver.exe')
    os.remove(rf'{caminho}\\chromedriver.zip')
    shutil.rmtree(rf'{caminho}\\driver')

    print("Driver atualizado com sucesso")

if __name__ == '__main__':
    update()