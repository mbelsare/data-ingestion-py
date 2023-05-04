from setuptools import find_packages, setup


def readme():
    with open("README.md") as f:
        return f.read()


def requirements():
    with open("./requirements.txt") as f:
        return f.read()


setup(
    name="data-ingestion-py",
    version="0.0.1",
    author="Manish",
    description="Data Ingestion using Python and PySpark",
    long_description=readme(),
    maintainer='Manish Belsare',
    maintainer_email='manishbelsare2003@gmail.com',
    url="https://github.com/mbelsare/data-ingestion-py",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": ["*"],
    },
    install_requires=[
    ],
    dependency_links=[],
)