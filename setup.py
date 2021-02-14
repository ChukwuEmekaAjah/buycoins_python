from setuptools import setup, find_packages
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(name='buycoins_client', 
    version='1.4.2', 
    description='Buycoins API Python client', 
    url='https://github.com/ChukwuEmekaAjah/buycoins_python', 
    author='Chukwuemeka Ajah', 
    author_email='talk2ajah@gmail.com', 
    license='MIT', 
    packages=find_packages(), 
    install_requires=['requests'], 
    zip_safe=True, 
    long_description=README, 
    long_description_content_type='text/markdown'
)