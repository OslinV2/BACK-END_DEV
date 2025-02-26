*** Settings ***
Documentation   Keywords de setup e teardown
Resource    ${ROOT}/resources/main.resource

*** Keywords ***
Iniciando Processo Conferencia Mensal CCT
    [Documentation]     Abre o navegador maximizado, e tem a pasta de download definida.
    ${start_time}=    Get Current Date   result_format=epoch
    Set Suite Variable    ${tempo_inicio}    ${start_time}
    Log Info   Sistema Prime iniciado   console=True  traceId=${TRACEID}  start_time=${start_time}
    Open Connections
    Create Directory    ${DOWNLOAD_DIRECTORY}
    Empty Directory    ${DOWNLOAD_DIRECTORY}

Finalizando Processo Conferencia Mensal CCT
    [Documentation]     Abre o navegador maximizado, e tem a pasta de download definida.
    ${end_time}=    Get Current Date   result_format=epoch
    Log Info   Sistema Prime finalizado   console=True  traceId=${TRACEID}  end_time=${end_time}
    ${diff_execucao}    Calcular Execucao    ${tempo_inicio}    ${end_time}
    Log Info   Execucao   console=True  traceId=${TRACEID}  diff_exec=${diff_execucao}
    Fechar Navegador


