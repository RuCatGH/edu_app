from setuptools import setup, find_packages

setup(
    name="edu_platform",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "Django>=4.2.0",
        "psycopg2-binary>=2.9.0",
    ],
)
