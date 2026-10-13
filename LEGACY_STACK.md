# Legacy stack freeze (iOS CDN)

This branch is frozen at the tip of `prod` that matches the live CloudFormation stack
`DevMediasStackprod` (account prod).

## Do not

- Rename the CloudFormation stack
- Let `GITHUB_REF_NAME` or `STACK_NAME` become `legacy` in CDK
- Merge `dev` / Dynamo IAC into this branch
- Disable termination protection on `DevMediasStackprod`

## Deploy

Use workflow `CD-legacy` (`workflow_dispatch` only). It hardcodes:

- `STACK_NAME=DevMediasStackprod`
- `GITHUB_REF_NAME=prod`

## Inventory (prod, us-east-1)

- Stack: `DevMediasStackprod` (termination protection enabled)
- Plans CloudFront: `E9X3EUABIC5YU` → `d37dze3m2lalwe.cloudfront.net`
- Subjects CloudFront: `E1XC2LFUOQ5S4N` → `d3c1aqxshha6rg.cloudfront.net`
- Plans bucket: `devmediasstackprod-plansstackplansbucket699f4d02-m8ewfz392smg`
- Subjects bucket: `devmediasstackprod-subjectstacksubjectbucket927c88-tglqq1xpktvo`
