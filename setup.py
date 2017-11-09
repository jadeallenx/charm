from setuptools import setup

setup(
    name="charm",
    version="0.1",
    packages=["charm"],
    scripts=['bin/fetch_upstream_resource_files.py'],
    install_requires=[
        'rsa',
        'requests',
        'bottle'
        ],
    package_data = {'': ['*.proto']},
    author="Mark Allen",
    author_email="mrallen1@yahoo.com",
    description="A lightweight hex package distribution service for Erlang/Elixir",
    license="Apache 2",
    keywords="package management elixir erlang",
    url="https://github.com/mrallen1/charm",
    long_description=open("README.md", "rb").read(),
    zip_safe=True,
)

