# -*- coding: utf-8 -*-

"""This module provides the :class:`FlashScope` class, which is responsible
to maintain the flash-scoped objects and control their lifecycle.

.. testsetup::

   from djangoflash.models import FlashScope

"""

class FlashScope(object):
    """This is the class responsible to maintain the flash-scoped objects
    and control their lifecycle. It works pretty much like a regular
    :class:`dict` object, but with some additional methods to *activate*
    and *expire* the flash-soped objects between requests.
    """
    
    def __init__(self):
        """Return a new :class:`FlashScope` object.
        """
        self._current = {}
        self._current_age = {}  # Stores the "age" of each flash-scoped object
        self._active = {}      # Stores just the active flash-scoped objects
    
    def __contains__(self, key):
        """Returns ``True`` if there's an *active* flash-scoped object under
        the given *key*.
        """
        return key in self._active
    
    def __getitem__(self, key):
        """Retrieves an *active* flash-scoped object. Raises a
        :exc:`KeyError` if *key* does not exists.
        """
        return self._active[key]
    
    def __setitem__(self, key, value):
        """Puts a *value* into this flash scope under the given *key*.
        """
        self._current[key] = value
        self._current_age[key] = 0
    
    def __delitem__(self, key):
        """Removes this flash-scoped object under the given *key*.
        """
        del self._current[key]
        del self._current_age[key]
        if self._active.has_key(key):
            del self._active[key]
    
    def __len__(self):
        """Returns the number of *active* flash-scoped objects.
        """
        return len(self._active)
    
    def is_active_empty(self):
        """Returns ``True`` if there's no *active* flash-scoped object.
        
        Example usage:
        
        .. doctest::
           
           >>> flash = FlashScope()
           >>> flash['message'] = 'My message'
           >>> flash.is_active_empty()
           True
           >>> flash.increment_age()
           >>> flash.is_active_empty()
           False
           >>> flash['message']
           'My message'
        """
        return len(self) == 0
    
    def is_current_empty(self):
        """Returns ``True`` if there's no flash-scoped objects at all.
        
        Example usage:
        
        .. doctest::
           
           >>> flash = FlashScope()
           >>> flash['message'] = 'My message'
           >>> flash.is_current_empty()
           False
           >>> flash.increment_age()
           >>> flash.is_active_empty()
           False
           >>> flash['message']
           'My message'
           >>> flash.increment_age()
           >>> flash.is_current_empty()
           True
        """
        return len(self._current) == 0
    
    def keys(self):
        """Returns the keys of all *active* flash-scoped objects.
        """
        return self._active.keys()
    
    def items(self):
        """Returns the list of all *active* flash-scoped objects as
        tuples ``(key, value)``.
        """
        return self._active.items()
    
    def get(self, key, default=None):
        """Gets the *active* flash-scoped object under the given *key*. If
        the *key* doesn't exists, the *default* value is returned instead.
        """
        return self._active.get(key, default)
    
    def pop(self, key, *args):
        """Removes and returns the *active* flash-scoped object under the
        given *key*.
        """
        value = self._active.pop(key, *args)
        del self._current_age[key]
        return value
    
    def has_key(self, key):
        """Returns ``True`` if there's an *active* flash-scoped object under the
        given *key*.
        """
        return self._active.has_key(key)
    
    def values(self):
        """Returns the list of all *active* flash-scoped objects.
        """
        return self._active.values()
    
    def iterkeys(self):
        """Returns an iterator over the keys of all *active* flash-scoped
        objects.
        """
        return self._active.iterkeys()
    
    def itervalues(self):
        """Returns an iterator over the values of all *active* flash-scoped
        objects.
        """
        return self._active.itervalues()
    
    def iteritems(self):
        """Returns an iterator over the items ``(key, value)`` of all *active*
        flash-scoped objects.
        """
        return self._active.iteritems()
    
    def put(self, **kwargs):
        """Puts values into this flash scope. This method is an alias to
        :meth:`__setitem__`.
        """
        for key, value in kwargs.items():
            self[key] = value
    
    def now(self, **kwargs):
        """Puts *active* values into this flash scope. Use this method when
        you need to make a flash-scoped object available to the current
        request; otherwise you would have to wait for the next request for
        this object to become *active*.
        
        .. note ::
        
           The flash-scoped objects added with :meth:`now` are *transient*,
           that is, they are going to be removed from this flash scope even
           if you :meth:`keep` them.
        
        Example usage:
        
        .. doctest::
        
           >>> flash = FlashScope()
           >>> flash.now(message='My message')
           >>> flash['message']
           'My message'
           >>> flash.keep('message') # Cannot keep a transient object
           >>> flash.increment_age()
           >>> 'message' in flash
           False
        
        """
        for key, value in kwargs.items():
            self._active[key] = value
    
    def keep(self, *args):
        """Prevents the given non-transient flash-scoped objects from being
        expired in the next request. If this method is called with no
        *args*, it acts on all flash-scoped objects.
        
        Example usage:
        
        .. doctest::
           
           >>> flash = FlashScope()
           >>> flash['message'] = 'My message'
           >>> flash.increment_age()
           >>> 'message' in flash
           True
           >>> flash.keep('message')
           >>> flash.increment_age()
           >>> 'message' in flash
           True
        
        """
        for key, value in self._current_age.items():
            if not args or key in args:
                if value > 0:
                    self._current_age[key] -= 1
    
    def _update_active(self):
        """Updates the dictionary that holds the *active* flash-scoped
        objects.
        """
        self._active = {}
        for key in self._current_age.keys():
            if not self._current_age[key] == 0:
                self._active[key] = self._current[key]
    
    def increment_age(self):
        """Increment the age of flash-scoped objects. After that, all old
        objects are automatically removed from this flash scope.
        
        .. note ::
        
           This method is called automatically by
           :class:`djangoflash.middleware.FlashMiddleware` when a HTTP
           request arrives, so **never** call this method yourself, unless you
           have a very good reason to do so.
        """
        for key, value in self._current_age.items():
            if value+1 < 2:
                self._current_age[key] += 1
            else:
                del self[key]
        self._update_active()
