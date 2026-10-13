# DevMedias IAC (CDK)

## Dual stack (legacy iOS + V2)

| | Legacy (iOS) | V2 (Android / migração) |
|--|--------------|-------------------------|
| Git | branch `legacy` (tip de `prod` congelado) | `dev` / `homolog` / `prod` |
| CD | `CD-legacy.yml` (manual only) | `CD.yml` |
| `STACK_NAME` | `DevMediasStackprod` (hardcoded) | `DevMediasStackV2{stage}` |
| `GITHUB_REF_NAME` | `prod` (hardcoded) | `dev` \| `homolog` \| `prod` |
| `STACK_GENERATION` | (empty) | `v2` |
| SSM | n/a / historical | `/devmedias_v2/{stage}/…` |
| Physical names | original | include `-v2-` segment |

**Rule:** git branch name is not CDK stage. Never let `legacy` flow into `STACK_NAME` or `GITHUB_REF_NAME`.

**Do not** push Dynamo/V2 IAC onto `DevMediasStackprod` — that would replace CloudFront and break the iOS CDN.

Promote to git `prod` only after homolog V2 is validated, and only with `CD.yml` already in V2 mode.

## Useful commands

```bash
cdk ls
cdk synth
cdk diff
cdk deploy
```
