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

## Fase 5 — Skills preload por agente ✅ COMPLETADA (2026-10-16)

**Skills precargadas por perfil:**
- investigador: grounded-citations, arxiv, blocked-page-recovery
- ejecutor: test-driven-development, systematic-debugging, python-debugpy

**Skills condicionales (via SOUL.md del orquestador):**
- textual-tui-apps → solo cuando la tarea es de TUI/terminal UI

**Evidencia funcional:**
- TDD: test escrito antes de implementación, ciclo RED→GREEN real
- Grounded citations: 6 hallazgos con URLs primarias
- Textual TUI: confirmada la invocación con `--skills textual-tui-apps`

**Impacto:** +~2,200 tokens en cold start, ~0 en warm cache (amortizado por
el caché de DeepSeek).

**Documentación completa:** README.md, sección "Skills preload por agente".

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

## Fase 2.6 — Migrar a instalación soportada

**Estado:** Pendiente
**Impacto:** Alto (desbloquea extract, native fetch, keyless ring, bug fixes)
**Esfuerzo:** Medio (backup, reinstalación, verificación)

**Contexto:** la instalación actual vía pipx/mise está deprecada. `hermes update`
no actualiza el paquete principal (solo las dependencias). Para acceder a las
versiones nuevas con todas las funcionalidades hay que migrar a un método
soportado (instalador oficial, AUR, script de migración).

**Beneficios esperados:**
- `web_extract` funcionando (native fetch keyless)
- Keyless ring de extract providers (sin API keys)
- Fix del bug #73192
- Updates regulares

**Riesgo:** los perfiles actuales (orquestador, investigador, ejecutor, revisor,
revisor-deep) pueden requerir migración manual. Los SOUL.md y wrappers deberían
sobrevivir.

**Plan sugerido:**
1. Backup completo de `~/.hermes` y `~/.local/bin/hermes-slim`
2. Consultar la doc oficial de platform-support
3. Elegir el método (AUR o instalador oficial)
4. Migrar en un entorno de prueba si es posible
5. Verificar que los 5 perfiles funcionan
6. Restaurar SOUL.md si hicieron falta
