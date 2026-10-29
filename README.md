# API Python + OpenAI

API em FastAPI que expoe recursos da OpenAI, escrita em **clean architecture**
para servir de referencia de estrutura.

## Camadas

```
src/
  domain/         # entities, exceptions, repositories — regra pura
  application/    # commands, queries, services, interfaces
  infra/          # applicationBdContext, config, mappers, services
  interfaces/     # api (os endpoints), shared
  main.py
```

As dependencias apontam para dentro: `domain/` nao conhece FastAPI nem o SDK da
OpenAI. Trocar de provedor de LLM mexe em `infra/services/` e em nada mais — e e
esse o ponto do exercicio.

## Rodar local

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe -m uvicorn src.main:app --reload
```

Precisa da chave da OpenAI no ambiente. **Nao versione o `.env`.**

## Natureza deste repositorio

E estudo de arquitetura, nao produto. O par dele e
[api-python-clean-architecture](https://github.com/Guilhermedneto/api-python-clean-architecture),
que aplica a mesma estrutura a um CRUD de usuarios com foco em seguranca.
