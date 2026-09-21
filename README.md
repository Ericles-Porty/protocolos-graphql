# GraphQL

Sistema de eventos acadêmicos exposto como API GraphQL, em Python (Ariadne, schema-first) e
SQLite.

Este repositório é um de uma série de cinco, o mesmo domínio implementado em cinco protocolos
diferentes para deixar a diferença visível em código, não só em slide:

- [protocolos-graphql](https://github.com/Ericles-Porty/protocolos-graphql) (este repositório)
- [protocolos-rest](https://github.com/Ericles-Porty/protocolos-rest)
- [protocolos-soap](https://github.com/Ericles-Porty/protocolos-soap)
- [protocolos-grpc](https://github.com/Ericles-Porty/protocolos-grpc)
- [protocolos-websocket](https://github.com/Ericles-Porty/protocolos-websocket)

## Domínio

`Aluno`, `Evento`, `Inscricao` e `Pagamento`, cobrindo os três tipos de relacionamento:

- **1:1** — uma inscrição tem no máximo um pagamento.
- **1:N** — um evento tem várias inscrições (e um aluno também).
- **N:M** — um aluno se inscreve em vários eventos, um evento recebe vários alunos, através da
  inscrição.

## Pré-requisitos

- Python 3.10 ou superior

## Como executar

```bash
git clone https://github.com/Ericles-Porty/protocolos-graphql.git
cd protocolos-graphql
pip install -r requirements.txt
cd src
python servidor.py
```

O banco (`dados.db`) é recriado e semeado do zero a cada vez que o servidor sobe. Abra
`http://localhost:8000/` no navegador pro GraphiQL (o schema fica navegável ali, sem precisar
abrir `schema.graphql`).

## Exemplos de utilização

```graphql
# a inscrição semeada já vem com aluno, evento e pagamento aninhados, numa única ida
{
  inscricao(id: 1) {
    status
    aluno { nome }
    evento { titulo }
    pagamento { valor status }
  }
}

# N:M nos dois sentidos, na mesma consulta
{
  aluno(id: 1) { nome eventos { titulo } }
  evento(id: 1) { titulo alunos { nome } }
}

# mutation: pagamento aprovado confirma a inscrição sozinho
mutation {
  registrarPagamento(inscricaoId: 4, valor: 30) { status }
}

# id inexistente: data vem null, o erro vem à parte em errors — não é HTTP 404
{ aluno(id: 999) { nome } }
```

## Estrutura do projeto

```text
src/
├── servidor.py       único ponto de entrada: liga os resolvers no schema
├── schema.graphql    o contrato (SDL): todo tipo, campo e operação disponível
└── banco.py          conexão sqlite3, esquema e seed (igual nos quatro repositórios)
```

## O que observar

- **Uma consulta, uma resposta com o formato exato dela.** Pedir `aluno { nome }` não traz email;
  pedir `evento { alunos { nome } }` atravessa o N:M numa única ida ao servidor.
- **O schema é escrito à mão** (`schema.graphql`), antes de qualquer resolver existir — o servidor
  recusa qualquer consulta que peça um campo que não está lá.
- **Erro não é HTTP.** Toda resposta volta com `200`; sucesso e falha se distinguem por `data` vir
  preenchido ou `errors` vir com algo dentro, nunca pelo código HTTP.
