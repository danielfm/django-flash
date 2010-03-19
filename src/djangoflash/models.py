# -*- coding: utf-8 -*-

"""This module provides the :class:`FlashScope` class, which provides a simple
way to pass temporary objects between views.
"""


# Map keys used when exporting/importing a FlashScope to/from a dict
_SESSION_KEY = '_session'
_USED_KEY    = '_used'


class FlashScope(object):
    """The purpose of this class is to implement the *flash*, which is a
    temporary storage mechanism that looks like a Python dictionary, so you
    can store values associated with keys and later retrieve them.
    
    It has one special property: by default, values stored into the *flash*
    during the processing of a request will be available during the processing
    of the immediately following request. Once that second request has been
    processed, those values are removed automatically from the storage.
    
    The following operations are supported by :class:`FlashScope` instances:

    .. describe:: len(flash)

       Returns the number of items in *flash*.

    .. describe:: flash[key]

       Returns the item of *flash* with key *key*.  Raises a :exc:`KeyError` if
       *key* is not found.

    .. describe:: flash[key] = value

       Sets ``flash[key]`` to *value*.

    .. describe:: flash(**items)

       Puts *items* into *flash*.

    .. describe:: del flash[key]

       Removes ``flash[key]``. Raises a :exc:`KeyError` if *key* is not found.

    .. describe:: key in flash

       Returns ``True`` if *flash* has a key *key*, else ``False``.

    .. describe:: key not in flash

       Equivalent to ``not key in flash``.

    .. describe:: flash.now[key] = value

       Sets ``flash[key]`` to *value* and marks it as *used*.

    .. describe:: flash.now(**items)

       Puts *items* into *flash* and marks those items  as *used*.

    .. describe:: flash.now.add(key, *values)

       Appends one or more *values* to *key* in *flash*.
    """

    def __init__(self, data=None):
        """Returns a new flash. If *data* is not provided, an empty flash is
        returned. Otherwise, the given *data* will be used to pre-populate
        this flash.
        """
        self.now = _ImmediateFlashScopeAdapter(self)
        if data:
            self._import_data(data)
        else:
            self._session, self._used = {}, {}

    def __contains__(self, key):
        """Returns ``True`` if there's a value under the given *key*.
        """
        return key in self._session

    def __getitem__(self, key):
        """Retrieves a value. Raises a :exc:`KeyError` if *key* does not exists.
        """
        return self._session[key]

    def __setitem__(self, key, value):
        """Puts a *value* under the given *key*.
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

    def __call__(self, **kwargs):
        """Puts one or more values into this flash.
        """
        for key, value in kwargs.items():
            self[key] = value

    def __len__(self):
        """Returns the number of values inside this flash.
        """
        return len(self._session)

    def _update_status(self, key=None, is_used=True):
        """Updates the status of a given value (or all values if no *key*
        is given). The *is_used* argument tells if that value should be marked
        as *used* (should be discarded) or *unused* (should be kept).

        If a *used* value is being marked as *used* again, it is automatically
        removed from this flash.
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
        """Gets the value under the given *key*. If the *key* is not found,
        *default* is returned instead.
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

    def put(self, **kwargs):
        """Puts one or more values into this flash.
        
        .. deprecated :: 1.7.1
           :meth:`put` is deprecated in favor of ``flash(key=value)``.
        """
        for key, value in kwargs.items():
            self[key] = value

    def add(self, key, *values):
        """Appends one or more *values* to *key* in this flash.
        """
        if key in self:
            current_value = self[key]
            if not isinstance(current_value, list):
                self[key] = [current_value]
                self[key].extend(values)
            else:
                current_value.extend(values)
                self[key] = current_value
        else:
            self[key] = list(values)

    def clear(self):
        """Removes all items from this flash.
        """
        self._session.clear()
        self._used.clear()

    def put_immediate(self, key, value):
        """Puts a value inside this flash and marks it as *used*.

        .. deprecated :: 1.7.1
           :meth:`put_immediate` is deprecated in favor of ``flash.now[key] = value``.
        """
        self[key] = value
        self._update_status(key)

    def discard(self, *keys):
        """Marks the entire current flash or a single value as *used*, so when
        the next request hit the server, those values will be automatically
        removed from this flash by :class:`FlashMiddleware`.
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

    def to_dict(self):
        """Exports this flash to a :class:`dict`.
        """
        return {_SESSION_KEY: self._session.copy(),
                _USED_KEY   : self._used.copy()}

    def _import_data(self, data):
        """Imports the given :class:`dict` to this flash.
        """
        if not isinstance(data, dict):
            raise TypeError('Expected a dictionary')

        if not _SESSION_KEY in data or not _USED_KEY in data:
            raise ValueError("Dictionary doesn't contains the expected data")

        if not isinstance(data[_SESSION_KEY], dict):
            raise ValueError("data['%s'] must be a dict." % _SESSION_KEY)

        if not isinstance(data[_USED_KEY], dict):
            raise ValueError("data['%s'] must be a dict." % _USED_KEY)

        self._session = data[_SESSION_KEY].copy()
        self._used    = data[_USED_KEY].copy()


class _ImmediateFlashScopeAdapter(object):
    """This class is used to add support for immediate flash values to an
    existing instance of :class:`FlashScope`. An immediate flash value is a
    value that is available to this request, but not to the next.
    """

    def __init__(self, delegate):
        """Returns a new flash wrapper which delegates certain calls to the
        given *delegate*.
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
        """Puts a *value* into this flash under the given *key*.
        """
        self.delegate[key] = value
        self.delegate.discard(key)

    def __call__(self, **kwargs):
        """Puts one or more values into this flash.
        """
        for key, value in kwargs.items():
            self[key] = value

    def add(self, key, *values):
        """Appends one or more values to a key in this flash.
        """
        self.delegate.add(key, *values)
        self.delegate.discard(key)
