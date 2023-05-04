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
    entry_points={
        'console_scripts': [
            'ingest_data=ingestion.spark.dataingestion:main',
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*"],
    },
    install_requires=[
    ],
    dependency_links=['https://cdn.mysql.com/Downloads/Connector-Python/mysql-connector-python-2.0.4.zip#md5'
                      '=3df394d89300db95163f17c843ef49df']

)
