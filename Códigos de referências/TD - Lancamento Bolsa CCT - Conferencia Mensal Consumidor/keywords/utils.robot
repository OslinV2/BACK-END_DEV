*** Settings ***
Documentation   Keywords auxiliares do processos
Resource        ${ROOT}/resources/main.resource

*** Keywords ***
Preencher Campos Login
    [Documentation]    Realiza o preenchimento dos campos do login
    [Arguments]    ${USER}    ${SENHA}
    ${retorno_status}    Set Variable    ${FALSE}
    Input Text    ${LOGIN.inpt_usuario}    ${USER}
    Input Password    ${LOGIN.inpt_senha}    ${SENHA}
    Execute Javascript    javascript: validaForm();
    ${status_alerta}    ${retorno_alerta}    Run Keyword And Ignore Error    Capturar Mensagem Alerta
    IF   "${status_alerta}" == "PASS"
        Acao Sobre Um Alerta    ACCEPT
        ${mensagem}    Set Variable    ${retorno_alerta}
    ELSE
        Wait Until Element Is Visible    ${LOGIN.input_token}    timeout=20
        ${mensagem}    Set Variable    Preenchimento campos login - sucesso
        ${retorno_status}    Set Variable    ${TRUE}
    END
    RETURN    ${retorno_status}     ${mensagem}

Capturar Mensagem De Um Alerta
    [Documentation]    A keyword deve receber uma string e verificar se existe um alert com a mensagem,
    ...                e retorna true caso o alert exista.
    [Arguments]    ${texto}
    ${status_mensagem_presente}    Run Keyword And Return Status
    ...                            Alert Should Be Present    ${texto}    action=OK
    RETURN    ${status_mensagem_presente}

Capturar Mensagem Alerta
    [Documentation]    A keyword realiza a captura da mensagem do alert
    ${mensagem_alert}    Handle Alert    action=LEAVE    timeout=10 s
    RETURN    ${mensagem_alert}

Acao Sobre Um Alerta
    [Documentation]    A keyword realiza uma ação sobre um alert aberto {ACCEPT, DISMISS, LEAVE}
    [Arguments]    ${acao}
    ${status_alert}    Run Keyword And Return Status    Handle Alert    action=${acao}    timeout=20 s
    RETURN    ${status_alert}

Captura Token Login  
    [Documentation]    Realiza a conexão com a caixa de entrada do email, captura os primeiros emails
    ...                recebidos, encontra aquele que contem o token e extrai o código
    Sleep    3
    ${retorno_token}    Capturar Token Prime
    RETURN    ${retorno_token[0]}   ${retorno_token[1]}

Preencher Token
    [Documentation]    Realiza o preenchimento do campo TOKEN e acessa o sistema Prime
    [Arguments]    ${token}
    ${retorno_status}    Set Variable    ${FALSE}
    Input Text    ${LOGIN.input_token}    ${token}
    Execute Javascript    javascript: validaForm();
    ${status_alerta}    ${retorno_alerta}    Run Keyword And Ignore Error    Capturar Mensagem Alerta
    IF   "${status_alerta}" == "PASS"
        Acao Sobre Um Alerta    ACCEPT
        ${mensagem}    Set Variable    ${retorno_alerta}
    ELSE
        Wait Until Element Is Visible    ${LOGIN.btn_menu}    timeout=20
        ${mensagem}    Set Variable    Acesso ao sistema Prime - sucesso
        ${retorno_status}    Set Variable    ${TRUE}
    END
    RETURN    ${retorno_status}     ${mensagem}

Navegar Prime
    [Documentation]    Keyword efetua o acesso à uma seção do Prime
    [Arguments]    ${url}   ${element}
    Go To    ${url}
    Wait Until Element Is Visible    ${element}    timeout=50
    RETURN    ${TRUE}

Pesquisar Contrato
    [Documentation]    Keyword efetua a pesquisa de um contrato
    [Arguments]    ${registro}

    Go To    ${URLS.secao_contratos}    
    Wait Until Element Is Visible    ${PRIME.select_estabelecimento}    timeout=50
    Input Text    ${PRIME.input_matricula}    ${registro}[Matrícula]
    Select From List By Label     ${PRIME.select_tipo_curso}    Cursos de Graduação Presencial
    Click Element    ${PRIME.btn_localizar}
    Sleep   3
    ${title_window}=        Get Window Titles
    Sleep    1
    Run Keyword And Ignore Error    Switch Window       title=${title_window}[1] 
    Wait Until Element Is Visible 	 locator=${PRIME.btn_incluir_contrato} 	 timeout=60
    ${valida_tela}=     Run Keyword And Return Status   Page Should Contain Element    ${PRIME.col_contratos}
    Sleep    10s
    IF  "${valida_tela}" == "True"
        Close Window
        Switch Window       title=${title_window}[0]
        Sleep   2
        Click Element    ${PRIME.radio_formato}
        Click Element    ${PRIME.btn_localizar}
        Empty Directory     ${DOWNLOAD_DIRECTORY}
        ${download_feito}    Run Keyword And Return Status
        ...    Wait Until Created    ${DOWNLOAD_DIRECTORY}/relacao_contratos.xls    timeout=${180}
        Sleep   2
        RETURN   ${TRUE}    Contrato baixado
    ELSE
        Log Info    Aluno Sem Contrato
        Close Window
        Switch Window       title=${title_window}[0]
        RETURN   ${TRUE}    Sem Contrato
    END    

Modificar Contrato
    [Documentation]    Keyword efetua a verificação e modificação de um contrato
    [Arguments]    ${registro}    ${status_verificacao}

    TRY
        ${retorno_status}    Set Variable    ${FALSE}
        ${retorno_contrato}    Definir Contrato    ${registro}    ${status_verificacao}
        IF     ${retorno_contrato[0]}
            Go To    ${URLS.secao_contratos}
            Wait Until Element Is Visible 	 ${PRIME.select_estabelecimento} 	 timeout=50
            # Input Text     ${PRIME.input_contrato}    	5030792
            Input Text     ${PRIME.input_contrato}    ${retorno_contrato[1]}
            Click Element    ${PRIME.btn_localizar}
            Sleep     5s
            ${title_window}=        Get Window Titles
            Run Keyword And Ignore Error    Switch Window       title=${title_window}[1]
            Run Keyword And Return Status    Wait Until Element Is Visible 	 locator=${PRIME.btn_contrato} 	 timeout=60
            ${valida_tela}=     Run Keyword And Return Status   Page Should Contain Element    ${PRIME.btn_contrato}

            IF  "${valida_tela}" == "True"
                IF     "${registro['Alteração']}" == "Próximo Semestre"
                    Close Window
                    Switch Window       title=${title_window}[0]
                    RETURN   ${TRUE}    Contrato modificado com sucesso
                END
                Click Element    ${PRIME.btn_contrato_especifico}
                IF     "${retorno_contrato[2]}" == "Confirmado"
                    Wait Until Element Is Visible 	 ${PRIME.btn_incluir_bolsa_contrato_confirmado} 	 timeout=50
                    ${html_content}=    Get Source
                    # Verifica se a bolsa é valida
                    ${retorno_verificacao}    Verificar Existencia Bolsa Contrato Confirmado    ${html_content}    ${registro}[Tipo Bolsa]
                    IF    ${retorno_verificacao[0]}
                        ${periodo_contrato}=    Get Text    ${PRIME.td_vigencia_contrato_confirmado}
                        @{datas_contrato}=     Split String    ${periodo_contrato}    ${SPACE}a${SPACE}
                        # Define datas novas do contrato
                        ${datas_lancamento}=     Get Datas Alteracao Contrato    ${retorno_contrato[3]}    ${datas_contrato[0]}     ${datas_contrato[1]}
                        IF     ${datas_lancamento[0]} 
                            # Pega o valor bruto da mensaldiade do aluno pra comparar posteriormente
                            ${retorno_mensalidade}    Get Valor Mensalidade    ${html_content}
                            IF     ${retorno_mensalidade[0]}
                                Click Element    ${PRIME.btn_incluir_bolsa_contrato_confirmado}
                                Wait Until Element Is Visible    ${PRIME.input_protocolo_contrato_confirmado}    timeout=50
                                Select From List By Label     ${PRIME.select_tipo_bolsa_contrato_confirmado}    ${registro}[Tipo Bolsa]
                                IF     "${registro['Tipo de Alteração']}" == "Exclusão"
                                    Input Text    ${PRIME.input_percentual_contrato_confirmado}    -${retorno_verificacao[2]}
                                    Input Text    ${PRIME.input_data_de_contrato_confirmado}    ${datas_lancamento[1]}
                                    Input Text    ${PRIME.input_data_ate_contrato_confirmado}    ${datas_lancamento[2]}
                                    IF      "${datas_lancamento[3]}" == "Contrato"
                                        Click Element    ${PRIME.btn_radio_tipo_contrato_contrato_confirmado}
                                    ELSE
                                        Click Element    ${PRIME.btn_radio_tipo_periodo_contrato_confirmado}
                                    END
                                    Click Element     ${PRIME.btn_pre_visualizar_contrato_confirmado}
                                    Wait Until Element Is Visible    ${PRIME.th_desconto_pre_visualizado_contrato_confirmado}    timeout=80
                                    ${html_content}=    Get Source
                                    ${retorno_comparacao}=     Compara Saldo Final Bolsa    ${html_content}    ${retorno_mensalidade[1]}
                                    IF     ${retorno_comparacao[0]}
                                        Sleep    12
                                        #Click Element     ${PRIME.btn_gravar_contrato_confirmado}
                                        Go Back
                                        Go Back
                                        Wait Until Element Is Visible    ${PRIME.td_vigencia_contrato_confirmado}    timeout=50
                                        Close Window
                                        Switch Window       title=${title_window}[0]
                                        RETURN   ${TRUE}    Contrato modificado com sucesso
                                    ELSE
                                        Close Window
                                        Switch Window       title=${title_window}[0]
                                        RETURN      ${FALSE}    Valor final da bolsa não confere em Contratos
                                    END
                                ELSE IF    "${registro['Tipo de Alteração']}" == "Alteração"
                                    Input Text    ${PRIME.input_percentual_contrato_confirmado}    -${retorno_verificacao[2]}
                                    Input Text    ${PRIME.input_data_de_contrato_confirmado}    ${datas_lancamento[1]}
                                    Input Text    ${PRIME.input_data_ate_contrato_confirmado}    ${datas_lancamento[2]}
                                    IF      "${datas_lancamento[3]}" == "Contrato"
                                        Click Element    ${PRIME.btn_radio_tipo_contrato_contrato_confirmado}
                                    ELSE
                                        Click Element    ${PRIME.btn_radio_tipo_periodo_contrato_confirmado}
                                    END
                                    Click Element     ${PRIME.btn_pre_visualizar_contrato_confirmado}
                                    Wait Until Element Is Visible    ${PRIME.th_desconto_pre_visualizado_contrato_confirmado}    timeout=80
                                    ${html_content}=    Get Source
                                    ${retorno_comparacao}=     Compara Saldo Final Bolsa    ${html_content}    ${retorno_mensalidade[1]}
                                    IF     ${retorno_comparacao[0]}
                                        Sleep    12
                                        #Click Element     ${PRIME.btn_gravar_contrato_confirmado}
                                        Go Back
                                        Go Back
                                        Sleep     5s
                                        ${status_alerta}    ${retorno_alerta}    Run Keyword And Ignore Error    Capturar Mensagem Alerta
                                        IF   "${status_alerta}" == "PASS"
                                            Acao Sobre Um Alerta    ACCEPT
                                        END
                                        Wait Until Element Is Visible    ${PRIME.td_vigencia_contrato_confirmado}    timeout=50
                                        Click Element    ${PRIME.btn_incluir_bolsa_contrato_confirmado}
                                        Wait Until Element Is Visible    ${PRIME.input_protocolo_contrato_confirmado}    timeout=50
                                        Select From List By Label     ${PRIME.select_tipo_bolsa_contrato_confirmado}    ${registro}[Tipo Bolsa]
                                        Input Text    ${PRIME.input_percentual_contrato_confirmado}    ${registro['Nova Porcentagem Bolsa']}
                                        Input Text    ${PRIME.input_data_de_contrato_confirmado}    ${datas_lancamento[1]}
                                        Input Text    ${PRIME.input_data_ate_contrato_confirmado}    ${datas_lancamento[2]}
                                        IF      "${datas_lancamento[3]}" == "Contrato"
                                            Click Element    ${PRIME.btn_radio_tipo_contrato_contrato_confirmado}
                                        ELSE
                                            Click Element    ${PRIME.btn_radio_tipo_periodo_contrato_confirmado}
                                        END
                                        Click Element     ${PRIME.btn_pre_visualizar_contrato_confirmado}
                                        Wait Until Element Is Visible    ${PRIME.th_desconto_pre_visualizado_contrato_confirmado}    timeout=80
                                        Sleep    20
                                        #Click Element     ${PRIME.btn_gravar_contrato_confirmado}
                                        Go Back
                                        Go Back
                                        Close Window
                                        Switch Window       title=${title_window}[0]
                                        RETURN   ${TRUE}    Contrato modificado com sucesso
                                    ELSE
                                        Close Window
                                        Switch Window       title=${title_window}[0]
                                        RETURN      ${FALSE}    Valor final da bolsa não confere em Contratos
                                    END
                                END
                            ELSE
                                Close Window
                                Switch Window       title=${title_window}[0]
                                RETURN      ${FALSE}    Erro ao capturar valor da mensalidade em Contratos
                            END
                        ELSE
                            Close Window
                            Switch Window       title=${title_window}[0]
                            RETURN      ${FALSE}    Erro ao definir validade em Contratos 
                        END
                    ELSE
                        Close Window
                        Switch Window       title=${title_window}[0]
                        RETURN      ${FALSE}    Mais de uma bolsa encontrada em Contratos
                    END
                ELSE IF     "${retorno_contrato[2]}" == "Aberto"
                    Wait Until Element Is Visible 	 ${PRIME.select_tipo_calculo_contrato_aberto} 	 timeout=50
                    ${label_desconto}=    Get Selected List Label    ${PRIME.select_tipo_desconto_contrato_aberto}
                    FOR    ${i}    IN RANGE    0    6
                        ${index_desconto}    Convert To String    ${i}
                        ${select_tipo_desconto}=     Replace String     ${PRIME.select_tipo_desconto_contrato_aberto_variavel}    {num}    ${index_desconto}   
                        TRY
                            ${label_desconto_variavel}=    Get Selected List Label    ${select_tipo_desconto}
                            IF     "${label_desconto_variavel}" == "${registro['Tipo Bolsa']}"
                                ${index}=    Set Variable    ${index_desconto}
                                Exit For Loop
                            END
                        EXCEPT
                            RETURN      ${FALSE}    Não encontrado bolsa encontrada em Contratos
                        END
                    END
                    IF     "${registro['Tipo de Alteração']}" == "Exclusão"
                        ${btn_exclusao}=     Replace String     ${PRIME.btn_exclusao_contrato_aberto}    {num}    ${index}
                        Click Element    ${btn_exclusao}
                        Click Button    ${PRIME.btn_atualizar_contrato_aberto}
                        Sleep     5s
                        ${status_alerta}    ${retorno_alerta}    Run Keyword And Ignore Error    Capturar Mensagem Alerta
                        IF   "${status_alerta}" == "PASS"
                            Acao Sobre Um Alerta    ACCEPT
                        END
                        ${status}    ${retorno_alerta}    Run Keyword And Ignore Error    Wait Until Element Is Visible 	 ${PRIME.td_erro_salvar_contrato} 	 timeout=10
                        IF  "${status}" == "PASS"
                            ${erro_salvar}=    Get Text    ${PRIME.td_erro_salvar_contrato}
                            Close Window
                            Switch Window       title=${title_window}[0]
                            RETURN      ${FALSE}    Erro ao excluir Contrato
                        END
                        Wait Until Element Is Visible 	 ${PRIME.btn_atualizar_contrato_aberto} 	 timeout=50
                        Close Window
                        Switch Window       title=${title_window}[0]
                        RETURN   ${TRUE}    Contrato modificado
                    ELSE IF    "${registro['Tipo de Alteração']}" == "Alteração"
                        # substituindo valores pelas máscaras
                        ${input_data_de}=     Replace String     ${PRIME.input_data_de_contrato_aberto_variavel}    {num}    ${index}
                        ${input_data_ate}=     Replace String     ${PRIME.input_data_ate_contrato_aberto_variavel}    {num}    ${index}
                        ${select_tipo_calculo}=     Replace String     ${PRIME.select_tipo_calculo_contrato_aberto_variavel}    {num}    ${index}
                        ${input_percentual_desconto}=     Replace String     ${PRIME.input_percentual_desconto_contrato_aberto_variavel}    {num}    ${index}

                        ${data_de_contrato}=     Get Value    ${input_data_de}
                        ${data_ate_contrato}=     Get Value    ${input_data_ate}
                        ${datas_lancamento}=     Get Datas Alteracao Contrato    ${retorno_contrato[3]}    ${data_de_contrato}     ${data_ate_contrato}
                        Select From List By Label     ${select_tipo_calculo}    ${datas_lancamento[3]}
                        Input Text    ${input_data_de}   ${datas_lancamento[1]}
                        Input Text    ${input_data_ate}    ${datas_lancamento[2]}
                        Input Text    ${input_percentual_desconto}    ${registro['Nova Porcentagem Bolsa']} 
                        Sleep     5s
                        Click Button    ${PRIME.btn_atualizar_contrato_aberto}
                        Sleep     5s
                        ${status_alerta}    ${retorno_alerta}    Run Keyword And Ignore Error    Capturar Mensagem Alerta
                        IF   "${status_alerta}" == "PASS"
                            Acao Sobre Um Alerta    ACCEPT
                        END
                        Sleep     5s
                        ${status_alerta}    ${retorno_alerta}    Run Keyword And Ignore Error    Capturar Mensagem Alerta
                        IF   "${status_alerta}" == "PASS"
                            Acao Sobre Um Alerta    ACCEPT
                        END
                        Wait Until Element Is Visible 	 ${PRIME.btn_atualizar_contrato_aberto} 	 timeout=50
                        ${status}    ${retorno_alerta}    Run Keyword And Ignore Error    Wait Until Element Is Visible 	 ${PRIME.td_erro_salvar_contrato} 	 timeout=5
                        IF  "${status}" == "PASS"
                            ${erro_salvar}=    Get Text    ${PRIME.td_erro_salvar_contrato}
                            Close Window
                            Switch Window       title=${title_window}[0]
                            RETURN      ${FALSE}    Erro ao excluir Contrato
                        END
                        #pegar alguma atualizacao
                        Close Window
                        Switch Window       title=${title_window}[0]
                        RETURN   ${TRUE}    Contrato modificado
                    END
                END
            END
        ELSE
            RETURN      ${FALSE}    Nenhum contrato válido
        END
    EXCEPT
        RETURN      ${FALSE}    Analise_manual
    END


Modificar Perfil Aluno
    [Documentation]    Keyword efetua a verificação e modificação da bolsa do aluno no perfil do aluno
    [Arguments]    ${registro}

    TRY
        Go To    ${URLS.secao_alunos}
        Wait Until Element Is Visible 	 ${PRIME.select_estabelecimento}    timeout=50
        Input Text    ${PRIME.input_codigo_alunos}    ${registro['Matrícula']}
        Click Element    ${PRIME.btn_localizar}
        Wait Until Element Is Visible    ${PRIME.body_aluno}    timeout=3
        ${valida_aluno}=    Get Text    ${PRIME.body_aluno}
        IF  "${valida_aluno}" == "Sua busca não retornou resultados."
            Log Info    Não foi encontrado aluno com RA: ${registro['Matrícula']}   console=True  traceId=${TRACEID}
            RETURN    ${FALSE}     Não foi encontrado aluno na seção de Alunos
        ELSE IF    "${valida_aluno}" == "Muitos registros encontrados. Favor específicar mais filtros."
            Log Info    Não foi encontrado aluno com RA: ${registro['Matrícula']}   console=True  traceId=${TRACEID}
            RETURN    ${FALSE}     RA inválido
        ELSE
            Click Element    ${PRIME.link_aluno}
            ${grade_aluno}=     Get Grade Aluno    ${registro}
            IF    ${grade_aluno[0]}
                ${btn_descontos_grade}=    Replace String    ${PRIME.btn_descontos_grade_aluno}    {grade}   ${grade_aluno[1]}
                Wait Until Element Is Visible    ${btn_descontos_grade}    timeout=50
                Click Element     ${btn_descontos_grade}
                ${td_grade}=    Replace String    ${PRIME.td_grade_aluno}    {grade}    ${grade_aluno[1]}
                Wait Until Element Is Visible    ${PRIME.btn_gravar_lancamento}    timeout=50
                IF    "${registro['Tipo de Alteração']}" == "Exclusão" and "${registro['Alteração']}" == "Imediata"
                    ${encontrou_bolsa}=    Set Variable    ${FALSE}
                    FOR     ${index_variavel}    IN RANGE    0     6
                        ${str_index}=        Convert To String    ${index_variavel}
                        ${select_tipo_desconto}=    Replace String    ${PRIME.select_tipo_desconto_aluno}    {index}    ${str_index}
                        TRY
                            ${label_desconto}=    Get Selected List Label    ${select_tipo_desconto}
                            IF    "${label_desconto}" == "${registro['Tipo Bolsa']}"
                                ${index}=    Set Variable    ${str_index}
                                ${btn_excluir_secao_aluno}=    Replace String    ${PRIME.btn_excluir_secao_aluno}    {num}    ${index}
                                Click Element    ${btn_excluir_secao_aluno}
                                ${encontrou_bolsa}=    Set Variable    ${TRUE}
                            END
                        EXCEPT
                            Exit For Loop
                        END
                    END
                    IF    ${encontrou_bolsa}
                        ${encontrou_bolsa}=    Set Variable    ${TRUE}
                    ELSE
                        RETURN     ${FALSE}    Bolsa não encontrada em Alunos
                    END
                    Sleep     5s
                    Click Element     ${PRIME.btn_gravar_lancamento}
                    ${status}    Run Keyword And Ignore Error    Wait Until Element Is Visible    ${btn_descontos_grade}    timeout=50
                    IF   "${status[0]}" == "PASS"
                        RETURN      ${TRUE}    Bolsa excluída imediatamente em Alunos
                    ELSE
                        RETURN      ${FALSE}    Erro ao excluir bolsa em Alunos
                    END
                ELSE IF    "${registro['Tipo de Alteração']}" == "Exclusão" and "${registro['Alteração']}" == "Próximo Semestre"
                    ${nova_data_fim}=    Obter Proximo Semestre
                    ${encontrou_bolsa}=    Set Variable    ${FALSE}

                    FOR     ${index_variavel}    IN RANGE    0     6
                        ${str_index}=        Convert To String    ${index_variavel}
                        ${select_tipo_desconto}=    Replace String    ${PRIME.select_tipo_desconto_aluno}    {index}    ${str_index}
                        TRY
                            ${label_desconto}=    Get Selected List Label    ${select_tipo_desconto}
                            IF    "${label_desconto}" == "${registro['Tipo Bolsa']}"
                                ${index}=    Set Variable    ${str_index}
                                ${input_data_ate_aluno}=    Replace String    ${PRIME.input_data_ate_aluno_variavel}    {num}    ${index}
                                Input Text    ${input_data_ate_aluno}    ${nova_data_fim}
                                ${encontrou_bolsa}=    Set Variable    ${TRUE}
                            END
                        EXCEPT
                            Exit For Loop
                        END
                    END
                    IF    ${encontrou_bolsa}
                        ${encontrou_bolsa}=    Set Variable    ${TRUE}
                    ELSE
                        RETURN     ${FALSE}    Bolsa não encontrada em Alunos
                    END

                    Sleep     5s
                    Click Element     ${PRIME.btn_gravar_lancamento}
                    ${status_alerta}    ${retorno_alerta}    Run Keyword And Ignore Error    Capturar Mensagem Alerta
                    IF   "${status_alerta}" == "PASS"
                        Acao Sobre Um Alerta    ACCEPT
                    END 
                    ${status}    Run Keyword And Ignore Error    Wait Until Element Is Visible    ${btn_descontos_grade}    timeout=50
                    IF   "${status[0]}" == "PASS"
                        RETURN    ${TRUE}    Bolsa excluída próximo semestre em Alunos
                    ELSE
                        RETURN    ${FALSE}    Erro ao excluir bolsa em Alunos
                    END
                ELSE IF    "${registro['Tipo de Alteração']}" == "Alteração"

                    ${encontrou_bolsa}=    Set Variable    ${FALSE}
                    FOR    ${index_variavel}    IN RANGE    0     6
                        ${str_index}=        Convert To String    ${index_variavel}
                        ${select_tipo_desconto}=    Replace String    ${PRIME.select_tipo_desconto_aluno}    {index}    ${str_index}
                        TRY
                            ${label_desconto}=    Get Selected List Label    ${select_tipo_desconto}
                            IF    "${label_desconto}" == "${registro['Tipo Bolsa']}"
                                ${input_percentual_bolsa}=      Replace String    ${PRIME.input_percentual_aluno_variavel}    {num}    ${str_index}
                                Input Text    ${input_percentual_bolsa}    ${registro['Nova Porcentagem Bolsa']}
                                ${encontrou_bolsa}=    Set Variable    ${TRUE}
                            END
                        EXCEPT
                            Exit For Loop
                        END
                    END
                    IF    ${encontrou_bolsa}
                        ${encontrou_bolsa}=    Set Variable    ${TRUE}
                    ELSE
                        RETURN    ${FALSE}    Bolsa não encontrada em Alunos
                    END

                    Sleep    15s
                    Click Element     ${PRIME.btn_gravar_lancamento}
                    ${status_alerta}    ${retorno_alerta}    Run Keyword And Ignore Error    Capturar Mensagem Alerta
                    IF   "${status_alerta}" == "PASS"
                        Acao Sobre Um Alerta    ACCEPT
                    END 
                    ${status}    Run Keyword And Ignore Error    Wait Until Element Is Visible    ${btn_descontos_grade}    timeout=50
                    IF   "${status[0]}" == "PASS"
                        RETURN      ${TRUE}    Porcentagem da bolsa alterada
                    ELSE
                        RETURN      ${FALSE}    Erro ao alterar porcentagem da bolsa em Alunos
                    END
                END
            ELSE
                RETURN    ${FALSE}    Grade não encontrada
            END
        END
    EXCEPT
        RETURN    ${FALSE}    Analise_manual
    END
