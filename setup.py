#!/usr/bin/env python
"""Setup.py for Hiccup server project."""

from setuptools import setup, find_packages

with open("README.md") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="hiccup",
    version="1.0.1",
    description="Hiccup crash reporting server",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Fairphone B.V.",
    packages=find_packages(),
    package_data={"": ["*.html", "*.css", "*.js"]},
    python_requires="==3.6.*",
    scripts=["manage.py"],
    install_requires=[
        "certifi==2018.8.24",
        "chardet==3.0.4",
        "coreapi==2.3.3",
        "coreschema==0.0.4",
        "defusedxml==0.5.0",
        "Django==1.11.14",
        "django-allauth==0.36.0",
        "django-bootstrap-form==3.4",
        "django-bootstrap3==10.0.1",
        "django-crispy-forms==1.7.2",
        "django-extensions==2.1.0",
        "django-filter==2.0.0",
        "django-frontend==1.8.0",
        "django-frontend-skeleton==3.0.0",
        "django-taggit==0.22.2",
        "djangorestframework==3.8.2",
        "drf-yasg==1.10.0",
        "future==0.16.0",
        "idna==2.7",
        "inflection==0.3.1",
        "itypes==1.1.0",
        "Jinja2==2.10",
        "MarkupSafe==1.0",
        "oauthlib==2.1.0",
        "openapi-codec==1.3.2",
        "pluggy==0.7.1",
        "psycopg2==2.7.5",
        "py==1.6.0",
        "python3-openid==3.1.0",
        "pytz==2018.5",
        "requests==2.19.1",
        "requests-oauthlib==1.0.0",
        "ruamel.yaml==0.15.64",
        "six==1.11.0",
        "uritemplate==3.0.0",
        "urllib3==1.23",
    ],
)
