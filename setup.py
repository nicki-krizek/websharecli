from setuptools import setup
from pathlib import Path


def get_install_requires() -> list:
    """Returns requirements.txt parsed to a list"""
    fname = Path(__file__).parent / 'requirements.txt'
    targets = []
    if fname.exists():
        with open(fname, 'r') as f:
            targets = f.read().splitlines()
    return targets


setup(
    name="websharecli",
    version="2.2.3rc1",
    description="webshare.cz CLI downloader",
    author="Tomas Krizek",
    author_email="tomas.krizek@mailbox.org",
    url="https://github.com/tomaskrizek/websharecli",
    license="GPLv3",
    packages=['websharecli'],
    package_data={'websharecli': ['static/*']},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'webshare=websharecli.cli:main'
        ]
    },
    long_description=open('README.rst').read(),
    install_requires=get_install_requires(),
    # install_requires=[
    #     'blessings',
    #     'PyYAML',
    #     'requests',
    #     'xmltodict',
    # ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Environment :: Console',
        'Topic :: Communications :: File Sharing',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
)
