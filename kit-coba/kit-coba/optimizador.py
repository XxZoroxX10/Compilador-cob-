# -*- coding: utf-8 -*-
# optimizador.py — Versión compacta corregida

class Optimizador:
    def __init__(self):
        self.original = []
        self.cuadruplos = []
        self.estadisticas = {'plegado': 0, 'subexp': 0, 'muerto': 0}

    def optimizar(self, cuadruplos):
        self.original = cuadruplos.copy()
        self.cuadruplos = []
        vistos = {}

        # Primera pasada: optimizaciones
        for op, arg1, arg2, res in cuadruplos:
            # 1. Plegado de constantes
            if op in '+-*/' and isinstance(arg1, (int, float)) and isinstance(arg2, (int, float)):
                try:
                    val = eval(f"{arg1}{op}{arg2}")
                    self.cuadruplos.append(('=', val, '_', res))
                    self.estadisticas['plegado'] += 1
                    continue
                except:
                    pass

            # 2. Subexpresiones comunes - SOLO para aritméticas
            if op in '+-*/':
                clave = (op, arg1, arg2)
                if clave in vistos:
                    self.cuadruplos.append(('=', vistos[clave], '_', res))
                    self.estadisticas['subexp'] += 1
                    continue
                else:
                    vistos[clave] = res

            self.cuadruplos.append((op, arg1, arg2, res))

        # 3. Eliminar código muerto
        usados = set()
        for op, arg1, arg2, res in self.cuadruplos:
            # NO eliminar gotoF, label, if, goto, print
            if op not in ['label', 'if', 'goto', 'gotoF', 'print']:
                if arg1 and arg1 != '_':
                    usados.add(arg1)
                if arg2 and arg2 != '_':
                    usados.add(arg2)
            # 🔴 NUEVO: Si es una comparación, el resultado se usa en gotoF
            if op in ['>', '<', '>=', '<=', '==', '!=']:
                usados.add(res)

        antes = len(self.cuadruplos)
        self.cuadruplos = [
            c for c in self.cuadruplos
            if c[0] in ['print', 'if', 'goto', 'label', 'gotoF'] or c[3] in usados
        ]
        self.estadisticas['muerto'] += antes - len(self.cuadruplos)

        return self.cuadruplos

    def imprimir_cuadruplos(self, titulo="Cuádruplos"):
        print(f"\n  {titulo}:")
        if not self.cuadruplos:
            print("    (No hay cuádruplos)")
            return
        for i, (op, arg1, arg2, res) in enumerate(self.cuadruplos, 1):
            print(f"    {i:3}  ({op}, {arg1}, {arg2}, {res})")

    def reportar(self):
        print(f"\n   Resumen:")
        print(f"    Originales: {len(self.original)} → Optimizados: {len(self.cuadruplos)}")
        print(f"    Ahorro: {len(self.original) - len(self.cuadruplos)} instrucciones")
        for k, v in self.estadisticas.items():
            if v > 0:
                print(f"    • {k}: {v}")