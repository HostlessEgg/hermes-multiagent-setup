# Métricas medidas del pipeline

## Pipeline de primalidad (caso 1)

### Costos por agente

| Agente | input_tokens | output_tokens | costo | tiempo |
|---|---|---|---|---|
| Orquestador | 12,700 | — | ~$0.001 | — |
| Investigador | 9,076 | — | $0.00244 | 67s |
| Ejecutor | 7,759 | — | $0.00228 | 39s |
| Revisor (v2) | 10,091 | 5,307 | $0.00324 | ~110s |
| **Total** | **~40K** | — | **~$0.009** | **~5min** |

### Comparación con agente único

| Escenario | Costo | Hallazgos críticos | Contexto |
|---|---|---|---|
| Agente único (calculadora) | $0.0077 | 0 | Contaminado |
| Pipeline 4 agentes | $0.009 | 1 | Aislado |

El pipeline cuesta +17% y produce hallazgos críticos verificables.

## Delegación simple (caso 2)

| Métrica | Valor |
|---|---|
| Costo del orquestador | ~$0.001 |
| Costo del ejecutor | $0.0009 |
| Costo total | ~$0.002 |
| Tiempo | ~30s |
| Contexto del orquestador | Limpio |
