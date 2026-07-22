# -*- coding: utf-8 -*-
# ================================================================
#  parser_coba.py — Analizador sintactico de Coba (PLY)
#  Lenguajes y Automatas II · Kit de arranque (Hito 0)
#
#  Este archivo toma los tokens del lexer y construye el ARBOL
#  del programa. Cada nodo del arbol es una tupla cuyo primer
#  elemento dice que tipo de nodo es. Ejemplos:
#
#     ('programa', nombre, [declaraciones], [enunciados])
#     ('decl', 'entero', ['a', 'b'])
#     ('asigna', 'x', expresion)
#     ('si', condicion, [bloque_verdadero], [bloque_sino] o None)
#     ('mientras', condicion, [bloque])
#     ('imprime', expresion)
#     ('+', izquierda, derecha)         <- operacion aritmetica
#     ('rel', '>', izquierda, derecha)  <- comparacion
#     ('id', 'x')                       <- uso de variable
#     ('num', 5)                        <- constante
#
#  Ese arbol es la entrada de TODAS las fases que construiras en
#  los siguientes hitos (semantico, cuadruplos, etc.).
#
#  Tiene 2 TODO que debes completar (busca "TODO-3" y "TODO-4").
# ================================================================

import ply.yacc as yacc
from lexer_coba import tokens  # el parser necesita conocer los tokens

# ----------------------------------------------------------------
# 1) El programa completo
# ----------------------------------------------------------------

def p_programa(p):
    'programa : PROGRAMA ID PUNTOYCOMA declaraciones INICIO enunciados FIN'
    p[0] = ('programa', p[2], p[4], p[6])

# ----------------------------------------------------------------
# 2) Declaraciones de variables
# ----------------------------------------------------------------

def p_declaraciones(p):
    '''declaraciones : declaracion declaraciones
                     | vacio'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_declaracion(p):
    'declaracion : tipo lista_ids PUNTOYCOMA'
    p[0] = ('decl', p[1], p[2])

def p_tipo(p):
    '''tipo : ENTERO
            | REAL'''
    p[0] = p[1]

def p_lista_ids(p):
    '''lista_ids : ID
                 | ID COMA lista_ids'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

# ----------------------------------------------------------------
# 3) Enunciados del cuerpo
# ----------------------------------------------------------------

def p_enunciados(p):
    '''enunciados : enunciado enunciados
                  | vacio'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_enunciado(p):
    '''enunciado : asignacion
                 | condicional
                 | ciclo
                 | impresion'''
    p[0] = p[1]

def p_asignacion(p):
    'asignacion : ID ASIGNA expresion PUNTOYCOMA'
    p[0] = ('asigna', p[1], p[3])

def p_condicional_si(p):
    'condicional : SI PARIZQ condicion PARDER LLAVEIZQ enunciados LLAVEDER'
    # El ultimo elemento (None) es el lugar del bloque 'sino',
    # que en esta version del condicional no existe.
    p[0] = ('si', p[3], p[6], None)

# ================================================================
# TODO-4 (Hito 0): agrega la regla del 'si ... sino ...'.
#   (Hazlo DESPUES de completar el TODO-1 del lexer, porque
#    necesita que exista el token SINO.)
#
#   La produccion completa es:
#
#   condicional : SI PARIZQ condicion PARDER LLAVEIZQ enunciados LLAVEDER SINO LLAVEIZQ enunciados LLAVEDER
#
#   y el nodo del arbol debe quedar asi:
#
#   p[0] = ('si', p[3], p[6], p[10])
#
#   Pistas:
#   - Copia la funcion p_condicional_si de arriba, renombrala
#     (por ejemplo p_condicional_si_sino) y ajusta la produccion.
#   - p[10] es el bloque de enunciados del sino (cuenta las piezas
#     de la produccion para convencerte).
#   - Al correr, yacc reportara "1 shift/reduce conflict". Es el
#     famoso conflicto del "sino colgante"; PLY lo resuelve solo y
#     correctamente. No es un error.
# ================================================================
def p_condicional_si_sino(p): #Esta función permite que el compilador reconozca y procese la estructura condicional con alternativa
    'condicional : SI PARIZQ condicion PARDER LLAVEIZQ enunciados LLAVEDER SINO LLAVEIZQ enunciados LLAVEDER'
    p[0] = ('si', p[3], p[6], p[10])
def p_ciclo(p):
    'ciclo : MIENTRAS PARIZQ condicion PARDER LLAVEIZQ enunciados LLAVEDER'
    p[0] = ('mientras', p[3], p[6])

def p_impresion(p):
    'impresion : IMPRIME PARIZQ expresion PARDER PUNTOYCOMA'
    p[0] = ('imprime', p[3])

# ----------------------------------------------------------------
# 4) Condiciones (comparaciones)
# ----------------------------------------------------------------

def p_condicion(p):
    'condicion : expresion oprel expresion'
    p[0] = ('rel', p[2], p[1], p[3])

def p_oprel(p):
    '''oprel : MAYOR
             | MENOR
             | MAYORIGUAL
             | MENORIGUAL
             | IGUALIGUAL
             | DIFERENTE'''
    p[0] = p[1]

# ----------------------------------------------------------------
# 5) Expresiones aritmeticas
#    La precedencia esta construida EN la gramatica:
#    expresion (+,-) llama a termino (*,/) que llama a factor.
#    Por eso * y / se evaluan antes que + y -.
# ----------------------------------------------------------------

def p_expresion(p):
    '''expresion : expresion MAS termino
                 | expresion MENOS termino
                 | termino'''
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])  # Crea nodo para + o -
    else:
        p[0] = p[1]  # Es un término, pasa tal cual

# ============================================================  <-- BIEN: fuera de p_expresion
# TODO-3 (Hito 0): agrega la alternativa de la division.
#   (Hazlo DESPUES de completar el TODO-2 del lexer, porque
#    necesita que exista el token DIV.)
#   Solo es agregar una linea a la produccion de arriba:
#
#       | termino DIV factor
#
#   El codigo de abajo ya no necesita cambios: funciona igual
#   para *, / o cualquier operador binario. # termino DIV factor RECONOCE el operador de divisió
# ============================================================
def p_termino(p):
    '''termino : termino POR factor 
               | termino DIV factor  
               | factor'''
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])  # Crea nodo para * o /
    else:
        p[0] = p[1]  # Es un factor, pasa tal cual
# --- FUNCIÓN 3: Factores (números, variables o paréntesis) ---
def p_factor(p):
    '''factor : PARIZQ expresion PARDER
              | ID
              | NUM_ENTERO
              | NUM_REAL'''
    if len(p) == 4:
        p[0] = p[2]                     # parentesis: regresa lo de adentro
    elif isinstance(p[1], str):
        p[0] = ('id', p[1])             # uso de una variable
    else:
        p[0] = ('num', p[1])            # constante numerica

# ----------------------------------------------------------------
# 6) Produccion vacia y manejo de errores
# ----------------------------------------------------------------

def p_vacio(p):
    'vacio :'
    p[0] = None

def p_error(p):
    if p:
        print("[Sintactico] Error cerca de '%s' (token %s) en la linea %d"
              % (p.value, p.type, p.lineno))
    else:
        print("[Sintactico] Error: el programa termino de forma inesperada "
              "(quiza falta 'fin' o una llave).")

# ----------------------------------------------------------------
# 7) Construir el parser
# ----------------------------------------------------------------
parser = yacc.yacc(debug=False)
