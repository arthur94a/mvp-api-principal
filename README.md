# MVP API Principal

API REST desenvolvida com FastAPI para autenticação de usuários e gerenciamento de veículos, servindo como backend do projeto Garage FIPE.

A API consome uma API externa de dados FIPE e realiza o cache dos dados coletados
em um banco próprio, reduzindo sobrecarga e aumentando a disponibilidade das informações.

## Tecnologias

- Python
- FastAPI
- SQLModel
- Uvicorn

## Pré-requisitos

Antes de iniciar, instale:

- Python 3.11 ou superior
- pip
- virtualenv (opcional, mas recomendado)
- Docker (opcional, para execução em container)

## Instalação e configuração local

1. Entre na pasta da API:

	cd mvp-api-principal

2. Crie o ambiente virtual:

	python -m venv venv

3. Ative o ambiente virtual:

	Windows (PowerShell):

	.\venv\Scripts\Activate

	Linux/Mac:

	source venv/bin/activate

4. Instale as dependências:

	pip install -r requirements.txt

## Executando a aplicação

Com o ambiente virtual ativo, execute:

uvicorn main:app --reload

A API ficará disponível em:

- http://localhost:8000

Documentação automática:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Executando com Docker

1. Build da imagem:

	docker build -t mvp_api_principal .

2. Suba o container na porta 8000:

	Linux/Mac:

	docker run -p 8000:8000 -v "$(pwd)/database:/app/database" mvp_api_principal

	Windows (PowerShell):

	docker run -p 8000:8000 -v "${PWD}/database:/app/database" mvp_api_principal

## Estrutura resumida

- routes: definição das rotas da API.
- models: modelos de dados e criação de tabelas.
- schemas: esquemas de validação e serialização.
- services: integrações e regras de negócio.
- utils: utilitários compartilhados.

## Observações

- O backend está configurado para aceitar requisições do frontend em http://localhost:5173.
- Certifique-se de manter a pasta database acessível para persistência local dos dados.