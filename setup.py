from distutils.core import setup
import setuptools  # noqa


setup(
    name="websharecli",
    version="2.2.2",
    description="webshare.cz CLI downloader",
    author="Tomas Krizek",
    author_email="tomas.krizek@mailbox.org",
    url="https://github.com/tkrizek/websharecli",
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
    install_requires=[
        'blessings',
        'PyYAML',
        'requests',
        'xmltodict',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Environment :: Console',
        'Topic :: Communications :: File Sharing',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
)
