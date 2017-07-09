========
isptweet
========

Installation
============

Simply install from PyPI like so:

.. code::

	pip install isptweet



Installation (from source)
==========================

Run

.. code::

	python setup.py install
	

Setup
=====

First, you'll need to obtain credentials from the Twitter API. Navigate to `apps.twitter.com <https://apps.twitter.com/>`_, and you should see the following page:

|tutorial-image-1|

Create your own application like so:

|tutorial-image-2|


And you should get some credentials (note that here, examples are used):

|tutorial-image-3|

Then grab the generated consumer key and secret, as well as your access token and secret. Then you'll have to invoke the script with the proper environment variables. My preferred way of doing this is to create some script, for example :code:`launch-isptweet.sh`, with the following body:

.. code:: bash

	#!/usr/bin/env bash
	
	export CONSUMER_KEY='CONSUMER_KEY'
	export CONSUMER_SECRET='CONSUMER_SECRET'

	export ACCESS_TOKEN='ACCESS_TOKEN'
	export ACCESS_TOKEN_SECRET='ACCESS_TOKEN_SECRET'
	
	isptweet testing 200 20


where all the value strings are your API credentials, and 200 and 20 are your download and upload speeds, respectively.

.. |tutorial-image-1| image:: https://raw.github.com/lschumm/isptweet/master/readme_images/1.png
.. |tutorial-image-2| image:: https://raw.github.com/lschumm/isptweet/master/readme_images/2.png
.. |tutorial-image-3| image:: https://raw.github.com/lschumm/isptweet/master/readme_images/3.png
