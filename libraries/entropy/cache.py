# -*- coding: utf-8 -*-
'''
    # DESCRIPTION:
    # Entropy Object Oriented Interface

    Copyright (C) 2007-2009 Fabio Erculiani

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
'''
# pylint ~ ok

from __future__ import with_statement
from entropy.core import Singleton
from entropy.misc import TimeScheduled, Lifo
import time

class EntropyCacher(Singleton):
    """
        Entropy asynchronous and synchronous cache writer
        and reader. This class is a Singleton and contains
        a thread doing the cache writes asynchronously, thus
        it must be stopped before your application is terminated
        calling the stop() method.
    """

    import entropy.dump as dumpTools
    import entropy.tools as entropyTools
    import copy

    def init_singleton(self):
        """
        Singleton overloaded method. Equals to __init__.
        This is the place where all the properties initialization
        takes place.
        """
        import threading
        self.__alive = False
        self.__cache_writer = None
        self.__cache_buffer = Lifo()
        self.__cache_lock = threading.Lock()

    def __copy_obj(self, obj):
        """
        Return a copy of an object done by the standard
        library "copy" module.

        @param obj: object to copy
        @type obj: any Python object
        @rtype: copied object
        @return: copied object
        """
        return self.copy.deepcopy(obj)

    def __cacher(self):
        """
        This is where the actual asynchronous copy takes
        place. __cacher runs on a different threads and
        all the operations done by this are atomic and
        thread-safe. It just loops over and over until
        __alive becomes False.
        """
        while 1:
            if not self.__alive:
                break
            with self.__cache_lock:
                data = self.__cache_buffer.pop()
            if data == None:
                break
            key, data = data
            d_o = self.dumpTools.dumpobj
            if not d_o:
                break
            d_o(key, data)

    def __del__(self):
        self.stop()

    def start(self):
        """
        This is the method used to start the asynchronous cache
        writer but also the whole cacher. If this method is not
        called, the instance will always trash and cache write
        request.

        @return: None
        """
        with self.__cache_lock:
            self.__cache_buffer.clear()
        self.__cache_writer = TimeScheduled(1, self.__cacher)
        self.__cache_writer.set_delay_before(True)
        self.__cache_writer.start()
        while not self.__cache_writer.isAlive():
            continue
        self.__alive = True

    def is_started(self):
        """
        Return whether start is called or not. This equals to
        checking if the cacher is running, thus is writing cache
        to disk.

        @return: None
        """
        return self.__alive

    def stop(self):
        """
        This method stops the execution of the cacher, which won't
        accept cache writes anymore. The thread responsible of writing
        to disk is stopped here and the Cacher will be back to being
        inactive. A watchdog will avoid the thread to freeze the
        call if the write buffer is overloaded.

        @return: None
        """

        self.__alive = False
        watch_dog = 20
        while self.__cache_buffer.is_filled() and (watch_dog > 0):
            watch_dog -= 1
            time.sleep(0.5)

        with self.__cache_lock:
            self.__cache_buffer.clear()
        if self.__cache_writer != None:
            self.__cache_writer.kill()
            self.__cache_writer.join()
            self.__cache_writer = None

    def sync(self, wait = False):
        """
        This method can be called anytime and forces the instance
        to flush all the cache writes queued to disk. If wait == False
        a watchdog prevents this call to get stuck in case of write
        buffer overloads.

        @param wait: indicates if waiting until done (synchronous mode)
            or not
        @type wait: bool

        @return: None
        """
        if not self.__alive:
            self.__cache_buffer.clear()
            return

        watch_dog = 10
        while self.__cache_buffer.is_filled() and ((watch_dog > 0) or wait) \
            and self.__alive:

            if not wait:
                watch_dog -= 1
            time.sleep(0.5)

        self.__cache_buffer.clear()

    def discard(self):
        """
        This method makes buffered cache to be discarded synchronously.

        @return: None
        """
        self.__cache_buffer.clear()
        with self.__cache_lock:
            self.__cache_buffer.clear() # make sure twice

    def push(self, key, data, async = True):
        """
        This is the place where data is either added
        to the write queue or written to disk (if async == False)
        only and only if start() method has been called.

        @param key: cache data identifier
        @type key: basestring
        @param data: picklable object
        @type data: any picklable object
        @param async: store cache asynchronously or not
        @type async: bool
        @rtype: None
        @return: nothing
        """
        if not self.__alive:
            return
        if async:
            with self.__cache_lock:
                self.__cache_buffer.push((key, self.__copy_obj(data),))
        else:
            self.dumpTools.dumpobj(key, data)

    def pop(self, key):
        """
        This is the place where data is retrieved from cache.
        You must know the cache identifier used when push()
        was called.

        @param key: cache data identifier
        @type key: basestring
        @rtype: Python object
        @return: object stored into the stack or None (if stack is empty)
        """
        with self.__cache_lock:
            l_o = self.dumpTools.loadobj
            if not l_o:
                return
            return l_o(key)

