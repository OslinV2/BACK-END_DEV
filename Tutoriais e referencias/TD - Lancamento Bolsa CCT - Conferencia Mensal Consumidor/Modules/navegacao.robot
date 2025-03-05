*** Settings ***
Documentation   Biblioteca responsável por toda navegação comum a todas as páginas do robô

Resource        ${ROOT}/resources/main.resource


*** Keywords ***
Fechar Navegador
  [Documentation]    Keyword que fecha o Browser
  Close All Browsers

Abrir Navegador
    [Documentation]     Abre o navegador maximizado, e tem a pasta de download definida.
    [Arguments]  ${URL}  ${download_dir}=${None}
    ${prefs}    Create Dictionary
    ...    plugins.always_open_pdf_externally=${True}
    ${options}    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()  sys
    Set Download Directory    ${download_dir}
    Call Method    ${options}    add_experimental_option  prefs  ${prefs}
    Call Method    ${options}    add_argument  start-maximized
    Call Method    ${options}    add_argument  disable-web-security
    Call Method    ${options}    add_argument  disable-notifications
    Call Method    ${options}    add_argument  disable-logging
    # Call Method    ${options}    add_argument  incognito
    Open Available Browser    url=${URL}    options=${options}
    Set Selenium Timeout  ${DEFAULT_SELENIUM_TIMEOUT}
    RETURN    ${TRUE}