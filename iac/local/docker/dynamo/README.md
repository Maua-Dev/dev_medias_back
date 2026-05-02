# DynamoDB Local

## Subir

Na pasta deste arquivo:

```bash
docker compose -f docker_compose.yaml up -d
```

Copie **`.env.example`** para **`.env`** na mesma pasta. O compose usa **`STACK_NAME`** no nome do container (ex.: `devmedias-dynamodb-local` vs `outro_repo-dynamodb-local`) para separar instâncias por projeto.

Se o container falhar com **`Unrecognized option: -sharedDb`**, o Java estava recebendo flags do DynamoDB **antes** de `-jar DynamoDBLocal.jar`. O compose deste repo define **`entrypoint` + `command`** nessa ordem para evitar isso.

- **`DYNAMO_HOST_PORT`**: porta no host (default `8000`). Outro repositório na mesma máquina: `8001`, e no app `ENDPOINT_URL=http://localhost:8001` (também em `STAGE=TEST`, se definido).
- O serviço escuta na porta mapeada (default **http://127.0.0.1:8000**).

## NoSQL Workbench

1. Abra o **Operation builder** (ou **Visualizer**).
2. **Manage connections** → **DynamoDB local**.
3. URL do endpoint: `http://localhost:8000` (ou `http://127.0.0.1:8000`).
4. Região: por exemplo `sa-east-1` (deve bater com `Environments` / credenciais fictícias `test`).

## Tabela única (`ACADEMIC_CATALOG_TABLE_NAME`)

O nome físico segue o **CDK** (`iac/components/dynamo_construct.py`): `DevMediasAcademicCatalogTable-{stage}` em minúsculas no sufixo (ex.: `DevMediasAcademicCatalogTable-test` com `STAGE=TEST`). No app, se `ACADEMIC_CATALOG_TABLE_NAME` não estiver definido, `Environments` usa o mesmo padrão (`src/.../academic_catalog_naming.py`).

- **Partition key** (string): `pk`
- **Sort key** (string): `sk`

Itens de curso e disciplina compartilham a tabela:

- `pk` = `{GLOBAL|userId}#CURSO#{código}` ou `{GLOBAL|userId}#DISCIPLINA#{code}`
- `sk` = `METADATA` (registro canônico; reserva outras SKs no futuro)
- `entity_type` = `CURSO` | `DISCIPLINA` (filtro no scan)

`GLOBAL` = catálogo padrão (usuário não logado). Com usuário logado, instancie o repositório com `user_id` para ler/gravar só o escopo daquele dono.

Variável principal: **`ACADEMIC_CATALOG_TABLE_NAME`**. Ainda são aceitos, por compatibilidade: `ENTITY_TABLE_NAME`, `DISCIPLINA_TABLE_NAME`, `CURSO_TABLE_NAME`.

## Criar tabela e popular dados

- **`src/shared/infra/external/dynamo/academic_catalog_table_setup.py`** — função `ensure_academic_catalog_table()` (cria a tabela com `pk` / `sk` se não existir). Fica junto do código de infra Dynamo.

Na **raiz do repositório** (com o Dynamo Local no ar):

```bash
STAGE=TEST python iac/local/docker/dynamo/load_curso_mock_to_dynamo.py
STAGE=TEST python iac/local/docker/dynamo/load_disciplina_mock_to_dynamo.py
```

Cada loader chama o setup e grava no escopo **GLOBAL** a partir dos mocks em `src/shared/infra/repositories/*_mock.py`.

Se `ENDPOINT_URL` ou `ACADEMIC_CATALOG_TABLE_NAME` forem diferentes do default, exporte antes de rodar.
