*** Settings ***
Documentation   Template robot main suite.
Resource        ${ROOT}/resources/main.resource

Suite Setup    Iniciando Processo Conferencia Mensal CCT
Suite Teardown    Finalizando Processo Conferencia Mensal CCT


*** Variables ***
${status}    FAIL

*** Tasks ***

Recuperar Registro Pendente
    [Documentation]    Task responsável por fazer a conexão com o banco de dados local,
    ...                verificar se existe algum registro a ser processado e retorná-lo.
    Set Suite Variable    ${vazio}    ${FALSE}
    ${status}    ${retorno_registro}    Run Keyword And Ignore Error    Recupera Registro Pendente
    IF    "${status}" == "PASS"
        IF    ${retorno_registro[0]}
            Log Info   Registro recuperado: ${retorno_registro[1]}   console=True  traceId=${TRACEID}
            Set Suite Variable    ${registro}    ${retorno_registro[1]}
            Log    ${registro}
            ${status_navegador}    ${retorno_navegacao}    Run Keyword And Ignore Error    Navegar Prime    ${URLS.secao_contratos}     ${PRIME.select_estabelecimento}
        ELSE
            Log    ${retorno_registro[1]}
            Log Info   Erro ao recuperar registro    console=True  traceId=${TRACEID}  mensagem=${retorno_registro[1]}   erro=Geral
            Set Suite Variable    ${vazio}    ${TRUE}
            Fechar Navegador
        END
    ELSE  
        Log Error   Erro ao recuperar status dos documentos no banco local   console=True  traceId=${TRACEID}  mensagem=${retorno_registro[1]}   erro=Geral    motivo_erro=${retorno_registro[1]}     alerta=${TRUE}     monitor=${TRUE}
    END

Abrir Browser
    [Documentation]    Task responsável por abrir o browser e acessar o sistema Prime
    Log Info   Iniciando sistema Prime  console=True  traceId=${TRACEID}
    Log    ${URL_PRIME}
    ${status}    ${retorno_browser}    Run Keyword And Ignore Error    Abrir Navegador    ${URL_PRIME}    ${DOWNLOAD_DIRECTORY}
    IF    "${status}" == "PASS"
        Log Info   Sistema Prime iniciado   console=True  traceId=${TRACEID}  sucesso=Finalizado
    ELSE  
        Log Error   Erro ao abrir browser   console=True  traceId=${TRACEID}  mensagem=${retorno_browser}   erro=Geral
    END

Preencher Login
    [Documentation]    Task responsável por preencher dados do login - Prime
    Log Info   Iniciando o preenchimento do login   console=True  traceId=${TRACEID}
    ${status}    ${retorno_login}    Run Keyword And Ignore Error    Preencher Campos Login    ${USER_PRIME}    ${PWD_PRIME}
    IF    "${status}" == "PASS"
        IF    ${retorno_login[0]}
            Log Info   ${retorno_login[1]}   console=True  traceId=${TRACEID}
        ELSE  
            Log Error   Erro nas credenciais login Prime  console=True  traceId=${TRACEID}  mensagem=${retorno_login[1]}    erro=Geral
        END
    ELSE  
        Log Error   Erro ao preencher dados login   console=True  traceId=${TRACEID}  mensagem=${retorno_login}    erro=Geral
    END

Recuperar Token Login 
    [Documentation]    Efetua a captura do email enviado pelo sistema Prime e extrai o código TOKEN
    Log Info   Iniciando a captura do token no email   console=True  traceId=${TRACEID}
    ${status}    ${retorno_token}    Run Keyword And Ignore Error    Captura Token Login
    IF    "${status}" == "PASS"
        IF    ${retorno_token[0]}
            Set Suite Variable    ${token}    ${retorno_token[1]}
            Log Info   Token recuperado   console=True  traceId=${TRACEID}
        ELSE
            Log Error   Erro ao extrair o token do body   console=True  traceId=${TRACEID} mensagem=${retorno_token[1]}    erro=Geral
        END
    ELSE
        Log Error   Erro ao recuperar o token   console=True  traceId=${TRACEID}  mensagem=${retorno_token}    erro=Geral
    END

Entrar Sistema Prime
    [Documentation]    Task responsável por preencher o token e acessar o sistema Prime
    Log Info   Iniciando o preenchimento do token no sistema Prime   console=True  traceId=${TRACEID}
    ${status}    ${retorno_token_login}    Run Keyword And Ignore Error    Preencher Token    ${token}
    IF    "${status}" == "PASS"
        IF    ${retorno_token_login[0]}
            Log Info   ${retorno_token_login[1]}   console=True  traceId=${TRACEID}
        ELSE  
            Log Error   Erro no código de acesso  console=True  traceId=${TRACEID}  mensagem=${retorno_token_login[1]}    erro=Geral
        END
    ELSE  
        Log Error   Erro ao preencher o TOKEN   console=True  traceId=${TRACEID}  mensagem=${retorno_token_login}    erro=Geral
    END

Verificar Contrato
    [Documentation]    Task responsável por Verificar o Contrato Ativo do aluno
    ${status}    ${retorno_verificacao}    Run Keyword And Ignore Error    Pesquisar Contrato    ${registro}
    Set Suite Variable    ${status_verificacao}    ${retorno_verificacao[1]}
    IF    "${status}" == "PASS"
        IF    ${retorno_verificacao[0]}
            Log Info   Efetuado a verificação do contrato   console=True  traceId=${TRACEID}
        ELSE
            Log Error   Erro ao efetuar a verificação do contrato  console=True  traceId=${TRACEID}    motivo_erro=${retorno_verificacao}    alerta=${TRUE}     monitor=${TRUE}
        END
    ELSE
        Log Error    Erro ao efetuar a verificação do contrato   console=True  traceId=${TRACEID}    motivo_erro=${retorno_verificacao}    alerta=${TRUE}     monitor=${TRUE}
    END

Modificar Contrato
    [Documentation]    Task responsável por excluir ou alterar bolsa do aluno no contrato
    ${status}    ${retorno_contrato}    Run Keyword And Ignore Error    Modificar contrato    ${registro}    ${status_verificacao}
    Set Suite Variable    ${status_contrato}    ${retorno_contrato} 
    IF    "${status}" == "PASS" and ${retorno_contrato[0]}
        Empty Directory     ${DOWNLOAD_DIRECTORY}
        Log Info   Efetuado a definição do contrato   console=True  traceId=${TRACEID}
    ELSE
        Log Error    Erro ao definir contrato   console=True  traceId=${TRACEID}    motivo_erro=${retorno_contrato}    alerta=${TRUE}     monitor=${TRUE}
    END

Modificar Aluno
    [Documentation]    Task responsável por excluir ou alterar bolsa do aluno no perfil do aluno
    ${status}    ${retorno_aluno}    Run Keyword And Ignore Error    Modificar Perfil Aluno    ${registro}
    Set Suite Variable    ${status_contrato}     ${retorno_aluno}
    IF    "${status}" == "PASS" and ${retorno_aluno[0]}
        Empty Directory     ${DOWNLOAD_DIRECTORY}
        Log Info   Efetuado a definição do contrato   console=True  traceId=${TRACEID}
    ELSE
        Log Error    Erro ao definir contrato   console=True  traceId=${TRACEID}    motivo_erro=${retorno_aluno}    alerta=${TRUE}     monitor=${TRUE}
    END

Atualizar Registro Bd
    [Documentation]    Task responsável atualizar o BD
    ${status}    ${retorno_bd}    Run Keyword And Ignore Error   Atualizar BD    ${registro}    ${status_contrato}
    Set Suite Variable    ${registro}     ${EMPTY}
    IF    "${status}" == "PASS" and ${retorno_bd[0]}
        Log Info   Atualizado registro   console=True  traceId=${TRACEID}
    ELSE IF    "${status}" == "PASS" and ${retorno_bd[0]}
        Log Info   Erro ao atualizar registro: ${retorno_bd[1]}  console=True  traceId=${TRACEID}       motivo_erro=${retorno_bd}     alerta=${TRUE}     monitor=${TRUE}
    ELSE
        Log Error    Erro ao atualizar registro   console=True  traceId=${TRACEID}       motivo_erro=${retorno_bd}     alerta=${TRUE}     monitor=${TRUE}
    END

Finalizacao
    [Documentation]    Task de finalização do robô
    Log Info   Finalizando processo   console=True  traceId=${TRACEID}
