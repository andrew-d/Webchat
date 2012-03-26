
# Webchat

This is a small little project that I wrote for a job interview.  It implements a simple websocket-based chat system.  It's built with [Tornado][1], [TornadIO2][2] and [Socket.IO][3] on the front-end.

I don't plan on updating this any more, but it's a good demo of what can be done in two hours or so with Python and Socket.IO.  If you want to try it out:

- Start the server: `python -m webchat.main`
- Navigate to the client: `http://localhost:8000/chat/index.html`
- Enter your username and login in the box at the top.  Currently, the system has a set of hard-coded username + password combinations.  If you successfully log in with one of those, you get an asterisk after your name.  The system strips asterisks from all other usernames.
- Type a message in the "Message:" box, and click "Submit".  Leaving the second box blank will send to all users, otherwise it will send only to the specific user.
- New messages will show up in the channel as other users type things.  You can open two browser windows to test things out.

There are probably lots of bugs.  Here's one that I noticed when testing: when you try to log in as an authenticated user, and fail, the system won't properly remove your connection, so you get all subsequent messages twice (and 3x if you fail twice, etc.)

# License

This project is licensed under the [MIT License][4]:

    Copyright (C) 2012 Andrew D

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

[1]: http://www.tornadoweb.org/
[2]: http://readthedocs.org/docs/tornadio2/en/latest/
[3]: http://socket.io/
[4]: http://en.wikipedia.org/wiki/MIT_License
