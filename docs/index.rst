Welcome to rtd's documentation!
===============================

This is a command line tool that helps you interface with ``Read the Docs <http://readthedocs.org>``_. It will hopefully expose useful features of the site, it's API, and other intersting tidbits around the site.


Basic Commands
==============

There are a few basic commands that we have implemented.

Basic Auth
----------

Certain commands, like creating new projects, require auth. We support 2 different methods of handling this. You can create a ``~/.rtdrc`` file, which will contain your ``username:password`` in that format.

If you don't have an ``.rtdrc`` file, you will be prompted for the credentials when you do something that requires them.

Getting to docs
---------------

We have made it easy to get to the documentation for a project from the command line.

``rtd`` - Open http://readthedocs.org in your browser.

``rtd <project>`` - Open http://project.rtfd.org, which will redirect to its latest version.

``rtd <project> <slug>`` - Will open to http://project.rtfd.org/slug, which will kick off a query against RTD's backend store of slug to documentation mapping. If nothing exists for your slug, you will be asked to figure out where it should go for future users.

Building docs
-------------

Sometimes you need to build a new version of your documentation. This is really simple currently.

``rtd build <slug>`` - This will kick off a build of the project.

Creating Docs
-------------

If you have a project that you want to host on RTD, it's never been easier to put it on the site. If you are already a member, you can upload docs with one command.

``rtd create <vcs> <name> <repo>`` - This will create a project with the designated options.

``rtd create <vcs> <name>`` - This will try to guess your repository if you use git, otherwise it will prompt you for the repo information.

Example: ``rtd create git rtd https://github.com/ericholscher.com/rtd``
