# Roadmap

Ideas evaluadas y pendientes de implementar, con análisis de tradeoff.

## Fase 1 — Completada

- [x] 4 agentes especializados (orquestador, investigador, ejecutor, revisor)
- [x] Delegación por subproceso con `-z/--oneshot`
- [x] Wrappers slim con `--toolsets` restringidos
- [x] SOUL.md específicos por rol
- [x] Auditoría de costos por delegación
- [x] Presupuesto explícito en el revisor
- [x] Validación en 2 dominios (programación, ciencias sociales)
- [x] Ciclo cerrado revisor → ejecutor → revisor

## Fase 2 — Modelos por agente ✅ COMPLETADA (2026-10-13)

**Modelos finales:**
- orquestador: `deepseek-chat`
- investigador: `deepseek-chat`
- ejecutor: `deepseek-reasoner`
- revisor: `deepseek-chat`
- revisor-deep: `deepseek-reasoner` (perfil nuevo)

**Hallazgos:** documentados en README.md (sección "Hallazgos de Fase 2").

## Fase 2.5 — Evaluar migración de investigador a reasoner

**Estado:** Pendiente
**Impacto:** Desconocido
**Esfuerzo:** Bajo (1 comando + 1 pipeline de prueba)

**Hipótesis:** el investigador con reasoner podría producir síntesis más
profundas, pero su rol es leer y citar, no razonar. Probablemente no vale
la pena el costo extra.

**Criterio de decisión:**
- Si mejora la calidad de citas y síntesis: migrar
- Si solo encarece sin mejorar: dejar en chat


## Fase 3 — Agente planificador

**Estado:** Pendiente
**Impacto:** Alto en tareas complejas, nulo en tareas simples
**Esfuerzo:** Medio

Descompone tareas en subtareas antes de delegar. Vale la pena solo para
tareas con 3+ pasos interdependientes.

## Fase 4 — Worktree para agentes paralelos

**Estado:** Pendiente
**Impacto:** Alto si las tareas tocan el mismo repo
**Esfuerzo:** Bajo

Usar `hermes -w` para correr agentes en paralelo sin colisiones de git.

## Fase 5 — Skills preload por agente

**Estado:** Pendiente
**Impacto:** Medio
**Esfuerzo:** Bajo

Preload de skills específicas por perfil con `--skills`.

## Fase 6 — Exploración MCP / A2A

**Estado:** Pendiente (solo si aparece la necesidad)
**Impacto:** Medio-bajo con el setup actual
**Esfuerzo:** Alto

MCP permitiría tools externas estandarizadas. A2A sería comunicación
bidireccional entre agentes — ya cubierto por subprocesos.

## Fase 7 — Hermes kanban

**Estado:** Pendiente
**Impacto:** Medio
**Esfuerzo:** Bajo

Tablero multi-perfil nativo de Hermes para coordinación visual.
