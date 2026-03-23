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
        self.semaphore = threading.Semaphore(5)  
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
              self.printerSleep()
              if self.outer.print_list.head is not None:
                 self.printDox(self.printerID)

        def printerSleep(self):
            sleepSeconds = random.randint(1, self.outer.MAX_PRINTER_SLEEP)
            time.sleep(sleepSeconds)

        def printDox(self, printerID):
               print(f"Printer ID: {printerID} : now available")
               self.outer.binary.acquire()   
               self.outer.print_list.queuePrint(printerID)
               self.outer.binary.release()   
               self.outer.semaphore.release()

    # Machine class
    class machineThread(threading.Thread):
        def __init__(self, machineID, outer):
            threading.Thread.__init__(self)
            self.machineID = machineID
            self.outer = outer  # Reference to the Assignment1 instance

        def run(self):
         while self.outer.sim_active:
          self.machineSleep()
          self.isRequestSafe(self.machineID)   
          self.printRequest(self.machineID)   
          self.postRequest(self.machineID) 

        def isRequestSafe(self, id):
         print(f"Machine {id} Checking availability")
         self.outer.semaphore.acquire()   
         self.outer.binary.acquire()      
         print(f"Machine {id} will proceed") 

        def machineSleep(self):
            sleepSeconds = random.randint(1, self.outer.MAX_MACHINE_SLEEP)
            time.sleep(sleepSeconds)

        def printRequest(self, id):
            print(f"Machine {id} Sent a print request")
            # Build a print document
            doc = printDoc(f"My name is machine {id}", id)
            # Insert it in the print queue
            self.outer.print_list.queueInsert(doc)
        
        def postRequest(self, id):
            print(f"Machine {id} Releasing binary semaphore")
            self.outer.binary.release()  