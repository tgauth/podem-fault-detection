import copy
import random
import plotly.graph_objs as go
from plotly.offline import plot
from collections import namedtuple


def load_circuit(filename, test_vector):
    """
    load the circuit instructions from the input file
    :param filename: string of filename, with ".txt" included
    :param test_vector: string of initial values for circuit inputs
    :return: circuit list, output_list, and io_dict
    """
    logic_file = open(filename)
    logic = logic_file.readlines()
    logic_file.close()

    Instruction = namedtuple('Instruction', 'gate input output')
    circuit = []
    io_dict = {}
    output_list = []

    max_input = 0

    for line in logic:
        parse_line = line.split()
        try:
            gate = parse_line.pop(0)
        except:
            # in case there is a new line at the end of the file
            gate = ""

        if gate in ["INV", "BUF"]:
            circuit.append(Instruction(gate=gate,
                                       input=[parse_line[0]],
                                       output=parse_line[1]))
            if max(int(parse_line[0]), int(parse_line[1])) > max_input:
                max_input = max(int(parse_line[0]), int(parse_line[1]))
        elif gate in ["AND", "NAND", "OR", "NOR"]:
            circuit.append(Instruction(gate=gate,
                                       input=[parse_line[0], parse_line[1]],
                                       output=parse_line[2]))
            if max(int(parse_line[0]), int(parse_line[1]), int(parse_line[2])) > max_input:
                max_input = max(int(parse_line[0]), int(parse_line[1]), int(parse_line[2]))
        elif gate in ["INPUT", "OUTPUT"]:
            parse_line.pop(len(parse_line)-1)
            if gate == "INPUT":
                for i, input_line in enumerate(parse_line):
                    io_dict[input_line] = int(test_vector[i])
            else:
                output_list = parse_line
                for output_line in parse_line:
                    io_dict[output_line] = -1

    # initialize any intermediate wires
    for i in range(1, max_input + 1):
        if str(i) not in io_dict.keys():
            io_dict[str(i)] = -1

    return circuit, output_list, io_dict, max_input


def evaluate_circuit(circuit, io_dict, input_net_fault_flag=True, net_no=None, fault=None):
    """
    :param circuit: list of circuit instructions, in named tuple form
    :param io_dict: dictionary of input, output, and intermediate wire values
    :return: dictionary of final input, output, and intermediate wire values
    """
    initial_circuit = copy.deepcopy(circuit)
    initial_io_dict = copy.deepcopy(io_dict)
    eval_circuits = []

    if input_net_fault_flag:
        # fault is on an input value
        io_dict[net_no] = fault

    while circuit:
        for circuit_instruction in circuit:
            # check if input(s) are available
            eval_flag = True
            for input_num in circuit_instruction.input:
                if io_dict[input_num] == -1:
                    eval_flag = False

            # add to eval list if inputs available
            if eval_flag:
                eval_circuits.append(circuit_instruction)
                circuit.remove(circuit_instruction)

        for eval_circuit in eval_circuits:
            if eval_circuit.gate == "INV":
                if io_dict[eval_circuit.input[0]] == 0:
                    io_dict[eval_circuit.output] = 1
                else:
                    io_dict[eval_circuit.output] = 0
            elif eval_circuit.gate == "BUF":
                io_dict[eval_circuit.output] = int(io_dict[eval_circuit.input[0]])
            elif eval_circuit.gate == "AND":
                if io_dict[eval_circuit.input[0]] and io_dict[eval_circuit.input[1]]:
                    io_dict[eval_circuit.output] = 1
                else:
                    io_dict[eval_circuit.output] = 0
            elif eval_circuit.gate == "NAND":
                if io_dict[eval_circuit.input[0]] and io_dict[eval_circuit.input[1]]:
                    io_dict[eval_circuit.output] = 0
                else:
                    io_dict[eval_circuit.output] = 1
            elif eval_circuit.gate == "OR":
                if io_dict[eval_circuit.input[0]] or io_dict[eval_circuit.input[1]]:
                    io_dict[eval_circuit.output] = 1
                else:
                    io_dict[eval_circuit.output] = 0
            elif eval_circuit.gate == "NOR":
                if io_dict[eval_circuit.input[0]] or io_dict[eval_circuit.input[1]]:
                    io_dict[eval_circuit.output] = 0
                else:
                    io_dict[eval_circuit.output] = 1

            if not input_net_fault_flag:
                # if fault is on an output net, check if its the one just calculated
                # and force the output to the fault value if it is
                if eval_circuit.output == net_no:
                    io_dict[eval_circuit.output] = fault

    return io_dict, initial_circuit, initial_io_dict


def format_output(io_dict, output_list):
    """
    format outputs into expected output vector order
    :param io_dict: dictionary of final input, output, and intermediate wire values
    :param output_list: list of keys for io_dict that are circuit outputs
    :return: string of circuit output vector (i.e. string of 1's and 0's)
    """
    output_string = []
    for i in output_list:
        output_string.append(str(io_dict[i]))
    return "".join(output_string)


def generate_fault_list(fault_list_filename, max_input):
    """
    generate the list of faults to be simulated
    :param fault_list_filename: string of the name of the file
    containing list of faults, or None if all faults are to be simulated
    :param max_input: integer of number of nets in the circuit
    :return: dictionary with net number key and list of faults to simulate as value
    """
    fault_sim_dict = {}
    if fault_list_filename:
        # initialize dictionary from file
        fault_file = open(fault_list_filename)
        lines = fault_file.readlines()
        fault_file.close()
        for line in lines:
            parse_line = line.split()
            net_no = str(parse_line[0])
            stuck_value = int(parse_line[1])
            if net_no not in fault_sim_dict.keys():
                fault_sim_dict[net_no] = [stuck_value]
            else:
                fault_sim_dict[net_no].append(stuck_value)
    else:
        for i in range(1, max_input + 1):
            fault_sim_dict[str(i)] = [0, 1]
    return fault_sim_dict


def simulate_fault_list(fault_sim_dict, circuit, io_dict, output_list):
    """
    simulate all the faults in the fault list and save output to list
    :param fault_sim_dict: dictionary with net number key and list of faults to simulate as value
    :param circuit: list of circuit instructions, in named tuple form
    :param io_dict: dictionary of final input, output, and intermediate wire values
    :return: list of circuit outputs in string form
    """
    fault_sim_circuit_outputs = []

    for net_no, faults_to_sim in fault_sim_dict.items():
        for fault in faults_to_sim:
            input_net_fault_flag = False
            if io_dict[net_no] != -1:
                input_net_fault_flag = True

            fault_io_dict, circuit, io_dict = evaluate_circuit(circuit, io_dict, input_net_fault_flag, net_no, fault)
            fault_output_vector = format_output(fault_io_dict, output_list)
            fault_sim_circuit_outputs.append(fault_output_vector)

    return fault_sim_circuit_outputs


def save_detected_faults(fault_free_output_vector, fault_circuit_outputs, fault_sim_dict, save_output=True):
    """
    compare fault outputs to fault free output and save detected faults to text file
    :param fault_free_output_vector: string, the expected output of the fault free circuit
    :param fault_circuit_outputs: list of strings, what the circuits with faults output
    :param fault_sim_dict: list of faults simulated (for ordering purposes)
    :return: fault_list (list of tuples - (net, fault)) and num_faults_detected (int)
    """
    if save_output:
        outfile = open("detected_faults.txt", "w")

    index = 0
    num_faults_detected = 0
    fault_list = []
    for net_no, faults in fault_sim_dict.items():
        for fault in faults:
            if fault_free_output_vector != fault_circuit_outputs[index]:
                fault_list.append((int(net_no), fault))
                num_faults_detected += 1
            index += 1

    if save_output:
        # used for general fault detection
        for line in sorted(fault_list):
            outfile.write("{} stuck-at-{}\n".format(line[0], line[1]))

        outfile.write("{} faults detected".format(num_faults_detected))
        outfile.close()

    return fault_list, num_faults_detected


def generate_test_vectors(num_inputs):
    """
    for part b of the assignment, randomly generates all possible binary test vectors for a circuit
    :param num_inputs: int, number of binary inputs to the circuit (upper bound on test vectors is 2^num_inputs - 1)
    :return: list of binary test vectors in a random order (seeded with 4 for replicability)
    """
    decimal_list = list(range(0, (2 ** num_inputs)-1))
    binary_list = [bin(decimal) for decimal in decimal_list]
    test_vectors = []
    for bin_num in binary_list:
        if len(bin_num[2:]) < num_inputs:
            append = '0' * (num_inputs - len(bin_num[2:]))
            input_test_vector = append + bin_num[2:]
        else:
            input_test_vector = bin_num[2:]
        test_vectors.append(input_test_vector)
    random.Random(4).shuffle(test_vectors)
    return test_vectors


def save_undetected_faults(fault_sim_dict, fault_list):
    """
    save the list of undetected faults to a text file
    :param fault_sim_dict: dictionary of all faults that were tested
    :param fault_list: tuple of faults that were actually detected
    :return: None
    """
    outfile = open("undetected_faults.txt", "w")
    for net, faults in fault_sim_dict.items():
        for fault in faults:
            if (int(net), fault) not in fault_list:
                outfile.write("{} {}\n".format(net, fault))
    outfile.close()
    
    
def run_fault_detection(test_vectors, filename):
    """
    apply test vectors to circuit until coverage thresholds of 75% and 90% are met
    :param test_vectors: list of binary test vectors to apply
    :param filename: text file containing circuit description
    :return: test_vect_for_75, test_vec_for_90 - integers representing the number of
    test vectors needed to reach each fault coverage threshold. also plots the
    fault coverage percentage as a function of the number of test vectors in a separate window
    """
    faults_detected = 0
    possible_faults = 0
    fault_coverage = []
    test_vec_for_75 = -1
    test_vec_for_90 = -1
    fault_list_filename = None
    for test_vector in test_vectors:
        # only continuing trying test vectors until we hit threshold
        if test_vec_for_90 == -1:
            circuit, output_list, circuit_io_dict, max_input = load_circuit(filename, test_vector)
            fault_free_io_dict, initial_circuit, initial_io_dict = evaluate_circuit(circuit, circuit_io_dict)
            fault_free_output_vector = format_output(fault_free_io_dict, output_list)
            fault_sim_dict = generate_fault_list(fault_list_filename, max_input)

            # initialize full fault list initially, but then only try to detect faults that haven't
            # been detected already, which get saved to this file after each test vector
            if not fault_list_filename:
                fault_list_filename = "undetected_faults.txt"
                possible_faults = float(len(fault_sim_dict.keys()) * 2)

            fault_circuit_outputs = simulate_fault_list(fault_sim_dict, initial_circuit, initial_io_dict, output_list)
            fault_list, num_detected = save_detected_faults(fault_free_output_vector, fault_circuit_outputs,
                                                            fault_sim_dict)
            # saved undetected faults to file for next vector to try to detect
            save_undetected_faults(fault_sim_dict, fault_list)

            # book-keeping
            faults_detected += num_detected
            fault_coverage.append(faults_detected)
            if faults_detected / possible_faults >= 0.75:
                if faults_detected / possible_faults >= 0.9:
                    test_vec_for_90 = len(fault_coverage)
                else:
                    test_vec_for_75 = len(fault_coverage)
        else:
            break

    # plotting
    num_test = [i for i in range(1, len(fault_coverage) + 1)]
    cov_perc = [x/possible_faults*100 for x in fault_coverage]
    trace = go.Scatter(x=num_test, y=cov_perc, mode='lines')
    layout = go.Layout(title="Fault Coverage as a Function of Randomly Applied Test Vectors",
                       yaxis=dict(title='Fault Coverage Percent (%)'),
                       xaxis=dict(title='Number of Random Test Vectors'))
    plot(go.Figure(data=[trace], layout=layout))
    return test_vec_for_75, test_vec_for_90
