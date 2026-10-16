# Hermes Multi-Agent Setup

Sistema de 4 agentes especializados sobre Hermes Agent + DeepSeek,
diseñado para minimizar consumo de tokens y mejorar calidad vía
delegación por subproceso y roles diferenciados.

## Resultados medidos

| Métrica | Agente único | Pipeline 4 agentes | Delta |
|---|---|---|---|
| Costo tarea compleja | ~$0.008 | ~$0.010 | +25% |
| **Calidad de auditoría** | Superficial | **Encuentra bugs críticos** | — |
| Aislamiento de contexto | Contaminado | Limpio por agente | — |
| Trazabilidad de costos | Por sesión | Por delegación | — |

El pipeline cuesta ligeramente más que un agente único pero produce
auditorías 10× más rigurosas y mantiene el contexto del orquestador
limpio indefinidamente.

## Arquitectura

```
Usuario
  │
  └─→ orquestador (terminal+file)
        │
        ├─→ simple   → responde directo
        │
        └─→ complejo → ejecuta wrapper slim:
              │
              ├─→ investigador-slim (web)                    → hallazgos con URLs
              ├─→ ejecutor-slim (terminal,file,code_execution) → artefactos probados
              └─→ revisor-slim (file,terminal)               → auditoría con contraejemplos
```

Cada delegación corre en **contexto aislado**. El orquestador solo ve
el stdout final del subagente.

## Hallazgos de diseño

### 1. Presupuesto explícito MEJORA la calidad del output

Contraintuitivo pero verificado empíricamente. Añadimos al revisor:

> Tienes 90 segundos y ~15 llamadas a terminal máximo. Si una prueba
> se acerca a su límite, córtala.

| Métrica | Revisor sin presupuesto | Revisor con presupuesto |
|---|---|---|
| Costo | $0.0042 | $0.0032 (−23%) |
| Tiempo | 211s | ~110s (−48%) |
| Muestras pequeñas | 5,000,000 | 200,006 |
| Muestras grandes | 6,000 | 1,200 |
| **Hallazgos CRÍTICOS** | **0** | **1** |

El presupuesto forzó al revisor a **priorizar las pruebas más reveladoras**
(contraejemplo ejecutable) sobre las voluminosas pero redundantes
(millones de números pequeños). Encontró un bug real que el revisor
sin límite no detectó.

**Lección generalizable:** sin restricción, un agente LLM diluye su
esfuerzo. Con restricción, prioriza lo que más información aporta.

### 2. Los tool schemas son el 75% del costo

`hermes prompt-size` revela:
- System prompt: ~18.9 KB
- Tool schemas: ~55.9 KB (30 tools)
- Total: ~14K tokens de peaje fijo por invocación

Restringir con `--toolsets` baja esto a ~3-4K tokens.

### 3. El caché de DeepSeek es fundamental

El peaje fijo se paga una vez. Después, el 95% son cache reads a
~10% del costo normal. Inversiones en SOUL.md estable se amortizan.

### 4. Los SOUL.md específicos cambian el comportamiento

Sin SOUL.md específico, todos los perfiles son agentes generalistas
idénticos. El "contrato de rol" en el system prompt es lo que hace
que un revisor audite y un ejecutor ejecute.

## Modelos por agente

| Agente | Modelo | Rol | Costo típico |
|---|---|---|---|
| orquestador | `deepseek-chat` | Clasificar y delegar | ~$0.001 |
| investigador | `deepseek-chat` | Búsqueda web y síntesis | ~$0.0006 |
| ejecutor | `deepseek-reasoner` | Código y artefactos | ~$0.0025 |
| revisor | `deepseek-chat` | Auditoría rutinaria | ~$0.003 |
| revisor-deep | `deepseek-reasoner` | Auditoría crítica | ~$0.007 |

## Cuándo usar cada revisor

**revisor-slim (chat, económico):**
- Validar output de tareas simples
- Verificar formato o completitud
- Cuando el costo importa más que la exhaustividad

**revisor-deep-slim (reasoner, más caro):**
- Auditoría de código crítico o correctitud matemática
- Verificación empírica contra referencias independientes
- Tareas con seguridad, dinero o datos sensibles
- Máxima confianza en el veredicto

## Hallazgos de Fase 2

Comparación medida en el caso de primalidad.

### Ejecutor

| Métrica | chat | reasoner | Delta |
|---|---|---|---|
| input_tokens | 7,759 | 1,958 | **−75%** |
| output_tokens | 4,026 | 7,453 | +85% |
| reasoning_tokens | 0 | 1,956 | nuevo |
| costo | $0.00228 | $0.00250 | +10% |

**Conclusión:** mismo costo, artefactos más robustos, menos iteraciones.
El razonamiento previo ahorra input tokens.

### Revisor

| Métrica | chat | reasoner | Delta |
|---|---|---|---|
| input_tokens | 10,091 | 11,338 | +12% |
| output_tokens | 5,307 | 17,156 | +223% |
| reasoning_tokens | 0 | 10,748 | nuevo |
| costo | $0.00324 | $0.00678 | +109% |

**Conclusión:** el doble de costo, 10× más verificación (2M casos vs 200K).
Encontró un error conceptual que el chat no detectó: identificó correctamente
que `3317044064679887385961981` es el menor pseudoprimo fuerte de las **13**
bases {2..41}, mientras el chat afirmó erróneamente que era de las **12**
bases {2..37}. Esa corrección justifica el costo extra para auditorías críticas.

## Tool calling en deepseek-reasoner

Verificado en Hermes v0.19.0: `deepseek-reasoner` soporta function calling
completo. El ejecutor y el revisor-deep usan `terminal`, `file` y
`code_execution` sin problemas. `reasoning_tokens` varía entre 0 (tareas
triviales) y 10,748 (auditorías complejas).

## Prerrequisitos

- Arch Linux (u otra distro con systemd)
- Hermes Agent v0.19.0+
- Cuenta de DeepSeek con API key
- `jq` (`sudo pacman -S jq`)
- `~/.local/bin` en PATH
- `uv` instalado

## Instalación

### 1. Crear perfiles

```bash
hermes profile create orquestador  --description "Clasifica y delega"
hermes profile create investigador --description "Busca y sintetiza"
hermes profile create ejecutor     --description "Ejecuta y entrega artefactos"
hermes profile create revisor      --description "Audita y encuentra bugs"
```

### 2. Configurar credenciales

Configura el `.env` del orquestador con tu DeepSeek API key:

```bash
nano ~/.hermes/profiles/orquestador/.env
# Añadir: DEEPSEEK_API_KEY=sk-...
```

Copiar a los demás perfiles:

```bash
for p in ejecutor investigador revisor; do
  cp ~/.hermes/profiles/orquestador/.env ~/.hermes/profiles/$p/.env
done
```

### 3. Fijar modelo

```bash
for p in orquestador ejecutor investigador revisor; do
  hermes -p $p config set model.provider deepseek
  hermes -p $p config set model.default deepseek-chat
done
```

### 4. Optimizar prompts

```bash
for p in orquestador ejecutor investigador revisor; do
  hermes -p $p config set tools.compact_schemas true   --force
  hermes -p $p config set skills.prompt_mode    compact --force
done
```

### 5. Instalar ddgs en el venv de Hermes

```bash
VENV_PYTHON=$(readlink -f $(which hermes) | xargs dirname)/python3
uv pip install --python "$VENV_PYTHON" ddgs
"$VENV_PYTHON" -c "from ddgs import DDGS; print('ddgs OK')"
```

### 6. Instalar wrappers

```bash
mkdir -p ~/.local/bin/hermes-slim
cp wrappers/*-slim ~/.local/bin/hermes-slim/
chmod +x ~/.local/bin/hermes-slim/*-slim
```

### 7. Instalar SOUL.md

```bash
cp souls/orquestador.md  ~/.hermes/profiles/orquestador/SOUL.md
cp souls/investigador.md ~/.hermes/profiles/investigador/SOUL.md
cp souls/ejecutor.md     ~/.hermes/profiles/ejecutor/SOUL.md
cp souls/revisor.md      ~/.hermes/profiles/revisor/SOUL.md
```

## Uso

### Modo interactivo

```bash
~/.local/bin/hermes-slim/orquestador-slim chat
```

### Modo one-shot (para scripts)

```bash
~/.local/bin/hermes-slim/orquestador-slim -z "PROMPT" \
  --usage-file /tmp/usage.json
```

### Delegación directa

```bash
~/.local/bin/hermes-slim/ejecutor-slim -z "TAREA: ... CONTEXTO: ... CRITERIO: ..." \
  --usage-file /tmp/exec.json

jq '{input_tokens, estimated_cost_usd, completed}' /tmp/exec.json
```

## Auditoría de costos

Cada delegación deja un JSON con:

```json
{
  "input_tokens": 1130,
  "cache_read_tokens": 17138,
  "total_tokens": 18268,
  "estimated_cost_usd": 0.0004151952,
  "api_calls": 3,
  "completed": true
}
```

Sumar costos de un pipeline completo:

```bash
cat /tmp/hermes-*.json | jq -s '{
  total_cost: ([.[] | .estimated_cost_usd // 0] | add),
  total_input: ([.[] | .input_tokens // 0] | add),
  delegations: length
}'
```

## Casos de uso validados

### Caso 1 — Pipeline completo de primalidad

Tarea: investigar el mejor algoritmo para detectar primos hasta 20 dígitos,
implementarlo, auditarlo.

Resultado:
- Investigador: Miller-Rabin con 13 bases primas
- Ejecutor: script probado, 0.34ms por número de 20 dígitos
- Revisor: encontró bug crítico en la constante de determinismo
  (con contraejemplo factorizado)
- Costo total: ~$0.010
- Tiempo total: ~5 min

### Caso 2 — Delegación simple

Tarea: crear /tmp/test.txt con "hola".

Resultado:
- Orquestador clasificó como EJECUCIÓN
- Delegó a ejecutor-slim
- Resumen final: 3 líneas
- Costo: ~$0.0009

## Troubleshooting

### "No inference provider configured"

Falta el `.env` del perfil. Copia del orquestador.

### "Venv entry point not found" en hermes doctor

Falso positivo en instalaciones vía pipx/mise. Ignorar.

### "No module named 'ddgs'"

Instalar en el venv específico de Hermes (paso 5). El Python del
sistema no sirve.

### "hermes config set" no aplica platform_toolsets

Bug conocido: escribe string en lugar de lista. Solución: usar
wrappers con `--toolsets` explícito.

### DuckDuckGo rate-limita

Considerar SearXNG self-hosted:

```bash
docker run -d --name searxng -p 8080:8080 searxng/searxng
echo "SEARXNG_URL=http://localhost:8080" >> ~/.hermes/.env
hermes config set web.backend searxng
```

## Referencia rápida

| Comando | Qué hace |
|---|---|
| `orquestador-slim chat` | Sesión interactiva |
| `orquestador-slim -z "..."` | One-shot |
| `orquestador sessions list` | Listar sesiones |
| `orquestador sessions export <id>` | Exportar a JSON |
| `hermes -p <perfil> prompt-size` | Ver system prompt |
| `hermes doctor` | Diagnóstico |

## Licencia

MIT — úsalo, modifícalo, compártelo.

## Créditos

Construido sobre [Hermes Agent](https://hermes-agent.nousresearch.com)
de Nous Research.

## Limitaciones conocidas

### Extracción de URLs (web_extract) no funciona en v0.19.0

**Síntoma:** el investigador puede buscar en web pero no puede leer el contenido
completo de las URLs.

**Causa raíz:** bug en Hermes v0.19.0 (Issue #73192). El orden de ejecución en
`tools/web_tools.py` está invertido — `_get_extract_backend()` corre antes que
`_ensure_web_plugins_loaded()`, así que el registro de backends está vacío y el
sistema cae al fallback (`web.backend` = ddgs), que es solo búsqueda. El fix está
en el PR #73183, incluido en versiones más recientes.

**Impacto:** el investigador puede hacer búsquedas web y citar snippets indexados,
pero no puede leer páginas completas. Para investigación que requiere análisis
profundo de documentos, esta limitación es importante.

**Workarounds intentados sin éxito:**
- `web.extract_backend: exa` → requiere EXA_API_KEY
- `web.extract_backend: parallel` → requiere PARALLEL_API_KEY
- `web.extract_backend: tavily` → el keyless se añadió en PR #88591 (posterior a v0.19.0)
- `web.backend: parallel` (fallback) → igual, requiere API key

**Solución real:** migrar a una instalación soportada de Hermes (no pipx/mise) y
actualizar a v0.21+. Esa versión incluye el native fetch provider (keyless),
el keyless ring (Exa/Parallel/Firecrawl/Keenable) y el fix del bug #73192.
