Webshare.cz CLI Downloader
==========================

| CLI interface for getting download links for movies and TV shows from
| webshare.cz.

Installation
------------
using source distribution, tested with Python 3.7, Debian Buster

create source distribution and install with pip

.. code:: bash

    $ python3 setup.py sdist
    $ pip3 install dist/websharecli-*.tar.gz

Customizing configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

Customize config in order to:

-  Activate VIP
-  Change default preferred video quality

See instructions in config file.

.. code:: bash

    $ vi ~/.config/webshare/config.yaml

Usage
-----

Search a download link of a single file
~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ webshare link-search matrix 1999 > link
    matrix 1999: The.Matrix.1999.BluRay.1080p.DTS-HDMA.AC3.x264.dxva-FraMeSToR (CZ,EN).mkv
    $ wget -i link

Search for download links of an entire series
~~~~~~~~~~~~~~~~~~~~~~~~~

Use asterisk (``*``) symbol to as a 00-99 wildcard.

.. code:: bash

    $ webshare link-search black mirror s02e* > links
    black mirror s03e00: Black Mirror S03E00 White Christmas CZtit.mp4
    black mirror s03e01: Black.Mirror.S03E01.PROPER.1080p.WEBRip.X264-DEFLATE.mkv
    black mirror s03e02: Black.Mirror.S03E02.PROPER.1080p.WEBRip.X264-DEFLATE.mkv
    black mirror s03e03: Black.Mirror.S03E03.PROPER.1080p.WEBRip.X264-DEFLATE.mkv
    black mirror s03e04: Black.Mirror.S03E04.PROPER.1080p.WEBRip.X264-DEFLATE.mkv
    black mirror s03e05: Black.Mirror.S03E05.1080p.WEBRip.X264-DEFLATE.mkv
    black mirror s03e06: Black.Mirror.S03E06.1080p.WEBRip.X264-DEFLATE.mkv
    black mirror s03e07: NOT FOUND
    black mirror s03e08: NOT FOUND
    black mirror s03e09: NOT FOUND
    Aborting after 3 failures
    $ wget -i links

List files
~~~~~~~~~~~~~~~~~

.. code:: bash

    $ webshare link-list requirem for a dream
     1.  12G mkv +0 76s2uj1ir4 Requiem.For.A.Dream.Director's.Cut.2000.1080p.BluRay.DTS.x264-DON.mkv
     2.  67K srt +0 5394mr11r1 Requiem.For.A.Dream.Director's.Cut.2000.1080p.BluRay.DTS.x264-DON.srt
     3. 1.7G mkv +1 5uR4b05kh2 Requiem for a Dream 2000 Unrated DC (1080p x265 10bit Tigole).mkv
     4. 1.4G mp4 +0 10z3ja4Xq2 Requiem.For.A.Dream.DIRECTORS.CUT.2000.1080p.BrRip.x264.YIFY.mp4
     5.  71K srt +0 28s39750D3 Requiem.For.A.Dream.DIRECTORS.CUT.2000.1080p.BrRip.x264.YIFY.srt
     6. 4.5G mkv +0 4Pr5rz6z13 Requiem.For.A.Dream.720p.x264.AC3-5.1-DiC.mkv
     7. 700M mp4 +0 15i6n36R32 Requiem.For.A.Dream.DIRECTORS.CUT.2000.720p.BrRip.x264.YIFY.mp4
     8. 1.2G avi +1 KRdAgRvv4F Requiem za sen (Requiem For a Dream).avi

Get download link using file id or file url
~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ webshare link-id 76s2uj1ir4 > link
    $ wget -i link

.. code:: bash

    $ webshare link-url https://webshare.cz/#/file/4jw52F2kv4/mocny-vladce-oz-2013-cz-dabing-brrip-xvid-avi > link
    $ wget -i link

Directly download the obtained link
~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ webshare link-search matrix 1999 --download
    $ webshare link-id 76s2uj1ir4 --download
    $ webshare link-url https://webshare.cz/#/file/4jw52F2kv4/mocny-vladce-oz-2013-cz-dabing-brrip-xvid-avi --download

Directly download the obtained link through TOR
~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ webshare link-search matrix 1999 --download --tor
    $ webshare link-id 76s2uj1ir4 --download --tor
    $ webshare link-url https://webshare.cz/#/file/4jw52F2kv4/mocny-vladce-oz-2013-cz-dabing-brrip-xvid-avi --download --tor

Exception below shows when tor is configured incorrectly

    Failed to establish a new connection: [Errno 111] Connection refused')

make sure you have tor installed

.. code:: bash

    $ apt install tor

make sure tor service is running

.. code:: bash

    $ systemctl status tor
    $ systemctl start tor

make sure tor runs on localhost:9050 (default), otherwise edit SocksPort in /etc/tor/torrc

.. code:: bash

    $ grep SocksPort /etc/tor/torrc

optionally, set custom tor port with --tor-port 9050

.. code:: bash

    $ webshare link-search matrix 1999 --download --tor-port XXXX

Scraping and downloading all files found
~~~~~~~~~~~~~~~~~~~

with this you get links of all files found

.. code:: bash

    $ webshare link-scrape matrix 1999 > links

directly download all scraped files with --download, optionally --tor or --tor-ports

.. code:: bash

    $ webshare link-scrape matrix 1999 --download

tor ports can be provided also --tor-ports XXXX YYYY

.. code:: bash

    $ webshare link-scrape matrix 1999 --download --tor-ports 9050 9051

by default, 4 files will be downloaded in parallel, see pool_size in config

if you want more performance, use --pool N and provide appropriate number of tor ports

CAUTION: each port can be used for 5 concurrent downloads at maximum (recommended 4)

if you want let's say 20 concurrent downloads, provide 5 tor ports

.. code:: bash

    $ webshare link-scrape matrix 1999 --download --tor-ports 9050 9051 9052 9053 --pool 16

when scraping large number of files, there is a chance of finding files with identical names

by default, all the files will be downloaded with altered name to prevent overwrite on the disk

if you want to omit the other files with identical filename, use --skip-same

.. code:: bash

    $ webshare link-scrape matrix 1999 --download --tor-ports 9050 9051 9052 9053 --pool 16 --skip-same

alternatively, you can use --dest-dir to select the output folder for the downloaded files

if the folder does not exist, it will be created automatically

.. code:: bash

    $ webshare link-scrape matrix 1999 --download --tor-ports 9050 9051 9052 9053 --pool 16 --dest-dir /some/folder/ --skip-same

Changelog
~~~~~~~~~
- **2.2.3**: if download fails, download link is obtained again, progress bars nicer
- **2.2.2**: syntax changed, supports direct download with tor, supports scraping
- **2.2.1**: support terminal colors everywhere
- **2.2.0**: handle keyboard interrupt; terminal colors; Python 3.6+ required
- **2.1.0**: add -x/--exclude filter and --ignore-vip
- **2.0.2**: fix hadling of single search result
- **2.0.1**: include missing config.yaml in PyPI package
- **2.0.0**: update to new API (send wst in request) - config update needed!
- **1.2.0**: add fail-over logic for unavailable links in download command
- **1.1.1**: added setuptools dependency, use YAML.safe_load()
- **1.1.0**: added filtering by file extension
- **1.0.2**: add README.rst to pypi package
