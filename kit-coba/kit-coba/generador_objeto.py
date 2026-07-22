# generador_objeto.py
def subir(operando):
    if isinstance(operando, (int, float)):
        return [("PUSH", operando)]
    elif operando != "_" and operando is not None:
        return [("LOAD", operando)]
    return []

def traducir_cuadruplo(op, arg1, arg2, res):
    instrucciones = []
    
    # === OPERACIONES ARITMÉTICAS ===
    if op in ['+', '-', '*', '/']:
        instrucciones += subir(arg1)
        instrucciones += subir(arg2)
        if op == '+': instrucciones.append(("ADD",))
        elif op == '-': instrucciones.append(("SUB",))
        elif op == '*': instrucciones.append(("MUL",))
        elif op == '/': instrucciones.append(("DIV",))
        instrucciones.append(("STORE", res))
    
    # === ASIGNACIÓN ===
    elif op == '=':
        instrucciones += subir(arg1)
        instrucciones.append(("STORE", res))
    
    # === IMPRESIÓN ===
    elif op == 'print':
        instrucciones += subir(arg1)
        instrucciones.append(("PRINT",))
    
    # === COMPARACIONES ===
    elif op in ['>', '<', '>=', '<=', '==', '!=']:
        instrucciones += subir(arg1)
        instrucciones += subir(arg2)
        if op == '>': instrucciones.append(("GT",))
        elif op == '<': instrucciones.append(("LT",))
        elif op == '>=': instrucciones.append(("GE",))
        elif op == '<=': instrucciones.append(("LE",))
        elif op == '==': instrucciones.append(("EQ",))
        elif op == '!=': instrucciones.append(("NE",))
        instrucciones.append(("STORE", res))
    
    # === ETIQUETA ===
    elif op == 'label':
        # 🔴 USAR res (la etiqueta está en res)
        instrucciones.append(("LABEL", res))
    
    # === SALTO INCONDICIONAL ===
    elif op == 'goto':
        # 🔴 USAR res (la etiqueta está en res)
        instrucciones.append(("GOTO", res))
    
    # === SALTO SI FALSO ===
    elif op == 'gotoF':
        instrucciones += subir(arg1)
        instrucciones.append(("GOTOF", res))
    
    return instrucciones

def generar_objeto(cuadruplos):
    programa = []
    for op, arg1, arg2, res in cuadruplos:
        programa += traducir_cuadruplo(op, arg1, arg2, res)
    return programa