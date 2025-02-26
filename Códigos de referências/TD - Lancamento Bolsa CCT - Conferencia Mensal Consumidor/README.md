# TD - Conferência Mensal - Consumidor #

### Descrição do Projeto ###
<p style='text-align: justify;'> O objetivo dessa automação é a Conferência Mensal das Bolsas Concedidas e a realização dos ajustes necessários nas bolsas que foram encontradas mudanças. Para isso, o robô baixa a planilha de bolsas concedidas, verifica a situação dos responsáveis pela bolsa, modifica a bolsa do aluno no Prime e atualiza o Sharepoint. 

### Descrição do Módulo ###
Robô responsável por atualizar a bolsa dos alunos com status pendentes.

### Conceitos ###
* **Prime**: Sistema utilizado para fazer a gestão de diversas áreas.
  * Prime - [Ambiente de Produção](https://a99a35.mannesoftprime.com.br/mannesoft/)
  * Prime - [Ambiente de Homologação](https://a99a35.mannesoftprime.com.br/homologacao/)

### Pré-requisitos ###

* MongoDB - [Página oficial](https://www.mongodb.com/try/download/community)
* OneDrive - [Página oficial](https://www.microsoft.com/pt-br/microsoft-365/onedrive/download)
* Python 3.8 - [Página oficial](https://www.python.org/downloads/release/python-380/)
* RCC- [Executável](https://bitbucket.org/fabricio_antoniasse/documentacoes-arquivos/src/main/RCC/)
* Vault - [Tutorial instalação](https://github.com/edugraminho/vault_secrets)

### Fluxo de execução ###
* 1. [TD - Conferência Mensal - Produtor](https://dev.azure.com/pucprexpcliente/PUCPR-Experiencia_Clientes/_git/TD%20-%20Lancamento%20Bolsa%20CCT%20-%20Conferencia%20Mensal%20Produtor)
* 2. [TD - Conferência Mensal - Consumidor](https://dev.azure.com/pucprexpcliente/PUCPR-Experiencia_Clientes/_git/TD%20-%20Lancamento%20Bolsa%20CCT%20-%20Conferencia%20Mensal%20Consumidor)
* 3. [TD - Conferência Mensal - Publicador](https://dev.azure.com/pucprexpcliente/PUCPR-Experiencia_Clientes/_git/TD%20-%20Lancamento%20Bolsa%20CCT%20-%20Conferencia%20Mensal%20Publicador)

### Fluxo de tasks ###
* Abaixo e à esquerda, o fluxo de tasks do processos e suas respectivas saídas.
* À direita, o fluxo de possíveis status saída de cada objeto (no caso, protocolo) dessa automação.
![img.png](./Arquivos/fluxograma_consumidor.png)

### Como configurar ###

* Preencher o Vault do processo com as informações necessárias:

  | Chave  |  Valor (Descrição)  |
  | ----------------- | --- |
  |AMBIENTE_PRIME_PASSWORD |  Senha do Prime para o usuário do robô |
  |AMBIENTE_PRIME_URL | Endereço do website da plataforma Prime |
  |AMBIENTE_PRIME_USER |  Usuário do robô para a plataforma Prime |
  |DNS_EMAIL| DNS do e-mail do Outlook |
  |EMAILS_ANALISTAS | Lista contendo os e-mails dos analistas do processo|
  |EMAIL_PASSWORD |  Senha do e-mail para o usuário Navi.Bot |
  |EMAIL_USERNAME |  Endereço de e-mail do Navi.Bot |
  |CONTROLE_COLLECTION_MONGO |  Nome da collection, no MongoDB, que contém os dados de controle |
  |COLABORADORES_COLLECTION_MONGO |  Nome da collection, no MongoDB, que contém os dados dos colaboradores|
  |DATABASE_MONGO |  Nome da Database - MongoDB |
  |PROTOCOLOS_ABERTOS_COLLECTION_MONGO|  Nome da collection, no MongoDB, que contém os protocolos abertos |
  |REGISTROS_COLLECTION_MONGO|  Nome da collection, no MongoDB, que contém os registros |
  |BOLSAS_CONCEDIDAS_COLLECTION_MONGO|  Nome da collection, no MongoDB, que contém os registros |
  |HISTORICO_CONFERENCIA_COLLECTION_MONGO|  Nome da collection, no MongoDB, que contém os registros |
  |TIPOS_PROTOCOLO |  Lista contendo os tipos de protocolo que serão pesquisados no Prime |

* Preencher o Vault com as informações de email:
  | Chave  |  Valor (Descrição)  |
  | ----------------- | --- |
  |CLIENT_ID |  Cliente ID do aplicativo do Azure do e-mail |
  |CLIENT_SECRET |   Cliente Secret do aplicativo do Azure do e-mail |
  |TENANT_ID |   Tenant ID do aplicativo do Azure do e-mail |
  |USER_ID |   User ID do aplicativo do Azure do e-mail |
  |PASSWORD |  Senha do e-mail (PUCPR) para o usuário do robô |
  |USERNAME |  Endereço de e-mail do usuário do robô |
  
  
 * Configurar as variáveis de ambiente:

    | Chave  |  Valor (Descrição)  |
    | ----------------- | --- |
    |HCV_SEAL |  Chave SEAL do vault |
    |AMBIENTE |  DEV (Desenvolvimento) ou PROD (Produção) |

* Executar projeto

    -- No diretório raiz do projeto
   ```
    $ rcc run
   ```

### Bibliotecas Utilizadas ###

* [RobotFramework](https://robotframework.org/)
* [SeleniumLibrary](https://robotframework.org/SeleniumLibrary/SeleniumLibrary.html)
* [Pandas](https://pandas.pydata.org/)
* [HVAC](https://hvac.readthedocs.io/en/stable/overview.html)
* [Pymongo](https://pymongo.readthedocs.io/en/stable/)

### Autores ###
* **Gabriel Antonio Moreira Silva** 
