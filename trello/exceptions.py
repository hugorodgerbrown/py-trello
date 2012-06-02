
class ResourceUnavailableException(Exception):
    
    """Exception representing a failed request to a resource."""

    def __init__(self, url, status_code, content):
        Exception.__init__(self)
        self._url = url
        self._status = status_code
        self._msg = content

    def __str__(self):
        print "Resource unavailable; API response = %(status)s %(message)s" % {'status':self._status, 'message':self._msg, 'url':self._url}
