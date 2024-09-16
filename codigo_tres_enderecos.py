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

    def new_label(self):
        """Gera um novo rótulo."""
        self.label_count += 1
        return f"L{self.label_count}"

    def generate(self, op, arg1=None, arg2=None, result=None):
        """Gera uma instrução de três endereços e a adiciona ao código."""
        instruction = (op, arg1, arg2, result)
        self.code.append(instruction)
        return instruction

    def generate_func_label(self, func_name):
        """Gera um rótulo para o início de uma função."""
        label = f"label func {func_name}"
        self.code.append((label,))

    def generate_param(self, param_name, param_type):
        """Gera uma instrução de parâmetro para a função."""
        self.code.append((f"param {param_name}: {param_type}",))

    def generate_return(self, value):
        """Gera a instrução de retorno."""
        self.code.append((f"ret {value}",))

    def end_func(self, func_name):
        """Gera o encerramento de uma função."""
        self.code.append((f"endfunc {func_name}",))

    def print_code(self):
        """Imprime o código de três endereços."""
        print("\nThree-Address Code:")
        for line in self.code:
            print(" ".join(str(x) for x in line if x is not None))
