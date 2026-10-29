# Teste técnico: Desenvolvedor(a) Júnior

## Contexto

Uma loja online quer enviar mensagens semanais aos clientes, de acordo com o perfil de compra de cada um. Hoje alguém faz isso à mão, com planilhas. Você vai construir um protótipo que automatiza esse trabalho.

## Dados

Use a API pública DummyJSON (gratuita, sem cadastro):

Clientes: https://dummyjson.com/users

Carrinhos de compra: https://dummyjson.com/carts

As listas são paginadas. Descubra na documentação como buscar todos os registros.

## O que entregar

### Extração

Um script que busca todos os clientes e todos os carrinhos.

Grave o JSON bruto em data/raw/AAAA-MM-DD/, com data e hora no nome do arquivo.

Uma nova execução nunca apaga nem sobrescreve os arquivos anteriores.

### Tabela de clientes

Em SQLite ou DuckDB, uma tabela com uma linha por cliente.

Colunas: id, nome completo, idade, sexo, estado, telefone, valor total dos carrinhos e quantidade total de itens.

### Classificação em trilhas

Cada cliente pode entrar em mais de uma trilha.

Para cada trilha sugerida, mostre o motivo (exemplo: “valor total R$ 12.450 ≥ R$ 10.000”).

A prioridade segue a ordem da tabela:

Prioridade | Trilha | Regra
--- | --- | ---
1 | Alto valor | valor total ≥ 10.000
2 | Compra em quantidade | itens ≥ 15
3 | Incentivo | valor total < 1.000
4 | Público jovem | idade < 30
5 | Geral | não se encaixou em nenhuma das anteriores

### Aplicação web simples (FastAPI ou Flask)

Lista de clientes, com filtro por trilha.

Página do cliente com os dados, as trilhas sugeridas e os motivos.

Um analista confirma ou ajusta as trilhas de cada cliente, e a decisão fica gravada no banco. Só clientes confirmados entram no cronograma.

### Cronograma

Cada trilha tem 3 mensagens, enviadas uma por semana, sempre no mesmo dia da semana (configurável).

O cliente faz uma trilha de cada vez, na ordem de prioridade: termina as 3 semanas da primeira e só então começa a próxima.

Mostre numa página os envios previstos para as próximas semanas.

### Envio simulado por WhatsApp

Escolha uma destas plataformas e leia a documentação da API dela:

Setabot: https://crm.setabot.com.br/api/help#inboxes

Botmaker: https://api.botmaker.com/v2.0/#/

Crie um botão “Simular envios de hoje”. Para cada mensagem do dia, monte a requisição exatamente como a documentação da plataforma escolhida pede: endpoint, método, cabeçalhos e corpo. Nas mensagens:

converta o telefone do cliente para o formato que a API exige;

substitua {nome} pelo primeiro nome do cliente.

Não faça a chamada real. Grave no histórico a requisição que seria enviada, com o cliente, a mensagem e a data.
O token de acesso deve vir de uma variável de ambiente, nunca escrito no código.

## Mensagens de cada trilha

### Alto valor

- “Olá, {nome}! Você é um dos nossos clientes especiais: a partir desta semana, tem frete grátis em todos os pedidos.”

- “{nome}, separamos produtos que combinam com suas últimas compras. Confira no app.”

- “{nome}, queremos ouvir você: responda nossa pesquisa de 1 minuto e ganhe um cupom de 10%.”

### Compra em quantidade

- “Olá, {nome}! Pedidos acima de 20 itens têm 5% de desconto automático.”

- “{nome}, você pode agendar a entrega para o dia que preferir. Veja como no app.”

- “{nome}, monte sua lista de compras recorrentes e receba um lembrete na hora de repor.”

### Incentivo

- “Olá, {nome}! Use o cupom BEMVINDO e ganhe 15% na próxima compra.”

- “{nome}, temos produtos a partir de R$ 9,90 com entrega rápida. Aproveite para experimentar.”

- “{nome}, seu cupom de 15% expira em 7 dias. Não deixe passar!”

### Público jovem

- “E aí, {nome}! Siga a gente nas redes e veja os lançamentos antes de todo mundo.”

- “{nome}, indique um amigo e vocês dois ganham R$ 20 de desconto.”

- “{nome}, chegou a nova coleção. Dá uma olhada e conta pra gente o que achou.”

### Geral

- “Olá, {nome}! Obrigado por comprar com a gente. Confira as novidades da semana.”

- “{nome}, ative as notificações do app para não perder nenhuma promoção.”

- “{nome}, conta pra gente como foi sua última compra respondendo uma pesquisa rápida.”

## Como publicar no GitHub

Crie um repositório público na sua conta do GitHub.

Branches e Pull Requests serão analisados, caso existam no projeto.

Abra uma issue no próprio repositório para cada item que não deu tempo de fazer.

## Prazo e regras

Você tem 10 dias corridos. Estimamos de 8 a 12 horas de trabalho.

Pode consultar qualquer material, inclusive ferramentas de IA. Na entrevista, você vai explicar cada parte do código e as decisões que tomou.

Prefira algo simples e funcionando a algo grande e incompleto. Inclua um README.md explicando como rodar o projeto.

### Diferenciais (opcionais):

- Dockerfile;

- testes rodando no GitHub Actions;

- tratamento de erro quando a API não responde.

Entrega: responda este e-mail com o link do repositório.
