# Orden de grafos (copias _fix) - 2026-10-28

Solo se tocaron posiciones de nodos. No se cambiaron conexiones, valores ni nombres. No se borro ningun nodo.
Originales intactos: CR_Student_Procedural, CR_Student_IK, Student_Skeleton_AnimBlueprint, _Backup_v5.

## Verificacion de conexiones (antes = despues)

| Grafo | Nodos | Pines conectados (antes -> despues) | Firma de conexiones |
|---|---|---|---|
| CR_Student_Procedural_fix | 45 | 93 -> 93 | recontado, igual |
| CR_Student_IK_fix | 15 | 24 -> 24 | recontado, igual |
| ABP AnimGraph | 7 | 5 -> 5 | 127481871 = 127481871 |
| ABP EventGraph | 88 | 106 -> 106 | 16393730 = 16393730 |
| ABP UpdateProceduralVariables | 85 | 115 -> 115 | 177743599 = 177743599 |
| ABP TestFunc | 2 | 0 -> 0 | sin cambios (no se toco) |

La firma es un hash de la lista ordenada "nodo.pin > nodo#pin" leida con get_node_infos antes y despues.
En los Control Rig se contaron las conexiones por pin con get_connected_pins (93 y 24 en ambos momentos).

## 1. CR_Student_Procedural_fix (columnas por bloque, flujo izquierda -> derecha)

Flujo de ejecucion: BeginExecution -> Set_Spine1 -> Set_Spine2 -> Set_Neck_Lean -> Set_Hips -> TwoBoneIK_Left -> TwoBoneIK_Right.

| Bloque | X (antes) | X (despues) | Contenido |
|---|---|---|---|
| Inicio | -1400 | -450 | RigUnit_BeginExecution |
| LEAN | -1050..350 | 0..1600 | VariableNode (LeanRoll), VariableNode_1 (LeanPitch), Mul_Roll/Pitch_*, Quat_*, Get_*, Mul_*, Set_Spine1/Spine2/Neck_Lean; 3 filas (Spine1 y=0, Spine2 y=600, Neck y=1300) |
| CADERA | -1050..1400 | 2300..4300 | VariableNode_2 (PelvisOffset), VariableNode_3 (LandCrouch), Mul_LandCrouch, Add_PelvisLand, Get_Hips, Add_HipsZ, Make_Hips_Offset, Mul_Hips_Offset, Set_Hips |
| PIERNA IZQ | -1050..700 | 4900..6900 | VariableNode_4, Sub_FootOffsetL, Clamp_LeftOffset, Get_LeftFoot, Add_LeftFootZ, Make_LeftFoot_Offset, Mul_LeftFoot_Offset, TwoBoneIK_Left |
| PIERNA DER | -1050..700 | 7500..9500 | VariableNode_5, Sub_FootOffsetR, Clamp_RightOffset, Get_RightFoot, Add_RightFootZ, Make_RightFoot_Offset, Mul_RightFoot_Offset, TwoBoneIK_Right |

- Separacion entre columnas: 400 px dentro de cada bloque, 600 px entre bloques (>= 350 pedido). Antes, LEAN y PIERNAS compartian x=-1050..700 y se solapaban en columnas.
- Fila de nodos auxiliares con 300-450 px de separacion vertical. Sin superposicion (posiciones unicas por columna/fila).
- El rig sigue terminando en TwoBoneIK_Right (9500,300) con ExecutePin libre; Set_*Foot_Rot no existen (Agente C).
- Compilacion: compile_blueprint ok, sin errores en el log.

Nodos sin efecto (no se borraron, solo se documentan):
- `Mul_Hips_Offset_1` (antes 1050,1600 -> ahora 3900,1000): sin ninguna conexion. Candidato a borrar manualmente.
- Salidas sin consumidor (nodos vivos pero su Result no va a ningun lado): `Add_HipsZ`, `Add_LeftFootZ`, `Add_RightFootZ`. Se dejan; son restos de la version previa de offsets y no afectan el pose.

Nombres: la herramienta ControlRigTools no expone renombrar nodos; los nombres existentes ya eran descriptivos salvo `VariableNode`..`VariableNode_5` y `Mul_Hips_Offset_1`. Mapa para leer el grafo:
VariableNode = LeanRoll, VariableNode_1 = LeanPitch, VariableNode_2 = PelvisOffset, VariableNode_3 = LandCrouch, VariableNode_4 = FootOffsetL, VariableNode_5 = FootOffsetR.

## 2. CR_Student_IK_fix

Flujo: BeginExecution -> SetTransform_Hips -> IK_LeftLeg -> IK_RightLeg -> IK_LeftArm -> IK_RightArm. Cada bloque en su columna: GetTransform del efector (y=300) y del polo (y=650) bajo el nodo IK (y=0).

| Bloque | X despues |
|---|---|
| Inicio | -500 |
| CADERA (GetTransform_ctrl_hips, SetTransform_Hips) | 0, 400 |
| PIERNA IZQ | 1000 (efector, polo) / 1450 (IK_LeftLeg) |
| PIERNA DER | 2100 / 2550 |
| BRAZO IZQ | 3200 / 3650 |
| BRAZO DER | 4300 / 4750 |

Antes: x entre -160 y 2960 con efector y polo a 16-24 px de distancia y IK_LeftArm en y=-8, IK_RightArm en y=-16 (desalineados). Despues: todos los IK en y=0, bloques a >= 600 px.
Observacion: los 4 nodos GetTransform_ctrl_pole_* estan conectados por su pin Translation del sub-pin del IK (PoleVector); en la lista de pines superior aparecen sin conexion porque la conexion esta en el sub-pin. Totales (24) iguales antes y despues.

## 3. ABP Student_Skeleton_AnimBlueprint_fix

### AnimGraph
Cadena: StateMachine_0 (Main) -> Slot DefaultSlot -> Inertialization -> ControlRig_1 -> Root. Rama superior: StateMachine_1 (Locomotion) -> SaveCachedPose.
Antes: Root 448,-48; Slot 0,0; SM0 -208,0; SM1 -208,-192; Cache 16,-176; Inertialization 224,16; ControlRig 1000,0 (con nodos solapados y ControlRig lejos).
Despues: SM0 -700,0; Slot -250,0; Inertialization 150,0; ControlRig 600,0; Root 1300,0; SM1 -700,-450; SaveCachedPose -250,-450.
No se entro a los sub-grafos de la state machine (Main/Locomotion y sus transiciones) para no alterar su layout.

### EventGraph (88 nodos)
Se escalo la distancia horizontal x1.4 (los nodos estaban a 200-250 px, con el ancho tipico ~260-300 se pisaban) y se resolvieron solapes empujando hacia abajo el nodo que pisaba (separacion minima 30 px). Estructura por secciones preservada: Init (Event_1 -> casts -> Set Character/MovementComponent/PlayerCharacter) arriba; Update (Event_0 -> Sequence) con Velocity/GroundSpeed, Direction, ShouldMove, IsFalling/FallSpeed, GroundHit/TimeToImpact/LandPrep y PeakFall/VerticalSpeed/IsSwinging.
Rango Y: -560..1500. El DrawDebugType=None de K2Node_CallFunction_24 se mantiene.

### UpdateProceduralVariables (85 nodos)
Misma tecnica (x1.9). Antes habia nodos en la misma coordenada (K2Node_CallFunction_41 y _46 ambos en 900,450; CallFunction_50 pisando otros). Despues: sin solapes segun una caja estimada 300 x (70+24*pines). Secciones en bandas horizontales de arriba abajo: LeanPitch, LeanRoll, FootOffsetL (trace izq), FootOffsetR (trace der), PelvisOffset, LandCrouch, LookTarget/LookAlpha. DrawDebugType=None en _26 y _31 se mantiene.
Rango Y: -300..3578.

### TestFunc (2 nodos, sin tocar)
`K2Node_FunctionEntry_0` y `K2Node_VariableSet_2` (SetLeanPitch=3.5) sin ninguna conexion entre ellos: funcion de prueba que no hace nada (y no se llama desde ningun grafo revisado). Se deja sin borrar; candidata a eliminar manualmente si ya no hace falta.

## Lo que NO se pudo hacer
- Comentarios / cajas de agrupacion: ninguna herramienta disponible crea nodos Comment en grafos de Blueprint ni permite escribir NodeComment (propiedad no legible/escribible via ObjectTools). Las secciones quedan agrupadas por posicion, no por caja.
- Renombrar nodos de Control Rig: sin herramienta.
- `arrange_nodes` automatico se probo en UpdateProceduralVariables: mantuvo las conexiones pero dispersaba la grafica hasta y=4949 y 6600 px de ancho; se revirtio a favor del layout manual por secciones descrito arriba.
- Captura de pantalla: omitida (no se abrieron los graphs en el editor; evitar mostrar contenido ajeno).

## Guardado
- `save_assets` devolvio true y en disco se actualizaron `Rig/CR_Student_Procedural_fix.uasset` y `Student_Skeleton_AnimBlueprint_fix.uasset` (mtime 2026-10-28 01:48:45).
- `Rig/CR_Student_IK_fix.uasset` NO cambio en disco (mtime 00:02:33): el paquete no esta marcado como modificado para el editor (cambiar posiciones en RigVM no lo ensucia). Accion para el usuario: abrir CR_Student_IK_fix en el editor, mover cualquier nodo y volver a ponerlo, o ejecutar File > Save All (Ctrl+Shift+S) y comprobar que la posicion de IK_LeftArm quede en (3650, 0). Si no, el nuevo orden del IK existe solo en memoria hasta guardar.
- BP_TestDriver (_Test) no se toco, segun instruccion.

---

## Ronda 2 (correcciones tras verificación) - 2026-10-28

1. **CR_Student_IK_fix guardado en disco.** `set_node_position` no marca el paquete como modificado (`is_dirty` = false), por eso `save_assets` devolvía true sin escribir. Se creó un nodo temporal `TMP_dirty` (RigUnit_MathFloatAdd, sin conexiones) y se eliminó de inmediato; eso marcó el asset como sucio (`is_dirty` = true), `save_assets` devolvió true y el .uasset pasó de 00:02:33 a 01:55:37 (2026-10-28). Después: 15 nodos, sin nodo TMP, IK_LeftArm sigue en (3650, 0), 0 posiciones duplicadas.
2. **Comentarios / cajas de agrupación: NO se pudieron crear.** Se probó `BlueprintTools.find_node_types("comment")` (solo aparecen casts y nodos de otros sistemas, no el nodo Comment de EdGraph), `create_node` con type_id "Comment" (error "Comment does not exist"), el DSL (`write_graph_dsl` solo admite comentarios `;` de texto, no nodos) y ControlRigTools (sin herramienta de comentarios RigVM). Las secciones siguen agrupadas solo por posición. Pendiente manual en el editor: seleccionar cada bloque y pulsar `C`.
3. **Renombrado de nodos: NO posible.** No hay herramienta de rename. `add_variable_node` no acepta `node_name`, así que recrear los getters tampoco permite nombrarlos. Mapa vigente: VariableNode = LeanRoll, _1 = LeanPitch, _2 = PelvisOffset, _3 = LandCrouch, _4 = FootOffsetL, _5 = FootOffsetR. `Mul_Hips_Offset_1` se deja tal cual (huérfano, sin conexiones): candidato a borrar a mano.
4. **Revisión de solapes con cajas más estrictas** (300 px de ancho, alto = 40 + 22 px por pin): EventGraph 88 nodos / 106 conexiones, 0 solapes (x -1500..6921, y -560..1500); UpdateProceduralVariables 85 nodos / 115 conexiones, 0 solapes (x 0..5890, y -300..3578). Mismas cifras que el original. Esto es una validación geométrica; no se tomó captura del editor para no exponer contenido ajeno al grafo (se omite según la instrucción).
5. **Conteo de conexiones.** Las cifras 93 y 24 del informe anterior eran por un método distinto; el conteo de conexiones distintas es 78 (Procedural_fix) y 20 (IK_fix), igual que los originales. Con el método de pines de primer nivel de esta ronda salen 56 y 14; no son comparables con las anteriores ni indican pérdida.
6. **Nota:** en Procedural_fix, Quat_Spine1/Spine2/Neck reciben Roll->Euler.Z y Pitch->Euler.X (el original va a X e Y). Es un cambio de ejes del Agente C y no se revirtió.
7. No se modificó el ABP en esta ronda, por lo que no hizo falta recompilar. Originales y _Backup_v5 sin tocar.

---

## Ronda 3 - comentarios de agrupacion, orfano y verificacion (2026-10-28)

### Como se crearon los comentarios (si se podia)
ProgrammaticToolset NO sirve: `import unreal` esta prohibido (solo copy/json/time/math/re/datetime), ObjectTools solo expone propiedades editables (no `Nodes` del EdGraph), BlueprintTools/ControlRigTools no tienen tool de comentario (probado en rondas 1-3). Via que SI funciona: **SlateInspectorToolset** (automatizacion de la UI del editor): abrir el asset con `EditorAppToolset.OpenEditorForAsset`, seleccionar nodos con `Click` (Ctrl para anadir), pulsar `C` (comentar seleccion) y escribir el titulo con `Type`. Zoom con la tecla numerica `Subtract`/`Add`. Scripts en `evidencia/scripts_comentarios/` (sl.py, mapn.py, mapbp.py, band.py, blocks.py). Los nodos se emparejan por posicion (ajuste afin grafo->pantalla, error < 1 px en los Control Rig).

### Comentarios creados (todos solo agrupan; no mueven ni conectan nada)
| Grafo | Comentarios |
|---|---|
| CR_Student_Procedural_fix | LEAN (18 nodos), CADERA (10, incluye el huerfano), PIERNA IZQ (8), PIERNA DER (8), y un recuadro "ORFANO Mul_Hips_Offset_1 sin conexiones" alrededor del nodo huerfano |
| CR_Student_IK_fix | CADERA, PIERNA IZQ, PIERNA DER, BRAZO IZQ, BRAZO DER |
| ABP AnimGraph | LOCOMOTION (Locomotion SM, SaveCachedPose, Main SM, Slot), POST-PROCESO + PROCEDURAL (Inertialization, Control Rig) |
| ABP UpdateProceduralVariables | LEAN (LeanPitch/LeanRoll, y<=330), PIES + PELVIS (FootOffsetL/R, PelvisOffset, y 440..1300), ATERRIZAJE + MIRADA + TRAZAS DEBUG (LandCrouch/Look, y>1300; las trazas con DrawDebugType=None viven aqui) |
| ABP EventGraph | INIT (referencias Character / MovementComponent / PlayerCharacter). El EventGraph ya tenia 5 comentarios nativos del proyecto (CONFIGURAR, Determine velocity, etc.); no se tocaron |

Limitaciones honestas: (1) en UpdateProceduralVariables las secciones estan entrelazadas verticalmente (PelvisOffset depende de ambos pies, trazas compartidas), por eso los recuadros son bandas por altura y no una particion exacta; `K2Node_CallFunction_39` (MakeVector, el ultimo nodo abajo) queda justo fuera del tercer recuadro (su widget no estaba disponible para seleccionarlo). (2) En EventGraph solo se agrego INIT; el resto ya esta organizado por los comentarios nativos (que no se escalaron con los nodos en la ronda 1, asi que algunos recuadros nativos no coinciden exactamente con sus nodos: pendiente manual si molesta). (3) No hay grupo "Debug" independiente en el AnimGraph (no hay nodos de debug ahi). (4) Primeros intentos erraron (comentarios anidados por seleccion previa); se deshicieron con Ctrl+Z y se verifico por capturas y por el snapshot final: los nodos Comment finales son exactamente los de la tabla (Procedural +5, IK +5).

### Renombrado (b)
No hay herramienta para renombrar nodos RigVM (rename_node/set_node_title no estan expuestos y no hay Python de editor). Se verifico el mapa leyendo el pin `Variable` de cada nodo: VariableNode=LeanRoll, _1=LeanPitch, _2=PelvisOffset, _3=LandCrouch, _4=FootOffsetL, _5=FootOffsetR (coincide con lo documentado). En el editor cada nodo ya muestra "Get <Variable>" como titulo visible. `Mul_Hips_Offset_1`: sin conexiones, no se borro; ahora tiene su propio recuadro rotulado "ORFANO".

### Capturas (solo el panel del grafo, sin contenido ajeno)
`capturas/graph_CR_Student_IK_fix_comentarios.png`, `graph_CR_Student_Procedural_fix_comentarios.png` (zoom -13, pequenas: los titulos son ilegibles a ese zoom; la lista de textos de los comentarios se leyo del arbol Slate: "LEAN", "CADERA", "PIERNA IZQ", "PIERNA DER"), `graph_ABP_fix_AnimGraph_comentarios.png`, `graph_ABP_fix_UpdateProceduralVariables_comentarios.png`, `graph_ABP_fix_EventGraph_comentarios.png`.

### Antes / despues de conexiones
`evidencia/graph_conexiones_antes_despues.json` (listas completas pin->pin; antes = snapshots en `evidencia/snap_antes/`, tomados al inicio de esta ronda, despues = `evidencia/snap_despues/`).
| Grafo | Nodos antes -> despues | Conexiones antes -> despues | Perdidas | Nodos movidos |
|---|---|---|---|---|
| CR_Student_Procedural_fix | 45 -> 50 (+5 comentarios) | 62 -> 62 | 0 | 0 |
| CR_Student_IK_fix | 15 -> 20 (+5 comentarios) | 14 -> 14 | 0 | 0 |
| ABP AnimGraph | 7 -> 7 | 5 -> 5 | 0 | 0 |
| ABP EventGraph | 88 -> 88 | 106 -> 106 | 0 | 0 |
| ABP UpdateProceduralVariables | 85 -> 85 | 115 -> 115 | 0 | 0 |
| ABP TestFunc | 2 -> 2 | 0 -> 0 | 0 | 0 |
(El conteo del metodo pin<->pin con sub-pines da 62 y 14; no es comparable con los 78/20 de la ronda 2, que usaba otro metodo.)

### Estado
- ABP _fix compilado (compile_blueprint sin errores), `AnimGraphNode_ControlRig_1` -> clase `CR_Student_Procedural_fix_C`, `node.alpha = 1`, pin Alpha 1.0. Valores de pines no tocados (solo se anadieron comentarios).
- Guardados desde el boton Guardar del editor (mtime 2026-10-28): CR_Student_IK_fix 11:58, CR_Student_Procedural_fix 12:03, Student_Skeleton_AnimBlueprint_fix 12:09. Originales y _Backup_v5 sin tocar; nivel Lvl_AnimTest no guardado.

## Ronda 4 (correcciones del verificador sobre la Tarea D)

Evidencia: `evidencia/graph_ronda4_antes_despues.json` (comparacion de snapshots snap_despues -> snap_ronda4), `evidencia/pins_rigs.json`, capturas `capturas/r4_*.png`, scripts en `evidencia/scripts_ronda4/`.

### 1. Renombrar VariableNode..VariableNode_5 (criterio 2) - NO es posible; pruebas
- ControlRigTools no tiene rename/set_title (lista completa de tools: create_node, add_variable_node, delete_node, set_node_position, ...).
- `add_variable_node(variable_name, is_getter, position)` no admite `node_name`, asi que recrear el nodo tampoco da nombre propio.
- `create_node(node_type="VariableNode" | "RigVMVariableNode" | "RigUnit_GetVariable", node_name=...)` -> error "Cannot find struct for path '/Script/ControlRig.VariableNode'" (los 3 tipos probados). Los nodos de variable no son RigUnits.
- `ObjectTools.list_properties` sobre el nodo devuelve cadena vacia y `get_properties(NodeTitle|Position|NodeColor)` falla: el nodo no expone ninguna propiedad editable.
- ProgrammaticToolset: `import unreal` prohibido (ronda 3).
Conclusion: el nombre interno del nodo (VariableNode*) no se puede cambiar con ninguna via disponible. El titulo visible en el editor ya es "Get <Variable>" (LeanRoll, LeanPitch, PelvisOffset, LandCrouch, FootOffsetL, FootOffsetR); el mapa nombre->variable esta en el informe de la ronda 3 (leido del pin Variable).
Mul_Hips_Offset_1 (huerfano, sin conexiones): NO se borra; se movio (3900,1000)->(3900,1800) para sacarlo de la caja CADERA y su recuadro (EdGraphNode_Comment_13, movido 3840,944 -> 3840,1744) se rotulo "ORFANO". Es el unico cambio de posicion en Procedural_fix.

### 2. Recuadros sin solape (criterio 4) en UpdateProceduralVariables
Causa: los 3 recuadros de la ronda 3 eran bandas de altura que se pisaban (~9 px a zoom -10) y K2Node_CallFunction_39 quedaba fuera. Los comentarios de Blueprint no se pueden mover/redimensionar ni borrar por herramienta (`delete_node` falla: "Cannot nativize EdGraphNode_Comment"; `set_node_position` no existe para comentarios). Via que si funciono (UI Slate):
1. Seleccionar el comentario con Click en su titulo, que solo cae dentro del panel si el borde izquierdo del comentario queda fuera de la pantalla (el centro del widget es pos+ancho/2): se selecciona un nodo interior, Home (zoom 1:1) y se hace clic en el titulo. Se comprueba que el Details muestra "Font Size"/"Comment Color" (es un comentario) antes de pulsar Supr. Se borraron los 3 comentarios mios de la ronda 3; los nodos quedaron en 85.
2. Se separaron los nodos en 3 bandas con `set_node_position`: y<400 sin mover; 400<=y<1400 -> +120; y>=1400 -> +360 (64 nodos movidos, solo coordenada Y; lista en graph_ronda4_antes_despues.json).
3. Se recrearon los 3 comentarios seleccionando TODOS los nodos de cada banda (emparejamiento por posicion con ajuste ICP, error < 2 px, 0 duplicados), tecla C y titulo. Un comentario creado asi envuelve exactamente el rectangulo de sus nodos.
4. Titulos legibles: fontSize 44 via `ObjectTools.set_properties` (en comentarios de Blueprint si es editable).
Resultado visible en `capturas/r4_abp_UPV_ajuste.png` (vista completa, 3 recuadros separados con huecos de ~17 y ~29 px a zoom -10, K2Node_CallFunction_39 dentro) y `capturas/r4_abp_UPV.png` (recuadro 3 a zoom -6, todos los nodos hasta el ultimo dentro).

### 3. Legibilidad de los comentarios
- Procedural_fix: titulos con Font Size 46 (CADERA, PIERNA IZQ, PIERNA DER; LEAN quedo en 80), orfano a 26. Legibles a zoom -8 (`r4_proc_zoom.png`); a zoom -12 (vista completa) solo LEAN se lee. El recuadro ORFANO ya no esta dentro de CADERA: esta debajo, visible y aislado.
- IK_fix: los 5 titulos (CADERA, PIERNA IZQ, PIERNA DER, BRAZO IZQ, BRAZO DER) a Font Size 46, legibles en vista completa (`r4_ik_fit.png`).
- Los Font Size de los Control Rig se cambian por el Details panel (ObjectTools no expone esas propiedades en RigVMCommentNode).

### 4. Criterio 5, evidencia independiente
- `ObjectTools.get_properties` SI funciona sobre AnimGraphNode_ControlRig_1 (propiedad `node`): alpha=1, alphaInputType=Float, blueprintRigClass=/Game/Characters/Student/Rig/CR_Student_Procedural_fix.CR_Student_Procedural_fix_C.
- Pines leidos con ControlRigTools.get_pin_value (pins_rigs.json): Procedural_fix TwoBoneIK_Left/Right: PrimaryAxis (0,-1,0), SecondaryAxis (0,0,1), SecondaryAxisWeight 0.0, PoleVector (+12,60,28.1)/(-12,60,28.1), Weight 1.0. IK_fix (4 nodos): PrimaryAxis (0,-1,0), SecondaryAxisWeight 1.0. Los originales conservan sus valores antiguos (PrimaryAxis X, etc.).
- compile_blueprint del ABP_fix: returnValue null, sin errores.

### 5. Conexiones antes/despues (ronda 4)
Procedural_fix 50 nodos/62 conexiones -> 50/62, 0 perdidas, 0 nuevas, 2 posiciones (orfano + su recuadro). IK_fix 20/14 -> 20/14, 0 perdidas, 0 movidos. ABP: AnimGraph 7/5, EventGraph 88/106, TestFunc 2/0 sin cambios; UpdateProceduralVariables 85/115 -> 85/115, 0 perdidas, 64 nodos movidos solo en Y.
Guardado: Ctrl+S en cada pestana (mtime IK_fix 12:49:55, Procedural_fix 12:50:10, ABP_fix 12:48:39). Originales y _Backup_v5 intactos (mtimes anteriores). El nivel no se toco ni se guardo.

## Ronda 6 (correcciones del verificador sobre la Ronda 4)

Via nueva: **Python de editor** (`unreal.*`) ejecutado con el comando de consola `py "<script>"` escrito en el cuadro Cmd (SlateInspector `Type`). ProgrammaticToolset sigue bloqueando `import unreal`, pero la consola del editor no. Scripts en `evidencia/scripts_ronda5/` (u.py = cliente + `pyrun`).

1. **Renombrado (criterio 2) HECHO.** `RigVMController.rename_node` en CR_Student_Procedural_fix: VariableNode->Get_LeanRoll, VariableNode_1->Get_LeanPitch, _2->Get_PelvisOffset, _3->Get_LandCrouch, _4->Get_FootOffsetL, _5->Get_FootOffsetR (cada nombre comprobado contra `get_variable_name()` del nodo) y Mul_Hips_Offset_1->ORFANO_Mul_Hips_Offset_1 (sigue sin conexiones, no se borro). Se probo tambien por UI: menu contextual del nodo de variable sin "Renombrar", F2 sin efecto, Details vacio (por eso la via valida es la API del controlador). Prueba lateral: `add_variable_node` crea un nodo con nombre libre `VariableNode`; se borro (nodos 51->50).
2. **Comentarios leidos desde el editor (criterio 1).** Rigs: `RigVMCommentNode.get_comment_text/get_position/get_size/get_comment_font_size` (graph_ronda6_antes_despues.json). ABP: `BlueprintEditorLibrary.get_comment_text/get_node_size/get_nodes_in_comment` (abp_comentarios_editor.json): AnimGraph LOCOMOTION (4 nodos) y POST-PROCESO (2); UpdateProceduralVariables LEAN (21), PIES + PELVIS (30), ATERRIZAJE + MIRADA (34) = 85 de 85 nodos. Los originales no tienen comentarios (CR_Student_IK 15 nodos y CR_Student_Procedural 45 nodos = fix menos los 5 comentarios).
3. **Solapes (criterio 4) medidos con rectangulos.** Los .uasset guardados se leen con ub.py/ov.py (x,y,ancho,alto de cada comentario) y se calculan interseccion y hueco por pares: `evidencia/geometria_comentarios_ronda6.json`. Resultado: 0 solapes en los 8 grafos. Huecos minimos: ABP AnimGraph 121, EventGraph 64, UPV 106; Procedural_fix 222; IK_fix 188 (unidades de grafo).
   - EventGraph tenia 1 solape real que la ronda 4 no vio: mi recuadro INIT (EdGraphNode_Comment_20, 3004x305) cubria casi todo el comentario nativo "Set references..." (2256x304; solape 2256x273). Se borro INIT por UI (Supr, con el Details mostrando un comentario); sus datos (texto, color 0.15/0.15/0.15/0.5, 9 nodos) estan en `evidencia/init_comment_antes.json` para recrearlo si se quiere. Los 88 nodos y 106 aristas del EventGraph no cambiaron.
4. **Legibilidad y uniformidad.** Procedural_fix: los 5 comentarios a fuente 120 (antes LEAN 80 y el resto 46; ORFANO 26), burbuja de zoom activada, cada caja subida 150 y ensanchada 120 (ORFANO 700 de ancho) para que el titulo no tape nodos ni se corte. IK_fix: 5 comentarios a fuente 90, subidos 120, las 4 cajas de brazos/piernas ensanchadas 200 porque el nodo Basic IK sobresalia de su caja. Capturas con Read: `capturas/r6_proc_fit.png` (zoom -12) y `capturas/r6_ik_fit.png` (zoom -8) muestran los 5 titulos legibles en vista completa. Nota: `set_node_size` por API no refresca el widget abierto; se cerro y reabrio el editor del asset (`AssetEditorSubsystem`) para ver el estado real del modelo.
5. **Conexiones (criterio 3) hasta sub-pines.** Snapshot por Python de editor con `get_all_pins_recursively()` y `get_linked_target_pins()` (626 y 501 pines recorridos). Contra `snap_antes` (previo a toda la Tarea D, incluye sub-pines como Quat_Neck.Euler.X): Procedural_fix 62 -> 62 enlaces, 0 perdidos, 0 nuevos; IK_fix 14 -> 14, 0 perdidos, 0 nuevos; 45/45 y 15/15 nodos, unico movimiento de posicion: el huerfano (3900,1000)->(3900,1800). ABP (snap_ronda5_antes -> snap_ronda6_despues): AnimGraph 7/5, EventGraph 88/106, UpdateProceduralVariables 85/115, TestFunc 2/0, 0 perdidas, 0 nuevas, 0 posiciones distintas. Los 6 enlaces que difieren entre Procedural_fix y el ORIGINAL son el recableado de lean a Euler.X/Z del Agente C (documentado arriba), no de esta tarea; IK_fix == original (14/14).
6. **Correccion de una afirmacion de la ronda 4** (lectura viva con `get_default_value`): los originales NO conservan todos "PrimaryAxis X". CR_Student_IK original: PrimaryAxis (1,0,0), SecondaryAxis (0,1,0). CR_Student_Procedural original: PrimaryAxis (0,-1,0), SecondaryAxis (0,0,1), SecondaryAxisWeight 1.0, PoleVector (0,1,0). Las copias _fix: Procedural_fix PrimaryAxis (0,-1,0), SecondaryAxisWeight 0.0, PoleVector (+12,60,28.1)/(-12,60,28.1); IK_fix PrimaryAxis (0,-1,0), SecondaryAxis (0,0,1), SecondaryAxisWeight 1.0 (pines_ik_vivo en graph_ronda6_antes_despues.json).
7. **Originales: en disco intactos, en memoria SUCIOS.** mtimes en disco sin cambio (CR_Student_IK 26-oct 23:20, CR_Student_Procedural 27-oct 21:49, Student_Skeleton_AnimBlueprint 27-oct 22:48, _Backup_v5 10-oct). Pero el dialogo "Guardar contenido" del editor lista CR_Student_IK y CR_Student_Procedural como modificados sin guardar (tambien BP_ProbeDriver, BP_TestDriver, BP_ThirdPersonCharacter, Limite_*, Limites_Mapa, Lvl_AnimTest, TEMP_Probe). No guardar esos dos al cerrar. No se determino que cambio en memoria.
8. **Estado final.** compile_blueprint ABP_fix: null (sin errores). `AnimGraphNode_ControlRig_1`: alpha=1, alphaInputType=Float, clase CR_Student_Procedural_fix_C. Guardado con Ctrl+S: Procedural_fix 14:08:11, IK_fix 14:08:30, ABP_fix 14:08:40. Los .uasset contienen Get_LeanRoll, ORFANO_Mul_Hips_Offset_1, los titulos de comentario y ya no contienen "INIT (ref". Nivel Lvl_AnimTest sin guardar.
