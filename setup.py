from setuptools import setup, find_namespace_packages

setup(
    name="edu_platform",
    version="0.1",
    package_dir={"": "edu_platform"},
    packages=find_namespace_packages(include=["edu_platform*"]),
    install_requires=[
        "Django>=4.2.0",
        "psycopg2-binary>=2.9.0",
    ],
)
