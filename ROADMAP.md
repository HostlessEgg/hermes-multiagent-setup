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

## Fase 2 — Modelos por agente

**Estado:** Pendiente
**Impacto:** Medio-alto
**Esfuerzo:** Bajo (1 comando por agente)

Cambiar los modelos según el rol:

| Agente | Modelo actual | Modelo sugerido | Razón |
|---|---|---|---|
| orquestador | deepseek-chat | deepseek-chat | Clasificar no requiere razonamiento profundo |
| investigador | deepseek-chat | deepseek-chat | Leer y sintetizar es suficiente |
| ejecutor | deepseek-chat | **deepseek-reasoner** | El razonamiento mejora la calidad del código |
| revisor | deepseek-chat | **deepseek-reasoner** | El razonamiento mejora la detección de bugs |

**Tradeoff:** `deepseek-reasoner` cuesta ~5-10× más por token. Pero produce
menos iteraciones porque razona mejor. El costo neto puede ser igual o menor
en tareas complejas.

**Plan:** Cambiar solo ejecutor y revisor, medir en 2-3 pipelines, decidir.

**Comando:**
```bash
hermes -p ejecutor config set model.default deepseek-reasoner
hermes -p revisor  config set model.default deepseek-reasoner
