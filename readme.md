# Best Life

Protótipo para classificar clientes, confirmar trilhas e simular mensagens semanais. Nenhuma mensagem é enviada de verdade.

## Executar localmente

Requisitos: Python 3.12 e acesso à internet para a extração. Execute na raiz do projeto:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/extract.py
python scripts/load_db.py
uvicorn app.main:app --reload
```

Acesse http://localhost:8000/customers. A documentação da API fica em /docs. Os dados ficam em `data/`, fora do Git.

## Usar com Docker

```bash
docker build -t best-life .
docker run --rm -v "$(pwd)/data:/app/data" best-life python scripts/extract.py
docker run --rm -v "$(pwd)/data:/app/data" best-life python scripts/load_db.py
cp -n .env.example .env
docker run --rm -p 8000:8000 --env-file .env -v "$(pwd)/data:/app/data" best-life
```

O volume mantém os dados entre execuções. O arquivo `.env` contém as variáveis de ambiente e não é enviado ao Git. Para simular, não é necessário preencher credenciais reais.

## Fluxo

1. Abra um cliente e confirme ou ajuste suas trilhas. Apenas clientes confirmados entram no cronograma; Geral deve ser escolhida sozinha.
2. Em Cronograma, escolha o dia da semana. O primeiro envio ocorre no dia escolhido a partir da data de confirmação; os demais ocorrem semanalmente, três por trilha, em ordem de prioridade. Alterar a seleção reinicia o cronograma desse cliente; alterar o dia recalcula as datas de todos os clientes.
3. Clique em **Simular envios de hoje**. Sem variáveis configuradas, a requisição usa indicações de exemplo para o token e o canal. O histórico registra a requisição sem guardar o token. Repetir a simulação no mesmo dia não duplica a mesma mensagem.

Opcionalmente, preencha `BOTMAKER_TOKEN` e `BOTMAKER_CHANNEL_ID` no arquivo `.env` com os dados da sua conta. Para carregá-los ao executar localmente:

```bash
set -a
source .env
set +a
uvicorn app.main:app --reload
```

A simulação segue o endpoint [Send messages da Botmaker](https://api.botmaker.com/v2.0/#/operations/send-messages), com `channelId`, telefone internacional sem pontuação em `contactId` e texto em `messages`. O token, quando configurado por variável de ambiente, aparece mascarado no histórico; sem ele, o histórico indica que é um exemplo. A API de mensagens de texto da Botmaker pressupõe uma conversa de WhatsApp aberta; o protótipo não verifica essa condição nem envia requisições. Os números da DummyJSON são fictícios.

O total do cliente é a soma dos valores dos carrinhos sem desconto; a quantidade é a soma de `totalQuantity`. Clientes sem carrinho recebem zero. Os valores da DummyJSON são apresentados como reais.
