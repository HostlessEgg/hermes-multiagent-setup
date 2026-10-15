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

