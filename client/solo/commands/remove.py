# -*- coding: utf-8 -*-
"""

    @author: Fabio Erculiani <lxnay@sabayon.org>
    @contact: lxnay@sabayon.org
    @copyright: Fabio Erculiani
    @license: GPL-2

    B{Entropy Command Line Client}.

"""
import sys
import argparse

from entropy.const import const_convert_to_unicode
from entropy.i18n import _
from entropy.output import blue, darkred, darkgreen, purple, teal, brown, \
    bold
from entropy.exceptions import DependenciesNotRemovable

import entropy.tools

from solo.utils import enlightenatom
from solo.commands.descriptor import SoloCommandDescriptor
from solo.commands._manage import SoloManage

class SoloRemove(SoloManage):
    """
    Main Solo Remove command.
    """

    NAME = "remove"
    ALIASES = ["rm"]
    ALLOW_UNPRIVILEGED = False

    INTRODUCTION = """\
Remove previously installed packages from system.
"""
    SEE_ALSO = "equo-install(1), equo-config(1)"

    def __init__(self, args):
        SoloManage.__init__(self, args)
        self._commands = {}

    def _get_parser(self):
        """
        Overridden from SoloCommand.
        """
        _commands = {}

        descriptor = SoloCommandDescriptor.obtain_descriptor(
            SoloRemove.NAME)
        parser = argparse.ArgumentParser(
            description=descriptor.get_description(),
            formatter_class=argparse.RawDescriptionHelpFormatter,
            prog="%s %s" % (sys.argv[0], SoloRemove.NAME))
        parser.set_defaults(func=self._remove)

        parser.add_argument(
            "packages", nargs='+',
            metavar="<package>", help=_("package name"))

        mg_group = parser.add_mutually_exclusive_group()
        mg_group.add_argument(
            "--ask", "-a", action="store_true",
            default=False,
            help=_("ask before making any changes"))
        _commands["--ask"] = {}
        _commands["-a"] = {}

        mg_group.add_argument(
            "--pretend", "-p", action="store_true",
            default=False,
            help=_("show what would be done"))
        _commands["--pretend"] = {}
        _commands["-p"] = {}

        parser.add_argument(
            "--verbose", "-v", action="store_true",
            default=False,
            help=_("verbose output"))
        _commands["--verbose"] = {}
        _commands["-v"] = {}

        parser.add_argument(
            "--nodeps", action="store_true",
            default=False,
            help=_("exclude package dependencies"))
        _commands["--nodeps"] = {}

        parser.add_argument(
            "--norecursive", action="store_true",
            default=False,
            help=_("do not calculate dependencies recursively"))
        _commands["--norecursive"] = {}

        parser.add_argument(
            "--deep", action="store_true",
            default=False,
            help=_("include dependencies no longer needed"))
        _commands["--deep"] = {}

        parser.add_argument(
            "--empty", action="store_true",
            default=False,
            help=_("when used with --deep, include virtual packages"))
        _commands["--empty"] = {}

        parser.add_argument(
            "--configfiles", action="store_true",
            default=False,
            help=_("remove package configuration files no longer needed"))
        _commands["--configfiles"] = {}

        parser.add_argument(
            "--force-system", action="store_true",
            default=False,
            help=_("force system packages removal (dangerous!)"))
        _commands["--force-system"] = {}

        self._commands = _commands
        return parser

    def bashcomp(self, last_arg):
        """
        Overridden from SoloCommand.
        """
        self._get_parser() # this will generate self._commands
        return self._hierarchical_bashcomp(last_arg, [], self._commands)

    def _remove(self, entropy_client):
        """
        Solo Remove command.
        """
        pretend = self._nsargs.pretend
        ask = self._nsargs.ask
        deps = not self._nsargs.nodeps
        deep = self._nsargs.deep
        empty = self._nsargs.empty
        recursive = not self._nsargs.norecursive
        system_packages_check = not self._nsargs.force_system
        remove_config_files = self._nsargs.configfiles
        packages = self._nsargs.packages

        exit_st, _show_cfgupd = self._remove_action(
            entropy_client, pretend, ask, deps, deep, empty,
            recursive, system_packages_check, remove_config_files,
            packages)
        if _show_cfgupd:
            self._show_config_files_update(entropy_client)
        return exit_st

    @staticmethod
    def _execute_action(entropy_client, inst_repo, removal_queue,
                        remove_config_files):
        """
        Execute the actual packages removal activity.
        """
        total = len(removal_queue)
        for count, package_id in enumerate(removal_queue, 1):

            atom = inst_repo.retrieveAtom(package_id)
            metaopts = {}
            metaopts['removeconfig'] = remove_config_files
            pkg = None
            try:
                pkg = entropy_client.Package()
                pkg.prepare((package_id,), "remove", metaopts)

                if "remove_installed_vanished" not in pkg.pkgmeta:

                    xterm_header = "equo (%s) :: %d of %d ::" % (
                        _("removal"), count, total)

                    entropy_client.output(
                        darkgreen(atom),
                        count=(count, total),
                        header=darkred(" --- ") + ">>> ")

                    exit_st = pkg.run(xterm_header = xterm_header)
                    if exit_st != 0:
                        return 1

            finally:
                if pkg is not None:
                    pkg.kill()

        entropy_client.output(
            "%s." % (blue(_("All done")),),
            header=darkred(" @@ "))
        return 0

    def _show_removal_info(self, entropy_client, package_ids,
                           manual=False):
        """
        Show packages removal information.
        """
        if manual:
            entropy_client.output(
                "%s:" % (
                    blue(_("These are the packages that "
                      "should be MANUALLY removed")),),
                header=darkred(" @@ "))
        else:
            entropy_client.output(
                "%s:" % (
                    blue(_("These are the packages that "
                      "would be removed")),),
                header=darkred(" @@ "))

        total = len(package_ids)
        inst_repo = entropy_client.installed_repository()

        for count, package_id in enumerate(package_ids, 1):

            atom = inst_repo.retrieveAtom(package_id)
            installedfrom = inst_repo.getInstalledPackageRepository(
                package_id)
            if installedfrom is None:
                installedfrom = _("Not available")

            on_disk_size = inst_repo.retrieveOnDiskSize(package_id)
            pkg_size = inst_repo.retrieveSize(package_id)
            extra_downloads = inst_repo.retrieveExtraDownload(package_id)
            for extra_download in extra_downloads:
                pkg_size += extra_download['size']
                on_disk_size += extra_download['disksize']

            disksize = entropy.tools.bytes_into_human(on_disk_size)
            disksize_info = "%s%s%s" % (
                bold("["),
                brown("%s" % (disksize,)),
                bold("]"))
            repo_info = bold("[") + brown(installedfrom) + bold("]")

            mytxt = "%s %s %s" % (
                repo_info,
                enlightenatom(atom),
                disksize_info)

            entropy_client.output(mytxt, header=darkred(" ## "))

    def _prompt_removal(self, entropy_client, inst_repo, package_ids,
                        system_packages_check):
        """
        Show list of packages that would be removed and ask User
        about dependencies calculation, if --ask has been provided.
        """
        ask = self._nsargs.ask
        verbose = self._nsargs.verbose
        pretend = self._nsargs.pretend
        plain_removal_queue = []
        deep_removal = True

        entropy_client.output(
            "%s:" % (
                teal(_("These are the chosen packages")),),
            header=darkgreen(" @@ "))

        total = len(package_ids)
        for count, package_id in enumerate(package_ids, 1):

            atom = inst_repo.retrieveAtom(package_id)
            if system_packages_check:
                valid = entropy_client.validate_package_removal(
                    package_id)
                if not valid:
                    mytxt = "%s: %s. %s." % (
                        enlightenatom(atom),
                        darkred(_("vital package")),
                        darkred(_("Removal forbidden")),
                    )
                    entropy_client.output(
                        mytxt,
                        level="warning",
                        count=(count, total),
                        header=bold("   !!! "))
                    continue

            plain_removal_queue.append(package_id)
            installedfrom = inst_repo.getInstalledPackageRepository(
                package_id)
            if installedfrom is None:
                installedfrom = _("Not available")

            on_disk_size = inst_repo.retrieveOnDiskSize(package_id)
            extra_downloads = inst_repo.retrieveExtraDownload(package_id)

            for extra_download in extra_downloads:
                on_disk_size += extra_download['disksize']

            disksize = entropy.tools.bytes_into_human(on_disk_size)
            disksizeinfo = " [%s]" % (
                bold(const_convert_to_unicode(disksize)),)

            entropy_client.output(
                "[%s] %s %s" % (
                    brown(installedfrom),
                    enlightenatom(atom),
                    disksizeinfo),
                count=(count, total),
                header=darkgreen("   # "))

        if verbose or ask or pretend:
            entropy_client.output(
                "%s: %d" % (
                    blue(_("Packages involved")),
                    total,),
                header=purple(" @@ "))

        return plain_removal_queue, deep_removal

    def _prompt_final_removal(self, entropy_client,
                              inst_repo, removal_queue):
        """
        Prompt some final information to User with respect to
        the removal queue.
        """
        total = len(removal_queue)
        mytxt = "%s: %s" % (
            blue(_("Packages that would be removed")),
            darkred(const_convert_to_unicode(total)),
        )
        entropy_client.output(
            mytxt, header=darkred(" @@ "))

        total_removal_size = 0
        total_pkg_size = 0
        for package_id in set(removal_queue):
            on_disk_size = inst_repo.retrieveOnDiskSize(package_id)
            if on_disk_size is None:
                on_disk_size = 0

            pkg_size = inst_repo.retrieveSize(package_id)
            if pkg_size is None:
                pkg_size = 0

            extra_downloads = inst_repo.retrieveExtraDownload(package_id)
            for extra_download in extra_downloads:
                pkg_size += extra_download['size']
                on_disk_size += extra_download['disksize']

            total_removal_size += on_disk_size
            total_pkg_size += pkg_size

        human_removal_size = entropy.tools.bytes_into_human(
            total_removal_size)
        human_pkg_size = entropy.tools.bytes_into_human(total_pkg_size)

        mytxt = "%s: %s" % (
            blue(_("Freed disk space")),
            bold(const_convert_to_unicode(human_removal_size)),
        )
        entropy_client.output(
            mytxt, header=darkred(" @@ "))

        mytxt = "%s: %s" % (
            blue(_("Total bandwidth wasted")),
            bold(str(human_pkg_size)),
        )
        entropy_client.output(
            mytxt, header=darkred(" @@ "))

    def _remove_action(self, entropy_client, pretend, ask,
                       deps, deep, empty, recursive,
                       system_packages_check, remove_config_files,
                       packages, package_ids=None):
        """
        Solo Remove action implementation.
        """
        inst_repo = entropy_client.installed_repository()
        if package_ids is None:
            packages = entropy_client.packages_expand(packages)
            package_ids = self._scan_installed_packages(
                entropy_client, inst_repo, packages)

        if not package_ids:
            entropy_client.output(
                darkred(_("No packages found")),
                level="error", importance=1)
            return 1, False

        plain_removal_queue, deep_removal = self._prompt_removal(
            entropy_client, inst_repo, package_ids, system_packages_check)

        if not plain_removal_queue:
            entropy_client.output(
                darkred(_("Nothing to do")),
                level="error", importance=1)
            return 1, False

        if ask and not pretend:
            if deps:
                question = "     %s" % (
                    _("Would you like to calculate dependencies ?"),
                )
                rc = entropy_client.ask_question(question)
                if rc == _("No"):
                    return 1, False
            else:
                question = "     %s" % (
                    _("Would you like to remove them now ?"),)
                deep_removal = False
                rc = entropy_client.ask_question(question)
                if rc == _("No"):
                    return 1, False

        removal_queue = []
        if deep_removal and deps:
            try:
                removal_queue += entropy_client.get_removal_queue(
                    plain_removal_queue,
                    deep = deep, recursive = recursive,
                    empty = empty,
                    system_packages = system_packages_check)
            except DependenciesNotRemovable as err:
                non_rm_pkg_ids = sorted(
                    [inst_repo.retrieveAtom(x[0]) for x in err.value])
                # otherwise we need to deny the request
                entropy_client.output("", level="error")
                entropy_client.output(
                    "  %s, %s:" % (
                        purple(_("Ouch!")),
                        brown(_("the following system packages"
                                " were pulled in")),
                        ),
                    level="error", importance=1)
                for pkg_in in non_rm_pkg_ids:
                    pkg_name = inst_repo.retrieveAtom(pkg_in)
                    entropy_client.output(
                        teal(pkg_name),
                        header=purple("    # "),
                        level="error")
                entropy_client.output("", level="error")
                return 1, False

        removal_queue += [x for x in plain_removal_queue if x \
            not in removal_queue]
        self._show_removal_info(entropy_client, removal_queue)
        self._prompt_final_removal(
            entropy_client, inst_repo, removal_queue)

        if pretend:
            return 0, False

        if ask:
            question = "     %s" % (
                _("Would you like to proceed ?"),)
            rc = entropy_client.ask_question(question)
            if rc == _("No"):
                return 1, False

        exit_st = self._execute_action(
            entropy_client, inst_repo, removal_queue,
            remove_config_files)
        return exit_st, True


SoloCommandDescriptor.register(
    SoloCommandDescriptor(
        SoloRemove,
        SoloRemove.NAME,
        _("remove packages from system"))
    )
