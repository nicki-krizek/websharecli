Webshare.cz CLI Downloader
==========================

| CLI interface for getting download links for movies and TV shows from
| webshare.cz.

Installation
------------

.. code:: bash

    $ pip3 install websharecli
    $ webshare sample-config

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

Download a single file
~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ webshare download matrix 1999 > link
    matrix 1999: The.Matrix.1999.BluRay.1080p.DTS-HDMA.AC3.x264.dxva-FraMeSToR (CZ,EN).mkv
    $ wget -i link

Download an entire series
~~~~~~~~~~~~~~~~~~~~~~~~~

Use asterisk (``*``) symbol to as a 00-99 wildcard.

.. code:: bash

    $ webshare download black mirror s02e* > links
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

Search for a file
~~~~~~~~~~~~~~~~~

.. code:: bash

    $ webshare search requirem for a dream
     1.  12G mkv +0 76s2uj1ir4 Requiem.For.A.Dream.Director's.Cut.2000.1080p.BluRay.DTS.x264-DON.mkv
     2.  67K srt +0 5394mr11r1 Requiem.For.A.Dream.Director's.Cut.2000.1080p.BluRay.DTS.x264-DON.srt
     3. 1.7G mkv +1 5uR4b05kh2 Requiem for a Dream 2000 Unrated DC (1080p x265 10bit Tigole).mkv
     4. 1.4G mp4 +0 10z3ja4Xq2 Requiem.For.A.Dream.DIRECTORS.CUT.2000.1080p.BrRip.x264.YIFY.mp4
     5.  71K srt +0 28s39750D3 Requiem.For.A.Dream.DIRECTORS.CUT.2000.1080p.BrRip.x264.YIFY.srt
     6. 4.5G mkv +0 4Pr5rz6z13 Requiem.For.A.Dream.720p.x264.AC3-5.1-DiC.mkv
     7. 700M mp4 +0 15i6n36R32 Requiem.For.A.Dream.DIRECTORS.CUT.2000.720p.BrRip.x264.YIFY.mp4
     8. 1.2G avi +1 KRdAgRvv4F Requiem za sen (Requiem For a Dream).avi

Download file by id
~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ webshare link 76s2uj1ir4 > link
    $ wget -i link

Changelog
~~~~~~~~~

- **1.1.0**: added filtering by file extension
- **1.0.2**: add README.rst to pypi package
