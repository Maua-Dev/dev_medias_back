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

## Legacy JSON export (V2 → iOS S3)

Lambda `export_legacy_catalog` (stack **V2**) scans Dynamo `DevMediasAcademicCatalogTable-v2-{stage}`
and writes legacy keys to the **legacy** subject bucket (not `*-v2-*`).

| Env | Purpose | Prod value |
|-----|---------|------------|
| `LEGACY_EXPORT_BUCKET_NAME` | Destination bucket | `devmediasstackprod-subjectstacksubjectbucket927c88-tglqq1xpktvo` |
| `LEGACY_EXPORT_SUBJECTS_KEY` | Subjects key | `allSubjects.json` |
| `LEGACY_EXPORT_COURSES_KEY` | Courses key | `courses.json` |
| `LEGACY_EXPORT_CLOUDFRONT_DISTRIBUTION_ID` | CDN invalidate | `E1XC2LFUOQ5S4N` (`d3c1aqxshha6rg.cloudfront.net`) |

When `LEGACY_EXPORT_BUCKET_NAME` is set (prod CD):

- IAM `s3:PutObject` on that bucket via `Bucket.from_bucket_name`
- EventBridge weekly: `cron(0 12 ? * SUN *)` UTC
- Manual invoke still works

### Bucket versioning (legado, one-shot CLI)

Applied outside CDK on the legacy subject bucket (avoids redeploying `DevMediasStackprod`):

- Versioning **Enabled**
- Lifecycle: keep **1** newer noncurrent version + expire noncurrent after **14** days

Rollback versioning:

```bash
aws s3api put-bucket-versioning \
  --bucket devmediasstackprod-subjectstacksubjectbucket927c88-tglqq1xpktvo \
  --versioning-configuration Status=Suspended \
  --profile AWSPowerUserAccessProd
```

### Smoke

```bash
aws lambda invoke \
  --function-name export_legacy_catalog-DevMediasStackV2prod-Prod \
  --profile AWSPowerUserAccessProd \
  /tmp/export-out.json && cat /tmp/export-out.json

aws s3api list-object-versions \
  --bucket devmediasstackprod-subjectstacksubjectbucket927c88-tglqq1xpktvo \
  --prefix allSubjects.json \
  --profile AWSPowerUserAccessProd
```

CDN: `https://d3c1aqxshha6rg.cloudfront.net/allSubjects.json`

## Useful commands

```bash
cdk ls
cdk synth
cdk diff
cdk deploy
```
