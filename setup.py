from setuptools import setup

setup(
    name="pyrbn",
    version="1.0.0",
    author="Adam Faulconbridge",
    author_email="afaulconbridge@googlemail.com",
    packages=["pyrbn"],
    description="pyrbn is a python random boolean network library.",
    long_description=open("README.md").read(),
    install_requires=[],
    extras_require={
        "dev": [
            "pytest-cov",
            "flake8",
            "pylint",
            "pip-tools",
            "pipdeptree",
            "pre-commit",
        ]
    },
)
