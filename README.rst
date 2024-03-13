Webshare.cz CLI Downloader
==========================

| CLI interface for getting download links for files from webshare.cz.

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

    $ webshare download my own awesome movie 2024 > link
    my own awesome movie: My.Awesome.Movie.2024.1080p.AC3.x264.(CZ,EN).mkv
    $ aria2c -i link

Download an entire series
~~~~~~~~~~~~~~~~~~~~~~~~~

Use asterisk (``*``) symbol to as a 00-99 wildcard.

.. code:: bash

    $ webshare download example series s02e* > links
    example series s03e00: NOT FOUND
    example series s03e01: Example.Series.S03E01.PROPER.1080p.WEBRip.X264.mkv
    example series s03e02: Example.Series.S03E02.PROPER.1080p.WEBRip.X264.mkv
    example series s03e03: Series.Example.wtf.S03E03.PROPER.1080p.WEBRip.X264.mkv
    example series s03e04: Example.Series.S03E04.PROPER.1080p.WEBRip.X264.mkv
    example series s03e05: Example.Series.S03E05.1080p.WEBRip.X264-DEFLATE.mkv
    example series s03e06: Example.Series.S03E06.1080p.WEBRip.X264-DEFLATE.mkv
    example series s03e07: NOT FOUND
    example series s03e08: NOT FOUND
    example series s03e09: NOT FOUND
    Aborting after 3 failures
    $ aria2c -i links

Search for a file
~~~~~~~~~~~~~~~~~

.. code:: bash

    $ webshare search my very own file
     1.  12G mkv +0 saod56f33a My.Very.Own.File.2000.1080p.BluRay.DTS.x264-XYZ.mkv
     2.  67K srt +0 FK094jFdfk My.Very.Own.File.2000.1080p.BluRay.DTS.x264-XYZ.srt
     3. 1.7G mkv +1 VMF94n1cgh my very own file 9001 unrated DC (1080p x265 10bit Alphabet).mkv
     4. 1.4G mp4 +0 knfg9FLgxe Random.Stuff.aka.My.Very.Own.File.DIRECTORS.CUT.2000.1080p.BrRip.x264.mp4

Download file by id
~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ webshare link saod56f33a > link
    $ aria2c -i link

Changelog
~~~~~~~~~

- **2.2.2**: documentation update
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
