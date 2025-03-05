from pathlib import Path
import variables

def browser_path():
    if not Path(variables.BROWSER_DIRECTORY).is_file():
        raise ValueError(f'O Browser para a versão especificada no '
                         f'projeto não está no local {variables.BROWSER_DIRECTORY}')
    return variables.BROWSER_DIRECTORY


def chromedriver_path():
    if not Path(variables.CHROMEDRIVER_DIRECTORY).is_file():
        raise ValueError(f'O chromedriver.exe para a versão especificada no '
                         f'projeto não está no local {variables.CHROMEDRIVER_DIRECTORY}')
    return variables.CHROMEDRIVER_DIRECTORY
