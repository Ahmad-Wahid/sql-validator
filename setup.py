
from setuptools import setup, find_packages

def load_requirements(file):
    with open(file, "r") as f:
        requirements = f.read().split("\n")
    return requirements


setup(
    name="sql_validator",
    version="0.1",
    packages=find_packages(),
    description="A python package to validate SQL Queries",
    author="Ahmad Wahid",
    author_email="ahmedwahid16101@email.com",
    url="https://github.com/Ahmad-Wahid/sql-validator",
    install_requires=load_requirements("requirements.txt"),
    entry_points={
        "console_scripts": ["sql_validator=sql_validator.commands:commands"],
    },
)
