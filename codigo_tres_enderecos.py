class ThreeAddressCodeGenerator:
    def __init__(self):
        self.code = []
        self.temp_count = 0
        self.label_count = 0

    def new_temp(self):
        """Gera um novo nome de variável temporária."""
        temp_name = f"t{self.temp_count}"
        self.temp_count += 1
        return temp_name

    def generate(self, op, arg1=None, arg2=None, result=None):
        """Gera uma instrução de três endereços e a adiciona ao código."""
        instruction = (op, arg1, arg2, result)
        self.code.append(instruction)
        return instruction

    def print_code(self):
        """Imprime o código de três endereços."""
        print("\nThree-Address Code:")
        for line in self.code:
            print(" ".join(str(x) for x in line if x is not None))

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

