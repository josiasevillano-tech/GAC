# DECISIONES.md

Proyecto: Generador Automático de Crucigramas (GAC)

Este documento registra las decisiones técnicas importantes tomadas durante el desarrollo del proyecto.

No pretende reemplazar la documentación de la arquitectura ni el historial de Git.

Su propósito es conservar el razonamiento detrás de las decisiones que afectan el diseño del sistema.

---

## 2026-07-22

### Decisión

Separar las heurísticas de `evaluate_candidate()`.

### Motivo

Permitir agregar nuevos criterios de evaluación sin modificar el algoritmo principal.

### Impacto

- `generator.py`
- Sistema de evaluación
- Facilita la incorporación de nuevas heurísticas.

---

## 2026-07-22

### Decisión

Reorganizar `generator.py` en secciones.

### Motivo

Reflejar el flujo lógico del algoritmo y facilitar el mantenimiento del código.

### Impacto

- Mayor legibilidad.
- Navegación más sencilla dentro del archivo.
- Base más estable para futuras ampliaciones.

---

## 2026-07-22

### Decisión

Eliminar la duplicidad en el cálculo de intersecciones.

### Motivo

Se identificó que dos métodos resolvían el mismo problema.

Mantener ambos aumentaba el mantenimiento y el riesgo de inconsistencias.

### Impacto

- Se conserva una única implementación.
- Menor complejidad del código.
- Mantenimiento más sencillo.

---

## 2026-07-25

### Decisión

Adoptar una estrategia de integración selectiva para los cambios desarrollados en ramas experimentales.

### Motivo

Durante el desarrollo se creó una rama experimental (`guia-ia`) para evaluar propuestas alternativas.

Se decidió que los cambios no serán incorporados mediante un `merge` automático, sino revisados individualmente antes de integrarse al proyecto principal.

### Impacto

- Mayor control sobre la evolución del proyecto.
- Se evita introducir cambios incompatibles.
- Cada incorporación queda justificada y documentada.

---

## Decisiones pendientes de evaluación

Las siguientes propuestas aún se encuentran bajo revisión y no forman parte oficialmente de la arquitectura del GAC.

### En evaluación

- Separación del sistema de métricas en un módulo independiente (`metrics.py`).
- Aleatorización del orden de palabras dentro de grupos de igual longitud.
- Sistema de experimentación mediante múltiples intentos (`experiments.py`).
- Evaluación ponderada de candidatos.
- Cambios en la organización de imports del proyecto.

Estas decisiones serán aceptadas, modificadas o descartadas después de su revisión técnica.
