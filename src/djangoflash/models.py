# -*- coding: utf-8 -*-

"""In order to manage the flash context, a dictionary-like object is
provided by this module.

The following Python code shows its main features:

    flash = FlashScope()
    
    #
    # It's pretty much a dictionary...
    #
    
    # Add a string to the flash context
    flash['key'] = 'value'
    flash.put(another_key='another value')
    
    # Check if a value is available at the flash context
    print 'key' in flash
    
    # Get an object from the flash context
    print flash['key']
    print flash.get('key', 'default value')
    
    # Remove an object from the flash scope
    del flash['key']
    
    
    #
    # ...but it's not only a dictionary!
    #
    
    # Keep an object in the flash context for one more request
    flash.keep('key')
    
    # Keep all objects in the flash context for one more request
    flash.keep()
    
    # Add an object to the flash context, but make it available for use
    # at THIS request
    flash.now(key='value')

Before every request, the method increment_age() should be called in order
to update the FlashScope's internal state (e.g. remove expired objects from
the context or update the list of objects available to the ongoing request):

    flash = FlashScope()
    
    # First request
    flash['key'] = 'value'
    print 'key' in flash   # -> False (object is not yet active)
    
    # Second request
    flash.increment_age()
    print 'key' in flash   # -> True (object is now active)
    
    # Third request
    print 'key' in flash   # -> False (expired object)
"""


class FlashScope(object):
    """This is a dictionary-like object used to manage the flash context.
    """
    
    def __init__(self):
        "Creates a new instance of FlashScope."
        self._session = {}
        self._session_age = {}  # Stores the "age" of each flash scoped object
        self._current = {}      # Stores just the active flash scoped objects
    
    def __contains__(self, key):
        """Returns True if there's an active (not expired) flash scoped object
        under the given key.
        """
        return key in self._current
    
    def __getitem__(self, key):
        """Retrieves an active (not expired) flash scoped object.
        """
        return self._current[key]
    
    def __setitem__(self, key, value):
        "Puts an object into the flash context."
        self._session[key] = value
        self._session_age[key] = 0
    
    def __delitem__(self, key):
        "Removes a flash scoped object."
        del self._session[key]
        del self._session_age[key]
        if self._current.has_key(key):
            del self._current[key]
    
    def is_active_empty(self):
        """Returns true if there's at least one active (not expired)
        flash scoped object. 
        """
        return len(self._current) == 0
    
    def is_current_empty(self):
        """Returns true if there's at least one flash scoped object to be
        activated on one of the following requests.
        """
        return len(self._session) == 0
    
    def keys(self):
        "Returns the keys of all active (not expired) flash scoped objects."
        return self._current.keys()
    
    def items(self):
        """Returns the list of all active (not expired) flash scoped objects
        as tuples (key, value).
        """
        return self._current.items()
    
    def get(self, key, default=None):
        """Gets the active (not expired) flash scoped object under the given
        key. If the key doesn't exists, the default value is returned instead.
        """
        return self._current.get(key, default)
    
    def pop(self, key, *args):
        """Removes and returns the active (not expired) flash scoped object
        under the given key.
        """
        value = self._current.pop(key, *args)
        del self._session_age[key]
        if self._current.has_key(key):
            del self._current[key]
        return value
    
    def has_key(self, key):
        """Returns True if there's an active (not expired) flash scoped object
        under the given key.
        """
        return self._current.has_key(key)
    
    def values(self):
        "Returns the list of all active (not expired) flash scoped objects."
        return self._current.values()
    
    def iterkeys(self):
        """Returns an iterator over the keys of all active (not expired)
        flash scoped objects.
        """
        return self._current.iterkeys()
    
    def itervalues(self):
        """Returns an iterator over the values of all active (not expired)
        flash scoped objects.
        """
        return self._current.itervalues()
    
    def iteritems(self):
        """Returns an iterator over the items (key, value) of all active
        (not expired) flash scoped objects.
        """
        return self._current.iteritems()
    
    def put(self, **kwargs):
        """Puts an object into the flash context. This method is an alias to
        __setitem__(self, key, value).
        """
        for key,value in kwargs.items():
            self[key] = value
    
    def now(self, **kwargs):
        """Puts an object into the active flash context. Use this method
        when you need to make a flash scoped object available to the same
        request; otherwise you would have to wait for the next request
        for this object to be available for use.
        """
        for key,value in kwargs.items():
            self._current[key] = value
    
    def keep(self, *args):
        """Stops the given flash scoped object from being expired, at least
        for one more request. If this method is called with no arguments,
        it acts on all flash scoped objects.
        """
        for key, value in self._session_age.items():
            if not args or key in args:
                if value > 0:
                    self._session_age[key] -= 1
    
    def _update_current(self):
        "Recreates the active flash scope."
        self._current = {}
        for key, value in self._session_age.items():
            if not self._session_age[key] == 0:
                self._current[key] = self._session[key]
    
    def increment_age(self):
        """Increment the age of flash scoped objects by 1. After that, all
        objects with age >= 2 are removed from the flash scope.
        """
        for key, value in self._session_age.items():
            if value+1 < 2:
                self._session_age[key] += 1
            else:
                del self[key]
        self._update_current()
