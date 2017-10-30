import requests

def f(s,*a,**kw):
    """
    Format the given string with the given arguments, similar to Python3's f string syntax
    :param s: The string
    :param a: arguments
    :param kw: keywords
    :return: The formatted string
    """
    return s.format(*a,**kw)

class Client(object):
    def __init__(self, url, authentication):
        """
        Create an icgc client object, capable of connecting to our servers and fetching data
        :param url: Should we set a default url here?
        :param authentication: The authentication token required to run the query (currently not used yet)
        """
        self.url = url
        self.authentication = authentication

    @classmethod
    def request_types(cls):
        """
        Return a list of valid request types
        :return: A list of strings naming valid request types
        """
        return ["donors", "genes", "mutation", "observation","file"]
    @classmethod
    def formats(cls):
        """
        Return a list of valid output formats
        :return: A list of strings naming valid output formats
        """
        return ["json"] # TODO: Add TSV

    def query(self, requestType, pql, format='json'):
        """
        Validate the query request, and return the results from the portal server
        :param requestType: Type of request: must be a string from "request_types"
        :param pql: Must be a valid PQL request for the given request_type
        :param format: Must be a string containing one of the valid output formats
        :return: The results from running the PQL query on the portal server in the specified output format
        """
        if requestType not in self.request_types():
            raise TypeError(f("Invalid Request Type {}, must be one of {}", requestType, self.request_types()))
        if format not in self.formats():
            raise TypeError(f("Invalid format {}, must be one of {}",format,self.formats()))

        url = self.url + f("/{}/pql?query={}",requestType,pql)

        return self.getUrl(url)

    def getUrl(self, url):
        """
        Helper method used to issue a request to the portal server's rest api, and get a result back
        :param url: The url to contact the server API with
        :return: The results from the server as a 'requests' response object; raises an IOError if we can't
                  connect.
        """

        #print(f"Fetching url {url}")
        resp = requests.get(url)
        if resp.status_code != 200:
            raise IOError(f('GET {} {}',url,resp.status_code))
        return resp
