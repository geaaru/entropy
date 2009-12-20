#!/usr/bin/python2 -O
# -*- coding: utf-8 -*-
"""

    @author: Fabio Erculiani <lxnay@sabayonlinux.org>
    @contact: lxnay@sabayonlinux.org
    @copyright: Fabio Erculiani
    @license: GPL-2

    B{Entropy Package Manager Server}.

"""

import os, sys
sys.path.insert(0, '../libraries')
sys.path.insert(1, '../client')
sys.path.insert(2, '../server')
sys.path.insert(3, '/usr/lib/entropy/client')
sys.path.insert(4, '/usr/lib/entropy/libraries')
sys.path.insert(5, '/usr/lib/entropy/server')
from entropy.i18n import _
import entropy.tools as entropyTools
from entropy.output import *
from entropy.const import *
from entropy.core.settings.base import SystemSettings
SysSettings = SystemSettings()

# Check if we need to disable colors
if not is_stdout_a_tty():
    nocolor()

myopts = [
    None,
    (0, " ~ "+SysSettings['system']['name']+" ~ "+sys.argv[0]+" ~ ", 1, 'Entropy Package Manager - (C) %s' % (entropyTools.get_year(),) ),
    None,
    (0, _('Basic Options'), 0, None),
    None,
    (1, '--help', 2, _('this output')),
    (1, '--version', 1, _('print version')),
    (1, '--nocolor', 1, _('disable colorized output')),
    None,
    (0, _('Application Options'), 0, None),
    None,
    (1, 'update', 3, _('scan the System looking for newly compiled packages')),
        (2, '--seekstore', 2, _('analyze the Entropy Store directory directly')),
        (2, '--repackage <atoms>', 1, _('repackage the specified atoms')),
        (2, '--noask', 2, _('do not ask anything except critical things')),
        (2, '--atoms <atoms>', 1, _('manage only the specified atoms')),
        (2, '--interactive', 2, _('run in interactive mode (asking things one by one)')),
    None,
    (1, 'inject <packages>', 1, _('add binary packages to repository w/o affecting scopes (multipackages)')),
    None,
    (1, 'query', 3, _('do some searches into repository databases')),
        (2, 'search', 3, _('search packages inside the default repository database')),
        (2, 'needed', 3, _('show runtime libraries needed by the provided atoms')),
        (2, 'depends', 2, _('show what packages depend on the provided atoms')),
        (2, 'tags', 3, _('show packages owning the specified tags')),
        (2, 'sets', 3, _('search available package sets')),
        (2, 'files', 3, _('show files owned by the provided atoms')),
        (2, 'belongs', 2, _('show from what package the provided files belong')),
        (2, 'description', 2, _('search packages by description')),
        (2, 'eclass', 3, _('search packages using the provided eclasses')),
        (2, 'list', 3, _('list all the packages in the default repository')),
        (2, 'graph', 3, _('show direct depdendencies tree for provided installable atoms')),
            (3, '--complete', 1, _('include system packages, build deps and circularity information')),
        (2, 'revgraph', 2, _('show reverse depdendencies tree for provided installed atoms')),
            (3, '--complete', 1, _('include system packages, build deps and circularity information')),
        (2, '--verbose', 2, _('show more details')),
        (2, '--quiet', 2, _('print results in a scriptable way')),
    None,
    (1, 'database', 2, _('repository database functions')),
        (2, '--initialize', 3, _('(re)initialize the current repository database')),
            (3, '--empty', 2, _('do not refill database using packages on mirrors')),
            (3, '--repo=<repo>', 2, _('(re)create the database for the specified repository')),
        (2, 'bump', 4, _('manually force a revision bump for the current repository database')),
            (3, '--sync', 3, _('synchronize the database')),
        (2, 'flushback [branches]', 2, _('flush back old branches packages to current branch')),
        (2, 'remove', 4, _('remove the provided atoms from the current repository database')),
        (2, 'multiremove', 3, _('remove the provided injected atoms (all if no atom specified)')),
        (2, 'create-empty-database', 2, _('create an empty repository database in the provided path')),
        (2, 'switchbranch <from branch> <to branch>', 3, _('switch to the specified branch the repository')),
        (2, 'md5remote', 3, _('verify remote integrity of the provided atoms (or world)')),
        (2, 'backup', 4, _('backup current repository database')),
        (2, 'restore', 4, _('restore a previously backed-up repository database')),
    None,
    (1, 'repo', 3, _('manage a repository')),
        (2, 'enable <repo>', 3, _('enable the specified repository')),
        (2, 'disable <repo>', 3, _('disable the specified repository')),
        (2, 'status <repo>', 3, _('show the current Server Interface status')),
        (2, 'manual-deps <repo> [atoms]', 1, _('handle packages manual dependencies')),
        (2, 'package-tag <repo> <tag-string> [atoms]', 1, _('clone a package assigning it an arbitrary tag')),
        (2, 'move <from> <to> [atoms]', 1, _('move packages from a repository to another')),
            (3, '--deps', 3, _('pulls dependencies in')),
        (2, 'copy <from> <to> [atoms]', 1, _('copy packages from a repository to another')),
            (3, '--deps', 3, _('pulls dependencies in')),
        (2, 'default <repo_id>', 2, _('set the default repository')),
    None,
    (1, 'spm', 3, _('source package manager functions')),
        (2, 'compile', 3, _('compilation function')),
            (3, 'categories', 2, _('compile packages belonging to the provided categories')),
                (4, '--list', 2, _('just list packages')),
                (4, '--nooldslots', 1, _('do not pull old package slots')),
            (3, 'pkgset', 3, _('compile packages in provided package set names')),
                (4, '--list', 2, _('just list packages')),
                (4, '--rebuild', 1, _('rebuild everything')),
                (4, '--dbupdate', 1, _('run database update if all went fine')),
                (4, '--dbsync', 1, _('run mirror sync if all went fine')),
        (2, 'orphans', 3, _('scan orphaned packages on SPM')),
    None,
    (1, 'deptest', 2, _('look for unsatisfied dependencies')),
    (1, 'libtest', 2, _('look for missing libraries')),
        (2, '--dump', 2, _('dump results to files')),
    (1, 'pkgtest', 2, _('verify the integrity of local package files')),
    (1, 'depends', 2, _('regenerate the depends table')),
    (1, 'libpaths', 2, _('regenerate the library paths table')),
    None,
    (1, 'cleanup', 2, _('remove downloaded packages and clean temp. directories)')),
    None,
]

options = sys.argv[1:]

# print version
if (' '.join(options).find("--version") != -1) or (' '.join(options).find(" -V") != -1):
    print_generic("reagent: "+etpConst['entropyversion'])
    raise SystemExit(0)

import re
opt_r = re.compile("^(\\-)([a-z]+)$")
for n in range(len(options)):
    if opt_r.match(options[n]):
        x = options[n]
        del options[n]
        options.extend(["-%s" % (d,) for d in x[1:]])

# preliminary options parsing
_options = []
for opt in options:
    if opt == "--nocolor":
        nocolor()
    elif opt in ["--quiet", "-q"]:
        etpUi['quiet'] = True
    elif opt in ["--verbose", "-v"]:
        etpUi['verbose'] = True
    elif opt in ["--ask", "-a"]:
        etpUi['ask'] = True
    elif opt in ["--pretend", "-p"]:
        etpUi['pretend'] = True
    else:
        _options.append(opt)
options = _options

# print help
if len(options) < 1 or ' '.join(options).find("--help") != -1 or ' '.join(options).find(" -h") != -1:
    print_menu(myopts)
    if len(options) < 1:
        print_error("not enough parameters")
    raise SystemExit(1)

rc = 1
if not entropyTools.is_root():
    print_error("you must be root in order to run "+sys.argv[0])

elif (options[0] == "update"):
    import server_reagent
    rc = server_reagent.update(options[1:])
    server_reagent.Entropy.close_server_databases()

elif (options[0] == "inject"):
    import server_reagent
    rc = server_reagent.inject(options[1:])
    server_reagent.Entropy.close_server_databases()

# database tool
elif (options[0] == "database"):
    if "switchbranch" in options:
        etpUi['warn'] = False
    import server_reagent
    server_reagent.database(options[1:])
    server_reagent.Entropy.close_server_databases()
    rc = 0

elif (options[0] == "query"):
    import server_query
    rc = server_query.query(options[1:])

elif (options[0] == "repo"):
    import server_reagent
    rc = server_reagent.repositories(options[1:])

elif (options[0] == "deptest"):
    import server_reagent
    server_reagent.Entropy.dependencies_test()
    server_reagent.Entropy.close_server_databases()
    rc = 0

elif (options[0] == "pkgtest"):

    import server_reagent
    server_reagent.Entropy.verify_local_packages(["world"], ask = etpUi['ask'])
    server_reagent.Entropy.close_server_databases()
    rc = 0

elif (options[0] == "libtest"):
    import server_reagent
    dump = "--dump" in options
    rc, pkgs = server_reagent.Entropy.test_shared_objects(
        dump_results_to_file = dump)
    x = server_reagent.Entropy.close_server_databases()

elif (options[0] == "depends"):
    import server_reagent
    rc = server_reagent.Entropy.depends_table_initialize()
    server_reagent.Entropy.close_server_databases()

elif (options[0] == "libpaths"):
    import server_reagent
    rc = server_reagent.Entropy.library_paths_table_initialize()
    server_reagent.Entropy.close_server_databases()

# cleanup
elif (options[0] == "cleanup"):
    rc = entropyTools.cleanup()

# deptest tool
elif (options[0] == "spm"):
    import server_reagent
    rc = server_reagent.spm(options[1:])
    server_reagent.Entropy.close_server_databases()

const_kill_threads()
raise SystemExit(rc)