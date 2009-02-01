# -*- coding: utf-8 -*-

"""In order to manage the flash context, a dictionary-like object is
provided by this module.

The following Python code shows its main features:

    # It's pretty much a dictionary...
    flash = FlashScope()
    
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
    flash.increment_age()
    print 'key' in flash   # -> False (expired object)
"""


class FlashScope(object):
    """This is a dict-like object used to manage the flash context.
    """
    
    def __init__(self):
        "Creates a new instance of FlashScope."
        self._current = {}
        self._current_age = {}  # Stores the "age" of each flash-scoped object
        self._active = {}      # Stores just the active flash-scoped objects
    
    def __contains__(self, key):
        """Returns True if there's an active flash-scoped object under
        the given key.
        """
        return key in self._active
    
    def __getitem__(self, key):
        """Retrieves an active flash-scoped object.
        """
        return self._active[key]
    
    def __setitem__(self, key, value):
        "Puts an object into the flash context."
        self._current[key] = value
        self._current_age[key] = 0
    
    def __delitem__(self, key):
        "Removes a flash-scoped object."
        del self._current[key]
        del self._current_age[key]
        if self._active.has_key(key):
            del self._active[key]
    
    def __len__(self):
        "Returns the number of active flash-scoped objects."
        return len(self._active)
    
    def is_active_empty(self):
        "Returns true if there's at least one active flash-scoped object."
        return len(self) == 0
    
    def is_current_empty(self):
        """Returns true if there's at least one flash-scoped object to be
        activated on one of the following requests.
        """
        return len(self._current) == 0
    
    def keys(self):
        "Returns the keys of all active flash-scoped objects."
        return self._active.keys()
    
    def items(self):
        """Returns the list of all active flash-scoped objects as
        tuples (key, value).
        """
        return self._active.items()
    
    def get(self, key, default=None):
        """Gets the active flash-scoped object under the given key. If the
        key doesn't exists, the default value is returned instead.
        """
        return self._active.get(key, default)
    
    def pop(self, key, *args):
        """Removes and returns the active flash-scoped object under the
        given key.
        """
        value = self._active.pop(key, *args)
        del self._current_age[key]
        if self._active.has_key(key):
            del self._active[key]
        return value
    
    def has_key(self, key):
        """Returns True if there's an active flash-scoped object under the
        given key.
        """
        return self._active.has_key(key)
    
    def values(self):
        "Returns the list of all active flash-scoped objects."
        return self._active.values()
    
    def iterkeys(self):
        """Returns an iterator over the keys of all active flash-scoped
        objects.
        """
        return self._active.iterkeys()
    
    def itervalues(self):
        """Returns an iterator over the values of all active flash-scoped
        objects.
        """
        return self._active.itervalues()
    
    def iteritems(self):
        """Returns an iterator over the items (key, value) of all active
        flash-scoped objects.
        """
        return self._active.iteritems()
    
    def put(self, **kwargs):
        """Puts an object into the flash context. This method is an alias to
        __setitem__(self, key, value).
        """
        for key, value in kwargs.items():
            self[key] = value
    
    def now(self, **kwargs):
        """Puts an object into the active flash context. Use this method
        when you need to make a flash-scoped object available to the same
        request; otherwise you would have to wait for the next request
        for this object to be available for use.
        """
        for key, value in kwargs.items():
            self._active[key] = value
    
    def keep(self, *args):
        """Stops the given flash-scoped object from being expired, at least
        for one more request. If this method is called with no arguments,
        it acts on all flash-scoped objects.
        """
        for key, value in self._current_age.items():
            if not args or key in args:
                if value > 0:
                    self._current_age[key] -= 1
    
    def _update_active(self):
        "Recreates the active flash scope."
        self._active = {}
        for key in self._current_age.keys():
            if not self._current_age[key] == 0:
                self._active[key] = self._current[key]
    
    def increment_age(self):
        """Increment the age of flash-scoped objects by 1. After that, all
        objects with age >= 2 are removed from the flash scope.
        """
        for key, value in self._current_age.items():
            if value+1 < 2:
                self._current_age[key] += 1
            else:
                del self[key]
        self._update_active()
