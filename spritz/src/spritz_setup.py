#!/usr/bin/python -tt
# -*- coding: iso-8859-1 -*-
#    Yum Exteder (yumex) - A GUI for yum
#    Copyright (C) 2006 Tim Lauridsen < tim<AT>yum-extender<DOT>org > 
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import os, sys
from entropyConstants import *
from entropy_i18n import _

class const:
    ''' This Class contains all the Constants in Yumex'''
    __spritz_version__   = etpConst['entropyversion']
    # Paths
    MAIN_PATH = os.path.abspath( os.path.dirname( sys.argv[0] ) )
    GLADE_FILE = MAIN_PATH+'/spritz.glade'
    if not os.path.isfile(GLADE_FILE):
        MAIN_PATH = '/usr/lib/entropy/spritz'
        GLADE_FILE = MAIN_PATH+'/spritz.glade'
    if MAIN_PATH == '/usr/lib/entropy/spritz':
        PIXMAPS_PATH = '/usr/share/pixmaps/spritz'
    else:
        PIXMAPS_PATH = MAIN_PATH+'/../gfx'
    if MAIN_PATH == '/usr/lib/entropy/spritz':
        ICONS_PATH = '/usr/share/pixmaps/spritz'
    else:
        ICONS_PATH = MAIN_PATH+'/pixmaps'

    pkg_pixmap = PIXMAPS_PATH+'/package-x-generic.png'
    ugc_small_pixmap = PIXMAPS_PATH+'/ugc.png'
    ugc_pixmap = PIXMAPS_PATH+'/ugc/icon.png'
    ugc_pixmap_small = PIXMAPS_PATH+'/ugc/icon_small.png'
    refresh_pixmap = PIXMAPS_PATH+'/ugc/refresh.png'
    star_normal_pixmap = PIXMAPS_PATH+'/star.png'
    star_selected_pixmap = PIXMAPS_PATH+'/star_selected.png'
    star_empty_pixmap = PIXMAPS_PATH+'/star_empty.png'
    empty_background = PIXMAPS_PATH+'/empty.png'
    loading_pix = PIXMAPS_PATH+'/loading.gif'

    # UGC
    ugc_ok_pix = PIXMAPS_PATH+'/ugc/ok.png'
    ugc_error_pix = PIXMAPS_PATH+'/ugc/error.png'
    ugc_generic_pix = PIXMAPS_PATH+'/ugc/generic.png'
    ugc_text_pix = PIXMAPS_PATH+'/ugc/text.png'
    ugc_video_pix = PIXMAPS_PATH+'/ugc/video.png'
    ugc_image_pix = PIXMAPS_PATH+'/ugc/image.png'
    ugc_view_pix = PIXMAPS_PATH+'/ugc/view.png'

    # ads
    plain_ad_pix = PIXMAPS_PATH+'/ad.png'

    # package categories
    PACKAGE_CATEGORIES = [
        "None",
        "Groups",
        "RPM Groups",
        "Age"]

    DAY_IN_SECONDS = 86400
    # Page -> Notebook page numbers
    PAGE_REPOS = 0
    PAGE_PKG = 1
    PAGE_OUTPUT = 2
    PAGE_GROUP = 3
    PAGE_QUEUE = 4
    PAGE_FILESCONF = 5
    PAGE_GLSA = 6
    PAGE_PREFERENCES = 7
    PAGES = {
       'packages'  : PAGE_PKG,
       'repos'     : PAGE_REPOS,
       'output'    : PAGE_OUTPUT,
       'queue'     : PAGE_QUEUE,
       'group'     : PAGE_GROUP,
       'filesconf' : PAGE_FILESCONF,
       'glsa'      : PAGE_GLSA,
       'preferences': PAGE_PREFERENCES
    }

    PREF_PAGE_SYSTEM = 0
    PREF_PAGE_NETWORKING = 1
    PREF_PAGE_UGC = 2
    PREF_PAGES = {
        'system': PREF_PAGE_SYSTEM,
        'networking': PREF_PAGE_NETWORKING,
        'ugc': PREF_PAGE_UGC
    }

    PACKAGE_PROGRESS_STEPS = ( 0.1, # Depsolve
                               0.5, # Download
                               0.1, # Transaction Test
                               0.3 ) # Running Transaction

    SETUP_PROGRESS_STEPS = ( 0.1, # Yum Config
                             0.2, # Repo Setup
                             0.1, # Sacksetup
                             0.2, # Updates
                             0.1, # Group
                             0.3) # get package Lists

    CREDITS = (
           (('Spritz Package Manager - %s' % __spritz_version__),
           ('Copyright 2008','Fabio Erculiani')),

           (_("Programming:"),
           ("Fabio Erculiani",)),

           (_("Translation:"),
            (
                "Andre Parhan (Dutch)",
                "Fabio Erculiani (Italian)",
                "Roger Calvò (Catalan)",
                "Daniel Halens (Spanish)",
                "N/A (French)",
                "N/A (German)",
                "N/A (Polish)",
                "N/A (Russian)",
                )
            ),


           (_("Dedicated to:"),
                ("Sergio Erculiani",)
           )

          )

class SpritzConf:
    """ Yum Extender Config Setting"""
    autorefresh = True
    recentdays = 14
    debug = False
    plugins = True
    usecache = False
    proxy = ""
    font_console = 'Monospace 8'
    font_pkgdesc = 'Monospace 8'

    color_console_background = '#FFFFFF'
    color_console_font = '#000000' # black
    color_normal = '#000000' # black
    color_install = '#418C0F' # dark green
    color_update = '#418C0F' #  dark green
    color_remove = '#A71B1B' # red
    color_reinstall = '#A71B1B'
    color_title = '#A71B1B' # red
    color_title2 = '#2A6AFF' # light blue
    # description below package atoms
    color_pkgdesc = '#FF1D1D' # red
    # description for masked packages and for pkg description in dialogs, notice board desc items
    color_pkgsubtitle = '#418C0F' # dark green
    color_subdesc = '#837350' # brown
    color_error = '#A71B1B' # red
    color_good = '#418C0F' # dark green
    color_background_good = '#418C0F' # red
    color_background_error = '#A71B1B' # dark green
    color_good_on_color_background = '#FFFFFF'
    color_error_on_color_background = '#FFFFFF'

    filelist = True
    changelog = False
    disable_repo_page = False
    branding_title = 'Spritz Package Manager'
    dummy_empty = 0
    dummy_category = 1

def cleanMarkupString(msg):
    import gobject
    msg = str(msg) # make sure it is a string
    msg = gobject.markup_escape_text(msg)
    #msg = msg.replace('@',' AT ')
    #msg = msg.replace('<','[')
    #msg = msg.replace('>',']')
    return msg

from htmlentitydefs import codepoint2name
def unicode2htmlentities(u):
   htmlentities = list()
   for c in u:
      if ord(c) < 128:
         htmlentities.append(c)
      else:
         htmlentities.append('&%s;' % codepoint2name[ord(c)])
   return ''.join(htmlentities)

class fakeoutfile:
    """
    A general purpose fake output file object.
    """

    def __init__(self, fn):
        self.fn = fn
        self.text_written = []

    def close(self):
        pass

    def flush(self):
        pass

    def fileno(self):
        return self.fn

    def isatty(self):
        return False

    def read(self, a):
        return ''

    def readline(self):
        return ''

    def readlines(self):
        return []

    def write(self, s):
        os.write(self.fn,s)
        #os.fsync(self.fn)
        self.text_written.append(s)
        # cut at 1024 entries
        if len(self.text_written) > 1024:
            self.text_written = self.text_written[-1024:]

    def write_line(self, s):
        self.write(s)

    def writelines(self, l):
        for s in l:
            self.write(s)

    def seek(self, a):
        raise IOError, (29, 'Illegal seek')

    def tell(self):
        raise IOError, (29, 'Illegal seek')

    def truncate(self):
        self.tell()

class fakeinfile:
    """
    A general purpose fake input file object.
    """
    def __init__(self, fn):
        self.fn = fn
        self.text_read = ''

    def close(self):
        pass

    def flush(self):
        pass

    def fileno(self):
        return self.fn

    def isatty(self):
        return False

    def read(self, a):
        return self.readline(count = a)

    def readline(self, count = 2048):
        x = os.read(self.fn,count)
        self.text_read += x
        return x

    def readlines(self):
        return self.readline().split("\n")

    def write(self, s):
        raise IOError, (29, 'Illegal seek')

    def writelines(self, l):
        raise IOError, (29, 'Illegal seek')

    def seek(self, a):
        raise IOError, (29, 'Illegal seek')

    def tell(self):
        raise IOError, (29, 'Illegal seek')

    truncate = tell