from setuptools import find_packages, setup

setup(
    name='bibliophiliac', 
    version='1.0.0',
    description='A Book Review App',
    author_email='judegachoki@gmail.com',
    packages=find_packages(),
    include_package_data=True, 
    zip_safe=False, 
    install_requires=[
        'flask',
    ],
)

