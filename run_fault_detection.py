from circuit_functions import *

""" SCRIPT USER INPUTS BEGIN """
# assumes file is in the same directory as script execution

filename = "s27.txt"
test_vectors = ['1110101']
# test_vectors = ['0101001']

# filename = "s298f_2.txt"
# test_vectors = ['10101010101010101']
# test_vectors = ['11101110101110111']

# filename = "s344f_2.txt"
# test_vectors = ['101010101010101011111111']
# test_vectors = ['111010111010101010001100']

# filename = "s349f_2.txt"
# # test_vectors = ['101010101010101011111111']
# test_vectors = ['111111101010101010001111']

""" SCRIPT USER INPUTS END """

fault_list_filename = None

print filename
for test_vector in test_vectors:
    circuit, output_list, circuit_io_dict, max_input = load_circuit(filename, test_vector)
    fault_free_io_dict, initial_circuit, initial_io_dict = evaluate_circuit(circuit, circuit_io_dict)
    fault_free_output_vector = format_output(fault_free_io_dict, output_list)
    fault_sim_dict = generate_fault_list(fault_list_filename, max_input)
    fault_circuit_outputs = simulate_fault_list(fault_sim_dict, initial_circuit, initial_io_dict, output_list)
    _, _ = save_detected_faults(fault_free_output_vector, fault_circuit_outputs, fault_sim_dict)


