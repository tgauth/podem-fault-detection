from circuit_functions import *

""" SCRIPT USER INPUTS BEGIN """
# assumes file is in the same directory as script execution
# filename = "s27.txt"
# num_inputs = 7

# filename = "s298f_2.txt"
# num_inputs = 17

# filename = "s344f_2.txt"
# num_inputs = 24

filename = "s349f_2.txt"
num_inputs = 24

""" SCRIPT USER INPUTS END """

test_vectors = generate_test_vectors(num_inputs)
test_vec_75, test_vec_90 = run_fault_detection(test_vectors, filename)
print filename
print test_vec_75
print test_vec_90
