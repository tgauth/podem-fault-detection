Deductive Fault Simulator Project Contents:
1. circuit_functions.py:
    - defines methods for loading the circuit from a file, simulating the circuit, generating faults lists, and tracking fault detection.
    - note: this has the same script name as Project A, but additional methods have been added to it and some methods from Project A were
    updated to meet the requirements of Project B. 
2. run_fault_detection.py: script to be run by the user for part A of the project.
    - inputs:
        filename (string): name of the file that contains circuit description (assumes file is also located in same directory)
        test_vectors (list of strings): circuit input as a string (i.e. '101010').
        fault_list_filename (string): filename of fault list to simulate (if any) or None (program will generate full fault list)
    - output: 
        *detected_faults.txt text file containing the faults detected in the format of "net number stuck-at-<value>"
3. run_fault_coverage.py: script to be run by the user for part B of the project.
    - inputs:
        filename (string): name of the file that contains circuit descrption (assumes file is also located in same directory)
        num_inputs (integer): number of inputs to the circuit
    - outputs:
        *prints to console the number of test vectors needed for 75% and 90% fault run_fault_coverage
        *opens a window with a graph of fault coverage percentage as a function of number of test vectors applied