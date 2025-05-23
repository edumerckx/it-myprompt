# it-myprompt

API _restful_ para chat integrado com llm. Possui recurso para criação de usuário e autenticação/geração de token - necessário para solicitações de chat. 

## Tecnologias
- [Python 3.12+](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/) 
- [PostgreSQL](https://www.postgresql.org/)
- [Langchain](https://www.langchain.com/)
- [OpenRouter](https://openrouter.ai/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Docker](https://www.docker.com/)
- [Poetry](https://python-poetry.org/) 
- [Pytest](https://docs.pytest.org/)
- [Testcontainers](https://testcontainers.com/)

Esboço de implementação na AWS está no [arquivo de arquitetura](ARQUITETURA.md)


## Como executar a aplicação

Embora a aplicação possa ser executada localmente, recomenda-se a utilização do _docker-compose_. É necessário uma _api key_ da **OpenRouter**

#### Variáveis de ambiente
```
OPENROUTER_API_KEY - api key fornecida pelo openrouter
OPENROUTER_API_URL - https://openrouter.ai/api/v1
OPENROUTER_MODEL - gpt-3.5-turbo
ACCESS_TOKEN_EXPIRE_MINUTES - 60
SECRET_KEY - secret que será utilizado no processo de autenticação
ALGORITHM - HS256
DATABASE_URL - postgresql+psycopg://<user>:<pass>@localhost:5432/<db> # alterar conforme instalação local
LOGGER_LEVEL - INFO

# a configuração de tracing abaixo é opcional
LANGSMITH_TRACING - true # habilita o tracing - se 'true' as demais deverão ser preenchidas
LANGSMITH_ENDPOINT - "https://api.smith.langchain.com"
LANGSMITH_API_KEY - api key gerada no site langsmith 
LANGSMITH_PROJECT - nome do projeto criado junto com o api key

```

#### Docker-compose

Para utilizar o _docker-compose_ garanta que o **docker** esteja instalado e as variáveis de ambientes estejam configuradas conforme o [arquivo de exemplo](.env-example)
No terminal, executar:
```sh
docker-compose up --build
```

#### Localmente

Para executar localmente é necessário que o ambiente tenha:
- **python** 3.12+ instalado
- **poetry** instalado - com ele é criado o 'ambiente virtual' e instaladas as dependências
- uma instância do **postgres** rodando - pode ser um container docker
- variáveis de ambiente configuradas (arquivo **.env**) - no projeto tem um [arquivo de exemplo](.env-example) 

Com os pré-requisitos atendidos executar os comandos:
```sh
# baixa o fonte
git clone git@github.com:edumerckx/it-myprompt.git

# acessa o diretório do projeto
cd it-myprompt

# instala dependências
poetry install

# ativa ambiente virutal
poetry shell

# executa migrations no bd
alembic upgrade head

# executa apliação no modo dev
task dev
```

Para os testes é necessário que o docker esteja rodando para atender o **testcontainers**. Com isso, executar:
```sh
task test
```

## Como funciona

Nas áreas logadas, o usuário só pode visualizar/editar os próprios dados.

Abaixo um exemplo do funcionamento utilizando o swagger:

![swagger](swagger.gif)

### OpenAPI

Com a aplicação rodando, é possível acessar o _swagger_ fornecido pelo _fastapi_ através do [/docs](http://localhost:8000/docs)

### Endpoints:
- Não é necessária autenticação
  - **POST /users/** - cria usuário
  - **POST /auth/token**  - login e geração de access-token
- Necessitam autenticação - _access-token_
  - **PUT /users/me**  - atualiza dados do usuário
  - **POST /chat** - chat 
  - **POST /auth/refresh_token**  - atualiza access-token

