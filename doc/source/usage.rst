Using Django-Flash
------------------

Once plugged to your project, Django-Flash automatically adds a ``flash``
attribute to the :class:`django.http.HttpRequest` objects received by your
views. This property points to a :class:`djangoflash.models.FlashScope`
instance, which supports most if not all operations provided by a simple Python
``dict``.

Here goes some examples on how to manipulate this scope from a view::

    def my_view(request):
        # Puts a string to the flash scope
        request.flash['key'] = 'value'
        
        # Alternative syntax that does the same as above
        request.flash.put(key='value')
        
        # Checks if the object is available at the flash scope
        'key' in request.flash
        
        # Gets an object from the flash scope
        request.flash['key']
        
        # Removes an object from the flash scope
        del request.flash['key']


To see the list of all methods available to you, take a look at the
:class:`djangoflash.models.FlashScope` documentation.

Although this example uses only *string* values, you are free to use, both as
keys and values, any object that can be *pickled*. See the
`pickle module <http://docs.python.org/library/pickle.html>`_ for more details
on this subject.


.. _flash-manipulation:

Manipulating the flash  contents
````````````````````````````````

You can use the *flash* the same way you use a plain ``dict`` since their
interface are very similar::

    def my_view(request):
        # Store a value
        request.flash['key'] = 'value'

        # Replace a value
        request.flash['key'] = 'another value'

        # Remove a value
        del request.flash['key']

        # And so on...
        for key, value in request.flash.items():
            print '%s - %s' % (key, value)


The *flash* also allows you to easily store several values under the same key.
To do this just use the :meth:`djangoflash.models.FlashScope.add` method::

    def my_view(request):
        # add() handles multiple values under the same key automatically
        request.flash.add('key', 'value')
        request.flash.add('key', 'another value')
        print request.flash['key'] # Output: ['value', 'another value']


.. _flash-default-lifecycle:

Flash-scoped objects: the default lifecycle
```````````````````````````````````````````

First let's see a basic example of how Django-Flash controls the
lifecycle of flash-scoped objects. Consider the following views::

    # URL: http://server/app/first
    def first_view(request):
        request.flash['message'] = 'My message'
        return HttpResponseRedirect(reverse(second_view))
    
    # URL: http://server/app/second
    def second_view(request):
        print request.flash['message'] # Output: My message
        request.flash['another_message'] = 'Something'
        return HttpResponseRedirect(reverse(third_view))
    
    # URL: http://server/app/third
    def third_view(request):
        print request.flash['another_message'] # Output: Something
        print 'message' in request.flash # Output: False
        return HttpResponseRedirect(reverse(fourth_view))
    
    # URL: http://server/app/fourth
    def fourth_view(request):
        return HttpResponse(...)


Let's say that we have opened our web browser and issued a request to
http://server/app/first\. When :meth:`first_view` executes, it stores an object
inside the *flash* under the key ``message``. The last line returns a HTTP
Redirect, which makes our web browser fire a ``GET`` request to
http://server/app/second\.

When :meth:`second_view` executes, it prints the content of the flash-scoped
object under the key ``message``, which was stored in the previous request by
:meth:`first_view`. The next line of code stores another object inside the
*flash* under the key ``another_message``. Again, the last line returns a HTTP
Redirect, which makes our web browser fire a ``GET`` request to
http://server/app/third\.

When :meth:`third_view` executes, the flash-scoped object under the key
``another_message``, which was stored in the previous request by
:meth:`second_view`, is available for use. But, at the same time, the
flash-scoped object added by :meth:`first_view` was automatically removed.


.. seealso::
   :ref:`modulesindex`


Lifecycle management
````````````````````

By default, all objects stored inside the *flash* survives until the *very next*
request, being automatically removed after that. Unfortunately, this default
behavior might not be enough in some situations.


Preventing flash-scoped objects from being removed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We can prevent flash-scoped objects from being removed by using the
:meth:`djangoflash.models.FlashScope.keep` method::

    def first_view(request):
        request.flash['message'] = 'Operation succeeded!'
        return HttpRedirectResponse(reverse(second_view))
        
    def second_view(request):
        print request.flash['message'] # Output: Operation succeeded!
        request.flash.keep('message')
        return HttpRedirectResponse(reverse(third_view))
    
    def third_view(request):
        print request.flash['message'] # Output: Operation succeeded!
        return HttpRedirectResponse(reverse(fourth_view))
    
    def fourth_view(request):
        print 'message' in request.flash # Output: False
        return HttpResponse(...)


If you want to keep *all* flash-scoped objects, just call the
:meth:`djangoflash.models.FlashScope.keep` method with no arguments::

    def second_view(request):
        request.flash.keep()
        return HttpRedirectResponse(reverse(third_view))


A more declarative way to keep values is also supported through the
:meth:`djangoflash.decorators.keep_messages` decorator::

    from djangoflash.decorators import keep_messages

    # Keeps the entire flash...
    @keep_messages
    def second_view(request):
        return HttpRedirectResponse(reverse(third_view))

    # ...or specific messages
    @keep_messages('message', 'another_message')
    def second_view(request):
        return HttpRedirectResponse(reverse(third_view))


Adding an immediate flash-scoped object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It's sometimes convenient to store an object inside the *flash* and use it on
the *current* request only.

This can be done by using the :attr:`djangoflash.models.FlashScope.now`
attribute::

    def first_view(request):
        request.flash.now['message'] = 'My message'
        request.flash.now(message='My message') # Alternative syntax
        print request.flash['message'] # Output: My message
        return HttpRedirectResponse(reverse(second_view))
    
    def second_view(request):
        print 'message' in request.flash # Output: False


Accessing flash-scoped objects from view templates
``````````````````````````````````````````````````

We already know how to access the *flash* from views. But what about the view
templates?

It's just as easy:

.. code-block:: html+django

   <html>
   <head>
       <title>My template</title>
   </head>
   <body>
       {% if flash.message %}
           <!-- There's a flash-scoped object under the 'message' key -->
           
           <div class="flash_message">
               <p>{{ flash.message }}</p>
           </div>
       {% endif %}
   </body>
   </html>


It's also possible to iterate over all flash-scoped objects using the
``{% for %}`` tag if you want to:

.. code-block:: html+django

   <html>
   <head>
       <title>My template</title>
   </head>
   <body>
       {% if flash %}
           <!-- There's one or more flash-scoped objects -->
           
           {% for value in flash.values %}
               <div class="flash_entry">
                   <p>{{ value }}</p>
               </div>
           {% endfor %}
       {% endif %}
   </body>
   </html>


.. seealso::
   :mod:`djangoflash.context_processors` module.

