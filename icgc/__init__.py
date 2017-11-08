#
# Copyright (c) 2017 The Ontario Institute for Cancer Research. All rights reserved.
#
# This program and the accompanying materials are made available under the terms of the GNU Public License v3.0.
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
"""
The ICGC module implements a simple Python REST client that can be used
to access our web portal
"""

import requests

BASE_URL="http://localhost:8080/api/v1/"

def fmt(format_string, *a, **kw):
    """
    Format the given string with the given arguments, similar to Python3's f
    string syntax
    :param format_string: The string
    :param a: arguments
    :param kw: keywords
    :return: The formatted string
    """
    return format_string.format(*a, **kw)

def report(name):
    n=1
    i=n
    total_bytes=0
    threshold=1024*1024;
    total_bytes=0
    while True:
          data_bytes= yield(total_bytes)
          total_bytes += data_bytes
          #print("Downloaded {} bytes".format(total_bytes))
          if total_bytes > i * threshold: 
             print("Downloaded {} MB to {}.tar".format(i,name))
             i+=n

def download(filters,include,name,fmt='TSV',base_url=BASE_URL, reporter=None):
    if reporter is None:
       reporter=report
    includes=[] 
    for k in include:
        txt ="{" + '"key":"{}", "value": "{}"'.format(k,fmt) +"}"
        includes.append(txt)
    url1=base_url + "download/submit?filters={}&info=[{}]".format(filters,",".join(includes))
    print("Sending request {}".format(url1))
    r=requests.get(url1)
    url2 =base_url + "download/{}".format(r.json()['downloadId'])
    r2=requests.request('GET',url2,headers={'Accept':'application/x-tar'},verify=False,stream=True)
    x = reporter(name)
    x.send(None)

    with open(name+".tar","wb") as f:
         for data in r2.iter_content(chunk_size=None):
             size=x.send(len(data)) 
             f.write(data)

    x.close()

def download_size(filters,base_url=BASE_URL):
    url= base_url + "download/size?filters={}".format(filters)

    sizes=get_data(url)['fileSize'] 
    d={}
    for entry in sizes:
        key=entry['label']
        value=entry['sizes']
        d[key]=value
    return d

def request_types():
    """
    Return a list of valid request types
    :return: A list of strings naming valid request types
    """
    return ["donors", "genes", "mutations", "occurrences"]

def formats():
    """
    Return a list of valid output formats
    :return: A list of strings naming valid output formats
    """
    return ["json"]

def query(request_type, pql, output_format='json',base_url=BASE_URL):
    """
    Validate the query request, and return the results from the portal server
    :param request_type: Type of request: must be a string from "request_types"
    :param pql: Must be a valid PQL request for the given request_type
    :param output_format: Must be a string containing one of the valid output formats
    :return: The results from running the PQL query on the portal server 
    """

    if request_type not in request_types():
       raise TypeError(fmt("Invalid Request Type {}, must be one of {}",
           request_type, request_types()))
    if output_format not in formats():
        raise TypeError(fmt("Invalid format {}, must be one of {}",
                                output_format, formats()))

    url = base_url + fmt("{}/pql?query={}", request_type, pql)

    return get_data(url)

def get_data(url):
    """
    Helper method used to issue a request to the portal server's rest
    api, and get a result back
    :param url: The url to contact the server API with
    :return: The results from the server as a 'requests' response object;
        raises an IOError if we can't connect.
    """

    # print(f"Fetching url {url}")
    resp = requests.get(url)
    if resp.status_code != 200:
        raise IOError(fmt('GET {} {}', url, resp.status_code))
    return resp.json()
