# Frappe Inspector GitHub Action

> Catch unsafe Frappe Framework and ERPNext changes before they reach production.

[![GitHub Action](https://img.shields.io/badge/GitHub_Action-v1-2088FF?logo=github-actions&logoColor=white)](https://github.com/Belius303/frappe-inspector-action)
[![Documentation](https://img.shields.io/badge/docs-Frappe_Inspector-0089FF)](https://github.com/Belius303/frappe-inspector-support/blob/main/docs/ci.md)

Frappe Inspector adds framework-aware static analysis to pull requests. It understands DocType schemas and related Python, JavaScript, hooks, patches, Custom Fields and Property Setters without executing project code.

Use **Community mode** for free static checks, or **Universal Pro migration mode** to compare schema changes against a Git baseline and generate machine-readable reports.

## What it catches

Depending on the selected mode, Frappe Inspector can report:

- references to removed DocType fields;
- field type and Link target changes;
- newly required fields without a default;
- uniqueness changes that can fail during migration;
- risky schema changes that need review;
- invalid or suspicious Frappe project references;
- common `hooks.py` and `patches.txt` problems;
- effective-schema changes from Custom Fields and Property Setters.

The Action can annotate files, write a GitHub job summary and fail the job at a configurable severity threshold.

## Free Community scan

No license key is required for `mode: scan`.

```yaml
name: Frappe checks

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  frappe-inspector:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: Belius303/frappe-inspector-action@v1
        with:
          mode: scan
          path: .
          fail-on: error
```

## Pro migration safety

Migration mode compares the current project with a Git baseline. Use `fetch-depth: 0` so the baseline ref is available.

Store your Universal Pro key as an encrypted Actions secret named `FRAPPE_INSPECTOR_LICENSE_KEY`. The key is masked and is never printed.

```yaml
name: Frappe migration safety

on:
  pull_request:

permissions:
  contents: read
  security-events: write

jobs:
  frappe-inspector:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: Belius303/frappe-inspector-action@v1
        with:
          path: .
          mode: migration
          base-ref: origin/${{ github.base_ref }}
          fail-on: error
          license-key: ${{ secrets.FRAPPE_INSPECTOR_LICENSE_KEY }}

      - uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: frappe-inspector.sarif
```

## Inputs

| Input | Required | Default | Description |
| --- | :---: | --- | --- |
| `path` | No | `.` | Frappe Bench or app path relative to the repository root |
| `mode` | No | `migration` | `scan` for Community checks or `migration` for Pro schema comparison |
| `base-ref` | Migration mode | — | Git ref used as the migration baseline |
| `fail-on` | No | `error` | Minimum finding severity that fails the job: `note`, `warning` or `error` |
| `include-safe` | No | `false` | Include safe additions in the migration report |
| `license-key` | Pro mode | — | Universal Pro key, passed from an encrypted GitHub secret |
| `markdown-file` | No | `frappe-inspector.md` | Markdown report path |
| `json-file` | No | `frappe-inspector.json` | Universal Pro JSON report path |
| `sarif-file` | No | `frappe-inspector.sarif` | Universal Pro SARIF report path |

## Outputs

| Output | Description |
| --- | --- |
| `errors` | Number of error findings |
| `warnings` | Number of warning findings |
| `risky` | Number of risky migration changes |
| `needs-review` | Number of migration changes requiring review |
| `sarif-file` | Generated SARIF report path |
| `json-file` | Generated JSON report path |

## Versioning

Use the stable major tag in workflows:

```yaml
- uses: Belius303/frappe-inspector-action@v1
```

## Privacy and security

- Analysis runs inside your GitHub Actions runner.
- Repository contents are not uploaded to Frappe Inspector for analysis.
- The Action does not execute Frappe project code.
- Pass license keys only through encrypted GitHub Actions secrets.
- Avoid printing or copying secrets into workflow logs.

## Documentation and support

- [Complete CI guide](https://github.com/Belius303/frappe-inspector-support/blob/main/docs/ci.md)
- [Community vs Pro](https://github.com/Belius303/frappe-inspector-support/blob/main/docs/free-vs-pro.md)
- [Pricing](https://frappeinspector.xyz/pricing)
- [Bug reports and feature requests](https://github.com/Belius303/frappe-inspector-support/issues)
- [Frappe Inspector website](https://frappeinspector.xyz)

Frappe Inspector is an independent third-party project and is not affiliated with or endorsed by Frappe Technologies, ERPNext or GitHub.
