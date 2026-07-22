# -*- coding: utf-8 -*-
# ================================================================
#  lexer_coba.py — Analizador lexico de Coba (PLY)
#  Lenguajes y Automatas II · Kit de arranque (Hito 0)
#
#  Este archivo convierte el codigo fuente de Coba en una lista
#  de tokens. Es la primera fase del compilador.
#
#  Tiene 2 TODO que debes completar (busca "TODO-1" y "TODO-2").
# ================================================================

import ply.lex as lex

# ----------------------------------------------------------------
# 1) Palabras reservadas
#    Se detectan dentro de t_ID: si el identificador leido esta en
#    este diccionario, se le cambia el tipo al token correspondiente.
# ----------------------------------------------------------------
reservadas = {
    'programa': 'PROGRAMA',
    'entero':   'ENTERO',
    'real':     'REAL',
    'inicio':   'INICIO',
    'fin':      'FIN',
    'si':       'SI',
    'sino': 'SINO',# AGREGADO: Palabra reservada para el 'else' del condicional-------
    # ============================================================
    # TODO-1 (Hito 0): agrega la palabra reservada 'sino'.
    #   Su token debe llamarse SINO.
    #   Pista: sigue el mismo patron que 'si' (una linea).
    # ============================================================
    'mientras': 'MIENTRAS',
    'imprime':  'IMPRIME',
}

# ----------------------------------------------------------------
# 2) Lista de tokens
#    PLY exige declarar aqui TODOS los tokens que el lexer produce.
# ----------------------------------------------------------------
tokens = [
    'ID', 'NUM_ENTERO', 'NUM_REAL',
    'MAS', 'MENOS', 'POR',
     'DIV',# AGREGADO: Token para el operador de división--------------------- '/'
    # ============================================================
    # TODO-2a (Hito 0): agrega aqui el token 'DIV'
    #   (la mitad 1 de 2 del operador de division).
    # ============================================================
    'ASIGNA',
    'MAYOR', 'MENOR', 'MAYORIGUAL', 'MENORIGUAL',
    'IGUALIGUAL', 'DIFERENTE',
    'PARIZQ', 'PARDER', 'LLAVEIZQ', 'LLAVEDER',
    'PUNTOYCOMA', 'COMA',
] + list(reservadas.values())

# ----------------------------------------------------------------
# 3) Reglas simples (un token = una expresion regular)
#    Nota: PLY prueba primero las regex mas largas, por eso '>='
#    gana sobre '>' aunque este despues.
# ----------------------------------------------------------------
t_MAS        = r'\+'
t_MENOS      = r'-'
t_POR        = r'\*'
# ================================================================
# TODO-2b (Hito 0): define la regla del token DIV para el
#   operador '/' (la mitad 2 de 2).
#   Pista: mira como estan definidos t_MAS y t_POR. Recuerda que
#   en una expresion regular algunos caracteres se escapan con \
#   ... aunque '/' en particular no lo necesita.
# ================================================================
t_MAYORIGUAL = r'>='
t_MENORIGUAL = r'<='
t_IGUALIGUAL = r'=='
t_DIFERENTE  = r'!='
t_DIV = r'/'# AGREGADO: Reconoce el operador de división-------------------
t_ASIGNA     = r'='
t_MAYOR      = r'>'
t_MENOR      = r'<'
t_PARIZQ     = r'\('
t_PARDER     = r'\)'
t_LLAVEIZQ   = r'\{'
t_LLAVEDER   = r'\}'
t_PUNTOYCOMA = r';'
t_COMA       = r','

# ----------------------------------------------------------------
# 4) Reglas con funcion (cuando hay que transformar el valor)
#    El orden importa: NUM_REAL va antes que NUM_ENTERO para que
#    "3.14" no se lea como el entero 3 seguido de ".14".
# ----------------------------------------------------------------

def t_NUM_REAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_NUM_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # Si la palabra esta reservada, el token cambia de tipo.
    t.type = reservadas.get(t.value, 'ID')
    return t

# ----------------------------------------------------------------
# 5) Cosas que se ignoran: comentarios, espacios y saltos de linea
# ----------------------------------------------------------------

def t_COMENTARIO(t):
    r'\#.*'
    pass  # no regresa token: el comentario desaparece

def t_nueva_linea(t):
    r'\n+'
    t.lexer.lineno += len(t.value)  # llevar la cuenta de lineas

t_ignore = ' \t'

# ----------------------------------------------------------------
# 6) Manejo de errores lexicos
# ----------------------------------------------------------------

def t_error(t):
    print("[Lexico] Caracter ilegal '%s' en la linea %d" % (t.value[0], t.lexer.lineno))
    t.lexer.skip(1)

# ----------------------------------------------------------------
# 7) Construir el lexer
# ----------------------------------------------------------------
lexer = lex.lex()
