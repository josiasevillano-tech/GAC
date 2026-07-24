# PLAN DE DESARROLLO DEL GAC

Versión del proyecto: 0.4.0

Estado: EN DESARROLLO

---

# OBJETIVO GENERAL

Desarrollar un generador automático de crucigramas (GAC) capaz de construir crucigramas de alta calidad mediante heurísticas progresivamente más sofisticadas, manteniendo una arquitectura limpia, modular y fácilmente extensible.

---

# REGLAS DEL PROYECTO

1. Solo se desarrolla un objetivo a la vez.

2. Ningún objetivo se considera terminado hasta:
   - ejecutar correctamente el programa;
   - realizar commit;
   - actualizar GitHub.

3. Toda modificación importante debe reflejarse en la documentación.

4. Nunca se modifica código mediante cambios parciales.
   Siempre se reemplazan métodos o secciones completas.

5. La arquitectura gobierna el código.
   No al contrario.

---

# ESTADO ACTUAL

## Arquitectura

✔ Reorganización completa de Generator.

✔ Métodos agrupados por responsabilidad.

✔ Eliminación de duplicidad de heurísticas.

---

## Función de evaluación

✔ score_compactness()

✔ score_intersections()

✔ evaluate_candidate()

✔ Pesos configurables

---

# OBJETIVO ACTUAL

Construir el sistema de métricas del generador.

Este sistema deberá permitir medir objetivamente la calidad de un crucigrama generado.

---

# PLAN DE DESARROLLO

## ETAPA 1
Arquitectura
Estado: COMPLETADA

---

## ETAPA 2
Heurísticas básicas
Estado: COMPLETADA

---

## ETAPA 3
Sistema de métricas
Estado: PENDIENTE

Objetivos:

✅ Número de palabras colocadas.
✅ Número de cruces.
✅ Área ocupada.
✅ Mostrar resultados automáticamente al finalizar la generación.

---

## ETAPA 4
Optimización de la evaluación
Estado: COMPLETADA

Objetivos:

✅ Ajuste de pesos implementado (weight_compactness, weight_intersections).
✅ Comparación entre configuraciones realizada.
✅ Experimentos controlados ejecutados (10 intentos por configuración).

---

## ETAPA 5
Mejoras del algoritmo
Estado: PENDIENTE

Objetivos:

□ Múltiples intentos de generación.

□ Selección del mejor tablero.

□ Backtracking.

---

## ETAPA 6
Optimización avanzada
Estado: PENDIENTE

Objetivos:

□ Nuevas heurísticas.

□ Penalizaciones.

□ Optimización global.

---

## ETAPA 7
Versión 1.0
Estado: PENDIENTE

Objetivos:

□ Documentación final.

□ Limpieza del código.

□ Pruebas finales.

□ Publicación.

---

# PRÓXIMO PASO

Implementar el sistema de métricas del GAC.

No desarrollar ninguna otra funcionalidad hasta completar esta etapa.

---

# BITÁCORA

2026-07-22

✔ Arquitectura reorganizada.

✔ Función de evaluación basada en heurísticas.

✔ Pesos configurables implementados.

✔ Proyecto sincronizado con GitHub.

2026-07-24

✅ Sistema de métricas implementado.
✅ Clase Metrics con word_count, cross_count, bounding_area, density.
✅ Reporte automático al finalizar generación.
✅ Imports corregidos y configuración de VS Code actualizada.
✅ Commit y push a GitHub.

2026-07-24

✅ ETAPA 4 completada.
✅ Sistema de experimentos creado (experiments.py).
✅ Pesos configurables funcionan correctamente.
✅ Hallazgo: el algoritmo actual es determinístico, por lo que los pesos
   no producen variación con el mismo conjunto de palabras.
✅ Conclusión: la sensibilidad a pesos requerirá aleatoriedad en el algoritmo,
   lo cual se abordará en la ETAPA 5 (múltiples intentos y backtracking).