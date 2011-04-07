#!/usr/bin/env python
import webbrowser
import httplib2
import sys

import json

BASE_SERVER = 'http://readthedocs.org'
API_SERVER = '%s/api/v1/' % BASE_SERVER

def import_project(slug):
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
        webbrowser.open('http://%s.rtfd.org' % slug)
    return False


if __name__ == "__main__":
    project = sys.argv[1]
    print "Checking %s" % project
    import_project(project)
