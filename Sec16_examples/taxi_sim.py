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
    # the first Event yielded is "leave garage". This suspends the coroutine and lets the simulation main loop proceed to the next scheduled event. When it's time to reactivate this process, the main loop will SEND the current simulation time, which is assigned to time
    time = yield Event(start_time, ident, 'leave garage')
    # this block will be repeated ONCE for each trip
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
    The simulation "clock" is held in the "sim_time" variable and is updated by the time of each event yielded


Part 2: 

The Simulator.__init__ method is shown below; the main structures of Simulator are:
    self.events:
        A PriorityQueue to hold Event instances. A PriorityQueue lets you put items, then get them ordered by item[0]; ie. the time attribute in the case of our Event namedtuple objects
    self.procs:
        A dict mapping each process number an active process in the simulation - a generator object representing one taxi. This will be bound to a copy of taxis dict shown above

*Priority queues are fundamental building block of DES: events are created in any order, placed in the queue and later retrieved in order according to the scheduled time of each one
'''
# example Part 2 - Simulator class initializer (__init__)
import queue

class Simulator:
    def __init__(self, procs_map):
        # The PriorityQueue to hold the scheduled events, ordered by increasing time
        self.events = queue.PriorityQueue()
        # We get the procs_map argument as a dict (or any mapping), but build a dict from it, to have a local copy because when the simulation runs, each taxi that goes home is removed from self.procs, and we don't want to change the object passed by the user
        # a procs_map would be something like we did in the "taxis" variable
        self.procs = dict(procs_map)

    # example continued (Part 3) - Simulator, a bare bone discrete event simulation class. Focusing on the run method
    # the simulation end_time is the ONLY required argument for run
    def run(self, end_time):
        ''' Schedule and display events until time is up '''
        # Use sorted to retrieve the self.procs items ordered by the key; we don't care about the key, so assign it to _.
        for _, proc in sorted(self.procs.items()):
            # next(proc) primes each coroutine by advancing it to the first yield, so it's ready to be sent data. An Event is yielded
            first_event = next(proc)
            # Add each event to the self.events PriorityQueue. The first event for each taxi is 'leave garage', as seen in the sample run
            # .put() puts an item in queue
            self.events.put(first_event)

        # main loop of the simulation
        # Zero sim_time, the simulation clock
        sim_time = 0
        # Main loop of the simulation: run while sim_time is less than the end_time
        while sim_time < end_time:
            # The main loop may also exit if there are no pending events in the queue
            # .empty() checks if the queue is empty
            if self.events.empty():
                print('*** end of events ***')
                break
            
            # Get Event with the smallest time in the priority queue; this is the current event
            current_event = self.events.get()
            # Unpack the Event data. This line updates the simulation clock, sim_time, to reflect the time when the event happened
            sim_time, proc_id, previous_action = current_event
            # Display the Event, identifying the taxi and adding indentation according to the taxi id
            print('taxi: ', proc_id, proc_id * ' ', current_event)
            # Retrieve the coroutine for the active taxi from the self.procs dictionary
            active_proc = self.procs[proc_id]
            # Compute the next activation time by adding the sim_time and the result of calling compute_duration(...) with the previous action, ie. 'pick up passenger', 'drop off passenger' etc.
            next_time = sim_time + compute_duration(previous_action)
            try:
                # Send the time to the taxi coroutine. The coroutine will yield the next_event or raise StopIteration if it's finished
                next_event = active_proc.send(next_time)
            except StopIteration:
                # If StopIteration is raised, delete the coroutine from the self.procs dictionary
                del self.procs[proc_id]
            else:
                # Otherwise, put the next_event in queue
                self.events.put(next_event)
        # If the loop exits because the simulation time passed, display the number of events pending (which may be zero by coincidence, sometimes)
        else:
            msg = '*** end of simulation time: {} events pending ***'
            print(msg.format(self.events.qsize))
        

# example Part 1 - to instantiate the Simulator class, the main function of taxi_sim.py builds a taxis dictionary like this:
DEPARTURE_INTERVAL = 5
num_taxis = 3

taxis = {i: taxi_process(i, (i+1) * 2, i * DEPARTURE_INTERVAL) for i in range(num_taxis)}
sim = Simulator(taxis)
# taxis = {0: taxi_process(ident=0, trips=2, start_time=0),
             # 1: taxi_process(ident=1, trips=4, start_time=5),
             # 2: taxi_process(ident=2, trips=6, start_time=10)}

'''
Part 1: 

values of the taxis dictionary will be three distinct generator objects with different parameters
    ie. taxi 1 will make 4 trips and begin looking for passengers at start_time=5. 
'''

# example - first two events placed in the queue may be:
# Event(time=14, proc=0, action='pick up passenger')
# Event(time=11, proc=1, action='pick up passenger')

'''
Part 3: 

the example above says that taxi 0 will take 14 minutes to pick up the first passenger, while taxi 1 - starting at time=10 - will take 1 minute and pick up the passenger at time=11.
if these are in a queue; the first event the main loop gets from the priority queue is "Event(time=11, proc=1, action='pick up passenger')


Main algorithm of the simulation, the Simulator.run method
    Invoked by the main function right after the Simulator is instantiated like so:
'''
# sim = Simulator(taxis)
# sim.run(end_time)


'''
***Note that the Simulator.run method uses else blocks TWO places that are NOT if statements:
    1. the main while loop has an else statement to report that the simulation ended because the end_time was reached - and not because there were no more events to process

    2. the try statement at the bottom of the while loop tries to get a next_event by sending the next_time to the current taxi process, and if that is successful the else block puts the next_event into the self.events queue
'''