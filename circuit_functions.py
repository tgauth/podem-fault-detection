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

    return circuit, output_list, io_dict


def evaluate_circuit(circuit, io_dict):
    """
    :param circuit: list of circuit instructions, in named tuple form
    :param io_dict: dictionary of input, output, and intermediate wire values
    :return: dictionary of final input, output, and intermediate wire values
    """
    eval_circuits = []
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
    return io_dict


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