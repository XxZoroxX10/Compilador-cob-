# -*- coding: utf-8 -*-
# ================================================================
#  semantico_coba.py — Análisis semántico de Cobá (Hito 1)
#  Lenguajes y Autómatas II
#
#  Funciones:
#   - Tabla de símbolos (insertar y buscar variables)
#   - Verificación de tipos en expresiones y asignaciones
#   - Detección de errores semánticos:
#       * Variable no declarada
#       * Redeclaración
#       * Asignación incompatible
#       * Operaciones con tipos incompatibles
# ================================================================

class TablaSimbolos:
    def __init__(self):
        self.tabla = {}
        self.direccion_actual = 0

    def insertar(self, nombre, tipo, linea):
        if nombre in self.tabla:
            print(f"[Semántico] Error: variable '{nombre}' redeclarada (línea {linea})")
            return False
        self.tabla[nombre] = {
            "tipo": tipo,
            "direccion": self.direccion_actual
        }
        self.direccion_actual += 1
        return True

    def buscar(self, nombre, linea):
        if nombre not in self.tabla:
            print(f"[Semántico] Error: variable '{nombre}' usada sin declarar (línea {linea})")
            return None
        return self.tabla[nombre]


# ---------------------------------------------------------------
# Verificación de tipos según las reglas de Cobá
# ---------------------------------------------------------------
def verificar_tipos(op, izq, der, linea):
    t1, t2 = izq["tipo"], der["tipo"]

    # Coerción implícita: entero + real → real
    if (t1, t2) in [("entero", "real"), ("real", "entero")]:
        return {"tipo": "real"}

    # Operaciones aritméticas
    if op in ["+", "-", "*"]:
        if t1 == "entero" and t2 == "entero":
            return {"tipo": "entero"}
        elif t1 == "real" or t2 == "real":
            return {"tipo": "real"}

    # División: siempre produce real si hay enteros
    if op == "/":
        if t1 in ["entero", "real"] and t2 in ["entero", "real"]:
            return {"tipo": "real"}

    # Comparaciones → Booleano
    if op in ["<", ">", "<=", ">=", "==", "!="]:
        if t1 in ["entero", "real"] and t2 in ["entero", "real"]:
            return {"tipo": "booleano"}

    # Booleanos con y/o → Booleano
    if op in ["y", "o"] and t1 == "booleano" and t2 == "booleano":
        return {"tipo": "booleano"}

    # Error
    print(f"[Semántico] Error: operación incompatible {t1} {op} {t2} (línea {linea})")
    return {"tipo": "error"}


# ---------------------------------------------------------------
# Evaluación de expresiones para obtener tipos
# ---------------------------------------------------------------
def evaluar_expresion(expr, tabla):
    if expr[0] == "num":
        return "entero" if isinstance(expr[1], int) else "real"
    elif expr[0] == "id":
        var = tabla.buscar(expr[1], linea=0)
        return var["tipo"] if var else "error"
    elif expr[0] in ["+", "-", "*", "/"]:
        t_izq = evaluar_expresion(expr[1], tabla)
        t_der = evaluar_expresion(expr[2], tabla)
        return verificar_tipos(expr[0], {"tipo": t_izq}, {"tipo": t_der}, linea=0)["tipo"]
    elif expr[0] == "rel":
        t_izq = evaluar_expresion(expr[2], tabla)
        t_der = evaluar_expresion(expr[3], tabla)
        return verificar_tipos(expr[1], {"tipo": t_izq}, {"tipo": t_der}, linea=0)["tipo"]
    else:
        return "error"


# ---------------------------------------------------------------
# Recorrido del AST para análisis semántico
# ---------------------------------------------------------------
def analizar_semantico(arbol):
    tabla = TablaSimbolos()
    _, nombre_prog, declaraciones, enunciados = arbol

    # Procesar declaraciones
    for decl in declaraciones:
        tipo, ids = decl[1], decl[2]
        for var in ids:
            tabla.insertar(var, tipo, linea=0)

    # Procesar enunciados
    for enun in enunciados:
        if enun[0] == "asigna":
            var = tabla.buscar(enun[1], linea=0)
            expr = enun[2]
            tipo_expr = evaluar_expresion(expr, tabla)
            if var and var["tipo"] != tipo_expr:
                print(f"[Semántico] Error: asignación incompatible {var['tipo']} ← {tipo_expr}")
