# vm_pila.py
class MaquinaPila:
    def __init__(self):
        self.pila = []
        self.memoria = {}
        self.pc = 0
        self.codigo = []

    def ejecutar(self, programa):
        self.codigo = programa
        self.pc = 0
        self.pila = []
        self.memoria = {}
        
        while self.pc < len(self.codigo):
            instr = self.codigo[self.pc]
            op = instr[0]
            arg = instr[1] if len(instr) > 1 else None
            
            if op == "PUSH":
                self.pila.append(arg)
            elif op == "LOAD":
                self.pila.append(self.memoria.get(arg, 0))
            elif op == "STORE":
                self.memoria[arg] = self.pila.pop()
            elif op == "ADD":
                b = self.pila.pop()
                a = self.pila.pop()
                self.pila.append(a + b)
            elif op == "SUB":
                b = self.pila.pop()
                a = self.pila.pop()
                self.pila.append(a - b)
            elif op == "MUL":
                b = self.pila.pop()
                a = self.pila.pop()
                self.pila.append(a * b)
            elif op == "DIV":
                b = self.pila.pop()
                a = self.pila.pop()
                if b != 0:
                    self.pila.append(a / b)
                else:
                    print("⚠️ División por cero")
                    self.pila.append(0)
            elif op == "PRINT":
                print(self.pila.pop())
            
            # === COMPARACIONES ===
            elif op == "GT":
                b = self.pila.pop()
                a = self.pila.pop()
                self.pila.append(1 if a > b else 0)
            elif op == "LT":
                b = self.pila.pop()
                a = self.pila.pop()
                self.pila.append(1 if a < b else 0)
            elif op == "GE":
                b = self.pila.pop()
                a = self.pila.pop()
                self.pila.append(1 if a >= b else 0)
            elif op == "LE":
                b = self.pila.pop()
                a = self.pila.pop()
                self.pila.append(1 if a <= b else 0)
            elif op == "EQ":
                b = self.pila.pop()
                a = self.pila.pop()
                self.pila.append(1 if a == b else 0)
            elif op == "NE":
                b = self.pila.pop()
                a = self.pila.pop()
                self.pila.append(1 if a != b else 0)
            
            # === SALTOS ===
            elif op == "LABEL":
                pass
            elif op == "GOTO":
                self._saltar_a(arg)
                continue
            elif op == "GOTOF":
                cond = self.pila.pop()
                if cond == 0:
                    self._saltar_a(arg)
                    continue
            
            else:
                print(f"⚠️ Instrucción desconocida: {op}")
            
            self.pc += 1
    
    def _saltar_a(self, etiqueta):
        for i, instr in enumerate(self.codigo):
            if instr[0] == "LABEL" and instr[1] == etiqueta:
                self.pc = i
                return
        print(f"⚠️ Etiqueta no encontrada: {etiqueta}")