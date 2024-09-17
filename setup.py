from setuptools import setup, find_packages

setup(
    name='sansPipe',
    version='1.2.10',
    description='Pipeline Utility for when there is no pipeline.',
    author='Adam Benson',
    author_email='AdamBenson.vfx@gmail.com',
    packages=find_packages(exclude=['setup.py', 'userSetup.py', '__init__.py']),
    include_package_data=True,
    py_modules=['sansPipe'],  # Include other files (like resources) specified in MANIFEST.in
    install_requires=[],  # List any external dependencies (PySide6 not needed since Maya includes it)
    entry_points={
        'console_scripts': [
            'sansPipe=sansPipe.sansPipe:main',  # Adjust 'main' to be the entry point function in sansPipe.py
        ],
    },
)
