# Tools/ue_scripts

Scripts Python que hablan con el editor de Unreal por el MCP nativo (`http://127.0.0.1:8000/mcp`).
Requisito: el editor abierto con el servidor MCP iniciado (`ModelContextProtocol.StartServer`, ver `CLAUDE.md`).

## Uso
```
cd "D:\Dev\Computacion_Grafica\Rumi 5.8\Tools\ue_scripts"
python diag_inspect_ik.py
```
Cada script añade su propia carpeta a `sys.path` (`os.path.dirname(os.path.abspath(__file__))`), por lo que
`import ue_mcp` funciona desde cualquier directorio de trabajo. `ue_mcp.py` es el cliente MCP compartido.

## Prefijos
| Prefijo | Para qué |
|---|---|
| `build_` | Crea assets/grafos desde cero (Control Rig procedural, sistema completo) |
| `fix_` | Modifica assets existentes para corregir/optimizar (rotaciones CR, parte 1 CR, parte 2 AnimBP) |
| `diag_` | Solo lectura: inspecciona nodos, pines, variables, grafos (antes check_/inspect_/find_/list_/read_/scratch_) |
| `test_` | Experimentos puntuales de nodos/conexiones/math |
| `verify_` | Comprobaciones finales (compilación, PIE en vivo, setup final) |
| `util_` | Utilidades (p. ej. guardar el Control Rig) |

## Advertencias
- Los `build_`/`fix_`/`test_` MODIFICAN assets del editor: no ejecutar sobre `CR_Student_Procedural`, `CR_Student_IK`,
  `Student_Skeleton_AnimBlueprint` ni `_Backup_v5` sin copia previa.
- Algunos scripts contienen rutas absolutas de assets (`/Game/...`) y una ruta de verificación en disco; revisarlas antes de reusar.
- Tras ejecutar, el usuario debe guardar con Ctrl+S en el editor.
- Historial de nombres viejos -> nuevos: `Docs/Reportes/manifiesto_orden_2026-10-28.txt`.
