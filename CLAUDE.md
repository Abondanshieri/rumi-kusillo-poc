# Contexto del proyecto Kusillo / Rumi

Este proyecto es la PoC de un juego educativo de matemáticas: protagonista **Rumi**, mecánica
central alrededor de un **yunque**, cámara isométrica, Unreal Engine 5.8. El usuario de estas
sesiones es **Franco**, animador del equipo.

## Equipo y cadena de dependencias

- **Diego** — narrativa y niveles, inicia la cadena (D-M1..D-M5).
- **Carlos** — arte 3D y concepto, alimenta a todos (C-M1..C-M5).
- **Franco (usuario)** — animación (F-M1..F-M5).
- **Jhasmani** — mecánicas, arquitectura, integración, y aprobador (J-M1..J-M5).

Dominó crítico: D-M1 (Diego) desbloquea todo lo visual → C-M1→C-M2 (Carlos) → C-M3 (rig de Rumi,
entrega crítica hacia Franco) y C-M5 (kit de entorno, entrega crítica hacia Diego). D-M4
(especificación de actividades, Diego) desbloquea a la vez F-M1 (Franco) y J-M3 (Jhasmani).

Tracker maestro (hitos, tareas, dependencias, reglas): `D:\Downloads\kusillo-plan-poc-tracker-es (1).xlsx`
— es la fuente de verdad de avance, pero puede estar desactualizado frente al estado real del
proyecto en disco (ver más abajo). Reléelo si hace falta el estado exacto de una tarea.

Las 8 reglas del equipo (resumen): nada cuenta hasta que está en Unreal; hitos binarios (no %);
dos reportes escritos por semana (martes y viernes); aprobación en 24h; registrar fecha
planificada vs real; reunión de fin de semana opcional y no crítica para el avance.

## Los 5 hitos de animación de Franco

1. **F-M1 — Inventario de animación.** Bloqueado por D-M4. Traducir la especificación de
   actividades de Diego en una lista cerrada de animaciones, categorizada en
   Movimiento / Interacción / Feedback, priorizada imprescindible vs deseable. Revisan Diego
   (completitud) y Jhasmani (aprobación).
2. **F-M2 — Blockout y timing** sobre rig provisional.
3. **F-M3 — Animaciones base** sobre el rig final de Rumi (necesita C-M3 de Carlos, entrega crítica).
4. **F-M4 — Animaciones de mecánica y feedback** (golpe al yunque, acierto, error) — alimenta J-M3.
5. **F-M5 — Pulido de la state machine** — alimenta J-M4 (integración).

**Arquitectura de Animation Blueprint acordada:** Locomotion State Machine simple (Idle/Walk/Run
vía Blend Space) + un estado "Busy/Interacting" que bloquea el input de movimiento. Interacción y
feedback como **Montages disparados por Slots**, no como estados nuevos — evita explosión de
transiciones y deja que Jhasmani dispare animaciones desde eventos de gameplay sin tocar la state
machine.

Mixamo: útil para blockout (F-M2) y nomenclatura del inventario (F-M1), pero el rig final de
Carlos (C-M3) probablemente tendrá proporciones estilizadas — va a necesitar retargeting vía
IK Rig / IK Retargeter, no reimportación directa.

## Estado real ya encontrado en este proyecto (2026-09-14)

En `Content/Characters/Student/` ya existe un personaje placeholder completo: `Student_Skeleton`,
`Student_Skeleton_AnimBlueprint`, `Student_Skeleton_BlendSpace`, y los clips `Student_Idle`,
`Student_walking_Anim`, `Student_Running`, `Student_Jump`, `Student_FallLoop` — probablemente obra
de Jhasmani en J-M1. El tracker marca 0% de avance en todo, pero esto ya es una base de
locomoción real. **Auditar esto antes de proponer crear un rig provisional nuevo o salir a buscar
animaciones en Mixamo para F-M2.**

## MCP de Unreal en este proyecto

El servidor que expone herramientas de Unreal a Claude Code es el plugin nativo/experimental de
Epic "Unreal MCP" (`Engine/Plugins/Experimental/ModelContextProtocol`) — no `MCPClientToolset`
(ese es un cliente, no sirve para esto). Por defecto `bAutoStartServer=false`, así que el servidor
**no arranca solo** al abrir el editor. Si las herramientas `unreal-mcp` no responden en esta
sesión:

- Sesión puntual: en el editor, `Window > Developer Tools > Output Log`, escribir
  `ModelContextProtocol.StartServer` en el campo de comando.
- Automático desde ahora: `Edit > Editor Preferences` → buscar "Model Context Protocol" →
  activar **"Auto Start Server"**.

El `.mcp.json` de esta carpeta ya apunta a `http://127.0.0.1:8000/mcp` — se generó solo la
primera vez que el servidor arrancó.

## Estructura de carpetas

- `Content/`, `Config/`, `Rumi.uproject` — proyecto UE (los assets solo se mueven/renombran desde el editor; ver `Docs/Reportes/propuesta_estructura_content.md`).
- `Docs/Hitos`, `Docs/Mensajes`, `Docs/Guias`, `Docs/Reportes`, `Docs/Avance` (entregas `AAAA-MM-DD_tema/`, indice en su README). Solo se conservan documentos vigentes y la evidencia que citan.
- `Tools/ue_scripts/` — scripts Python vía MCP (`ue_mcp.py` + prefijos build/fix/diag/verify/util); `Tools/payloads_mcp/`, `Tools/ocr_pages.ps1`.
- `Archivo_No_Proyecto/<AAAA-MM-DD>/<categoria>/` — todo lo que no necesita el proyecto (capturas descartadas, scripts de prueba, evidencia/snapshots intermedios, duplicados, temporales). Nada se borra: `Archivo_No_Proyecto/INDEX.md` lista cada movimiento y `revertir.py` lo deshace. Si algo falta de un informe, buscarlo ahí antes de regenerarlo.
- Raiz limpia: nada suelto salvo `CLAUDE.md`, `README.md`, `.mcp.json`, `Rumi.uproject`, `.gitignore`, `.gitattributes`.
