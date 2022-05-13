from setuptools import find_packages, setup

setup(
    name='FAIR metrics tests for Rare Disease research',
    version='0.1.0',
    url='https://github.com/LUMC-BioSemantics/RD-FAIRmetric-F4.git',
    author='Vincent Emonet',
    author_email='vincent.emonet@gmail.com',
    description='FAIR metrics tests service for Rare Disease research.',
    packages=find_packages(),
    install_requires=open("requirements.txt", "r").readlines(),
)