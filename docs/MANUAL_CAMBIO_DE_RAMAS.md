# MANUAL_CAMBIO_DE_RAMAS.md

# Manual de Procedimiento para Cambiar de Rama

**Proyecto:** Generador Automático de Crucigramas (GAC)

---

## Objetivo

Este procedimiento tiene como finalidad evitar la pérdida de trabajo al cambiar entre las ramas del proyecto (`main` y `guia-ia`).

**Regla de oro:**

> **Nunca cambiar de rama si existen cambios sin guardar.**

Antes de ejecutar `git switch` o `git checkout`, siempre verificar el estado del repositorio.

---

# Procedimiento General

## Paso 1. Verificar el estado del repositorio

Ejecutar:

```bash
git status
```

### Si aparece:

```text
nothing to commit, working tree clean
```

Se puede cambiar de rama con seguridad.

Ir al Paso 4.

---

### Si aparecen archivos modificados:

Ejemplo:

```text
modified:
    src/gac/generator.py
    docs/DECISIONES.md
```

No cambiar todavía de rama.

Continuar con el Paso 2.

---

# Paso 2. Decidir cómo guardar el trabajo

Existen dos opciones.

## Opción A (Recomendada)

El trabajo ya está terminado.

Guardar definitivamente.

```bash
git add .
git commit -m "Descripción clara del avance"
```

Ejemplo:

```bash
git commit -m "ETAPA 3: agregar sistema de métricas"
```

Después verificar nuevamente:

```bash
git status
```

Debe indicar:

```text
nothing to commit, working tree clean
```

---

## Opción B

El trabajo todavía está en proceso.

Guardar temporalmente mediante **stash**.

```bash
git stash push -m "Descripción temporal"
```

Ejemplo:

```bash
git stash push -m "Avances en métricas antes de revisar guia-ia"
```

Verificar:

```bash
git status
```

Debe quedar limpio.

---

# Paso 3. Cambiar de rama

Para ir a la rama principal:

```bash
git switch main
```

Para ir a la rama experimental:

```bash
git switch guia-ia
```

Comprobar:

```bash
git status
```

Debe indicar la rama correcta y un árbol limpio.

---

# Paso 4. Recuperar un trabajo guardado con Stash

Consultar los trabajos almacenados:

```bash
git stash list
```

Ejemplo:

```text
stash@{0}: On main: Avances en métricas
```

Recuperar el más reciente:

```bash
git stash pop
```

Verificar nuevamente:

```bash
git status
```

Los archivos modificados volverán a aparecer.

---

# Uso de git push

## ¿Cuándo utilizarlo?

Utilizar únicamente cuando se desea enviar los commits al repositorio remoto.

```bash
git push
```

## ¿Cuándo NO es obligatorio?

Si únicamente se desea cambiar de rama y continuar trabajando localmente.

En ese caso basta con:

* git add
* git commit

No es necesario hacer `git push`.

---

# Flujo de trabajo recomendado

## Cambiar de main hacia guia-ia

```text
git status
        │
        ▼
¿Hay cambios?

      Sí
       │
       ├── Trabajo terminado
       │       │
       │       ▼
       │   git add .
       │   git commit
       │
       └── Trabajo incompleto
               │
               ▼
          git stash

        ▼
git switch guia-ia
```

---

## Regresar desde guia-ia hacia main

```text
git status
        │
        ▼
¿Hay cambios?

      Sí
       │
       ▼
git add .
git commit

        ▼
git switch main

        ▼
git stash list

        ▼
git stash pop
```

---

# Buenas prácticas

* Hacer commits pequeños y frecuentes.
* Escribir mensajes descriptivos.
* No mezclar varias funcionalidades en un mismo commit.
* No hacer `merge` sin revisar previamente los cambios.
* Mantener actualizado `ESTADO_DE_DESARROLLO.md`.
* Registrar las decisiones importantes en `DECISIONES.md`.
* Verificar siempre el resultado de `git status` antes y después de cambiar de rama.

---

# Regla Final

**Si existe alguna duda sobre el estado del repositorio, detenerse y ejecutar primero:**

```bash
git status
```

La mayoría de los problemas con Git pueden evitarse verificando el estado del repositorio antes de realizar cualquier otra operación.
