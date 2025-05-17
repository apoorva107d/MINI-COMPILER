class TAC:
    def __init__(self):
        self.instructions = []
        self.temp_count = 0
        self.label_count = 0

    def new_temp(self):
        """Generate a new temporary variable."""
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp

    def new_label(self):
        """Generate a new label."""
        label = f"L{self.label_count}"
        self.label_count += 1
        return label

    def emit(self, op, arg1=None, arg2=None, result=None):
        """Emit a TAC instruction."""
        instruction = {"op": op, "arg1": arg1, "arg2": arg2, "result": result}
        self.instructions.append(instruction)
        if op in ["+", "-", "*", "/", "<", ">"]:
            print(f"[TAC Generation] Emitted: {result} = {arg1} {op} {arg2}")
        elif op in ["goto", "if", "label"]:
            print(f"[TAC Generation] Emitted: {op} {arg1}")
        else:
            print(f"[TAC Generation] Emitted: {result} = {arg1}")
        return instruction

    def to_string(self):
        """Convert TAC instructions to string."""
        return "\n".join(
            f"{i['result']} = {i['arg1']} {i['op']} {i['arg2']}" if i['op'] in ["+", "-", "*", "/", "<", ">"]
            else f"{i['op']} {i['arg1']}" if i['op'] in ["goto", "if", "label"]
            else f"{i['result']} = {i['arg1']}"
            for i in self.instructions
        )
