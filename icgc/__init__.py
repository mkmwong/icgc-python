# Copyright (c) 2017 The Ontario Institute for Cancer Research. All rights
# reserved.
#
# This program and the accompanying materials are made available under the
# terms of the GNU Public License v3.0. You should have received a copy of
# the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING,BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

"""
The ICGC module implements a simple Python REST client that can be used
to access our web portal
"""
from __future__ import unicode_literals, print_function, absolute_import, division
import requests

BASE_URL = "https://dcc.icgc.org/api/v1/"

class ICGCBrowser(object):
    """
    A class that lets you browse the content of our repository
    """
    def __init__(self,token,path="/"):
        self.token = ""
        self.home = path
        self.path = path

    def resolve_path(self, path):
        if path is None:
            return self.path

        if path.startswith("/"):
            return path

        if path.startswith(".."):
            return self._resolve_parent(path,self.home)

        return self.path + "/" + path

    def _resolve_parent(self, path, base):
        if path == "..":
            return self._parent(base)
        elif path.startswith("../"):
            print("Recursing with {},{}".format(path[2:],self._parent(base)))
            return self._resolve_parent(path[2:],self._parent(base))
        else:
            return base  + path

    def _parent(self, path):
        if path == "/":
            raise TypeError("Path {} has no parent!".format(path))
        parent, _, folder = path.rpartition("/")

        return parent

    def _name(self, path):
        parent, _, name = path.rpartition("/")
        return name


    def cd(self, path=None):
        if path is None:
            path=self.home
        self.path = self.resolve_path(path)

    def ls(self, path=None):
        path = self.resolve_path(path)
        url = self._get_info_url(path)
        reply=requests.get(url)
        return reply.json()


    def get(self, path=None, file=None):
        path=self.resolve_path(path)
        url=self._get_download_url(path)
        reply=requests.get(url)

        with open(self._name(path),"wb") as f:
            f.write(reply.content)


    def _get_download_url(self, path):
        return "{}download?fn={}".format(BASE_URL, path)

    def _get_info_url(self, path):
        return "{}download/info{}".format(BASE_URL,path)

def _api_url(format_string, *args, **kw):
    return BASE_URL + format_string.format(*args, **kw)


def default_reporter(name, interval=1, units=1024 * 1024):
    """
    Generator that reports on the status of a file download
    :param name: The name of the file being downloaded
    :param interval: The number of MB to download before printing
    an update.
    :param units: The number of bytes per unit of interval (default=1MB,
    or 1024*1024). You could set this to 1024 for KB, or 1024*1024*1024
    for GB, for example.
    :return: An iterator that can be used to report the file status
    When the iterator is sent the size of the current chunk that was
    most recently downloaded, it replies with the total amount downloaded
    so far, rounded to the nearest MB.
    """
    report = interval

    total_bytes = 0
    while True:
        data_bytes = yield total_bytes
        total_bytes += data_bytes

        if total_bytes > report * units:
            print("Downloaded {} MB to {}.tar".format(report, name))
            report += interval


def _info_param(include, output_format):
    includes = []
    for k in include:
        txt = "{" + '"key":"{}", "value": "{}"'.format(k, output_format) + "}"
        includes.append(txt)
    return ",".join(includes)


def download(pql, include, filename, output_format='TSV',
             reporter=default_reporter):
    """
    Download pql for the categories in the include list as a tar file
    :param pql: The PQL(Portal Query Language) query to select items with
    :param include: The download file types to use (keys from download_size())
    :param filename: The name of the tarfile (.tar will be appended)
    :param output_format: TSV or JSON (default TSV)
    :param reporter: generator function to use to monitor download.
            It defaults to the generator returned by the "default_reporter"
            method in this class.
    :return:
    """
    info = _info_param(include, output_format)
    url = _api_url("download/submitPQL?pql=select(*),{}&info=[{}]", pql, info)
    result = requests.get(url)
    download_id = result.json()['downloadId']
    _download_tarfile(download_id, filename, reporter)


def _download_tarfile(download_id, filename, reporter):
    url = _api_url("download/{}", download_id)
    result = requests.request('GET', url,
                              headers={'Accept': 'application/x-tar'},
                              verify=False, stream=True)

    if result.status_code >= 400:
        raise IOError("Couldn't get {}: status code {}".
                      format(url, result.status_code))

    report = reporter(filename)
    report.send(None)

    with open(filename + ".tar", "wb") as filehandle:
        for data in result.iter_content(chunk_size=None):
            report.send(len(data))
            filehandle.write(data)
    report.close()


def download_size(pql):
    """
    Get the sizes of the download
    :param pql:
    :return:
    """
    url = _api_url("download/sizePQL?pql={}", pql)
    sizes = _get_data(url)['fileSize']
    dictionary = {}
    for entry in sizes:
        key = entry['label']
        value = entry['sizes']
        dictionary[key] = value
    return dictionary


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
    return ["json", "TSV"]


def query(request_type, pql, output_format='json'):
    """
    Validate the query request, and return the results from the portal server
    :param request_type: Type of request: must be a string from
    "request_types"
    :param pql: Must be a valid PQL request for the given request_type
    :param output_format: Must be a string containing one of the valid
    output formats
    :return: The results from running the PQL query on the portal server
    """

    if request_type not in request_types():
        raise TypeError("Invalid Request Type {}, must be one of {}".format(
            request_type, request_types()))
    if output_format not in formats():
        raise TypeError("Invalid format {}, must be one of {}".format(
            output_format, formats()))

    url = _api_url("{}/pql?query={}", request_type, pql)
    return _get_data(url)


def _get_data(url):
    """
    Helper method used to issue a request to the portal server's rest
    api, and get a result back
    :param url: The url to contact the server API with
    :return: The results from the server as a 'requests' response object;
        raises an IOError if we can't connect.
    """

    resp = requests.get(url)
    if resp.status_code != 200:
        raise IOError('GET {} {}'.format(url, resp.status_code))
    return resp.json()
