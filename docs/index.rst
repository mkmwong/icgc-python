.. icgc documentation master file, created by
   sphinx-quickstart on Fri Nov  3 16:04:44 2017.

The ICGC Python REST Client
============================

The ICGC REST client is a simple python module that allows you to access the **International Consortium for Cancer and Genomics** web portal directly through Python, with a minimum of coding effort.

It lets you write queries in our Portal Query Language ( `PQL <https://github.com/icgc-dcc/dcc-portal/blob/develop/dcc-portal-pql/PQL.md>`_ ) that fetch data from the ICGC web portal as JSON objects. From there, you can use the power of Python to process and analyze the data within those objects however you see fit.  

Here's an example that shows you how easy it is to get started!
::

    import icgc
    client = icgc.Client()
    # get information about donors as a JSON object
    donor_info=client.query(request_type='donors',pql='select(*)')    	
    print(donor_info)

Installation
------------
You can install icgc using *pip* by running:
    **pip install icgc**

If you prefer, you can also download the source code from the url below.

Contribute
----------
If you'd like to contribute to this project, it's hosted on github.
  
See https://github.com/icgc-dcc/icgc-python
