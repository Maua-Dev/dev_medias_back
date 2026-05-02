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

## Tabela única (`ENTITY_TABLE_NAME`, default `devmedias_academic_catalog_table`)

- **Partition key** (string): `pk`
- **Sort key** (string): `sk`

Itens de curso e disciplina compartilham a tabela:

- `pk` = `{GLOBAL|userId}#CURSO#{código}` ou `{GLOBAL|userId}#DISCIPLINA#{code}`
- `sk` = `METADATA` (registro canônico; reserva outras SKs no futuro)
- `entity_type` = `CURSO` | `DISCIPLINA` (filtro no scan)

`GLOBAL` = catálogo padrão (usuário não logado). Com usuário logado, instancie o repositório com `user_id` para ler/gravar só o escopo daquele dono.

Variável de ambiente: **`ENTITY_TABLE_NAME`** (ou, por compatibilidade, `DISCIPLINA_TABLE_NAME` / `CURSO_TABLE_NAME`).
