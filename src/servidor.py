"""Sistema de eventos acadêmicos exposto como API GraphQL (Ariadne, schema-first).

Único ponto de entrada. Sobe com:  python servidor.py
Playground (GraphiQL) em:          http://localhost:8000/
"""

from __future__ import annotations

from pathlib import Path

import banco
from ariadne import MutationType, ObjectType, QueryType, load_schema_from_path, make_executable_schema
from ariadne.wsgi import GraphQL

banco.inicializar()

tipo_defs = load_schema_from_path(Path(__file__).parent / "schema.graphql")

query = QueryType()
mutation = MutationType()
tipo_aluno = ObjectType("Aluno")
tipo_evento = ObjectType("Evento")
tipo_inscricao = ObjectType("Inscricao")
tipo_pagamento = ObjectType("Pagamento")


@query.field("aluno")
def resolver_aluno(_pai: None, _info: object, id: str) -> dict | None:
    return banco.buscar_aluno(int(id))


@query.field("evento")
def resolver_evento(_pai: None, _info: object, id: str) -> dict | None:
    return banco.buscar_evento(int(id))


@query.field("inscricao")
def resolver_inscricao(_pai: None, _info: object, id: str) -> dict | None:
    return banco.buscar_inscricao(int(id))


@tipo_aluno.field("eventos")
def resolver_eventos_do_aluno(aluno: dict, _info: object) -> list[dict]:
    return banco.eventos_do_aluno(aluno["id"])


@tipo_evento.field("alunos")
def resolver_alunos_do_evento(evento: dict, _info: object) -> list[dict]:
    return banco.alunos_do_evento(evento["id"])


@tipo_inscricao.field("aluno")
def resolver_inscricao_aluno(inscricao: dict, _info: object) -> dict | None:
    return banco.buscar_aluno(inscricao["aluno_id"])


@tipo_inscricao.field("evento")
def resolver_inscricao_evento(inscricao: dict, _info: object) -> dict | None:
    return banco.buscar_evento(inscricao["evento_id"])


@tipo_pagamento.field("inscricaoId")
def resolver_pagamento_inscricao_id(pagamento: dict, _info: object) -> int:
    return pagamento["inscricao_id"]


@mutation.field("criarAluno")
def resolver_criar_aluno(_pai: None, _info: object, nome: str, email: str) -> dict:
    return banco.criar_aluno(nome, email)


@mutation.field("criarEvento")
def resolver_criar_evento(_pai: None, _info: object, titulo: str, data: str) -> dict:
    return banco.criar_evento(titulo, data)


@mutation.field("inscrever")
def resolver_inscrever(_pai: None, _info: object, alunoId: str, eventoId: str) -> dict:
    return banco.inscrever(int(alunoId), int(eventoId))


@mutation.field("registrarPagamento")
def resolver_registrar_pagamento(_pai: None, _info: object, inscricaoId: str, valor: float) -> dict:
    return banco.registrar_pagamento(int(inscricaoId), valor)


schema = make_executable_schema(tipo_defs, query, mutation, tipo_aluno, tipo_evento, tipo_inscricao, tipo_pagamento)

app = GraphQL(schema, debug=False)


if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    print("GraphQL (GraphiQL) em http://localhost:8000/")
    make_server("0.0.0.0", 8000, app).serve_forever()
