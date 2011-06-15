from argparse import ArgumentParser
import commands
import webbrowser
import httplib2
import sys
import json
import re
import os
import inspect

#I recommend reading this file from the bottom up.

BASE_SERVER = 'http://readthedocs.org'
API_SERVER = '%s/api/v1' % BASE_SERVER
VERBOSE = False
##################
# Helper Functions
##################


class NoRoutes(Exception):
    pass


def _guess_repo(vcs):
    if vcs == "git":
        #This is mainly to handle writable github repos.
        repo = commands.getoutput('git remote -v |grep origin |grep fetch | cut -f2')
        repo = repo.split(' ')[0].replace('git@', '').replace(':', '/')
        if not "://" in repo:
            repo = "git://%s" % repo
        print repo
        return repo
    else:
        return None


def _get_auth_string(user, password):
    return "Basic %s" % ("%s:%s" % (user, password)).encode("base64").strip()


def _read_creds(filename):
    try:
        line = open(filename).readline()
    except IOError:
        return (None, None)
    un, pw = line.split(":")
    return (un.strip(), pw.strip())


def _get_project_data(slug):
    GET_URL = "%s/project/%s" % (API_SERVER, slug)
    h = httplib2.Http(timeout=5)
    resp, proj_info = h.request(GET_URL, "GET")
    return json.loads(proj_info)


def _dump_results(resp, content):
    print "Status: %s" % resp.status

########
# Routes
########


def create_project(vcs, name, repo=''):
    user, password = _read_creds(os.path.expanduser("~/.rtdrc"))
    if not user:
        user = raw_input("Username: ")
        password = raw_input("Password: ")
    if repo == '':
        repo = _guess_repo(vcs)
        if not repo:
            print "Couldn't guess repo, please input it."
            repo = raw_input("Repository: ")
    auth = _get_auth_string(user=user, password=password)
    post_url = "%s/project/" % API_SERVER
    post_data = json.dumps({
        "name": name,
        "repo": repo,
        "repo_type": vcs,
    })
    h = httplib2.Http(timeout=5)
    resp, content = h.request(post_url, "POST", body=post_data,
        headers={'content-type': 'application/json',
                 'AUTHORIZATION': auth}
            )
    _dump_results(resp, content)
    resp, proj_info = h.request(resp['location'], "GET")
    proj_obj = json.loads(proj_info)
    proj_url = "http://readthedocs.org%s" % proj_obj['absolute_url']
    print "URL for your project: %s"
    webbrowser.open(proj_url)


def build_project(slug):
    proj_obj = _get_project_data(slug)
    post_url = "http://readthedocs.org/build/%s" % proj_obj['id']
    h = httplib2.Http(timeout=5)
    resp, content = h.request(post_url, "POST")
    _dump_results(resp, content)


def get_docs(project, extra=''):
    URL = "%s/project/%s/" % (API_SERVER, project)
    h = httplib2.Http(timeout=5)
    try:
        resp, content = h.request(URL, "GET")
    except AttributeError:
        #XXX:dc: Is this really what httplib2 raises?
        print "Socket error trying to pull from Read the Docs"
        return False
    if resp['status'] == '200':
        content_dict = json.loads(content)
        print content_dict['description']
        if extra:
            url = 'http://%s.rtfd.org/%s' % (project, extra)
        else:
            url = 'http://%s.rtfd.org/' % project
        if VERBOSE:
            print "Opening browser to %s" % url
        webbrowser.open(url)
        return True
    else:
        print "Invalid return data"
        _dump_results(resp, content)
        return False


def main():
    parser = ArgumentParser(prog="rtd")
    parser.add_argument('--verbose', action='store_true')
    subparsers = parser.add_subparsers()

    get_docs_parser = subparsers.add_parser(
        "get", help='get to the documentation for a project')
    get_docs_parser.add_argument('project', metavar="PROJ", nargs='?')
    get_docs_parser.add_argument('extra', metavar="EXTRA", nargs='?')
    get_docs_parser.set_defaults(func=get_docs)

    create_proj_parser = subparsers.add_parser(
        "create", help='create a project')
    create_proj_parser.add_argument('vcs', metavar="VCS", nargs=1,
                                    help="hg or git")
    create_proj_parser.add_argument('name', metavar="NAME", nargs=1)
    create_proj_parser.add_argument('repo', metavar="REPO", nargs='?')
    create_proj_parser.set_defaults(func=create_project)

    build_proj_parser = subparsers.add_parser(
        "build", help='build project docs')
    build_proj_parser.add_argument('slug', metavar="SLUG", nargs=1,
                                    help="url slug for the project")
    build_proj_parser.set_defaults(func=build_project)

    args = parser.parse_args()
    if args.verbose:
        global VERBOSE
        VERBOSE = True
    arg_dict = {}
    for arg in inspect.getargspec(args.func).args:
        arg_dict.update({arg: getattr(args, arg, '')})
    args.func(**arg_dict)
