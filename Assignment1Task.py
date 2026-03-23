import threading
import time
import random

from printDoc import printDoc
from printList import printList

class Assignment1:
    # Simulation Initialisation parameters
    NUM_MACHINES = 50        # Number of machines that issue print requests
    NUM_PRINTERS = 5         # Number of printers in the system
    SIMULATION_TIME = 30     # Total simulation time in seconds总模拟时间
    MAX_PRINTER_SLEEP = 3    # Maximum sleep time for printers打印机的最大休眠时间
    MAX_MACHINE_SLEEP = 5    # Maximum sleep time for machines机器的最大休眠时间
    QUEUE_CAPACITY = 5

    # Initialise simulation variables
    def __init__(self):
        self.sim_active = True
        self.print_list = printList()  # Create an empty list of print requests创建一个空的打印请求队列
        self.mThreads = []             # list for machine threads机器线程列表
        self.pThreads = []             # list for printer threads打印机线程列表
        self.semaphore = threading.Semaphore(self.QUEUE_SIZE)  
        self.binary = threading.Semaphore(1)   

    def startSimulation(self):
        # Create Machine and Printer threads
        # Write code here
        for i in range(self.NUM_MACHINES):
            machine = self.machineThread(i, self)
            self.mThreads.append(machine)

        for i in range(self.NUM_PRINTERS):
            printer = self.printerThread(i, self)
            self.pThreads.append(printer)
    
  

            
        # Start all the threads
        # Write code here
        for p in self.pThreads:
            p.start()
        for m in self.mThreads:
            m.start()
        # Let the simulation run for some time
        time.sleep(self.SIMULATION_TIME)
  
        # Finish simulation
        self.sim_active = False

        # Wait until all printer threads finish by joining them
        # Write code here
        for _ in range(self.NUM_MACHINES):
            self.empty_slots.release()
        for _ in range(self.NUM_PRINTERS):
            self.full_slots.release()

        for t in self.pThreads:
            t.join()
        for t in self.mThreads:
            t.join()

    # Printer class
    class printerThread(threading.Thread):
        def __init__(self, printerID, outer):
            threading.Thread.__init__(self)
            self.printerID = printerID
            self.outer = outer  # Reference to the Assignment1 instance

        def run(self):
            while self.outer.sim_active:
                # Simulate printer taking some time to print the document
                
                # Grab the request at the head of the queue and print it
                # Write code here
                self.outer.full_slots.acquire()  # Wait until there is at least one print request in the queue
                if not self.outer.sim_active:
                    break

                with self.outer.queue_lock:  # Lock the queue to safely access it
                    self.printDox(self.printerID) 
                     # Print the document at the head of the queue
                self.outer.empty_slots.release()  # Signal that there is now one more empty slot in the queue
                self.printerSleep()  # Simulate the printer taking some time to print the document

        def printerSleep(self):
            sleepSeconds = random.randint(1, self.outer.MAX_PRINTER_SLEEP)
            time.sleep(sleepSeconds)

        def printDox(self, printerID):
            print(f"Printer ID: {printerID} : now available")
            # Print from the queue
            self.outer.print_list.queuePrint(printerID)

    # Machine class
    class machineThread(threading.Thread):
        def __init__(self, machineID, outer):
            threading.Thread.__init__(self)
            self.machineID = machineID
            self.outer = outer  # Reference to the Assignment1 instance

        def run(self):
            while self.outer.sim_active:
                # Machine sleeps for a random amount of time
                self.machineSleep()
                # Machine wakes up and sends a print request
                # Write code here
                if not self.outer.sim_active:
                    break
                self.outer.empty_slots.acquire()  # Wait until there is at least one empty slot in the queue
                if not self.outer.sim_active:
                    self.outer.empty_slots.release()  # Release the slot if the simulation is no longer active
                    break

                with self.outer.queue_lock:  # Lock the queue to safely access it
                    self.printRequest(self.machineID)  # Send a print request

                self.outer.full_slots.release()  # Signal that there is now one more full slot in the queue

        def machineSleep(self):
            sleepSeconds = random.randint(1, self.outer.MAX_MACHINE_SLEEP)
            time.sleep(sleepSeconds)

        def printRequest(self, id):
            print(f"Machine {id} Sent a print request")
            # Build a print document
            doc = printDoc(f"My name is machine {id}", id)
            # Insert it in the print queue
            self.outer.print_list.queueInsert(doc)