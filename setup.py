from setuptools import setup
from setuptools import find_packages

version = "0.0.5"
name = "solgraphPlus"

setup(
    name=name,
    version=version,
    packages=find_packages(),
    author="t0hka",
    author_email="s4ndalph0n.t0hka@gmail.com",
    description=(
        "An upgraded version of Solgraph:Display function information in the contract"),
    keywords=["solidity","dot","graph"],
    url="https://github.com/VelitasDao/Solgraph-Plus",
    install_requires=["jsonpath==0.82","graphviz==0.20.1","solidityParserPlus==0.0.4"],
)
