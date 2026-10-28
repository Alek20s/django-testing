# Django Automated Testing

A Python project demonstrating automated testing of Django web applications. The repository contains tests for two applications: **YaNews** and **YaNote**.

The project focuses on verifying application behaviour, access permissions, page availability, form handling, redirects, and response content. It demonstrates a structured, repeatable approach to testing web applications and checking that requirements are met.

## Testing Skills Demonstrated

- **Python test automation** using `pytest` and Django's `unittest`-based test classes.
- **Web application testing** with Django's test client.
- **Test design** using fixtures, parametrised test cases, and reusable test setup.
- **Route and access-control testing**, including HTTP status codes, redirects, and permissions for authenticated and anonymous users.
- **Functional testing** of application logic, forms, and page content.
- **Database-aware testing** for Django models and application behaviour.
- **Regression testing** to help identify unintended changes when the application is updated.

## Applications Covered

### YaNews

Automated tests cover routes, page content, and application logic. The tests check page responses, expected redirects, and behaviour for users with different permissions.

### YaNote

Automated tests cover base functionality, routes, page content, and application logic. They check access to note-related pages, user permissions, and expected application behaviour.

## Technology Stack

- Python
- Django 5.1
- pytest
- pytest-django
- Django test client
- SQLite / Django test database configuration

## Project Structure

```text
django-testing/
├── ya_news/
│   └── news/pytest_tests/
│       ├── conftest.py
│       ├── test_content.py
│       ├── test_logic.py
│       └── test_routes.py
├── ya_note/
│   └── notes/tests/
│       ├── test_base.py
│       ├── test_content.py
│       ├── test_logic.py
│       └── test_routes.py
├── requirements.txt
├── run_tests.sh
└── README.md
```

## Installation

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv venv
```

Windows:

```powershell
venv\Scripts\activate
```

macOS / Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Tests

From the project root, run the supplied test script:

```bash
bash run_tests.sh
```

The script runs the project's automated checks. Review the output to see whether the tests pass.

## Relevance to Software Test Analyst Roles

This project provides practical examples of Python-based automated testing, test-case design, web application validation, access-control checks, and regression testing. These are transferable skills for quality assurance work alongside developers and business analysts.

The repository currently demonstrates Django test-client testing; it does **not** claim to implement Selenium browser automation, Postman/ReadyAPI API testing, or SQL Server stored-procedure testing.

