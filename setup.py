from setuptools import setup, find_packages

setup(
    name='sansPipe',
    version='1.3.11',
    description='Pipeline Utility for when there is no pipeline.',
    author='Adam Benson',
    author_email='AdamBenson.vfx@gmail.com',
    packages=find_packages(exclude=['setup.py', 'userSetup.py', '__init__.py']),
    include_package_data=True,
    py_modules=['sansPipe', 'sp_tools'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'sansPipe=sansPipe.sansPipe:main',
        ],
    },
)
