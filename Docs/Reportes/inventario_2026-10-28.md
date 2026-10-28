# Inventario del proyecto - 2026-10-28

Raiz: `D:/Dev/Computacion_Grafica/Rumi 5.8` (no es repo git aun). Regla: nada se borra; lo obsoleto se archiva con manifiesto.

| Elemento (antes) | Que es | Decision | Ubicacion final |
|---|---|---|---|
| `Rumi.uproject`, `Config/` | Proyecto UE 5.8 y configuracion | Se mantiene | igual |
| `Content/` | Assets del juego | NO se toca en disco (registro de assets roto; renombrar rompe referencias). Solo propuesta | `Docs/Reportes/propuesta_estructura_content.md` |
| `Binaries/ Intermediate/ Saved/ DerivedDataCache/` | Caches regenerables de UE | No se tocan | igual (fuera de git) |
| `CLAUDE.md` | Contexto del proyecto | Se mantiene; se anade seccion "Estructura de carpetas" | igual |
| `.mcp.json`, `.claude/settings.local.json`, `.gemini/settings.json` | Config de MCP/agentes | No se tocan (funcionales) | igual |
| `Docs/F-M1_Inventario_Animacion.md`, `Docs/F-M2_Arquitectura_AnimBP.md` | Entregables de hitos | Agrupados | `Docs/Hitos/` |
| `Docs/Mensaje_Jhasmani_F-M1.md` | Mensaje al aprobador | Renombrado y agrupado | `Docs/Mensajes/F-M1_Mensaje_a_Jhasmani.md` |
| `Docs/Reporte_Docente_Avance.md` | Reporte al docente | Prefijo de fecha (14-sep) | `Docs/Reportes/2026-09-14_Reporte_Docente_Avance.md` |
| `guia-state-machine-rumi.md` (raiz) | Guia de state machine | Agrupada | `Docs/Guias/Guia_StateMachine_Rumi.md` |
| `Docs/Avance/` | Entregas por fecha | Se mantiene (convencion `AAAA-MM-DD_tema`) | igual |
| `ue_mcp.py` | Cliente MCP HTTP, importado por 56 scripts | Movido junto a ellos, mismo nombre | `Tools/ue_scripts/ue_mcp.py` |
| 57 scripts `.py` sueltos en raiz (sesion de rig 27-oct) | Construccion, correccion, diagnostico, pruebas | Movidos a una carpeta con prefijo por categoria: `build_` `fix_` `diag_` (check/inspect/find/list/read/scratch) `test_` `verify_` `util_` | `Tools/ue_scripts/` |
| `ocr_pages.ps1` | Utilidad OCR de capturas | Movido | `Tools/ocr_pages.ps1` |
| `p_call.json p_desc.json p_init.json` | Payloads de prueba MCP | Movidos | `Tools/payloads_mcp/` |
| `__pycache__/` | Cache de Python | Archivado (no borrado) | `Docs/Reportes/Archivo/__pycache__/` |

Nota sobre los scripts: son historicos (sesion de arreglo del rig Student) y siguen siendo utiles como referencia; no se descartaron. Su contenido no se modifico; `import ue_mcp` funciona porque Python incluye la carpeta del script (verificado). El `sys.path.insert` con la raiz queda obsoleto pero inofensivo.

Pendiente fuera de alcance: repo remoto (siguiente agente); ordenar assets en Content (requiere editor).

## Anexos (actualizacion de verificacion)
- **Content/Characters/_Archive/Rumi_Unused/**: 26 assets archivados por el agente del rig. Fuente: `Docs/Avance/2026-10-28_rig-student-fix/evidencia/movimientos_archivo.txt` (enlazada tambien desde `manifiesto_orden_2026-10-28.txt`). Decision: se conserva tal cual (reversible).
- **Conteo**: 69 archivos movidos antes = 69 despues (ver manifiesto).
- **.gitignore** creado en la raiz (cachés UE, `__pycache__`/`*.pyc` incluido `Docs/Reportes/Archivo/__pycache__`, settings.local, .gemini, .env).
- **Tools/ue_scripts/README.md** creado (uso y prefijos). `sys.path.insert` obsoleto corregido en 23 scripts.
- **Tools/ocr_pages.ps1**, **Tools/payloads_mcp/**: utilidades conservadas, ver indice en `Docs/Avance/README.md`.

