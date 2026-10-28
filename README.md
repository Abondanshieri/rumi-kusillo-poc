# Rumi / Kusillo — PoC

Prueba de concepto de un juego educativo de matemáticas. Protagonista: **Rumi**. Mecánica central alrededor de un **yunque**, cámara isométrica. Motor: **Unreal Engine 5.8**.

## Estructura

| Carpeta | Contenido |
|---|---|
| `Content/` | Assets de Unreal (personajes, mapas, Animation Blueprints, rigs). `Content/Characters/_Archive/Rumi_Unused/` guarda assets sin uso, versionados tal cual. |
| `Config/` | Configuración del proyecto (`*.ini`). |
| `Docs/Hitos/` | Entregables de hitos (F-M1 inventario de animación, F-M2 arquitectura AnimBP). |
| `Docs/Mensajes/` | Mensajes al equipo. |
| `Docs/Guias/` | Guías técnicas (state machine de Rumi). |
| `Docs/Reportes/` | Reportes, inventarios, manifiesto de orden y `Archivo/` con material descartado (nada se borra). |
| `Docs/Avance/` | Bitácora de avance con capturas recortadas del personaje. |
| `Tools/ue_scripts/` | Scripts Python para automatizar el editor vía MCP (ver su `README.md`). |
| `Tools/payloads_mcp/` | Payloads de ejemplo para el servidor MCP. |
| `Archivo_No_Proyecto/` | Material que no necesita el proyecto, archivado por fecha y categoria (nada se borra; ver su `INDEX.md`). |
| `.mcp.json` | Apunta al servidor Unreal MCP local `http://127.0.0.1:8000/mcp`. |
| `CLAUDE.md` | Contexto del proyecto para Claude Code. |

No se versionan `Binaries/`, `Intermediate/`, `Saved/` ni `DerivedDataCache/` (se regeneran).

## Cómo abrirlo

1. Instalar **Unreal Engine 5.8** y **Git LFS** (`git lfs install`).
2. Clonar: `git clone https://github.com/Abondanshieri/rumi-kusillo-poc.git` (LFS descarga los `.uasset`).
3. Doble clic en `Rumi.uproject` (o clic derecho > *Switch Unreal Engine version* si hace falta).
4. Opcional, para usar herramientas MCP: `Edit > Editor Preferences > Model Context Protocol > Auto Start Server`, o en el Output Log `ModelContextProtocol.StartServer`.

## Equipo

- **Diego** — narrativa y niveles
- **Carlos** — arte 3D y concepto
- **Franco** — animación
- **Jhasmani** — mecánicas, arquitectura e integración (aprobador)

Reglas del equipo: nada cuenta hasta que está en Unreal; hitos binarios; reportes martes y viernes; aprobación en 24 h.
