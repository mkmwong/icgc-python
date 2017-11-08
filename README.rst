.. icgc documentation master file, created by
   sphinx-quickstart on Fri Nov  3 16:04:44 2017.

The ICGC Python REST Client
============================

The ICGC REST client is a simple python module that allows you to access the **International Consortium for Cancer and Genomics** web portal directly through Python, with a minimum of coding effort.

It lets you write queries in our Portal Query Language ( `PQL <https://github.com/icgc-dcc/dcc-portal/blob/develop/dcc-portal-pql/PQL.md>`_ ) that fetch data from the ICGC web portal as JSON objects. From there, you can use the power of Python to process and analyze the data within those objects however you see fit.  

Here's an example that shows you how easy it is to get started!
::

    import icgc
    local_server="http://localhost:8080/api/v1/"
    for request_type in icgc.request_types():
        response = icgc.query(request_type=request_type, pql='select(*)',base_url=local_server)
        print(request_type, "===\n\n", response)

Here's an example that demonstrates downloading some donor data
::

    import icgc 
    
    KB=1024
    MB=1024*KB
    
    filters='{"donor":{"primarySite":{"is":["Brain"]}}}'
    
    # See what different items are available for our current choice of filter 
    # and how big they are
    
    sizes = icgc.download_size(filters)
    print("Sizes are: {}".format(sizes))
    
    # Let's choose to download as many different bits of information as we can fit 
    # in a reasonably small download, say 10 MB in size, and just download those
    # ones.
    
    max_size=10 * MB 
    current_size=0
    
    # We'll just keep adding items to our list as long as they don't put us over our
    # download total.
    includes=[]
    for k in sizes:
        item_size=sizes[k]
        if current_size + item_size < max_size: 
           includes.append(k)
           current_size += item_size
    
    print("Including items {}".format(includes))
    print("Approximate download size={:.2f} MB".format(current_size / MB))
    
    # Download the information, and save the results in the file "test1.tar"
    icgc.download(filters,includes,"test1")

Installation
------------
You can install icgc using *pip* by running:
    **pip install icgc**

If you prefer, you can also download the source code from the url below.

Contribute
----------
If you'd like to contribute to this project, it's hosted on github.
  
See https://github.com/icgc-dcc/icgc-python
