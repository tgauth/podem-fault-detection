from circuit_functions import *

""" SCRIPT USER INPUTS BEGIN """
# assumes file is in the same directory as script execution

# filename = "test.txt"
# net_no = 5
# stuck_at_value = 0

filename = "s27.txt"
net_no = 10  # must be between 1 and 20
stuck_at_value = 1  # must be 0 or 1

# filename = "s298f_2.txt"
# net_no = 70  # must be between
# stuck_at_value = 1  # must be 0 or 1

# filename = "s344f_2.txt"
# net_no = 91  # must be between
# stuck_at_value = 1  # must be 0 or 1

# filename = "s349f_2.txt"
# net_no = 7  # must be between
# stuck_at_value = 0  # must be 0 or 1

""" SCRIPT USER INPUTS END """

print filename
po = PodemOrchestrator(net_no, stuck_at_value)
po.load_circuit(filename)
test_possible = po.podem()
if test_possible:
    test_vector = po.format_output(po.input_list)
    print(test_vector)
else:
    print("no test vector found")

