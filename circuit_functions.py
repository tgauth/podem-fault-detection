import copy
import random
from collections import namedtuple
from boolean_operations import *


class PodemOrchestrator:
    def __init__(self, net_no, stuck_at_value):
        self.net_no = str(net_no)
        self.stuck_at_value = stuck_at_value
        self.circuit = []
        self.io_dict = {}
        self.previous_io_dicts = []
        self.input_list = []
        self.output_list = []
        self.dfrontier = []
        self.initialized = False

    def inject_fault(self):
        """
        update the io_dict of the net with a fault, based on the stuck-at-value,
        where 2 represents s-a-1 and -2 represents s-a-0
        """
        if self.stuck_at_value:
            # stuck at 1 (D')
            self.io_dict[self.net_no] = 2
        else:
            # stuck at 0 (D)
            self.io_dict[self.net_no] = -2

    def error_at_po(self):
        """
        returns a boolean that is true if there is a D/D'
        on any of the circuit outputs, and false if not
        """
        for output_net in self.output_list:
            if abs(self.io_dict[output_net]) == 2:
                return True
        return False

    def update_dfrontier(self):
        """
        generates the list of gates on the dfrontier (if any)
        """
        dfrontier = []
        for circuit_instruction in self.circuit:
            fault_flag = False
            undefined_flag = False
            # needs to be a multi-input gate
            if len(circuit_instruction.input) > 1:
                for input_num in circuit_instruction.input:
                    # check if an input has a D/D'
                    if abs(self.io_dict[input_num]) == 2:
                        fault_flag = True
                    # check if an input is undefined
                    if self.io_dict[input_num] == -1:
                        undefined_flag = True
                # if both are true, gate is a candidate for d-frontier
                if fault_flag and undefined_flag:
                    dfrontier.append(circuit_instruction)
        self.dfrontier = dfrontier

    def load_circuit(self, filename, test_vector=None):
        """
        load the circuit instructions from the input file
        :param filename: string of filename, with ".txt" included
        :param test_vector: string of initial values for circuit inputs
        circuit list, input_list, output_list, and io_dict get
        assigned to Podem Orchestrator object variables
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
                    if test_vector:
                        # projects and b will supply a test vector
                        for i, input_line in enumerate(parse_line):
                            io_dict[input_line] = int(test_vector[i])
                    else:
                        # podem will not have a test vector
                        input_list = parse_line
                        for i, input_line in enumerate(parse_line):
                            io_dict[input_line] = -1
                else:
                    output_list = parse_line
                    for output_line in parse_line:
                        io_dict[output_line] = -1

        # initialize any intermediate wires
        for i in range(1, max_input + 1):
            if str(i) not in io_dict.keys():
                io_dict[str(i)] = -1

        self.circuit = circuit
        self.output_list = output_list
        self.io_dict = io_dict
        self.input_list = input_list

    def evaluate_circuit(self):
        """
        evaluate the circuit to the extent that we can given the inputs
        """
        # preserve circuit instructions in object but copy to pop-able list
        circuit = copy.deepcopy(self.circuit)
        eval_circuits = []
        num_evals_prev = 100000

        while circuit:
            for circuit_instruction in circuit:
                # check if output needs calculating
                eval_flag = False
                if self.io_dict[circuit_instruction.output] in [-1, -2, 2]:
                    eval_flag = True

                # add to eval list if output hasn't been calculated yet
                if eval_flag:
                    eval_circuits.append(circuit_instruction)

            num_evals = len(eval_circuits)
            while eval_circuits:
                eval_circuit = eval_circuits.pop(0)

                if eval_circuit.gate == "INV":
                    if self.io_dict[eval_circuit.input[0]] == 0:
                        self.io_dict[eval_circuit.output] = 1
                    elif self.io_dict[eval_circuit.input[0]] == 1:
                        self.io_dict[eval_circuit.output] = 0
                    elif self.io_dict[eval_circuit.input[0]] == 2:
                        self.io_dict[eval_circuit.output] = -2
                    elif self.io_dict[eval_circuit.input[0]] == -2:
                        self.io_dict[eval_circuit.output] = 2
                elif eval_circuit.gate == "BUF":
                    self.io_dict[eval_circuit.output] = int(self.io_dict[eval_circuit.input[0]])
                elif eval_circuit.gate == "AND":
                    self.io_dict[eval_circuit.output] = and_nand(self.io_dict[eval_circuit.input[0]],
                                                                 self.io_dict[eval_circuit.input[1]])
                elif eval_circuit.gate == "NAND":
                    self.io_dict[eval_circuit.output] = and_nand(self.io_dict[eval_circuit.input[0]],
                                                                 self.io_dict[eval_circuit.input[1]], True)
                elif eval_circuit.gate == "OR":
                    self.io_dict[eval_circuit.output] = or_nor(self.io_dict[eval_circuit.input[0]],
                                                               self.io_dict[eval_circuit.input[1]])
                elif eval_circuit.gate == "NOR":
                    self.io_dict[eval_circuit.output] = or_nor(self.io_dict[eval_circuit.input[0]],
                                                               self.io_dict[eval_circuit.input[1]], True)

                if eval_circuit.output == self.net_no:
                    if self.io_dict[eval_circuit.output] == inverse(self.stuck_at_value):
                        # can only inject the fault if it differs from ff value
                        self.inject_fault()
                        self.initialized = True

            # if we're evalulating the same # of gates we probably aren't accomplishing anything
            if num_evals == num_evals_prev:
                break
            else:
                num_evals_prev = num_evals

    def format_output(self, output_list):
        """
        format outputs into expected output vector order (can be circuit inputs too)
        :param output_list: list containing net numbers to be formatted
        :return string: net number values formatted in order of output list
        """
        output_string = []
        for i in output_list:
            if self.io_dict[i] == -1:
                # input can be 0 or 1 because we never had to initialize it
                output_string.append(str(random.Random(4).randint(0, 1)))
            elif self.io_dict[i] == -2:
                output_string.append('1')
            elif self.io_dict[i] == 2:
                output_string.append('0')
            else:
                output_string.append(str(self.io_dict[i]))
        return "".join(output_string)

    def objective(self):
        """
        podem objective function - first objective is to initialize the fault
        if it is an input fault, the D/D' is the objective, otherwise
        the objective is to map the inverse of the stuck-at-value onto a PI,
        and if the fault is already initialized we select a gate from the
        d-frontier to propagate the fault to the output
        """
        # the target fault is l (net_no) s-a-v (stuck_at_value)
        # if l is a primary input return net_no, D/D' value
        if self.net_no in self.input_list and self.io_dict[self.net_no] == -1:
            self.initialized = True
            if self.stuck_at_value:
                return self.net_no, 2
            else:
                return self.net_no, -2
        elif self.io_dict[self.net_no] == -1:
            self.initialized = False
            return self.net_no, inverse(self.stuck_at_value)
        else:
            # select a gate from the D-frontier
            # select an input (j) of g with value x (-1)
            # find controlling value (c) of gate
            # return j, inverse(c)
            circuit_instruction = self.dfrontier.pop(0)
            if "AND" in circuit_instruction.gate:
                controlling_val = 0
            else:
                controlling_val = 1
            for input_num in circuit_instruction.input:
                if self.io_dict[input_num] == -1:
                    return input_num, inverse(controlling_val)

    def backtrace(self, net_no, value):
        """
        podem backtrace function
        :param net_no: string representing the desired net number
        :param value: int representing the desired value of the net number
        """
        # map objective into PI assignment
        # while k is a gate output
        while net_no not in self.input_list:
            # find inversion (i) of k
            # select an input (j) of k with value x (-1)
            # v = value XOR inversion
            # k = j
            for circuit_instruction in self.circuit:
                if circuit_instruction.output == net_no:
                    if circuit_instruction.gate == "INV":
                        net_no = circuit_instruction.input[0]
                        value = inverse(value)
                    elif circuit_instruction.gate in ["NAND", "NOR"]:
                        if self.io_dict[circuit_instruction.input[0]] == -1:
                            net_no = circuit_instruction.input[0]
                        else:
                            net_no = circuit_instruction.input[1]
                        value = value ^ 1
                    elif circuit_instruction.gate in ["AND", "OR"]:
                        if self.io_dict[circuit_instruction.input[0]] == -1:
                            net_no = circuit_instruction.input[0]
                        else:
                            net_no = circuit_instruction.input[1]
                        value = value ^ 0
                    else:  # buffer instruction
                        net_no = circuit_instruction.input[0]
                    break
        # once we find a PI
        return net_no, value

    def imply(self, net_no, value):
        """
        the imply function saves the current state of the circuit
        and then evaluates it after assigned the value to the net_no
        :param net_no: string, the net number to be updated
        :param value: int, the value to be assigned to the net number
        """
        self.previous_io_dicts.append(copy.deepcopy(self.io_dict))
        self.io_dict[net_no] = value
        # simulate circuit
        self.evaluate_circuit()
        # update d-frontier list
        self.update_dfrontier()

    def reverse(self):
        """
        if imply was unsuccessful, then revert to previous circuit conditions
        """
        self.io_dict = self.previous_io_dicts.pop(-1)

    def podem(self):
        """
        recursive method of assignment values to primary inputs to
        generate a test vector that activates the desired fault
        """
        # if error at PO return success
        if self.error_at_po():
            return True
        # if test not possible return failure
        if self.io_dict[self.net_no] == self.stuck_at_value:
            return False
        if self.initialized and not self.dfrontier:
            return False
        k, vk = self.objective()
        j, vj = self.backtrace(k, vk)
        self.imply(j, vj)
        # recursion:
        is_success = self.podem()
        if is_success:
            return True
        self.reverse()
        if abs(vj) != 2:
            vj = inverse(vj)
        self.imply(j, vj)
        is_success = self.podem()
        if is_success:
            return True
        self.reverse()
        self.imply(j, -1)
        return False


