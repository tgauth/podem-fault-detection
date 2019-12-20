PODEM Project Contents:
1. boolean_operations.py: 
    - defines helpful boolean functions used to evaluate the circuit
    - methods: inverse, and_nand, and or_nor1. 
2. circuit_functions.py:
    - defines PodemOrchestrator class which has the attributes and methods needed to generate a test vector for a user-defined fault.
    - note: this has the same script name as Projects A and B, but additional methods have been added to it and some methods from Projects 
    A and B were updated to suit the requirements of Project C. 
3. run_podem.py: script to be run by the user for Project C.
    - inputs:
        filename (string): name of the file that contains circuit description (assumes file is also located in same directory)
        net_no (integer): net number of the fault
        stuck_at_value (Boolean): value that the fault is stuck-at (0 or 1)
    - output: 
        *prints a test vector to the console, or prints "no test vector found" 