# Frappe Inspector GitHub Action

Block unsafe Frappe Framework and ERPNext schema changes during pull requests.

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
          base-ref: origin/${{ github.base_ref }}
          license-key: ${{ secrets.FRAPPE_INSPECTOR_LICENSE_KEY }}
      - uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: frappe-inspector.sarif
```

The Action annotates changed files, writes a job summary and fails when the configured severity threshold is reached. `mode: scan` provides Community static checks. `mode: migration` and SARIF/JSON outputs require Universal Pro.

Use `fetch-depth: 0` so the baseline ref is available. Store the license in an encrypted Actions secret; it is masked and never printed.

Documentation and support: https://github.com/Belius303/frappe-inspector-support
