# http_charfinder.py: the main and init functions

@asyncio.coroutine
# the init coroutine yields a server for the event loop to drive
def init(loop, address, port):
    # the aiohttp.web.Application class represents a Web application ...
    app = web.Application(loop=loop)
    # ... with routes mapping URL patterns to handler functions; here GET / is routed to the home function
    app.route.add_route('GET', '/home')
    # the app.make_handler method returns an aiohttp.web.RequestHandler instance to handle HTTP requests according to the routes set up in the app object
    handler = app.make_handler
    # create_server brings up the server, using handler as the protocol handler and binding it to address and port
    server = yield from loop.create_server(handler, address, port)

    # return the address and port of the first server socket
    return server.sockets[0].getsockname()


def main(address="127.0.0.1", port=8888):
    port = int(port)
    loop = asyncio.get_event_loop()
    # run init to start the server and get its address and port
    host = loop.run_until_complete(init(loop, address, port))
    print('Serving on {}. Hit CTRL-C to stop.'.format(host))
    try:
        # run the event loop; main will block here while the event loop is in control
        loop.run_forever()
    # CTRL + C pressed
    except KeyboardInterrupt:
        pass
    # close the event loop
    loop.close()

if __name__ == "__main__":
    main(*sys.argv[1:])


'''
try contrasting how the servers are set up in http_charfinder.py and tcp_charfinder.py

note: in the tcp example, the server was created and scheduled to run in the main function
    server_coro = asyncio.start_server(handle_queries, address, port, loop=loop)
    server = loop.run_until_complete(server_coro)

note: in the http example, the init function creates the server:
    server = yield from loop.create_server(handler, address, port)
    *init itself is a coroutine and is ran by the main() function
        host = loop.run_until_complete(init(loop, address, port))

BOTH asyncio.start_server and loop.create_server are coroutines that return asyncio.Server objects that are driven to completion in order to start up a server

*a coroutine only does anything when driven, and to drive an asyncio.coroutine you EITHER use "yield from" or pass it to one of several asyncio functions that take coroutine/future arguments, such as run_until_complete

take a look at the home function below
'''

# http_charfinder.py (continued): home function (configured to handle the / root URL in our HTTP server)

# a route handler receives an aiohttp.web.Request instance
def home(request):
    # get the query string stripped of leading and trailing blanks
    query = request.GET.get('query', '').strip()
    # log query to server console 
    print('Query: {!r}'.format(query))
    # if there was a query, bind res to HTML table rows rendered from result of the query to the index, and msg to a status message
    if query:
        descriptions = list(index.find_descriptions(query))
        res = '\n'.join(ROW_TPL.format(**vars(descr)) for descr in descriptions)
        msg = index.status(query, len(descriptions))
    else:
        descriptions = []
        res = ''
        msg = 'Enter words describing characters.'

    # render the html page
    html = template.format(query=query, result=res, message=msg)

    # log response to server console
    print('Sending {} results'.format(len(descriptions)))
    # build Response and return it
    return web.Response(content_type=CONTENT_TYPE, text=html)


'''
note: home() is NOT a coroutine and does NOT need to be if there are NO  "yield from" expressions in it
'''