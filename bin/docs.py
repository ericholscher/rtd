#!/usr/bin/env python
import webbrowser
import httplib2
import sys

import json

BASE_SERVER = 'http://readthedocs.org'
API_SERVER = '%s/api/v1/' % BASE_SERVER

def import_project(slug, extra):
    URL = API_SERVER + "project/%s/" % slug
    h = httplib2.Http(timeout=5)
    try:
        resp, content = h.request(URL, "GET")
    except AttributeError:
        print "Socket error trying to pull from Read the Docs"
        return False
    if resp['status'] == '200':
        content_dict = json.loads(content)
        print content_dict['description']
        url = 'http://%s.rtfd.org/%s' % (slug, extra)
        print "Opening browser to %s" % url
        webbrowser.open(url)
    return False


if __name__ == "__main__":
    project = sys.argv[1]
    extra = ""
    if len(sys.argv) == 3:
        extra = sys.argv[2]
    import_project(project, extra)
