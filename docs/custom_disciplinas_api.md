## Custom disciplinas (device-scoped)

App Flutter envia `X-Device-Id: <uuid>` (gerado no device, sem login). Catálogo oficial continua público; matérias custom ficam no partition Dynamo do `device_id`.

### Persistência (sem migration de tabela)

Tabela single-table existente (`ACADEMIC_CATALOG`):

| Campo | Catálogo | Custom |
|-------|----------|--------|
| PK | `GLOBAL#DISCIPLINA#{code}` | `{device_id}#DISCIPLINA#{code}` |
| SK | `METADATA` | `METADATA` |
| `device_id` | `null` | UUID do header |
| `is_custom` | `false` | `true` |

Constraint natural: `code` único por owner (PK). Índice por `device_id` = scan/`begins_with` no prefixo `{device_id}#DISCIPLINA#`.

Não há coluna nova em tabela separada — só atributos na entity + isolamento por PK.

### Header

```
X-Device-Id: 550e8400-e29b-41d4-a716-446655440000
```

- Ausente ou UUID inválido nas rotas custom → **400**
- Em `GET get-all-disciplinas`: header **opcional**; se presente e válido, merge das customs; se presente e inválido → **400**

---

### 1) GET `/mss-medias/get-all-disciplinas`

**Sem header** — só catálogo:

```http
GET /mss-medias/get-all-disciplinas
```

```json
[
  {
    "course": "ECM",
    "name": "Engenharia de Computação",
    "code": "ECM101",
    "period": "2024.1",
    "exam_weight": 0.6,
    "assignment_weight": 0.4,
    "exams": [{"name": "P1", "weight": 0.6}],
    "assignments": [{"name": "T1", "weight": 0.4}],
    "courses": {"ECM": 4},
    "study_plan_download_pdf_url": "https://...",
    "exams_code": "C4/2015",
    "device_id": null,
    "is_custom": false,
    "created_at": null,
    "updated_at": null
  }
]
```

**Com `X-Device-Id`** — catálogo + customs daquele device (lista; customs no final):

```http
GET /mss-medias/get-all-disciplinas
X-Device-Id: 550e8400-e29b-41d4-a716-446655440000
```

Item custom (shape compatível com `CourseModel`):

```json
{
  "course": "CUSTOM",
  "name": "Minha matéria",
  "code": "MIN001",
  "period": "",
  "exam_weight": 0.7,
  "assignment_weight": 0.3,
  "exams": [{"name": "P1", "weight": 1.0}],
  "assignments": [],
  "courses": {},
  "study_plan_download_pdf_url": null,
  "exams_code": null,
  "device_id": "550e8400-e29b-41d4-a716-446655440000",
  "is_custom": true,
  "created_at": "2026-10-02T15:00:00Z",
  "updated_at": "2026-10-02T15:00:00Z"
}
```

Device A **nunca** vê customs do device B.

---

### 2) POST `/mss-medias/create-custom-disciplina`

```http
POST /mss-medias/create-custom-disciplina
X-Device-Id: 550e8400-e29b-41d4-a716-446655440000
Content-Type: application/json

{
  "code": "MIN001",
  "name": "Minha matéria",
  "period": "2026.1",
  "examWeight": 0.7,
  "assignmentWeight": 0.3,
  "exams": [{"name": "P1", "weight": 1.0}],
  "assignments": []
}
```

- Mínimo: `name`, `code`
- Aceita snake_case ou camelCase (`examWeight` / `exam_weight`, …)
- `device_id` / `deviceId` no body → **400** (só header)
- **201** matéria criada (`is_custom: true`, `device_id` do header)
- **409** se `code` já existe para aquele device
- **403** se o device já tem **20** matérias custom (limite por `device_id`)
- **400** header/campos inválidos

---

### 3) PUT `/mss-medias/update-custom-disciplina`

```http
PUT /mss-medias/update-custom-disciplina
X-Device-Id: 550e8400-e29b-41d4-a716-446655440000
Content-Type: application/json

{
  "code": "MIN001",
  "name": "Nome atualizado",
  "exam_weight": 0.6,
  "assignment_weight": 0.4
}
```

- `code` no body (ou query `?code=MIN001`)
- Só atualiza se existir no partition do `device_id` e `is_custom`
- Catálogo / outro device → **404** (não vaza existência)
- **200** matéria atualizada

---

### 4) DELETE `/mss-medias/delete-custom-disciplina`

```http
DELETE /mss-medias/delete-custom-disciplina?code=MIN001
X-Device-Id: 550e8400-e29b-41d4-a716-446655440000
```

ou body `{"code":"MIN001"}`.

- Mesma regra de ownership
- Nunca remove item `GLOBAL` por esta rota
- **200** com a matéria removida; **404** se não achar no device

---

### Breaking changes

- Resposta de `get-all-disciplinas` passa a incluir campos `device_id`, `is_custom`, `created_at`, `updated_at` (defaults seguros para catálogo). Front que já normaliza snake/camel continua ok.
- Com `X-Device-Id` inválido no GET, passa a retornar **400** (antes o header era ignorado).
- Paths novos; GET path inalterado.

### Rate limit

Throttle dedicado no POST não foi ligado a API key (app público). Recomendado: throttle de stage no API Gateway / WAF se spam aparecer. `create-curso` admin continua com API key.
