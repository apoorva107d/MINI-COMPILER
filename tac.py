class TAC:
    def __init__(self):
        self.instructions = []
        self.temp_count = 0
        self.label_count = 0

    def new_temp(self):
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp

    def new_label(self):
        label = f"L{self.label_count}"
        self.label_count += 1
        return label

    def emit(self, op, arg1=None, arg2=None, result=None):
        if op == "if" and arg1:
            instr = {"op": op, "arg1": arg1, "arg2": None, "result": None}
        else:
            instr = {"op": op, "arg1": arg1, "arg2": arg2, "result": result}
        self.instructions.append(instr)
        print(f"[TAC Generation] Emitted: {self.to_string_last()}")

    def to_string_last(self):
        instr = self.instructions[-1]
        op, arg1, arg2, result = instr["op"], instr["arg1"], instr["arg2"], instr["result"]
        if op == "label":
            return f"label {arg1}"
        elif op == "goto":
            return f"goto {arg1}"
        elif op == "if":
            return f"if {arg1}"
        elif op in ["+", "-", "*", "/", "<", ">"]:
            return f"{result} = {arg1} {op} {arg2}"
        elif op == "=":
            return f"{result} = {arg1}"
        return ""

    def to_string(self):
        lines = []
        for instr in self.instructions:
            op, arg1, arg2, result = instr["op"], instr["arg1"], instr["arg2"], instr["result"]
            if op == "label":
                lines.append(f"label {arg1}")
            elif op == "goto":
                lines.append(f"goto {arg1}")
            elif op == "if":
                lines.append(f"if {arg1}")
            elif op in ["+", "-", "*", "/", "<", ">"]:
                lines.append(f"{result} = {arg1} {op} {arg2}")
            elif op == "=":
                lines.append(f"{result} = {arg1}")
        return "\n".join(lines)

    def optimize(self):
        constants = {}
        new_instructions = []
        for instr in self.instructions:
            op, arg1, arg2, result = instr["op"], instr["arg1"], instr["arg2"], instr["result"]
            if op == "=" and isinstance(arg1, (int, float)):
                constants[result] = arg1
                print(f"[Optimization] Propagated: {result} → {arg1}")
            elif op in ["+", "-", "*", "/"]:
                val1 = constants.get(arg1, arg1)
                val2 = constants.get(arg2, arg2)
                if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                    ops = {"+": lambda x, y: x + y, "-": lambda x, y: x - y, "*": lambda x, y: x * y, "/": lambda x, y: x / y}
                    value = ops[op](val1, val2)
                    constants[result] = value
                    new_instructions.append({"op": "=", "arg1": value, "arg2": None, "result": result})
                    print(f"[Optimization] Folded: {result} = {value}")
                    continue
            elif op in ["<", ">"]:
                val1 = constants.get(arg1, arg1)
                val2 = constants.get(arg2, arg2)
                if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                    value = 1 if (val1 < val2 if op == "<" else val1 > val2) else 0
                    constants[result] = value
                    new_instructions.append({"op": "=", "arg1": value, "arg2": None, "result": result})
                    print(f"[Optimization] Folded: {result} = {value}")
                    continue
            new_instructions.append(instr)
        self.instructions = new_instructions
        print(f"[Optimization] Reduced {len(self.instructions)} instructions")
