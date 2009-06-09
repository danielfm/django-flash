# -*- coding: utf-8 -*-

"""This module provides the :class:`FlashScope` class, which provides a simple
way to pass temporary objects between views.
"""

class FlashScope(object):
    """The purpose of this class is to implement the *flash* scope, which is
    a storage context that is a middle ground between the request context and
    the session context. More specifically, the *flash* scope provides a simple
    way to pass temporary objects from a view method to another (or to a view
    template).
    
    Anything you place in this scope will survive for the next request only,
    being automatically removed.

    The following operations are supported by :class:`FlashScope` instances:

    .. describe:: len(f)

       Returns the number of items in the flash scope *f*.

    .. describe:: f[key]

       Returns the item of *f* with key *key*.  Raises a :exc:`KeyError` if
       *key* is not in the flash scope.

    .. describe:: f[key] = value

       Sets ``f[key]`` to *value*.

    .. describe:: del f[key]

       Removes ``f[key]`` from *f*.  Raises a :exc:`KeyError` if *key* is not
       in the map.

    .. describe:: key in f

       Returns ``True`` if *f* has a key *key*, else ``False``.

    .. describe:: key not in f

       Equivalent to ``not key in f``.

    .. describe:: f.now[key] = value

       Sets ``f[key]`` to *value* and marks it as *used*.

    .. describe:: f.now(**items)

       Puts the given *items* into *f* and marks them as *used*.
    """

    def __init__(self):
        """Returns a new :class:`FlashScope` object.
        """
        self._session = {}
        self._used = {}
        self.now = _ImmediateFlashScopeAdapter(self)

    def __contains__(self, key):
        """Returns ``True`` if there's a value under the given *key*.
        """
        return key in self._session

    def __getitem__(self, key):
        """Retrieves a value. Raises a :exc:`KeyError` if *key* does not exists.
        """
        return self._session[key]

    def __setitem__(self, key, value):
        """Puts a *value* into this flash scope under the given *key*.
        """
        self._session[key] = value
        self._update_status(key, is_used=False)

    def __delitem__(self, key):
        """Removes the value under the given *key*.
        """
        if key in self:
            del self._session[key]
        if key in self._used:
            del self._used[key]

    def __len__(self):
        """Returns the number of values inside this flash scope.
        """
        return len(self._session)

    def _update_status(self, key=None, is_used=True):
        """Updates the status of a given value (or all values if no *key*
        is given). The *is_used* argument tells if that value should be marked
        as *used* (should be discarded) or *unused* (should be kept).

        If a *used* value is being marked as *used* again, it is automatically
        removed from this flash scope.
        """
        if not key:
            for existing_key in self.keys():
                self._update_status(existing_key, is_used)
        else:
            if not is_used:
                if key in self._used:
                    del self._used[key]
            else:
                if key in self._used:
                    del self[key]
                else:
                    self._used[key] = None

    def keys(self):
        """Returns the list of keys.
        """
        return self._session.keys()

    def values(self):
        """Returns the list of values.
        """
        return self._session.values()

    def items(self):
        """Returns the list of items as tuples ``(key, value)``.
        """
        return self._session.items()

    def iterkeys(self):
        """Returns an iterator over the keys.
        """
        return self._session.iterkeys()

    def itervalues(self):
        """Returns an iterator over the values.
        """
        return self._session.itervalues()

    def iteritems(self):
        """Returns an iterator over the ``(key, value)`` items.
        """
        return self._session.iteritems()

    def get(self, key, default=None):
        """Gets the value under the given *key*. If the *key* doesn't exists,
        the *default* value is returned instead.
        """
        return self._session.get(key, default)

    def pop(self, key, default=None):
        """Removes the specified *key* and returns the corresponding value. If
        *key* is not found, *default* is returned instead.
        """
        value = self._session.pop(key, default)
        if key in self._used:
            del self._used[key]
        return value

    def has_key(self, key):
        """Returns ``True`` if there's a value under the given *key*.

        .. deprecated:: 1.4.2
           :meth:`has_key()` is deprecated in favor of ``key in f``.
        """
        return self._session.has_key(key)

    def put(self, **kwargs):
        """Puts one or more values into this flash scope.
        """
        for key, value in kwargs.items():
            self[key] = value

    def clear(self):
        """Removes all items from this flash scope.
        """
        self._session.clear()
        self._used.clear()

    def put_immediate(self, key, value):
        """Puts a value inside this flash scope and marks it as *used*.
        """
        self._session[key] = value
        self._update_status(key)

    def discard(self, *keys):
        """Marks the entire current flash or a single value as *used*, so when
        the next request hit the server, those values will be automatically
        removed from this flash scope by :class:`FlashMiddleware`.
        """
        self._update_status(*keys)

    def keep(self, *keys):
        """Prevents specific values from being removed on the next request.
        If this method is called with no args, the entire flash is preserved.
        """
        if not keys:
            self._update_status(is_used=False)
        else:
            for key in keys:
                self._update_status(key, is_used=False)

    def update(self):
        """Mark for removal entries that were kept, and delete unkept ones.

        .. note::
           This method is called automatically by
           :class:`djangoflash.middleware.FlashMiddleware` when a HTTP
           request hits the server, so never call this method yourself, unless
           you have a very good reason to do so.
        """
        self._update_status()


class _ImmediateFlashScopeAdapter(object):
    """This class is used to add support for immediate flash values to an
    existing instance of :class:`FlashScope`. An immediate flash value is a
    value that is available to this request, but not to the next.
    """

    def __init__(self, delegate):
        """Returns a new :class:`_ImmediateFlashScopeAdapter` object which
        delegates certain calls to the given *delegate*.
        """
        self.delegate = delegate

    def __getitem__(self, key):
        """Retrieves a value. Raises a :exc:`KeyError` if *key* does
        not exists.
        """
        return self.delegate[key]

    def __contains__(self, key):
        """Returns ``True`` if there's a value under the given *key*.
        """
        return key in self.delegate

    def __setitem__(self, key, value):
        """Puts a *value* that *won't* be available to the next request, only to
        the current.
        """
        self.delegate.put_immediate(key, value)

    def __call__(self, **kwargs):
        """Puts values that *won't* be available to the next request, only to
        the current.
        """
        for key, value in kwargs.items():
            self[key] = value
