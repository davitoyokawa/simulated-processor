class Processador:
    def __init__(self, path, tamanho_mem=2048):
        self.opcode = None
        self.ir = None
        self.pc = 0
        self.ra = 0
        self.mem = [0] * tamanho_mem  # Tamanho padrão = 2048
        self.reg = [0] * 32
        self.tam_mem = tamanho_mem
        self.sp = 31

        self.instrucoes = []
        with open(path) as file:
            for linha in file.readlines():
                self.ir = linha.strip().split(" ")  # Pega a instrução
                self.instrucoes.append(self.ir)  # Adiciona na lista de instruções

    def execute(self):
        self.ir = self.instrucoes[self.pc]

        self.pc += 1
        self.opcode = self.ir[0]
        eq = self.ir[1].split(",")
        # executa a instrução correspondente ao opcode
        # Aritméticas
        for i in range(len(eq)):
            eq[i] = eq[i].replace("r", "")
        if self.opcode == 'add':  # Atribui à rd a soma de rs e rt // rd←rs+rt
            rd = int(eq[0])
            rs = int(eq[1])
            rt = int(eq[2])
            self.reg[rd] = self.reg[rs] + self.reg[rt]
            self.sp -= 1
            self.mem[self.sp] = self.reg[rd]
        elif self.opcode == 'addi':  # Atribui à rd a subtração entre rs e um valor imediato // rd ← rs+vimm
            rd = int(eq[0])
            rs = int(eq[1])
            vimm = int(eq[2])
            self.reg[rd] = self.reg[rs] + vimm
            self.sp -= 1
            self.mem[self.sp] = self.reg[rd]
        elif self.opcode == 'sub':  # Atribui à rd a soma de rs e rt // rd←rs-rt
            rd = int(eq[0])
            rs = int(eq[1])
            rt = int(eq[2])
            self.reg[rd] = self.reg[rs] - self.reg[rt]
            self.sp -= 1
            self.mem[self.sp] = self.reg[rd]
        elif self.opcode == 'subi':  # Atribui à rd a subtração entre rs e um valor imediato
            rd = int(eq[0])
            rs = int(eq[1])
            vimm = int(eq[2])
            self.reg[rd] = self.reg[rs] - vimm
            self.sp -= 1
            self.mem[self.sp] = self.reg[rd]
        elif self.opcode == 'mul':  # Atribui à rd o produto entre rs e rt // rd←rs*rt
            rd = int(eq[0])
            rs = int(eq[1])
            rt = int(eq[2])
            self.reg[rd] = self.reg[rs] * self.reg[rt]
            self.sp -= 1
            self.mem[self.sp] = self.reg[rd]
        elif self.opcode == 'div':  # Atribui à rd o quociente da divisão de rs por rt // rd←rs div rt
            rd = int(eq[0])
            rs = int(eq[1])
            rt = int(eq[2])
            if rt != 0:
                self.reg[rd] = int(self.reg[rs] / self.reg[rt])
                self.sp -= 1
                self.mem[self.sp] = self.reg[rd]

        # Desvios
        elif self.opcode == 'blt':  # Salta caso rs seja maior que rt // Se rs < rt então pc←vimm
            rs = int(eq[0])
            rt = int(eq[1])
            vimm = int(eq[2])
            if self.reg[rs] > self.reg[rt]:
                self.pc = vimm
            else:
                self.pc += vimm

        elif self.opcode == 'bgt':  # Salta caso rs seja menor que rt // Se rs > rt então pc←vimm
            rs = int(eq[0])
            rt = int(eq[1])
            vimm = int(eq[2])
            if self.reg[rs] < self.reg[rt]:
                self.pc = vimm
            else:
                self.pc += vimm
        elif self.opcode == 'beq':  # Salta caso rs e rt sejam iguais // Se rs = rt então pc←vimm
            rs = int(eq[0])
            rt = int(eq[1])
            vimm = int(eq[2])
            if self.reg[rs] == self.reg[rt]:
                self.pc = vimm
            else:
                self.pc += vimm
        elif self.opcode == 'j':  # Salto incondicional // pc ←vimm
            self.pc += int(eq[0])
        elif self.opcode == 'jr':  # Salto incondicional para um endereço no registrador // pc ← rd
            self.pc += eq[0]
        elif self.opcode == 'jal':  # Salto incondicional com armazenamento de endereço de retorno // ra ← pc+1 e pc ← vimm
            vimm = int(eq[1])
            self.ra = self.pc + 1
            self.pc += vimm

        # Memória
        elif self.opcode == 'lw':  # Carrega da memória para o registrador rd // rd ←M[vimm+rs]
            rd = int(eq[0])
            vimm = int(eq[1].split("(")[0])
            rs = int(eq[1].split("(")[1].replace(")", ""))

            addr = rs + vimm
            self.reg[rd] = self.mem[addr]
            self.sp -= 1
            self.mem[self.sp] = self.reg[rd]
        elif self.opcode == 'sw':  # Armazena o valor de rs na memória // M[vimm+rt] ←rs
            rs = int(eq[0])
            vimm = int(eq[1].split("(")[0])
            rt = int(eq[1].split("(")[1].replace(")", ""))

            addr = rt + vimm
            self.mem[addr] = rs

        # Movimentação
        elif self.opcode == 'mov':  # Movimentação de registrador para registrador // rd ← rs
            rd = int(eq[0])
            rs = int(eq[1])
            self.reg[rd] = self.reg[rs]
            self.sp -= 1
            self.mem[self.sp] = self.reg[rd]
        elif self.opcode == 'movi':  # Movimentação de imediato para registrador // rd ←vimm
            rd = int(eq[0])
            vimm = int(eq[1])
            self.reg[rd] = vimm
            self.sp -= 1
            self.mem[self.sp] = self.reg[rd]

        elif self.opcode == 'backup':
            rd = int(eq[0])
            self.reg[rd] = self.mem[self.sp]
            self.sp += 1

        # incrementa o PC para apontar para a próxima instrução
        else:
            print(f"opcode desconhecido {self.opcode}")
            self.opcode -= 1

    def run(self):
        while 0 <= self.pc < len(self.instrucoes):
            self.execute()
            self.mostra_registro()
            # self.mostra_memoria(0, self.tam_mem)

    def mostra_registro(self):
        # exibe o estado atual dos registradores
        print(f"PC: {self.pc}  SP: {self.sp}  RA: {self.ra}")
        for i in range(len(self.reg)):
            print(f"r{i} : {self.reg[i]}")
        print("\n")

    def mostra_memoria(self, start, end):
        # exibe o estado atual da memória
        for i in range(start, end):
            print(f"{i}: {self.mem[i]}")


if __name__ == "__main__":
    processador = Processador('add_mov.txt', 2048)
    processador.run()
