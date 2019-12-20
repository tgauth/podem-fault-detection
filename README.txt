Logic Simulator Project Contents:
1. circuit_functions.py: defines methods for loading the circuit from a file and simulating the circuit.
2. run_logic_simulator.py: script to be run by the user.
    - inputs:
        filename (string): name of the file that contains circuit description (assumes file is also located in same directory)
        test_vectors (list of strings): circuit inputs as a string (i.e. '101010'). accepts a list so multiple test vectors can be simulated in single script execution.
    - output: prints to console test vector(s) and corresponding output vector(s) in the format of <test vector>: <output vector>