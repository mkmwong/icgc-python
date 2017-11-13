.. icgc documentation master file, created by
   sphinx-quickstart on Fri Nov  3 16:04:44 2017.

The ICGC Python REST Client
============================

The ICGC REST client is a simple python module that allows you to access the **International Consortium for Cancer and Genomics** web portal directly through Python, with a minimum of coding effort.

It lets you write queries in our Portal Query Language ( `PQL <https://github.com/icgc-dcc/dcc-portal/blob/develop/dcc-portal-pql/PQL.md>`_ ) that fetch data from the ICGC web portal as JSON objects. From there, you can use the power of Python to process and analyze the data within those objects however you see fit.  

Here's an example that shows you how easy it is to get started!
::
    """
    query.py
    
    This script demonstrates running a simple PQL query against the ICGC data
    portal with the icgc module.
    """
    from __future__ import absolute_import, print_function
    
    import icgc
    icgc.BASE_URL = "http://localhost:8080/api/v1/"
    
    
    def run():
        """
        Demonstrate PQL by displaying 1 of each request type as JSON output
        """
        for request_type in icgc.request_types():
            response = icgc.query(request_type=request_type,
                                  pql='select(*),limit(1)')
            print(request_type, "===\n\n", response)
    
    
    if __name__ == '__main__':
        run()

Here's an example that demonstrates downloading some donor data
::
    """
    download.py
    
    This is an example script to download donor information from a copy of the
    ICGC web portal running on your local machine.
    """
    from __future__ import absolute_import, division, print_function
    import icgc
    
    icgc.BASE_URL = "http://localhost:8080/api/v1/"
    
    KB = 1024
    MB = 1024 * KB
    
    
    def run():
        """
        Show an example of a PQL download with automated decision making.
    
        We download up to a maximum of 10 MB of data from the portal, of any type
        that will fit within our download limit, and save our the results as a
        tarfile named 'test.tar'.
        """
        pql = 'eq(donor.primarySite,"Brain")'
    
        # Find which items are available that match our pql query, and how big
        # each of the result file are.
    
        sizes = icgc.download_size(pql)
        print("Sizes are: {}".format(sizes))
    
        # Let's choose to download as many different bits of information as we can
        # fit in a reasonably small download, say 10 MB in size, so that we don't
        # have to wait a long time for it to download.
    
        # We'll only include  a file in our tarfile if the total is below our
        # 10 MB limit. Our tarfile size calculation is approximate; the
        # files inside the tarfile get compressed; so the total size of the tarfile
        # that we download might be smaller than we calculate.
    
        max_size = 10 * MB
        current_size = 0
    
        # We'll just keep adding items to our list as long as they don't put us
        # over our download total.
        includes = []
        for k in sizes:
            item_size = sizes[k]
            if current_size + item_size < max_size:
                includes.append(k)
                current_size += item_size
    
        print("Including items {}".format(includes))
        print("Approximate download size={:.2f} MB".format(current_size / MB))
    
        # Download the information, and save the results in the file "test.tar"
        icgc.download(pql, includes, "test")
    
    
    if __name__ == "__main__":
        run()

Installation
------------
You can install icgc using *pip* by running:
    **pip install icgc**

If you prefer, you can also download the source code from the url below.

Contribute
----------
If you'd like to contribute to this project, it's hosted on github.
  
See https://github.com/icgc-dcc/icgc-python
