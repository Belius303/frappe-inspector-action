# Frappe Inspector GitHub Action

> Frappe-aware security analysis, SARIF and migration safety for ERPNext pull requests.

[![GitHub Action](https://img.shields.io/badge/GitHub_Action-v1-2088FF?logo=github-actions&logoColor=white)](https://github.com/Belius303/frappe-inspector-action)
[![Documentation](https://img.shields.io/badge/docs-Frappe_Inspector-0089FF)](https://github.com/Belius303/frappe-inspector-support/blob/main/docs/ci.md)

Frappe Inspector adds framework-aware static analysis to pull requests. It understands DocType schemas and related Python, JavaScript, hooks, patches, Custom Fields, Property Setters, whitelisted endpoints, permission guards and unsafe migrations without executing project code.

On the 22-case controlled Frappe-specific benchmark, Frappe Inspector 1.4.0 detects all 20 expected findings with 0 false positives, including 3 migration-only findings. On the 17-finding generic subset, Bandit 1.9.4 detects 2 with 3 false positives, and Semgrep 1.172.0 detects 1 with 0 false positives. This is a controlled Frappe benchmark, not a global claim over every static analyzer.

## What it catches

Depending on the selected mode, Frappe Inspector can report:

- dynamic SQL and request-controlled query identifiers;
- guest endpoints that bypass permissions or expose documents;
- SSRF, filesystem path and dynamic execution sinks;
- client-only authorization gaps;
- references to removed DocType fields;
- field type and Link target changes;
- newly required fields without a default;
- uniqueness changes that can fail during migration;
- invalid or suspicious hooks and patches;
- effective-schema changes from Custom Fields and Property Setters.

The Action annotates files, writes a GitHub job summary and can upload SARIF for GitHub code scanning. Universal Pro can additionally apply CI policy and suppressions, report only new findings, maintain one bounded PR comment, and generate HTML, audit and migration-plan artifacts.

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

## Universal Pro migration safety

Migration mode compares the current project with a Git baseline. Use `fetch-depth: 0` so the baseline ref is available.

Store your Universal Pro key as an encrypted Actions secret named `FRAPPE_INSPECTOR_LICENSE_KEY`. The key is masked and is never printed.

The inputs below are implemented in the current worktree but are not available from the published Action `v1` yet. Keep existing `v1` workflows on the published input set, and do not grant `pull-requests: write` until a release includes `pr-comment`.

```yaml
name: Frappe migration safety

on:
  pull_request:

permissions:
  contents: read
  pull-requests: write
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
          new-only: true
          pr-comment: true
          github-token: ${{ github.token }}
          policy-file: .frappe-inspector/policy.json
          suppressions-file: .frappe-inspector/suppressions.json
          html-file: artifacts/frappe-inspector.html
          audit-file: artifacts/frappe-inspector-audit.json
          migration-plan-file: artifacts/frappe-inspector-plan.json
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
| `new-only` | No | `false` | Pro: report static findings not already present at `base-ref` |
| `pr-comment` | No | `false` | Pro: upsert one bounded PR summary comment; safely skips non-PR, tokenless, fork and forbidden contexts |
| `github-token` | PR comment | — | Token used only for the PR comment, normally `${{ github.token }}` |
| `policy-file` | No | — | Pro: JSON policy path; disabled when empty |
| `suppressions-file` | No | — | Pro: JSON suppressions path; disabled when empty |
| `license-key` | Pro mode | — | Universal Pro key, passed from an encrypted GitHub secret |
| `markdown-file` | No | `frappe-inspector.md` | Markdown report path |
| `json-file` | No | `frappe-inspector.json` | Universal Pro JSON report path |
| `sarif-file` | No | `frappe-inspector.sarif` | Universal Pro SARIF report path |
| `html-file` | No | — | Optional Pro HTML report path |
| `audit-file` | No | — | Optional Pro JSON audit report path |
| `migration-plan-file` | No | — | Optional Pro JSON migration plan path; requires `mode: migration` |

All new inputs are off by default. `policy-file` uses the versioned core policy schema. Rules may be disabled or assigned `note`, `warning` or `error`, and `minimumSeverity` can remove lower-severity findings:

```json
{
  "version": 1,
  "minimumSeverity": "warning",
  "rules": [
    { "ruleId": "FI044", "severity": "error" },
    { "ruleId": "FI030", "enabled": false }
  ]
}
```

`suppressions-file` uses the versioned core suppression schema loaded from the trusted base ref. Each entry requires an ID, justification, author, creation time and expiry. Applied, expired and unused entries are retained in `audit-file`:

```json
{
  "version": 1,
  "suppressions": [
    {
      "ruleId": "FI044",
      "path": "apps/sales/api.py",
      "justification": "URL is validated by the shared allowlist",
      "author": "security-team",
      "createdAt": "2026-08-02T00:00:00Z",
      "expiresAt": "2026-12-31T23:59:59Z"
    }
  ]
}
```

## Outputs

| Output | Description |
| --- | --- |
| `errors` | Number of error findings |
| `warnings` | Number of warning findings |
| `risky` | Number of risky migration changes |
| `needs-review` | Number of migration changes requiring review |
| `sarif-file` | Generated SARIF report path |
| `json-file` | Generated JSON report path |
| `html-file` | Generated HTML report path, or empty when disabled |
| `audit-file` | Generated audit JSON path, or empty when disabled |
| `migration-plan-file` | Generated migration plan path, or empty when disabled |

## Versioning

Use the stable major tag in workflows:

```yaml
- uses: Belius303/frappe-inspector-action@v1
```

## Evidence and support

- [Benchmark methodology](https://github.com/Belius303/frappe-inspector-support/blob/main/docs/benchmarks.md)
- [Complete CI guide](https://github.com/Belius303/frappe-inspector-support/blob/main/docs/ci.md)
- [Community vs Pro](https://github.com/Belius303/frappe-inspector-support/blob/main/docs/free-vs-pro.md)
- [Pricing](https://frappeinspector.xyz/pricing)
- [Bug reports and feature requests](https://github.com/Belius303/frappe-inspector-support/issues)
- [Frappe Inspector website](https://frappeinspector.xyz)

Frappe Inspector is independent third-party software and is not affiliated with or endorsed by Frappe Technologies, ERPNext or GitHub.
