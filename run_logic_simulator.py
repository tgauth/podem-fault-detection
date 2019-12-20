from circuit_functions import *

""" SCRIPT INPUTS """
# assumes file is in the same directory as script execution
# filename = "s27.txt"
# test_vectors = ['1110101', '0001010', '1010101', '0110111', '1010001']

# filename = "s298f_2.txt"
# test_vectors = ['10101010101010101', '01011110000000111', '11111000001111000',
#                 '11100001110001100', '01111011110000000']

# filename = "s344f_2.txt"
# test_vectors = ['101010101010101011111111', '010111100000001110000000',
#                 '111110000011110001111111', '111000011100011000000000',
#                 '011110111100000001111111']

filename = "s349f_2.txt"
test_vectors = ['101010101010101011111111', '010111100000001110000000',
                '111110000011110001111111', '111000011100011000000000',
                '011110111100000001111111']

print filename
for test_vector in test_vectors:
    circuit, output_list, io_dict = load_circuit(filename, test_vector)
    io_dict = evaluate_circuit(circuit, io_dict)
    output_vector = format_output(io_dict, output_list)
    print test_vector + ": " + output_vector

