# CommonKit 🚀

Bem-vindo ao CommonKit!

## Estrutura do Repositório 📚

O repositório é organizado da seguinte forma:

```bash
📁 CommonKit/
│
├── 📁 utils/                                   # Pasta contendo todos o códigos comuns entre os projetos, logger, conexões, acessos ao Prime
│   ├── 📁 microsoft/                           # Pasta contendo código relacionado a números primos
│   │   ├── 🐍 __init__.py                      # Arquivo de inicialização do pacote 'microsoft'
│   │   ├── 🐍 email_integration.py             # Arquivo de integração com email
│   │   ├── 🐍 msal_auth.py                     # Arquivo de autenticação utilizando msal
│   │   ├── 🐍 sharepoint_integration.py        # Arquivo de integração com sharepoint
│   │   ├── 🐍 teams_integration.py             # Arquivo de integração com teams
│   │   └── ...
│   ├── 📁 prime/                               # Pasta contendo código relacionado a números primos
│   │   ├── 🐍 __init__.py                      # Arquivo de inicialização do pacote 'selenium_drive'
│   │   └── ...
│   ├── 📁 selenium_drive/                      # Pasta contendo o driver do Selenium
│   │   ├── 🐍 __init__.py                      # Arquivo de inicialização do pacote 'selenium_drive'
│   │   ├── 🐍 remote_driver.py                 # Arquivo contendo a classe do driver de conexão do Selenium
│   │   └── ...
│   ├── 🐍 criptador.py                         # Arquivo contendo código relacionado à criptografia
│   ├── 🐍 db_connection.py                     # Arquivo contendo código de conexão com banco de dados
│   ├── 🐍 email_handler.py                     # Arquivo contendo código relacionado ao manuseio de e-mails
│   ├── 🐍 logger.py                            # Arquivo contendo código de registro de logs
│   └── 🐍 timer.py                             # Arquivo contendo código relacionado a temporização
│
├── ⚙️ .env                                     # Arquivo de configuração de variáveis de ambiente
├── 📝 .gitignore                               # Arquivo para ignorar arquivos desnecessários no controle de versão
├── 📝 README.md                                # Documentação do projeto
└── ...
```

## Utilização 🛠️

Para utilizar o CommonKit como um submodule em seu projeto, siga estes passos:

1. Clone o repositório principal do seu projeto:

    ```bash
        git clone https://seu-repositorio-principal.git
    ```

2. Adicione o CommonKit como um submodule no seu projeto:

    ```bash
        git submodule add https://dev.azure.com/pucprexpcliente/PUCPR-Experiencia_Clientes/_git/CommonKit utils
    ```

3. Após adicionar o submodule, você precisará inicializá-lo e atualizá-lo:

    ```bash
        git submodule init
        git submodule update
    ```

Agora você pode acessar os utilitários do CommonKit em seu projeto.

## Contato 📬

Você pode entrar em contato com os responsáveis pelo projeto através dos seguintes e-mails:

- [Ricardo Taverna](ricardo.taverna1@pucpr.br)
- [Gabriel Ernesto Barbosa Pereira](ernesto.gabriel@pucpr.br)
- [Matheus Henrique Rosa](m.rosa1@pucpr.br)
- [Cesar Cunha Ziobro](c.ziobro@pucpr.br)
- [Carlens Oslin](carlens.oslin@pucpr.br)

## Licença 📔

Este projeto é propriedade da <span style="color:red">PUCPR</span>. Consulte a política de licenciamento interno da empresa para obter informações sobre como este código pode ser utilizado.
