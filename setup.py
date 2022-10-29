import os
import re

from setuptools import find_packages, setup

ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')

requires = [
    'pandas>=1.4.1',
    'minio>=7.1.5',
    'pyarrow>=7.0.0',
    'fastparquet>=0.8.0',
    's3fs>=2022.2.0',
    'requests>=2.27.1',
    'awswrangler>=2.16.1'
]


def get_version():
    init = open(os.path.join(ROOT, 'forecast_client', '__init__.py')).read()
    return VERSION_RE.search(init).group(1)


setup(
    name='forecast_client',
    version=get_version(),
    description='The Forecast API SDK for Python',
    long_description=open('README.rst').read(),
    author='RamonAmez',
    url='https://github.com/ramonAV98/forecast_client',
    packages=find_packages(exclude=['tests*']),
    package_data={"forecast_client": ["data/endpoints.json"]},
    include_package_data=True,
    install_requires=requires,
    python_requires=">=3.7",
    project_urls={
        'Source': 'https://github.com/ramonAV98/forecast_client',
    }
)
