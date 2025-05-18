class CodeGen:
    def __init__(self, tac):
        self.tac = tac
        self.assembly = []

    def generate(self):
        for instr in self.tac.instructions:
            op, arg1, arg2, result = instr["op"], instr["arg1"], instr["arg2"], instr["result"]
            if op == "=":
                self.assembly.append(f"mov {result}, {arg1}")
                print(f"[CodeGen] Emitted: mov {result}, {arg1}")
            elif op in ["+", "-", "*", "/"]:
                op_map = {"+": "add", "-": "sub", "*": "mul", "/": "div"}
                self.assembly.append(f"mov eax, {arg1}")
                self.assembly.append(f"{op_map[op]} eax, {arg2}")
                self.assembly.append(f"mov {result}, eax")
                print(f"[CodeGen] Emitted: {result} = {arg1} {op} {arg2}")
            elif op in ["<", ">"]:
                self.assembly.append(f"mov eax, {arg1}")
                self.assembly.append(f"sub eax, {arg2}")
                self.assembly.append(f"mov {result}, eax")
                print(f"[CodeGen] Emitted: {result} = {arg1} {op} {arg2}")
            elif op == "if":
                self.assembly.append(f"cmp {arg1.split()[0]}, 0")
                self.assembly.append(f"jne {arg1.split()[-1]}")
                print(f"[CodeGen] Emitted: if {arg1}")
            elif op == "goto":
                self.assembly.append(f"jmp {arg1}")
                print(f"[CodeGen] Emitted: goto {arg1}")
            elif op == "label":
                self.assembly.append(f"{arg1}:")
                print(f"[CodeGen] Emitted: label {arg1}")
        return self.assembly

    def to_string(self):
        return "\n".join(self.assembly)
