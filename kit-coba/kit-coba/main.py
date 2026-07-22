# -*- coding: utf-8 -*-
# ================================================================
#  main.py — Programa principal del compilador de Cobá
#  Lenguajes y Automatas II · Hito 4 (Unidad 4)
#
#  Uso:
#      python main.py ejemplos/ejemplo_basico.coba
#
#  Ejecuta las fases del compilador sobre el archivo indicado:
#    Fase 1: análisis léxico   -> imprime la lista de tokens
#    Fase 2: análisis sintáctico -> imprime el árbol del programa
#    Fase 3: análisis semántico -> tabla de símbolos y errores
#    Fase 4: código intermedio -> lista de cuádruplos
#    Fase 5: optimización -> optimización local y de ciclos
#    Fase 6: código objeto -> traducción a instrucciones de la VM
#    Fase 7: ejecución -> máquina virtual de pila
# ================================================================

import sys
from lexer_coba import lexer
from parser_coba import parser
from semantico_coba import analizar_semantico   # Fase 3
import generador                                # Fase 4
from optimizador import Optimizador             # Fase 5
import generador_objeto                         # Fase 6
import vm_pila                                  # Fase 7


def imprimir_arbol(nodo, nivel=0):
    """Imprime el árbol (tuplas anidadas) con sangría por nivel."""
    sangria = '    ' * nivel
    if nodo is None:
        return
    if isinstance(nodo, tuple):
        print(sangria + str(nodo[0]))
        for hijo in nodo[1:]:
            imprimir_arbol(hijo, nivel + 1)
    elif isinstance(nodo, list):
        for elemento in nodo:
            imprimir_arbol(elemento, nivel)
    else:
        print(sangria + repr(nodo))


def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <archivo.coba>")
        print("Ejemplo: python main.py ejemplos/ejemplo_basico.coba")
        return

    ruta = sys.argv[1]
    try:
        with open(ruta, encoding='utf-8') as f:
            codigo = f.read()
    except FileNotFoundError:
        print("No se encontró el archivo: %s" % ruta)
        return

    # ---------- Fase 1: análisis léxico ----------
    print("=" * 50)
    print("FASE 1: TOKENS")
    print("=" * 50)
    lexer.lineno = 1
    lexer.input(codigo)
    for tok in lexer:
        print("  línea %3d   %-12s %r" % (tok.lineno, tok.type, tok.value))

    # ---------- Fase 2: análisis sintáctico ----------
    print()
    print("=" * 50)
    print("FASE 2: ÁRBOL SINTÁCTICO")
    print("=" * 50)
    lexer.lineno = 1
    arbol = parser.parse(codigo, lexer=lexer)

    if arbol is None:
        print("  No se pudo construir el árbol (revisa los errores de arriba).")
        return

    imprimir_arbol(arbol)
    print()
    print("Listo: el programa es léxica y sintácticamente válido.")

    # ---------- Fase 3: análisis semántico ----------
    print()
    print("=" * 50)
    print("FASE 3: ANÁLISIS SEMÁNTICO")
    print("=" * 50)
    analizar_semantico(arbol)

    # ---------- Fase 4: generación de cuádruplos ----------
    print()
    print("=" * 50)
    print("FASE 4: CÓDIGO INTERMEDIO (CUÁDRUPLOS)")
    print("=" * 50)
    
    generador.temp_counter = 0
    generador.label_counter = 0
    generador.cuadruplos = []
    
    generador.gen_bloque(arbol[3])
    cuadruplos_original = generador.cuadruplos.copy()
    generador.imprimir_cuadruplos()

    # ---------- Fase 5: OPTIMIZACIÓN ----------
    print()
    print("=" * 50)
    print("FASE 5: OPTIMIZACIÓN LOCAL Y DE CICLOS")
    print("=" * 50)
    
    optimizador = Optimizador()
    cuadruplos_opt = optimizador.optimizar(cuadruplos_original)
    optimizador.imprimir_cuadruplos("Optimizados")
    optimizador.reportar()

    # ---------- Fase 6: CÓDIGO OBJETO ----------
    print()
    print("=" * 50)
    print("FASE 6: CÓDIGO OBJETO")
    print("=" * 50)
    programa_objeto = generador_objeto.generar_objeto(cuadruplos_opt)
    for i,instr in enumerate(programa_objeto):
        print(f"{i:3} {instr}")

    # ---------- Fase 7: EJECUCIÓN EN VM ----------
    print()
    print("=" * 50)
    print("FASE 7: EJECUCIÓN EN VM")
    print("=" * 50)
    vm = vm_pila.MaquinaPila()
    vm.ejecutar(programa_objeto)


if __name__ == '__main__':
    main()
