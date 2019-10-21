==========
Log Server
==========

Small example of how to implement a "``tail -f``" file server in Python using
asyncio_. Streaming of the file contents to the client is done using
WebSockets_.

In order to monitor file changes Linux's inotify_ (using aionotify_) is used in
conjunction with aiofile_ to read files asynchronously (using POSIX's `aio.h`_).

Thus, this example can only run in Linux using modern kernels.


.. _asyncio: https://docs.python.org/3/library/asyncio.html
.. _WebSockets: https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API
.. _inotify: https://en.wikipedia.org/wiki/Inotify
.. _aionotify: https://github.com/rbarrois/aionotify
.. _aiofile: https://github.com/mosquito/aiofile
.. _aio.h: http://man7.org/linux/man-pages/man7/aio.7.html


Usage
=====

Server
------

Start the server with::

    $ cd server
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip3 install -r requirements.txt
    $ ./server.py

This will start a server that listen on port ``9292``. There is one endpoint::

    /follow/{filename}

The server will look for ``filename`` in the current working directory and
start streaming its content.

There is a small tool `noiser.py` that will make sure to make noise on a file.
So, in another terminal, you may start making noise in a file with::

    $ ./noiser.py afile.log

Thus ``/follow/afile.log`` will allow to follow the writes in that file.


Clients
-------

There is an assorted collection of clients:

- HTML5 / Javascript.
- React.
- Python 3 synchronous.
- Python 3 asynchronous.

Feel free to explore the code in the `clients/` directory.


License
=======

::

   Copyright (C) 2019 KuraLabs S.R.L

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing,
   software distributed under the License is distributed on an
   "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
   KIND, either express or implied.  See the License for the
   specific language governing permissions and limitations
   under the License.
