/*
 * Copyright (c) 2017 The Ontario Institute for Cancer Research. All rights reserved.                             
 *                                                                                                               
 * This program and the accompanying materials are made available under the terms of the GNU Public License v3.0.
 * You should have received a copy of the GNU General Public License along with                                  
 * this program. If not, see <http://www.gnu.org/licenses/>.                                                     
 *                                                                                                               
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY                           
 * EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES                          
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT                           
 * SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,                                
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED                          
 * TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;                               
 * OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER                              
 * IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN                         
 * ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */
"""
The ICGC module implements a simple Python REST client that can be used
to access our web portal
"""

import requests


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


class Client(object):
    """
    The Client class is a simple python REST client for accessing the data
    available through the ICGC web portal.
    """

    def __init__(self, url="http://dcc.icgc.org", authentication=None):
        """
        Create an icgc client object, capable of connecting to our servers
        and fetching data
        :param url: Should we set a default url here?
        :param authentication: The authentication token required to run the
        query (currently not used yet)
        """
        self.url = url
        self.authentication = authentication

    @classmethod
    def request_types(cls):
        """
        Return a list of valid request types
        :return: A list of strings naming valid request types
        """
        return ["donors", "genes", "mutations", "occurrences"]

    @classmethod
    def formats(cls):
        """
        Return a list of valid output formats
        :return: A list of strings naming valid output formats
        """
        return ["json"]

    def query(self, request_type, pql, output_format='json'):
        """
        Validate the query request, and return the results from the portal
        server
        :param request_type: Type of request: must be a string from
        "request_types"
        :param pql: Must be a valid PQL request for the given request_type
        :param output_format: Must be a string containing one of the valid
        output formats
        :return: The results from running the PQL query on the portal server
        in the specified output format
        """
        if request_type not in self.request_types():
            raise TypeError(fmt("Invalid Request Type {}, must be one of {}",
                                request_type, self.request_types()))
        if output_format not in self.formats():
            raise TypeError(fmt("Invalid format {}, must be one of {}",
                                output_format, self.formats()))

        url = self.url + fmt("/{}/pql?query={}", request_type, pql)

        return self.get_data(url)

    @staticmethod
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
