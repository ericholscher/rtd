from argparse import ArgumentParser
import commands
import webbrowser
import json
import os
import inspect
from subprocess import PIPE, Popen
from pydoc import pager
from httplib import HTTPConnection
from getpass import getpass

#I recommend reading this file from the bottom up.

BASE_SERVER = 'readthedocs.org'
API_URL = '/api/v1'
MEDIA_SERVER = 'media.readthedocs.org'
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
    URL = "%s/project/%s/?format=json" % (API_URL, slug)
    if VERBOSE:
        print "Getting %s" % URL
    conn = HTTPConnection(BASE_SERVER)
    try:
        conn.request("GET", URL)
        resp = conn.getresponse()
        if resp.status == 200:
            return json.loads(resp.read())
    finally:
        conn.close()


def _dump_results(resp, content):
    print "Status: %s" % resp.status

########
# Routes
########


def create_project(vcs, name, repo=''):
    user, password = _read_creds(os.path.expanduser("~/.rtdrc"))
    if not user:
        user = raw_input("Username: ")
        password = getpass("Password: ")
    if repo == '':
        repo = _guess_repo(vcs)
        if not repo:
            print "Couldn't guess repo, please input it."
            repo = raw_input("Repository: ")
    auth = _get_auth_string(user=user, password=password)
    post_url = "%s/project/" % API_URL
    post_data = json.dumps({
        "name": name,
        "repo": repo,
        "repo_type": vcs,
    })
    conn = HTTPConnection(BASE_SERVER)
    try:
        conn.request("POST", post_url, body=post_data,
                 headers={'content-type': 'application/json',
                          'AUTHORIZATION': auth}
                 )
        resp = conn.getresponse()
        status = resp.status
        content = resp.read()
    finally:
        conn.close()
    if status != 201:
        print "There was a problem creating this project"
        _dump_results(resp, content)
        return

    proj_obj = _get_project_data(name)
    proj_url = "http://%s%s" % (BASE_SERVER, proj_obj['absolute_url'])
    print "URL for your project: %s" % proj_url
    webbrowser.open(proj_url)


def build_project(slug):
    proj_obj = _get_project_data(slug)
    if proj_obj is None:
        print "Project could not be built"
        return
    post_url = "/build/%s" % proj_obj['id']
    conn = HTTPConnection(BASE_SERVER)
    try:
        conn.request("POST", post_url)
        resp = conn.getresponse()
        status, content = resp.status, resp.read()
    finally:
        conn.close()

    if status == 200:
        print "Kicked off build"
    else:
        print "Project could not be built"
        _dump_results(status, content)


def get_docs(project, extra=''):
    proj = _get_project_data(project)
    if proj is not None:
        print proj['description']
        if extra:
            url = 'http://%s.rtfd.org/%s' % (project, extra)
        else:
            url = 'http://%s.rtfd.org/' % project
        if VERBOSE:
            print "Opening browser to %s" % url
        webbrowser.open(url)
        return True
    else:
        print "Project was not found"


def get_manpage(project, extra=''):
    if 'readthedocs' in BASE_SERVER:
        URL = "/man/%s/latest/%s.1" % (project, project)
        base = MEDIA_SERVER
    else:
        URL = "/media/man/%s/latest/%s.1" % (project, project)
        base = BASE_SERVER
    conn = HTTPConnection(base)
    try:
        conn.request("GET", URL)
        resp = conn.getresponse()
        status, content = resp.status, resp.read()
    except AttributeError:
        #XXX:dc: Is this really what httplib2 raises?
        print "Socket error trying to pull from Read the Docs"
    finally:
        conn.close()
    if status == 200:
        cmd = Popen(['/usr/bin/env', 'groff', '-E', '-man', '-Tascii'],
                    stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, err = cmd.communicate(input=content)
        if err:
            print err
        else:
            pager(out)
    else:
        print "No manpage entry for %s" % project


def main():
    global BASE_SERVER
    global API_SERVER
    global VERBOSE

    parser = ArgumentParser(prog="rtd")
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--server', default=BASE_SERVER,
                        help="ie: readthedocs.org")
    subparsers = parser.add_subparsers()

    get_docs_parser = subparsers.add_parser(
        "get", help='get to the documentation for a project')
    get_docs_parser.add_argument('project', metavar="PROJ", nargs='?')
    get_docs_parser.add_argument('extra', metavar="EXTRA", nargs='?')
    get_docs_parser.set_defaults(func=get_docs)

    create_proj_parser = subparsers.add_parser(
        "create", help='create a project')
    create_proj_parser.add_argument('vcs', metavar="VCS",
                                    help="hg or git")
    create_proj_parser.add_argument('name', metavar="NAME")
    create_proj_parser.add_argument('repo', metavar="REPO", nargs='?')
    create_proj_parser.set_defaults(func=create_project)

    build_proj_parser = subparsers.add_parser(
        "build", help='build project docs')
    build_proj_parser.add_argument('slug', metavar="SLUG",
                                    help="url slug for the project")
    build_proj_parser.set_defaults(func=build_project)

    manpage_parser = subparsers.add_parser(
        "man", help='get to the documentation for a project')
    manpage_parser.add_argument('project', metavar="PROJ", nargs='?')
    manpage_parser.add_argument('extra', metavar="EXTRA", nargs='?')
    manpage_parser.set_defaults(func=get_manpage)

    args = parser.parse_args()
    if args.verbose:
        VERBOSE = True

    if args.server:
        BASE_SERVER = args.server
        API_SERVER = '%s/api/v1' % args.server

    arg_dict = {}
    for arg in inspect.getargspec(args.func).args:
        arg_dict.update({arg: getattr(args, arg, '')})
    args.func(**arg_dict)
