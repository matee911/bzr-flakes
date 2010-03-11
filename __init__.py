# -*- coding: utf-8 -*-

"""
.bzrflakes example:

[ignore]
path=file/to/excluded_file.py:another/file.py
"""

from bzrlib.lazy_import import lazy_import
lazy_import(globals(), """
import compiler
import os, sys
import pyflakes
from ConfigParser import ConfigParser
from bzrlib.branch import Branch
from bzrlib import (
    commands,
    workingtree,
)
""")

def check(codeString, filename):
    try:
        from pyflakes import Checker # <=0.2.1
    except ImportError:
        from pyflakes.checker import Checker # >0.2.1

    try:
        tree = compiler.parse(codeString)
    except (SyntaxError, IndentationError):
        value = sys.exc_info()[1]
        (lineno, offset, line) = value[1][1:]
        if line.endswith("\n"):
            line = line[:-1]
        print >> sys.stderr, 'could not compile %r:%d:' % (filename, lineno)
        print >> sys.stderr, line
        print >> sys.stderr, " " * (offset-2), "^"
        return

    try:
        w = Checker(tree, filename)
    except Exception, e:
        print >> sys.stderr, 'A problem occured in %s: %s' % (filename, e)
        return
        
    w.messages.sort(lambda a, b: cmp(a.lineno, b.lineno))
    filter_func = lambda m: isinstance(m, pyflakes.messages.UndefinedName)
    messages = filter(filter_func, w.messages)
    for warning in messages:
        print warning


def checkPath(filename):
    """Based on pyflakes bin"""
    return check(file(filename).read(), filename)


def _is_valid(f, wt, ignored_files=[]):
    if not f[0].endswith('.py'):
        return False
    if not f[2] == 'file':
        return False
    if f[0] in wt.filter_unversioned_files([f[0]]):
        return False
    if f[0] in ignored_files:
        return False
    return True


def ignored_files():
    confp = ConfigParser()
    if os.path.isfile('.bzrflakes'):
        confp = ConfigParser()
        confp.read('.bzrflakes')
        if confp.has_section('ignore'):
            path = confp.get('ignore', 'path')
            return path.split(':')
    return []


def undefined():
    wt = workingtree.WorkingTree.open('.')
    ignored = ignored_files()
    wt.lock_read()
    paths = [f[0] for f in wt.list_files(True) if _is_valid(f, wt, ignored)]
    wt.unlock()
    for f in paths:
        checkPath(f)

class cmd_undefined(commands.Command):
    """Looks for undefined names in python code."""
    def run(self):
        undefined()

class cmd_flakes_ignore(commands.Command):
    """Ignore specified files"""

    takes_args = ['paths*']

    def run(self, paths_list):
        if not os.path.exists('.bzrflakes'):
            fh = open('.bzrflakes', 'w')
            fh.close()
        confp = ConfigParser()
        confp.readfp(open('.bzrflakes'))
    
        # add section 'ignore'
        if not confp.has_section('ignore'):
            confp.add_section('ignore')
    
        if confp.has_option('ignore', 'path'):
            paths = confp.get('ignore', 'path')
            paths = ":".join(paths.split(':')+paths_list)
        else:
            paths = ":".join(paths_list)
        confp.set('ignore', 'path', paths)
        confp.write(file('.bzrflakes', 'w'))
    
    
    

def hook_undefined(local, master, old_revno, old_revid, future_revno, future_revid, tree_delta, future_tree):
    print ""
    print "Looking for undefined names."
    undefined()
    
commands.register_command(cmd_undefined)
commands.register_command(cmd_flakes_ignore)
Branch.hooks.install_named_hook('pre_commit', hook_undefined, 'pre commit undefined names')
