# settings.py
INSTALLED_APPS = [
    # ...
    "rest_framework",
    "drf_spectacular",
]
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
SPECTACULAR_SETTINGS = {
    "TITLE": "Billing portal API",
    "DESCRIPTION": "Invoices and customers for the billing portal.",
    "VERSION": "1.0.0",
}
