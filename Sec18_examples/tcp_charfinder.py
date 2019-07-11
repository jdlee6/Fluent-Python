# tcp_charfinder.py (part 1) - A simple TCP server using asyncio.start_server 

''' part 1 '''

import sys
import asyncio
# UnicodeNameIndex is the class that builds the index of names and provides querying methods
from charfinder import UnicodeNameIndex

CRLF = b'\r\n'
PROMPT = b'?> '

# When instantiated, UnicodeNameIndex uses charfinder_index.pickle, if available, or builds it, so the first run may take a few seconds longer to start
index = UnicodeNameIndex()

@asyncio.coroutine
# This is the coroutine we need to pass to asyncio_startserver; the arguments received are an asyncio.StreamReader and an asyncio.StreamWriter
# asyncio.StreamReader: represents a reader object that provides API to read data from the IO stream
# asyncio.StreamWriter: represents a writer object that provides APIs to write data to the IO stream
def handle_queries(reader, writer):
    # This loop handles a session which lasts until any control character is received from the client
    while True:
        # The StreamWriter.write method is not a coroutine, just a plain function; this line sends the ?> prompt (writes the data to the stream)
        # can NOT yield from
        writer.write(PROMPT)
        # SteamWriter.drain flushes the writer buffer; it is a coroutine, so it must be called with yield from
        # MUST yield from
        yield from writer.drain()
        # StreamReader.readline is a coroutine; it returns bytes
        data = yield from reader.readline()
        try:
            query = data.decode().strip()
        # A UnicodeDecodeError may happen when the Telnet client sends control characters; if that happens, we pretend a null character was sent, for simplicity
        except UnicodeDecodeError:
            query = '\x00'
        # This returns the remote address to which the socket is connected
        # get_extra_info(): access optional transport information
        client = writer.get_extra_info('peername')
        # Log the query to the server console
        print('Received from {}: {!r}'.format(client, query))
        if query:
            # Exit the loop if a control or null character was received
            # chr(32), chr(31) . . . and below return no output (no characters are assigned therefore it will be null if the number is below 32)
            # note: chr() is the opposite of ord()
            if ord(query[:1]) < 32:
                break
            # This returns a generator that yields strings with the Unicode codepoint, the actual character and its name, i.e. U+0039\t9\tDIGIT NINE; for simplicity I build a list from it
            lines = list(index.find_description_strs(query))
            if lines:
                # Send the lines converted to bytes using the default UTF-8 encoding, appending a carriage return and a line feed to each; note that the argument is a generator expression
                # .writelines() writes a list (or any iterable) of bytes to the stream
                writer.writelines(line.encode() + CRLF for line in lines)
            # Write a status line such as 627 matches for 'digit'
            writer.write(index.status(query, len(lines)).encode() + CRLF)

            # Flush the output buffer
            yield from writer.drain()
            # Log the response to the server console 
            print('Sent {} results'.format(len(lines)))

    # Log the end of the session to the server console
    print('Close the client socket')
    # Close the StreamWriter
    writer.close()


'''
all I/O in the example above is in bytes (default encoding UTF-8):
    1. decode the strings received from the network
    2. encode the strings sent out

some of the I/O are coroutines and must be driven with "yield from" while others are simple functions
*asyncio docs label which methods/functions are coroutines and which are not

take a look at def main(): in tcp_charfinder.py below
'''


# tcp_charfinder.py (continued): main function sets up and tears down the event loop and the socket server

# the main function can be called with NO arguments because default arguments are set already
def main(address='127.0.0.1', port=2323):
    port = int(port)
    # asyncio creates a new event loop and sets it as the current one
    loop = asyncio.get_event_loop()
    # when completed, the coroutine object returned by asyncio.start_server returns an instance of asyncio.Server, a TCP socket server
    server_coro = asyncio.start_server(handle_queries, address, port, loop=loop)
    # Drive server_coro to bring up the server
    server = loop.run_until_complete(server_coro)

    # Get address and port of the first socket of the server and ...
    # .getsockname() returns (ip, port)
    host = server.sockets[0].getsockname()
    # ... display it on the server console. This is the first output generated by this script on the server console
    print('Serving on {}. Hit CTRL-C to stop.'.format(host))
    try:
        # run the event loop; this is where main will block until killed when ctrl-c is pressed on the server console
        loop.run_forever()
    # ctrl + c pressed
    except KeyboardInterrupt: 
        pass

    print('Server shutting down.')
    # close the server 
    server.close()
    # server.wait_closed() returns a future; use loop.run_until_complete to let the future do its job
    loop.run_until_complete(server.wait_closed())
    # terminate the event loop
    loop.close()

if __name__ == "__main__":
    main(*sys.argv[1:])


'''
note: run_until_complete() accepts either a coroutine (result of start_server) or a future (result of server.wait_closed) 
    if coroutine --> wraps coroutine in a Task

take a look at the output of tcp_charfinder.py below to get a sense of control flow
'''


# tcp_charfinder.py (continued): server side of the session depicted in figure 18-2

# $ python3 tcp_charfinder.py
# This is the output of main()
# Serving on ('127.0.0.1', 2323). Hit CTRL-C to stop.

# First iteration of the while loop in handle_queries
# Received from ('127.0.0.1', 62910): 'chess black'
# Sent 6 results

# Second iteration of the while loop
# Received from ('127.0.0.1', 62910): 'sun'
# Sent 10 results

# The user hit CTRL-C; the server receives a control character and closes the session
# Received from ('127.0.0.1', 62910): '\x00'

# The client socket is closed but the server is still running, ready to service another client
# Close the client socket


'''
note: main() almost immediately displays the Serving on . . . message and blocks in the loop.run_forever() call
    control flows into the event loop and STAYS there, occasionally coming back to handle_queries coroutine, which yields control BACK to the event loop whenever it needs to wait for the network as it sends or receives data

asyncio.Stream . . . : provides a ready to use server so you only need to implement a handler function (plain callback or a coroutine)
'''