class TuringMachine:
    def __init__(self, transitions, start_state='q0', accept_state='qa', reject_state='qr', blank_symbol=''):
        self.transitions = transitions
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.blank_symbol = blank_symbol

    def run(self, input_):
        tape = list(input_) if input_ else []
        current_symbol = tape[0] if tape else self.blank_symbol
        right_hand_side = tape[1:] if len(tape) > 1 else []
        left_hand_side = []
        current_state = self.start_state

        while True:
            if current_state == self.accept_state:
                action = 'Accept'
            elif current_state == self.reject_state:
                action = 'Reject'
            else:
                action = None

            config = {
                'state': current_state,
                'left_hand_side': left_hand_side,
                'symbol': current_symbol,
                'right_hand_side' : right_hand_side
            }
            yield (action, config)

            if action is not None:
                break

            key = (current_state, current_symbol)
            if key not in self.transitions:
                current_state = self.reject_state
                continue

            next_state, write_symbol, direction = self.transitions[key]
            current_state = next_state
            current_symbol = write_symbol

            if direction == 'R':
                left_hand_side.append(write_symbol)
                if right_hand_side:
                    current_symbol = right_hand_side.pop(0)
                else:
                    current_symbol = self.blank_symbol
            elif direction == 'L':
                right_hand_side.insert(0, write_symbol)
                if left_hand_side:
                    current_symbol = left_hand_side.pop()
                else:
                    current_symbol = self.blank_symbol

    def accepts(self, input_, **kwargs):
        for action, config in self.run(input_):
            if action == 'Accept':
                return True
            elif action == 'Reject':
                return False
        return None

    def rejects(self, input_, **kwargs):
        result = self.accepts(input_, **kwargs)
        if result is None:
            return None
        return not result

    def debug(self, input_, step_limit=100, colored=False):
        step = 0
        for action, config in self.run(input_):
            if step >= step_limit:
                print("...")
                break
            print(f"config = {config}")
            step += 1
            if action is not None:
                break