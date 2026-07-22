# generador.py
# Generador de cuádruplos para Cobá

contador_temp = 0
contador_etiqueta = 0
cuadruplos = []

def nuevo_temp():
    global contador_temp
    contador_temp += 1
    return "t" + str(contador_temp)

def nueva_etiqueta():
    global contador_etiqueta
    contador_etiqueta += 1
    return "L" + str(contador_etiqueta)

def emitir(op, arg1, arg2, res):
    cuadruplos.append((op, arg1, arg2, res))

# ------------------ Expresiones ------------------

def gen_expr(nodo):
    """
    Genera cuádruplos para una expresión.
    """
    # Si es string (nombre de variable)
    if isinstance(nodo, str):
        return nodo
    
    # Si es None
    if nodo is None:
        return "_"
    
    # Constante numérica
    if nodo[0] == "num":
        return nodo[1]
    
    # Variable
    if nodo[0] == "id":
        return nodo[1]
    
    # 🔴 COMPARACIONES: ("rel", op, izq, der)
    if nodo[0] == "rel":
        izq = gen_expr(nodo[2])
        der = gen_expr(nodo[3])
        t = nuevo_temp()
        # 🔴 CORREGIDO: emitir con el operador real (>, <, <=, etc.)
        emitir(nodo[1], izq, der, t)
        return t
    
    # Operaciones aritméticas: ("+", izq, der)
    izq = gen_expr(nodo[1])
    der = gen_expr(nodo[2])
    t = nuevo_temp()
    emitir(nodo[0], izq, der, t)
    return t

# ------------------ Instrucciones ------------------

def gen_asignacion(nodo):
    lugar = gen_expr(nodo[2])
    emitir("=", lugar, "_", nodo[1])

def gen_imprime(nodo):
    valor = gen_expr(nodo[1])
    emitir("print", valor, "_", "_")

def gen_si(nodo):
    cond = gen_expr(nodo[1])
    L1 = nueva_etiqueta()
    L2 = nueva_etiqueta()
    emitir("gotoF", cond, "_", L1)
    gen_bloque(nodo[2])
    emitir("goto", "_", "_", L2)
    emitir("label", "_", "_", L1)
    if len(nodo) > 3 and nodo[3] is not None:
        gen_bloque(nodo[3])
    emitir("label", "_", "_", L2)

def gen_mientras(nodo):
    L1 = nueva_etiqueta()
    L2 = nueva_etiqueta()
    emitir("label", "_", "_", L1)
    cond = gen_expr(nodo[1])
    emitir("gotoF", cond, "_", L2)
    gen_bloque(nodo[2])
    emitir("goto", "_", "_", L1)
    emitir("label", "_", "_", L2)

# ------------------ Bloques ------------------

def gen_bloque(lista_nodos):
    for n in lista_nodos:
        if n is None:
            continue
        if isinstance(n, str):
            continue
        if n[0] == "asigna":
            gen_asignacion(n)
        elif n[0] == "imprime":
            gen_imprime(n)
        elif n[0] == "si":
            gen_si(n)
        elif n[0] == "mientras":
            gen_mientras(n)

# ------------------ Salida ------------------

def imprimir_cuadruplos():
    for i, (op, arg1, arg2, res) in enumerate(cuadruplos, start=1):
        print(f"{i:2}  ({op}, {arg1}, {arg2}, {res})")