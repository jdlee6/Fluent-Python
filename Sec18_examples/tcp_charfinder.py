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
def handle_queries(reader, writer):
    # This loop handles a session which lasts until any control character is received from the client
    while True:
        # can NOT yield from
        # The StreamWriter.write method is not a coroutine, just a plain function; this line sends the ?> prompt
        writer.write(PROMPT)
        # MUST yield from
        # SteamWriter.drain flushes the writer buffer; it is a coroutine, so it must be called with yield from
        yield from writer.drain()
        # StreamWriter.readline is a coroutine; it returns bytes
        data = yield from reader.readline()
        try:
            query = data.decode().strip()
        # A UnicodeDecodeError may happen when the Telnet client sends control characters; if that happens, we pretend a null character was sent, for simplicity
        except UnicodeDecodeError:
            query = '\x00'
        # This returns the remote address to which the socket is connected
        client = writer.get_extra_info('peername')
        # Log the query to the server console
        print('Received from {}: {!r}'.format(client, query))
        if query:
            # Exit the loop if a control or null character was received
            if ord(query[:1]) < 32:
                break
            # This returns a generator that yields strings with the Unicode codepoint, the actual character and its name, i.e. U+0039\t9\tDIGIT NINE; for simplicity I build a list from it
            lines = list(index.find_description_strs(query))
            if lines:
                # Send the lines converted to bytes using the default UTF-8 encoding, appending a carriage return and a line feed to each; note that the argument is a generator expression
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