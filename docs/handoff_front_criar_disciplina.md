# Handoff Front — Tela Criar Disciplina Custom

**Para:** agente/dev Flutter (Dev Médias)  
**De:** backend  
**Status backend:** implementado (unit tests ok). Deploy cloud pode ainda não estar no ar — confirmar URL do stage antes de integrar.  
**Doc técnico completo:** `docs/custom_disciplinas_api.md` (repo back)

---

## Objetivo da tela

Permitir que o usuário crie uma matéria personalizada, persistida no backend, escopada ao device (sem login).

Fluxo mínimo MVP desta tela:
1. Garantir `deviceId` local (UUID)
2. Formulário → POST create
3. Em sucesso: atualizar lista local / refetch GET subjects com o mesmo header
4. Tratar 409 (código duplicado) e 400

Edit/delete podem vir em seguida com os mesmos contratos (seção “Próximos”).

---

## Pré-requisito: `deviceId`

| Item | Detalhe |
|------|---------|
| Quando | 1º open do app (ou antes da 1ª call de custom/GET com merge) |
| Formato | UUID v4 string, ex. `550e8400-e29b-41d4-a716-446655440000` |
| Persistência | SharedPreferences / Hive — **nunca regenerar** se já existir |
| Envio | Header **`X-Device-Id`** em toda request de custom (e no GET se quiser ver as customs) |
| Body | **Não** enviar `deviceId` / `device_id` no JSON → backend retorna 400 |

---

## Base path

Padrão API Gateway deste MSS:

```
{API_BASE}/mss-medias/...
```

Endpoints novos (nomes literais do back, kebab-case):

| Ação | Método | Path relativo a `/mss-medias` |
|------|--------|-------------------------------|
| Listar (catálogo ± customs) | `GET` | `/get-all-disciplinas` |
| **Criar custom** | `POST` | `/create-custom-disciplina` |
| Atualizar custom | `PUT` | `/update-custom-disciplina` |
| Deletar custom | `DELETE` | `/delete-custom-disciplina` |

Sugestão env:

```dart
// exemplo
API_SUBJECTS = '$API_BASE/mss-medias/get-all-disciplinas'
API_CREATE_CUSTOM_SUBJECT = '$API_BASE/mss-medias/create-custom-disciplina'
```

---

## POST criar — contrato da tela

### Request

```http
POST /mss-medias/create-custom-disciplina
X-Device-Id: <uuid-do-device>
Content-Type: application/json
```

```json
{
  "code": "MIN001",
  "name": "Minha matéria",
  "period": "2026.1",
  "examWeight": 0.7,
  "assignmentWeight": 0.3,
  "exams": [
    { "name": "P1", "weight": 1.0 }
  ],
  "assignments": [
    { "name": "T1", "weight": 1.0 }
  ],
  "courses": {},
  "examsCode": null
}
```

Backend aceita **camelCase ou snake_case** (`examWeight` / `exam_weight`, etc.). Preferir o mesmo estilo do `CourseModel` (camelCase no Dart → JSON).

### Campos

| Campo | Obrigatório | Default se omitido | Notas UI |
|-------|-------------|--------------------|----------|
| `code` | **sim** | — | string não vazia; único **por device** |
| `name` | **sim** | — | string não vazia |
| `period` | não | `""` | opcional na UI |
| `examWeight` | não | `0.5` | double |
| `assignmentWeight` | não | `0.5` | double |
| `exams` | não | `[]` | lista `{name, weight}` |
| `assignments` | não | `[]` | lista `{name, weight}` |
| `courses` | não | `{}` | map curso→ano; custom pode mandar `{}` |
| `course` | não | `"CUSTOM"` | string; pouco relevante no app |
| `examsCode` | não | `null` | opcional |
| `studyPlanDownloadPdfUrl` | — | sempre `null` no create | **não enviar** / ignorar |
| `deviceId` | — | — | **proibido no body** |
| `isCustom` | — | setado pelo back | não enviar |

### Response 201

Mesmo shape que o front já parseia em subjects + flags novas:

```json
{
  "course": "CUSTOM",
  "name": "Minha matéria",
  "code": "MIN001",
  "period": "2026.1",
  "exam_weight": 0.7,
  "assignment_weight": 0.3,
  "exams": [{ "name": "P1", "weight": 1.0 }],
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

Resposta do back hoje vem em **snake_case** (`exam_weight`, `is_custom`, …). O normalizador atual do front (`examWeight` / `exam_weight`) cobre isso.

### Erros que a tela deve tratar

| Status | Quando | UX sugerida |
|--------|--------|-------------|
| **201** | ok | Fechar form / toast sucesso / refetch lista |
| **400** | sem header, UUID inválido, `name`/`code` vazio, tipos errados, `deviceId` no body | Mensagem genérica ou do body (string) |
| **409** | `code` já existe **neste** device | “Já existe uma matéria com esse código” + focar campo code |
| **5xx** | falha servidor | retry / erro genérico |

Body de erro costuma ser **string** (não objeto), ex.: `"The item alredy exists for this code"`.

---

## GET lista — após criar / na home

```http
GET /mss-medias/get-all-disciplinas
X-Device-Id: <uuid>
```

- **Sem** header → só catálogo oficial  
- **Com** UUID válido → catálogo + customs do device (`is_custom: true` nas customs)  
- Header **presente mas inválido** → **400** (não enviar string vazia / lixo)

Lista JSON (array). Customs vêm **depois** do catálogo.

**Importante para UI:** usar `isCustom == true` (ou `is_custom`) para:
- mostrar badge “Personalizada”
- habilitar editar/excluir só nessas
- **nunca** oferecer edit/delete em item de catálogo

Campos novos no GET (breaking light): `device_id`, `is_custom`, `created_at`, `updated_at` — catálogo vem com `is_custom: false`, `device_id: null`.

---

## Sugestão de formulário (MVP)

Campos mínimos na tela:
1. **Nome** (`name`) — required  
2. **Código** (`code`) — required; validar não vazio; opcional: uppercase / alfanumérico  
3. **Período** (`period`) — opcional  
4. **Peso provas / trabalhos** (`examWeight`, `assignmentWeight`) — defaults 0.5/0.5 ou UI com sliders que somem 1.0 (back **não** valida soma = 1)  
5. Lista dinâmica **Provas** / **Trabalhos** — cada item `name` + `weight`

Botão salvar → POST → se 201, invalidar cache de subjects e voltar.

---

## Checklist implementação front

- [ ] Gerar + persistir UUID `deviceId` no 1º uso  
- [ ] Interceptor / client HTTP: injetar `X-Device-Id` nas rotas de subjects custom + GET subjects  
- [ ] Extender `CourseModel` (ou equivalente) com `isCustom`, `deviceId?`, timestamps opcionais  
- [ ] Tela criar → POST `create-custom-disciplina`  
- [ ] Tratar 409 no campo código  
- [ ] Após criar: GET com header e mesclar na UI (ou usar body 201)  
- [ ] Não permitir editar/apagar matérias com `isCustom != true`  
- [ ] Confirmar `API_BASE` do stage (dev/homolog) após deploy do back  

---

## Próximos (fora do MVP da tela criar, já no back)

**PUT** `/update-custom-disciplina` — body com `code` + campos a alterar + header  
**DELETE** `/delete-custom-disciplina?code=...` — header obrigatório  

Ownership: outro device / catálogo → **404** (não 403), de propósito.

---

## Fora de escopo (não implementar agora)

- Login / OAuth  
- Migração de device / código de recuperação  
- Sync de notas (continuam no Hive local)  
- Criar/editar matérias do catálogo oficial pelo app  

---

## Smoke manual rápido (quando API estiver deployada)

```bash
DEVICE=550e8400-e29b-41d4-a716-446655440000
BASE=https://<api-id>.execute-api.<region>.amazonaws.com/<stage>/mss-medias

curl -s -X POST "$BASE/create-custom-disciplina" \
  -H "Content-Type: application/json" \
  -H "X-Device-Id: $DEVICE" \
  -d '{"code":"MIN001","name":"Teste Front","examWeight":0.7,"assignmentWeight":0.3,"exams":[{"name":"P1","weight":1}]}'

curl -s "$BASE/get-all-disciplinas" -H "X-Device-Id: $DEVICE" | head
```
