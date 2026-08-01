import frappe
import requests


def run_customer_search(value):
    query = f"select name from tabCustomer where name = {value}"
    return frappe.db.sql(query)


@frappe.whitelist()
def search_customers(term):
    return run_customer_search(term)


@frappe.whitelist(allow_guest=True)
def update_customer(name):
    doc = frappe.get_doc("Customer", name)
    doc.save(ignore_permissions=True)


@frappe.whitelist()
def fetch_preview(url):
    return requests.get(url).text
