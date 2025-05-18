class TACInterpreter:
    def __init__(self, tac):
        self.tac = tac
        self.variables = {}
        self.labels = {}
        self.pc = 0

    def execute(self):
        # Map labels to instruction indices
        for i, instr in enumerate(self.tac.instructions):
            if instr["op"] == "label":
                self.labels[instr["arg1"]] = i
        print(f"[Interpreter] Labels: {self.labels}")

        max_steps = 1000  # Prevent infinite loops
        steps = 0

        while 0 <= self.pc < len(self.tac.instructions):
            if steps > max_steps:
                raise Exception("[Interpreter Error] Infinite loop detected")
            steps += 1

            instr = self.tac.instructions[self.pc]
            op, arg1, arg2, result = instr["op"], instr["arg1"], instr["arg2"], instr["result"]
            print(f"[Interpreter] PC={self.pc}: {op} {arg1} {arg2} {result}")

            if op == "=":
                self.variables[result] = self.get_value(arg1)
                print(f"[Interpreter] {result} = {self.variables[result]}")
                self.pc += 1
            elif op in ["+", "-", "*", "/"]:
                val1 = self.get_value(arg1)
                val2 = self.get_value(arg2)
                ops = {
                    "+": lambda x, y: x + y,
                    "-": lambda x, y: x - y,
                    "*": lambda x, y: x * y,
                    "/": lambda x, y: x / y
                }
                self.variables[result] = ops[op](val1, val2)
                print(f"[Interpreter] {result} = {val1} {op} {val2} = {self.variables[result]}")
                self.pc += 1
            elif op in ["<", ">"]:
                val1 = self.get_value(arg1)
                val2 = self.get_value(arg2)
                self.variables[result] = 1 if (val1 < val2 if op == "<" else val1 > val2) else 0
                print(f"[Interpreter] {result} = {val1} {op} {val2} = {self.variables[result]}")
                self.pc += 1
            elif op == "if":
                condition_str = arg1.split()
                if len(condition_str) != 5 or condition_str[1] != "!=" or condition_str[2] != "0" or condition_str[3] != "goto":
                    raise Exception(f"[Interpreter Error] Invalid if condition: {arg1}")
                condition = self.get_value(condition_str[0])
                label = condition_str[4]
                print(f"[Interpreter] if {condition_str[0]} = {condition}, jump to {label} if not zero")
                if condition != 0:
                    if label not in self.labels:
                        raise Exception(f"[Interpreter Error] Label {label} not found")
                    self.pc = self.labels[label]
                else:
                    self.pc += 1
            elif op == "goto":
                if arg1 not in self.labels:
                    raise Exception(f"[Interpreter Error] Label {arg1} not found")
                print(f"[Interpreter] goto {arg1}")
                self.pc = self.labels[arg1]
            elif op == "label":
                self.pc += 1
            else:
                raise Exception(f"[Interpreter Error] Unknown op: {op}")

        print(f"[Interpreter] Execution finished. Variables: {self.variables}")
        return self.variables

    def get_value(self, arg):
        if arg is None:
            return 0
        if isinstance(arg, (int, float)):
            return arg
        return self.variables.get(arg, 0)
