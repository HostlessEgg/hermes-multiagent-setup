# Lecciones aprendidas construyendo un sistema multi-agente sobre Hermes

## 1. `delegate_task` NO invoca perfiles

La herramienta `delegate_task` de Hermes lanza subagentes efímeros,
no invoca perfiles con nombre. Para delegar a otro perfil hay que
usar `--oneshot` (`-z`) vía subproceso.

**Implicación:** la orquestación real requiere wrappers de shell que
invoquen `hermes -p <perfil> -z "..."`.

## 2. `--toolsets` solo funciona con `-z` y `--tui`

Si intentas pasar `--toolsets` a subcomandos como `sessions`, el
parser falla. Los wrappers slim deben usarse solo con `-z` o `--tui`.

## 3. Los tool schemas dominan el costo

30 tools = 55 KB de schemas = ~14K tokens de peaje fijo. Restringir
con `--toolsets` es la optimización más grande disponible.

## 4. El caché de DeepSeek cambia la economía

Un SOUL.md de 400 tokens:
- Primera llamada: cuesta ~400 tokens
- Llamadas siguientes: ~40 tokens (cache read)

Invertir en SOUL.md estable es rentable.

## 5. Presupuesto explícito mejora calidad

Verificado empíricamente: el revisor con presupuesto de 90s encontró
un bug crítico que el revisor sin límite (211s) no detectó. La
restricción fuerza priorización.

## 6. Los agentes one-shot deben ser autosuficientes

Un subagente invocado con `-z` NO ve la conversación del orquestador.
Todo el contexto necesario debe ir en el prompt de delegación.

## 7. El formato de respuesta es contractual

Definir el formato exacto en el SOUL.md (RESULTADO / ARCHIVOS /
VERIFICACIÓN) produce outputs parseables. Sin formato explícito, los
agentes divagan.

## 8. Los roles requieren SOUL.md distintos

Sin SOUL.md específico, todos los perfiles son agentes generalistas
idénticos con diferente nombre. El comportamiento diferenciado emerge
del system prompt, no del nombre del perfil.

## 9. La instalación vía pipx/mise tiene particularidades

- `hermes doctor` da falsos positivos con "Venv entry point not found"
- `hermes tools post-setup` no encuentra el venv real
- Los paquetes lazy (ddgs) deben instalarse manualmente en el venv
  correcto (`~/.local/share/mise/installs/pipx-hermes-agent/<version>/hermes-agent/bin/python3`)

## 10. Los wrappers con `--toolsets` son la solución práctica

Los bugs de `platform_toolsets` en config.yaml se evitan usando
wrappers de shell que inyectan el flag en cada invocación.
