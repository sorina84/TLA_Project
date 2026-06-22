# -*- coding: utf-8 -*-
from turing_machine import TuringMachine
from test_turing_machine_example1 import print_states

#create the Turing machine
transitions = {
    ('q0', '1'): ('q_prep', '1', 'R'),
    ('q0', '0'): ('q_prep', '0', 'R'),
    
    ('q_prep', '1'): ('q_prep', '1', 'R'),
    ('q_prep', '0'): ('q_prep', '0', 'R'),
    ('q_prep', ''): ('q_back', '0', 'L'), 

    ('q_back', '1'): ('q_back', '1', 'L'),
    ('q_back', '0'): ('q_back', '0', 'L'),
    ('q_back', ''): ('q_start', '', 'R'),  


    ('q_start', '1'): ('q1', 'X', 'R'),
    ('q_start', '0'): ('q_clean', '0', 'R'), 


    ('q1', '1'): ('q1', '1', 'R'),
    ('q1', '0'): ('q2', '0', 'R'),

    ('q2', 'Y'): ('q2', 'Y', 'R'),
    ('q2', '1'): ('q3', 'Y', 'R'),
    ('q2', '0'): ('q_reset', '0', 'L'), 

    ('q3', '1'): ('q3', '1', 'R'),
    ('q3', '0'): ('q3', '0', 'R'),
    ('q3', ''): ('q4', '1', 'L'), 


    ('q4', '1'): ('q4', '1', 'L'),
    ('q4', '0'): ('q4', '0', 'L'),
    ('q4', 'Y'): ('q2', 'Y', 'R'),

    ('q_reset', 'Y'): ('q_reset', '1', 'L'),
    ('q_reset', '0'): ('q_reset_0', '0', 'L'),
    ('q_reset_0', '1'): ('q_reset_0', '1', 'L'),
    ('q_reset_0', 'X'): ('q_start', 'X', 'R'), 


    ('q_clean', '1'): ('q_clean', '1', 'R'),
    ('q_clean', '0'): ('q_clean', '0', 'R'),
    ('q_clean', ''): ('qa', '', 'R'), 

    


}
if __name__ == "__main__":
    print_states(transitions)
    machine = TuringMachine(transitions)

    def run(input_):
        w = input_
        print("Input:",w)
        print("Accepted" if machine.accepts(w) else "Rejected")
        machine.debug(w, step_limit=1000)

        print()

    # SHOULD ACCEPT
    run("110111")
    # outputs 111111

    # SHOULD ACCEPT
    run("11101111")
    # outputs 111111111111

    run("01111")
