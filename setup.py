from distutils.core import setup


setup(
    name="webshare-downloader",
    version="1.0.0",
    description="webshare.cz CLI downloader",
    author="Tomas Krizek",
    author_email="tomas.krizek@mailbox.org",
    url="https://github.com/tomaskrizek/webshare-downloader",
    license="GPLv3",
    packages=['webshare'],
    entry_points={
        'console_scripts': [
            'webshare=webshare.cli:main'
        ]
    },
    long_description=open('README.md').read(),
    install_requires=[
        'PyYAML',
        'requests',
        'xmltodict',
    ],
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Environment :: Console',
        'Topic :: Communications :: File Sharing',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
)
