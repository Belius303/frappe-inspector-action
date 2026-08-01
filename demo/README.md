# Frappe Inspector Action Demo

This fixture intentionally contains Frappe-specific security findings:

- whitelisted request data reaching dynamic SQL through a local helper;
- a guest endpoint using `ignore_permissions=True` without a visible guard;
- request-controlled data reaching an outbound HTTP request.

The `Frappe Inspector Demo` workflow runs the public Action against this fixture, writes annotations and a GitHub job summary, uploads the Markdown report, and uploads SARIF when the repository has a Universal Pro secret configured.
