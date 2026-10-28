# Avance

Entregas de progreso ordenadas por fecha, una carpeta por entrega.

## Convencion de nombres
`AAAA-MM-DD_tema-corto/` con `informe.md`, `capturas/` (solo recortes del muneco/escena, nombres descriptivos con prefijo numerico) y `evidencia/` (manifiestos, logs, datos).

## Como agregar una entrega nueva
1. Crear la carpeta `AAAA-MM-DD_tema-corto/` con `capturas/` y `evidencia/`.
2. Copiar `_plantilla/informe.md` a la carpeta y completarlo con datos reales.
3. Anadir una fila al indice de abajo.

## Recordatorio de reglas del equipo
Dos reportes escritos por semana: **martes y viernes**. Nada cuenta hasta que esta en Unreal; hitos binarios.

## Indice de entregas
| Fecha | Carpeta | Resumen |
|---|---|---|
| 2026-10-28 | [2026-10-28_rig-student-fix](2026-10-28_rig-student-fix/informe.md) | Correccion de piernas deformes del Student en copias `_fix`; A/B no concluyente; archivado no aplicado |

Plantilla: [_plantilla/informe.md](_plantilla/informe.md)

## Otros documentos del proyecto (indice final, 2026-10-28)
| Carpeta | Contenido |
|---|---|
| `Docs/Hitos/` | Entregables por hito: F-M1 Inventario, F-M2 Arquitectura AnimBP |
| `Docs/Mensajes/` | Mensajes al equipo (F-M1 a Jhasmani) |
| `Docs/Guias/` | Guias tecnicas (State Machine de Rumi) |
| `Docs/Reportes/` | Reporte al docente, inventario/manifiesto de orden, propuesta de estructura de Content |
| `Docs/Reportes/Archivo/` | Manifiesto del archivado previo (`MANIFIESTO.txt`) |
| `Archivo_No_Proyecto/` | Capturas descartadas, scripts de prueba, evidencia/snapshots intermedios, duplicados y temporales, por fecha y categoria; `INDEX.md` + `revertir.py` (nada se borra) |
| `Tools/ue_scripts/` | Scripts Python del MCP de Unreal (prefijos build/fix/diag/test/verify/util) |
| `Tools/ue_scripts/README.md` | Como usar los scripts y significado de cada prefijo |
| `Tools/ocr_pages.ps1` | Utilidad PowerShell de OCR de paginas (suelta, movida desde la raiz) |
| `Tools/payloads_mcp/` | Cuerpos JSON de prueba del MCP (`p_init`, `p_desc`, `p_call`) |
| `Docs/Reportes/propuesta_estructura_content.md` | Estructura ideal de `Content/` y plan para aplicarla desde el editor con redirectors |
| `Docs/Reportes/inventario_2026-10-28.md` / `manifiesto_orden_2026-10-28.txt` | Inventario del proyecto y movimientos (origen -> destino, conteo, reversion) |
| `Content/Characters/_Archive/Rumi_Unused/` | 26 assets de Rumi archivados (no usados); manifiesto en `2026-10-28_rig-student-fix/evidencia/movimientos_archivo.txt` |
| `.gitignore` | Excluye cachés de UE, `__pycache__`/`*.pyc`, settings locales y .env |

