"""
The setup.py file is an essential part of the Python packaging ecosystem.
It is a script that helps you to package and distribute your code.
It is the standard way to package and distribute Python libraries.
It is a Python script that defines the metadata about your Python package
(such as its name, version, author, etc.) and the dependencies that it requires.
"""
from setuptools import setup, find_packages
from typing import List


def get_requirements() -> List:
    """
    Read the requirements.txt file and return the list of dependencies
    """
    requirement_list: List[str] = []

    try:
        with open("requirements.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                # ignore empty lines and -e .
                if requirement and requirement != "-e .":
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")

    return requirement_list


setup(
    name="Network Security",
    version="0.0.1",
    author="Danny",
    packages=find_packages(),
    install_requires=get_requirements(),
)
