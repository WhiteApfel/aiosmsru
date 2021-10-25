from os import environ

from setuptools import find_packages, setup

classifiers = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries",
]

with open("README.md", "r") as f:
    readme = f.read()


def requirements():
    with open("requirements.txt", "r") as req:
        return [r for r in req.read().split("\n") if r]


setup(
    name="aiosmsru",
    version=environ.get("TAG_VERSION").replace("v", ""),
    author="WhiteApfel",
    author_email="white@pfel.ru",
    url="https://github.com/WhiteApfel/aiosmsru",
    packages=find_packages("."),
    description="(A)sync client for sms.ru with pydantic responses",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="Mozilla Public License 2.0",
    classifiers=classifiers,
    keywords="sms wrapper api russia",
    install_requires=requirements(),
)
