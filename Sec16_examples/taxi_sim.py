'''
number of  taxicabs are created - each will make a fixed number of trips and then go home
    taxi leaves garage and starts looking for a passenger
    lasts until a passenger is picked up and a trip starts
    when passenger is dropped off, the taxi goes back to searching for a passenger

times are in whole minutes
each change of state in each cab is reported as an event

*take a look at figure 16-3 on page 493 for the output
full example is shown on example A-6 (we'll only show the parts relevant to coroutines in this example)

two important functions:
    1. taxi_process (coroutine)
        coroutines uses two objects defined elsewhere: the "compute_delay()" function returns a time interval in minutes and the Event class, a namedtuple defined like:
            Event = collections.namedtuple('Event', 'time proc action')
                time: when the event will occur
                proc: identifier of the taxi process instance
                action: string describing activity

    2. Simulator.run method (where the main loop of the simulation is execution)
'''

# example - taxi_process coroutine which implements the activities of each taxi
from collections import namedtuple
Event = namedtuple('Event', 'time proc action')

# taxi_process will be called once per taxi, creating a generator object to represent its operations. ident is the number of the taxi (ie. 0, 1, 2 in the sample run); trips is the number of trips this taxi will make before going home; start_time is when the taxi leaves the garage
def taxi_process(ident, trips, start_time=0):
    ''' yield to simulator issuing event at each state change '''
    # the first Event yielded is "leave garage". This suspsends the coroutine and lets the simulation main loop proceed to the next scheduled event. When it's time to reactivate this process, the main loop will send the current simulation time, which is assigned to time
    time = yield Event(start_time, ident, 'leave garage')
    # this block will be repeated once for each trip
    for i in range(trips):
        # An Event signaling passenger pick up is yielded. The coroutine pauses here. When the time comes to reactivate this coroutine, the main loop will again send the current time.
        time = yield Event(time, ident, 'pick up passenger')
        # An Event signaling passenger drop off is yielded. The coroutine is suspended again, waiting for the main loop to send it the time of when it's reactivated
        time = yield Event(time, ident, 'drop off passenger')
    
    # The for loop ends after the given number of trips, a final 'going home' event is yielded. The coroutine will suspend for the last time. When reactivated, it will be sent the time from the simulation main loop, but here I don't assign it to any variable because it will NOT be used
    yield Event(time, ident, 'going home')

# When the coroutine falls off the end, the generator object raises StopIteration
# end of taxi_process


'''
take a look at the examples we did in the Terminal on Section16.py

In the simulation, the taxi coroutines are driven by the main loop in the Simulator.run method:
    The simulation "clock" is held in the sim_time variable and is updated by the time of each event yielded

The Simulator.__init__ method is shown below; the main structures of Simulator are:
    self.events:
        A PriorityQueue to hold Event instances. A PriorityQueue lets you put items, then get them ordered by item[0]; ie. the time attribute in the case of our Event namedtuple objects
    self.procs:
        A dict mapping each process number an active process in the simulation - a generator object representing one taxi. This will be bound to a copy of taxis dict shown above

*Priority queues are fundamental building block of DES: events are created in any order, placed in the queue and later retrieved inorder according to the scheduled time of each one
'''
# example - Simulator class initializer
import queue

class Simulator:
    def __init__(self, procs_map):
        # The PriorityQueue to hold the scheduled events, ordered by increasing time
        self.events = queue.PriorityQueue()
        # We get the procs_map argument as a dict (or any mapping), but build a dict from it, to have a local copy because when the simulation runs, each taxi that goes home is removed from self.procs, and we don't want to change the object passed by the user
        self.procs = dict(procs_map)


# example - to instantiate the Simulator class, the main function of taxi_sim.py builds a taxis dictionary like this:
DEPARTURE_INTERVAL = 5
num_taxis = 3

taxis = {i: taxi_process(i, (i+1) * 2, i * DEPARTURE_INTERVAL) for i in range(num_taxis)}
sim = Simulator(taxis)
