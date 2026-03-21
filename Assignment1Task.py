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

    # Initialise simulation variables
    def __init__(self):
        self.sim_active = True
        self.print_list = printList()  # Create an empty list of print requests创建一个空的打印请求队列
        self.mThreads = []             # list for machine threads机器线程列表
        self.pThreads = []             # list for printer threads打印机线程列表

    def startSimulation(self):
        # Create Machine and Printer threads
        # Write code here
        P1 = self.printerThread(1, self)
        P2 = self.printerThread(2, self)
        P3 = self.printerThread(3, self)
        M1 = self.machineThread(11, self)
        M2 = self.machineThread(22, self)    
        M3 = self.machineThread(33, self)
        M4 = self.machineThread(44, self)
    
        self.pThreads.append(P1)
        self.pThreads.append(P2)
        self.pThreads.append(P3)
        self.mThreads.append(M1)
        self.mThreads.append(M2)        
        self.mThreads.append(M3)
        self.mThreads.append(M4)

            
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
                self.printerSleep()
                # Grab the request at the head of the queue and print it
                # Write code here
                self

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

        def machineSleep(self):
            sleepSeconds = random.randint(1, self.outer.MAX_MACHINE_SLEEP)
            time.sleep(sleepSeconds)

        def printRequest(self, id):
            print(f"Machine {id} Sent a print request")
            # Build a print document
            doc = printDoc(f"My name is machine {id}", id)
            # Insert it in the print queue
            self.outer.print_list.queueInsert(doc)