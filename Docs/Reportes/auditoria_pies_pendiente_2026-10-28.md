# Auditoria de pies en pendiente (rampa lisa) - 2026-10-28 (rev. 3, corregida tras segunda verificacion)

Sintoma reportado por Franco: en la rampa lisa, al SUBIR la puntera del pie se mete un poco en la superficie; al BAJAR la puntera queda flotando. En gradas funcionaria mejor.

Alcance: SOLO LECTURA sobre Unreal. No se edito, compilo, guardo ni se toco PIE/camara/nivel. Unico archivo escrito en el proyecto: este informe.

**Rev. 3 (esta):** responde las 9 objeciones de la segunda verificacion. Resumen de lo que cambia:
1. Cita del 0.07: la cifra de rotacion del pie citada ahora es la del rig ACTUAL (modo Location): idle 0.07/0.16, walk 0/1.35, run 0/0, jump 0/0.64; las de Direction (idle/walk 0/0, run 0.56/2.2, jump 0/0.6) se citan aparte como el estado anterior (3.3).
2. Lecturas en vivo: el tool MCP nativo de la sesion (`mcp__unreal-mcp`) devolvia ECONNREFUSED, pero el cliente Python del proyecto (`Tools/ue_scripts/ue_mcp.py`, puerto 8000, escuchando el PID 23088) SI responde. Con el se RELEYERON EN VIVO en esta revision: pines de TwoBoneIK, huesos Foot/ToeBase/Toe_End, rampa de 28 grados, clamp/interp/trazas del ABP `_fix` en memoria, capsula y CharacterMovement, nivel activo (seccion 0 y 10).
3. Contradiccion del registro (seccion 10): resuelta. El clamp -40/30 se leyo en vivo del ABP en memoria, no de un volcado de disco.
4. El 4.8 cm sigue siendo una prediccion estatica; ahora se contrasta con datos de huesos ANIMADOS ya existentes en disco (`sweep_OFF.json`, `sweep_LOCX12.json`), lo que destapo un sesgo vertical constante no considerado antes (nueva 3.7) y un analisis cuantitativo del retraso de `FInterpTo` (nueva 3.8) que ya no se descarta.
5. Mutaciones: 10.1 aclara que no puedo atribuir el guardado de las 16:43 y que esta revision tampoco guardo nada.
6. Criterios de aceptacion: cada umbral lleva su base y se marca [S] o [C] (7.3); el `FInterpTo` inicial 25/15 se descarta por calculo (6.4).

**Rev. 2:** corrige lo objetado por el verificador (nombres de nodos, cifras de compensacion, cita del 0.07, y la falsa afirmacion de 'editor apagado'). En la rev. 1 el editor no respondia; en esta revision el editor SI esta corriendo y el MCP responde, asi que se repitieron lecturas en vivo (marcadas **[V]**).

## 0. Leyenda de evidencia (leer primero)

- **[V]** leido EN VIVO del editor en esta revision (MCP, solo lectura: `ControlRigTools.list_pins/get_pin_value/get_global_transform`, `SceneTools.find_actors/trace_world/get_current_level`, `BlueprintTools.get_graph/find_nodes/get_node_infos`, `ObjectTools.get_properties`; via el cliente Python `ue_mcp.py`).
- **[F]** leido del codigo fuente de UE 5.8 instalado en `D:/Games/UE_5.8/Engine/Plugins/...` (cabeceras `.h` y `.cpp`).
- **[D]** leido del DISCO en esta sesion: JSON de evidencia de rondas previas (`G3_dump_antes.json`, `snap_ronda6_final.json`, `pins_rigs.json`) y los `.uasset` de `Content/__ExternalActors__` (parseados byte a byte: nombres, Location/Rotation/Scale3D de cada componente).
- **[M-previo]** medido por rondas anteriores con el editor (informe de la Ronda 5/6 y auditoria del esqueleto). No re-medido hoy.
- **[C]** calculado por mi a partir de [D] / [M-previo] (aritmetica, se muestra la formula).
- **[S]** SUPOSICION / conocimiento general de UE. Hay que verificarla.
- **[NO MEDIDO]** no pude medirlo.

**Estado del editor en esta revision [V]:** `UnrealEditor.exe` corre (PID 23088) y `netstat` muestra el puerto 8000 en LISTENING por ese PID. El tool MCP nativo de la sesion dio ECONNREFUSED, pero el cliente Python `ue_mcp.py` conecta y responde (probado con `trace_world`, `get_properties`, `get_current_level`). `SceneTools.get_current_level` devuelve `/Game/ThirdPerson/Lvl_ThirdPerson` (no `Lvl_AnimTest` como indicaba el encargo; no lo cargue ni lo cambie, solo lo lei). PIE: no existe un tool `IsPIERunning` en el toolset; la evidencia de que PIE esta apagado es indirecta: `find_actors` no halla ningun `BP_ThirdPersonCharacter` en el mundo del editor y las rutas `UEDPIE_0_Lvl_*` del personaje devuelven 'not valid Object'. **No se arranco PIE** (regla: no tocar PIE/camara/nivel), por eso la medicion de huesos animados en movimiento (punto 5) sigue pendiente; en su lugar se hizo una medicion estatica con colision real (seccion 3.5). Los volcados en disco de la rev. 1 siguen citados como [D] donde no se releyeron.

## 1. Resumen ejecutivo (5 lineas)

0. (rev. 3) Hay ademas un sesgo constante de ~-4.5 cm en el rig actual (`90 - Distance` con mesh a -94.5 y capsula flotando 2.15, seccion 3.7) y un retraso de `FInterpTo` de `v*tan(theta)/12` de signo contrario al geometrico (3.8): el balance real solo se resuelve midiendo huesos animados en PIE (pendiente).
1. Causa raiz mas probable [C]+[D]: el rig solo SUBE/BAJA el tobillo en Z segun UNA traza bajo el tobillo; el pie conserva el pitch de la animacion (plano, 0 grados), asi que en una pendiente theta la puntera queda a `d*tan(theta)` del suelo (d = tobillo->bola ~ 9.1 cm): sube = se hunde, baja = flota.
2. Magnitud esperada [C]: 28 grados (Rampa de ThirdPerson) -> 4.8 cm en la bola; 35 grados -> 6.4 cm; hasta 9 cm si se mira el Toe_End. Es el orden de lo que se ve en pantalla (un pie de 11 cm).
3. No hay normal de superficie, ni rotacion del pie, ni traza independiente de bola/puntera; el efector del IK recibe la rotacion de la animacion sin cambios (`Get_Foot.Rotation -> Effector.Rotation`) [D].
4. Faltantes secundarios: suavizado `FInterpTo` lento (retraso transitorio de varios cm), IK siempre activo en el aire, pole fijo, sin foot-lock [D]/[S].
5. Diseno propuesto: normal por pie -> cuaternion de alineacion con limites -> efector, + traza de bola para pitch fino + Alpha por estado; 12-17 h, ~70% automatizable por MCP/Python; criterio: penetracion/flotacion de bola <= 0.5 cm en reposo sobre 28 y 35 grados.

## 2. Geometria real de rampas (punto 1 del encargo)

### 2.1 /Game/ThirdPerson (Lvl_ThirdPerson) - leido de los `.uasset` [D]

Las dos rampas son cubos `/Engine/BasicShapes/Cube` (100 uu) escalados y rotados: **superficie plana lisa, SIN gradas**.

| Actor (prefab) | Componente | Rotacion (Pitch,Yaw,Roll) | Escala | Dimensiones [C] (cm) | Angulo [D]/[C] | Longitud de superficie [C] | Subida [C] |
|---|---|---|---|---|---|---|---|
| Plataforma_Altura (loc raiz 0,50,0) | `Rampa` | (0, -90, **28**) | 1.8, 4.5, 0.2 | 180 x 450 x 20 | **28 grados** (roll) | 450 | 450*sin28 = 211 |
| Plataforma (loc raiz 1300,1300,0) | `Rampa` | (0, 0, **-35**) | 1.1, 2.4, 0.15 | 110 x 240 x 15 | **35 grados** (roll) | 240 | 240*sin35 = 138 |

**Releido en vivo [V]** (nivel activo `Lvl_ThirdPerson`): actor `Plataforma_Altura`, componente `Rampa`: RelativeRotation (pitch -0, yaw -90, roll 28.000), RelativeScale3D (1.8, 4.5, 0.2), `StaticMesh = /Engine/BasicShapes/Cube`, `collisionProfileName = BlockAllDynamic`, `collisionEnabled = QueryAndPhysics`, `Deck` a z=200 con escala (2,2,0.2). Bounds del actor: X -475.4..100, Y -607.5..150, Z -16..290. **Angulo medido con trazas verticales (`trace_world`) cada 30 cm (rev. 3: releido, 13 impactos en y=-540):** la altura sube 15.95 cm por cada 30 cm de avance -> `atan(15.95/30) = 28.0 grados`, lineal sin escalones (ver 3.5). La rampa de 35 grados (`Plataforma`) no esta en el nivel activo actual: sigue [D] del `.uasset`.

Comprobacion cruzada [C]: Plataforma_Altura tiene `Deck` a z=200 (+250 de barandas) -> la subida de 211 sobre el centro del cubo es coherente. Plataforma tiene deck a z=150 -> 138 + espesor, coherente. Colision de la rampa de 28 grados: `BlockAllDynamic`, `QueryAndPhysics` [V]. Material fisico: ninguno (`physMaterialOverride None`) [V].

Ambos angulos estan por debajo del `WalkableFloorAngle` por defecto del CMC (44.76 grados) [S], por lo que el personaje las sube caminando.

### 2.2 /Game/AnimTest/Lvl_AnimTest - leido de los `.uasset` [D]

Las rampas usan el mesh `/Game/LevelPrototyping/Meshes/SM_Ramp` (rampa lisa del kit de Epic) con escalas distintas. Rotacion = (Pitch, Yaw, Roll) del componente.

| Etiqueta / actor | Location | Rotacion | Escala (X,Y,Z) |
|---|---|---|---|
| Rampa_Ascenso_1 (Puente_Colgante) | (-1410.8, -239.0, 0) | (0, 90, 0) | 4.5, 3.2, 2.2 |
| Rampa_Ascenso_2 (Puente_Colgante) | (-1050, 0, 220) | (0, 0, 0) | 4.5, 3.2, 1.15 |
| Rampa_Retorno_Suelo (Puente_Colgante) | (800, 370.2, 0) | (0, 90, 0) | 3.75, 6.125, 5.175 |
| 8 rampas de la "Canopy_Troncos" | (+-800, 0, 0) | yaw 0 / 90 / 180 / -90 | 1.8, 4.2, 1.5 |
| 1 rampa Canopy | (800, 0, 0) | (0, -90, 0) | 1.8, 5.25, 1.5 |

**Angulo y longitud de las rampas de AnimTest: [NO MEDIDO]** (el nivel AnimTest no esta cargado en el editor; cargarlo seria cambiar el nivel y esta prohibido). El angulo depende de las dimensiones nativas de `SM_Ramp` (no estan en el `.uasset`: la geometria esta en los datos derivados, no en disco; probe con busqueda de bounds en floats/doubles y no aparecio). Formula: `angulo = atan( (Sz*Hn) / (Srun*Ln) )`, con Hn/Ln = subida/avance nativos del mesh y Srun = escala del eje de avance. Si SM_Ramp fuera 400 de avance x 200 de subida [S, NO verificado], Rampa_Ascenso_1 daria ~14-19 grados segun el eje, y las de Canopy ~10-14 grados. **Para medirlo en vivo:** `SkeletalMesh/StaticMeshTools.get_bounds` + `SceneTools.trace_world` en dos puntos del eje de avance (script listo en 7.2). Material de colision: [NO MEDIDO] (los `M_Grad_*` son materiales visuales; el perfil de colision viene del mesh).

**Rampa lisa vs gradas:** las 4 familias de rampa (2 en ThirdPerson, SM_Ramp en AnimTest) son planos lisos. No hay gradas en ninguno de los dos niveles [D] (no aparece ningun mesh de escalera/escalon en los nombres de los 79 actores externos).

## 3. Pipeline actual de datos (punto 2)

### 3.1 UpdateProceduralVariables del ABP `_fix` [D: `G3_dump_antes.json`, grafo `UpdateProceduralVariables`]

Por pie (izq. `K2Node_CallFunction_26`, der. `_31`), cada frame:

| Elemento | Valor leido [D] |
|---|---|
| Nodo | `LineTraceByChannel` (un solo rayo recto, NO esfera/capsula) |
| Canal | `TraceTypeQuery1` (Visibility por defecto [S]), `bTraceComplex=false`, ignora `Character` (via `MakeArray`), `DrawDebugType=None` |
| Origen (Start) | `MakeVector( X,Y de GetSocketLocation("LeftFoot"/"RightFoot") , Z = Z de GetActorLocation )` -> XY del TOBILLO, Z del centro de la capsula |
| Destino (End) | mismo XY, `Z = ActorZ - 150` |
| Ancla | XY en el tobillo; Z de referencia en la capsula (NO en el suelo, NO en la puntera) |
| Valor objetivo | `Select(Index = hit AND NOT IsFalling; Option0 = 0, Option1 = 90 - Distance)` -> `Clamp(-40, 30)` (en este volcado) |
| Interpolacion | `FInterpTo(Current = FootOffsetX, Target, DeltaTime, InterpSpeed = 12)` |
| Salida | `FootOffsetL`, `FootOffsetR` |
| Pelvis | `PelvisOffset = Min(FootOffsetL, FootOffsetR)` (nodo `Min(Float)` tras `Set FootOffsetR`) |
| Constantes implicitas | 90 = semialtura de capsula asumida [S: el valor 90 no se leyo del CharacterMovement en esta sesion] |

Signo: `offset = 90 - Distance`; suelo mas alto bajo el pie -> Distance menor -> offset positivo -> el pie SUBE [C].

**Discrepancia del clamp: RESUELTA y RELEIDA EN VIVO [V] en esta revision** sobre el ABP en memoria (`BlueprintTools.get_node_infos` del grafo `UpdateProceduralVariables`, no un volcado de disco): `K2Node_CallFunction_28` y `_33` = Clamp Min -40 / Max 30; `_29` y `_34` = FInterpTo InterpSpeed 12; `_26` y `_31` = LineTraceByChannel `TraceTypeQuery1`, `bTraceComplex false`, `DrawDebugType None`, `bIgnoreSelf true`. Otros nodos del grafo (no de pies): Clamp 0..7 con FInterpTo 6, Clamp -8..8 con FInterpTo 8, Clamp 0.2..1 con FInterpTo 10. Lectura previa del verificador: `Clamp(-40, 30)` en `K2Node_CallFunction_28` y `_33`, `FInterpTo` velocidad 12 en `_29` y `_34`, `TraceTypeQuery1`, `bTraceComplex false`, `DrawDebugType None`. El '0..35' del encargo era aproximado; el valor real es **-40..30**. No afecta la causa raiz.

### 3.2 Nodo ControlRig en el AnimGraph

Cadena: StateMachine -> Slot -> Inertialization -> ControlRig_1 -> Root [D: orden_graph.md]. Pin `Alpha` = 1.0 (leido en la ronda 6; `node.alpha` NO tiene efecto, manda el pin) [M-previo]. El ControlRig va al final, correcto para IK de pies. `inputMapping` de las variables (FootOffsetL/R, PelvisOffset, LandCrouch, LeanRoll/Pitch): [NO re-leido hoy].

### 3.3 CR_Student_Procedural_fix - como consume los datos [D: `snap_ronda6_final.json`, `pins_rigs.json`]

Orden de ejecucion: BeginExecution -> Set_Spine1 -> Set_Spine2 -> Set_Neck_Lean -> **Set_Hips** -> TwoBoneIK_Left -> TwoBoneIK_Right.

| Cadena | Conexiones leidas |
|---|---|
| Hips | `Get_PelvisOffset -> Add_PelvisLand.A`; `Mul_LandCrouch -> Add_PelvisLand.B`; `Add_PelvisLand.Result -> Make_Hips_Offset.Translation.Z`; `Mul(Get_Hips.Transform, Make_Hips_Offset) -> Set_Hips.Value` |
| Pie izq. | `Sub_FootOffsetL = Get_FootOffsetL - Get_PelvisOffset`; `Sub -> Clamp_LeftOffset` (solo alimenta `Add_LeftFootZ`, huerfano) y `Sub -> Make_LeftFoot_Offset.Translation.Z`; `Mul(Get_LeftFoot.Transform, Make_LeftFoot_Offset) -> TwoBoneIK_Left.Effector`; **`Get_LeftFoot.Transform.Rotation -> TwoBoneIK_Left.Effector.Rotation`** |
| Pie der. | idem con `R` |
| Huerfanos | `Add_HipsZ`, `Add_LeftFootZ`, `Add_RightFootZ` (sus Result no van a ningun lado); `Make_*Foot_Offset.Translation` X/Y quedan sin conectar (=0, intencional) |
| TwoBoneIK | PrimaryAxis (0,-1,0), SecondaryAxis (0,0,1) con SecondaryAxisWeight 0, PoleVectorKind Location, pole (+-12, 60, 28.1), PoleVectorSpace None, Weight 1, bPropagateToChildren True |

Lectura algebraica [C]: `Set_Hips` sube la cadera `P` y los hijos la siguen, luego `Get_Foot` se lee con ese arrastre (`foot_anim + P`) y el efector recibe `foot_anim + P + (FootOffset - P) = foot_anim + FootOffset`. Es decir, el efector final es **solo la posicion de animacion del pie + FootOffset en Z**; PelvisOffset se cancela en el pie y solo desplaza la cadera. Esto supone que la traslacion de `Make_*` se suma en Z global (en `FTransform` A*B la traslacion de B se suma sin rotar por A) [S, coincide con que "sube bien el talon" en pantalla]. El nodo de rotacion NO modifica nada: `Effector.Rotation` = rotacion de animacion del pie [D]. Esto cuadra con la medicion previa [M-previo, `Docs/Avance/2026-10-28_rig-student-fix/informe.md` linea 125], rotacion del hueso Foot rig ON vs OFF a fase igualada (mediana/max, grados):

| Modo del pole | idle | walk | run | jump |
|---|---|---|---|---|
| Location (el rig ACTUAL, `_fix`) | 0.07 / 0.16 | 0 / 1.35 | 0 / 0 | 0 / 0.64 |
| Direction (estado ANTERIOR al arreglo, ya no vigente) | 0 / 0 | 0 / 0 | 0.56 / 2.2 | 0 / 0.6 |

(Correccion rev. 3: la rev. 2 mezclo las filas y cito como 'actuales' las cifras de Direction. Las vigentes son las de Location.) La conclusion no cambia: el rig actual no gira el pie (maximo 1.35 grados en walk).

### 3.4 Por que sube bien el talon y la puntera se hunde; por que al bajar la puntera flota

Datos del esqueleto **releidos en vivo [V]** (`ControlRigTools.get_global_transform`, `initial=true`, `CR_Student_Procedural_fix`, cm):

| Hueso | X | Y | Z |
|---|---|---|---|
| LeftFoot | 6.291 | -1.226 | **7.339** |
| LeftToeBase | 8.258 | 7.575 | **0.782** |
| LeftToe_End | 10.574 | 1.896 | 0.823 |
| RightFoot | -5.997 | -1.222 | **7.339** |
| RightToeBase | -7.964 | 7.757 | **0.782** |
| RightToe_End | -6.023 | 13.666 | 1.382 |

Calculo [C] desde esa tabla: Foot->ToeBase L = sqrt(1.967^2 + 8.800^2 + 6.557^2) = **11.15 cm**; distancia horizontal d = sqrt(1.967^2 + 8.800^2) = **9.01 cm** (R: horizontal **9.20 cm**, 3D 11.29). Coincide con la auditoria del esqueleto. **Hallazgo nuevo:** `LeftToe_End` esta en Y=1.9, es decir ~5.7 cm DETRAS de `LeftToeBase` (Y=7.57): su posicion de bind es incoherente con la derecha (Y=13.67) -> **no usar Toe_End izquierdo como referencia de puntera**; usar `ToeBase` (bola). El talon no existe como hueso [S].

1. La traza esta en el XY del tobillo. Si el rig colocara el tobillo a `suelo(XY tobillo) + 7.34`, la suela estaria apoyada bajo el tobillo. **Correccion rev. 3:** ese es el comportamiento IDEAL; el rig real NO lo cumple, deja el tobillo ~4.5 cm mas bajo (sesgo constante, ver 3.7). El analisis de abajo (`d*tan(theta)`) es el termino de pendiente y se SUMA a ese sesgo.
2. El pie conserva el pitch de la animacion (suela horizontal). En una pendiente theta la superficie bajo la bola esta `d*tan(theta)` mas alta (subiendo) o mas baja (bajando), con `d` = distancia horizontal tobillo->bola = `sqrt(11.15^2 - (7.34-0.78)^2) = sqrt(124.3 - 43.0) = 9.02 cm` (izq.) y `9.20 cm` (der.) [C] (el calculo directo por coordenadas da 9.01 / 9.20).
3. **Subida:** la bola/puntera queda por debajo del plano -> penetra `d*tan(theta)`. **Bajada:** queda por encima -> flota `d*tan(theta)`. El talon (detras del tobillo) hace lo inverso: en subida flota un poco, en bajada se hunde un poco; en el plano que vea el usuario domina la puntera porque `d_puntera > d_talon` [S: longitud de talon no medida, estimada 4-5 cm].

Error esperado en la bola, `e = 9.1 * tan(theta)` [C]:

| Pendiente | tan | Bola (d=9.1 cm) | Toe_End estimado (d~13 cm [S]) |
|---|---|---|---|
| 10 grados | 0.176 | 1.6 cm | 2.3 cm |
| 15 grados | 0.268 | 2.4 cm | 3.5 cm |
| 28 grados (Rampa ThirdPerson) | 0.532 | **4.8 cm** | 6.9 cm |
| 35 grados (Plataforma) | 0.700 | **6.4 cm** | 9.1 cm |

Efectos que agravan [C]/[S]:
- **Retraso del `FInterpTo`**: con velocidad 12 la constante de tiempo es 83 ms y, ante una rampa de entrada, el retraso estacionario es `rate/12`. El objetivo cambia con la zancada (el pie oscila +-30 cm respecto del centro de capsula -> +-16 cm de altura de suelo a 28 grados en ~0.4 s, ~80 cm/s) -> retraso transitorio de hasta ~6-7 cm al caminar [S, ordenes de magnitud, no medido].
- Dos pies interpolan con la misma velocidad, pero la cadera usa `Min(L,R)`: si un pie sube y el otro baja, la cadera sigue al mas bajo y el pie alto puede no alcanzar (ver `Clamp`).
- Pole fijo (+-12, 60, 28.1) en espacio de componente: no sigue el yaw del pie ni la inclinacion [D].

### 3.5 Medicion estatica con colision REAL (sustituye parcialmente al punto 5) [V]+[C]

No se arranco PIE. Se uso el mundo de colision del editor: `SceneTools.trace_world` (solo lectura) sobre la rampa de 28 grados, y se modelo exactamente lo que hace el rig actual [D]/[F]: tobillo a `suelo(XY tobillo) + 7.339`, rotacion del pie = la de la animacion (suela plana), ToeBase a `ankle_z - 6.557` (Z de bind). Luego se trazo el suelo real bajo el XY de la bola (d = 9.03 cm hacia donde mira el pie) y bajo un talon estimado (4.5 cm detras, [S]).

| Caso (rampa 28 grados) | Suelo bajo tobillo (z) | Suelo bajo la bola | Error del hueso ToeBase (+flota / -penetra) | Error de la SUELA bajo la bola |
|---|---|---|---|---|
| Subiendo (mira -X), tobillo x=-350/-250/-150 | 157.80 / 104.63 / 51.46 | 4.80 cm mas alto | **-4.02 cm** (igual en los 3 puntos) | **-4.80 cm** (penetra) |
| Bajando (mira +X), mismos x | idem | 4.80 cm mas bajo | **+5.58 cm** | **+4.80 cm** (flota) |
| Talon estimado (4.5 cm detras), subiendo / bajando | idem | -2.39 / +2.39 | +2.39 / -2.39 | flota 2.4 al subir / penetra 2.4 al bajar |

**Aviso rev. 3:** esta tabla modela un rig IDEAL (tobillo a suelo + 7.339). El rig real deja el tobillo ~4.5 cm mas bajo (3.7), por lo que los errores reales serian `-4.80 - 4.5` al subir y `+4.80 - 4.5` al bajar si el sesgo fuese puro; sin medir en PIE. Lectura: el error de la suela es `d*tan(28) = 9.03 * 0.5317 = 4.80 cm` [C], reproducido por trazas reales (el hueso ToeBase queda 0.78 cm por encima de la suela, de ahi -4.02 / +5.58 en el hueso). Es **simetrico en la suela y NO depende de la altura en la rampa**, como predice la geometria. Es una prediccion con colision real, **no una lectura de huesos animados en PIE**: confirma el orden de magnitud y el signo (sube = hunde, baja = flota) pero no descarta efectos dinamicos (interpolacion, animacion de andar).

### 3.6 Comprobacion de que `Effector.Rotation` SI rota el pie [V]+[F]

La duda que dejaba la causa #1 sin respaldo: en `TwoBoneIK` (Basic IK) el efector, rota el hueso final? **Si, con dos pruebas independientes:**
1. [V] Pines en vivo de `TwoBoneIK_Left/Right` en `CR_Student_Procedural_fix`: `EffectorBone = LeftFoot / RightFoot` (no 'None'), `Weight 1.0`, `bPropagateToChildren True`, `SecondaryAxisWeight 0`, `PoleVectorKind Location`, `Pole = (+-12, 60, 28.1)`, `bEnableStretch False`, `DebugSettings.bEnabled False`.
2. [F] `RigUnit_TwoBoneIKSimple.cpp` (UE 5.8): `FTransform TransformC = Effector;` (linea 151) -> tras resolver, `Hierarchy->SetGlobalTransform(CachedEffectorItemIndex, TransformC, bPropagateToChildren)` (linea 218) **si hay hueso efector**. Es decir el hueso `Foot` recibe la ROTACION completa de `Effector.Rotation` (con `Weight=1`; con Weight<1 hace Slerp, lineas 204-211). Por tanto cambiar `Effector.Rotation` gira el pie y la rotacion es el punto de intervencion correcto.
3. Aviso [F]: el nodo `FRigUnit_TwoBoneIKSimple` ('Basic IK') esta marcado `Deprecated = "4.25"` en el codigo (reemplazo: `FRigUnit_TwoBoneIKSimplePerItem`, mismo comportamiento, pines `ItemA/ItemB/EffectorItem`). Funciona en 5.8 pero conviene migrar al hacer el cambio (`GetUpgradeInfo` ya mapea los pines).

### 3.7 NUEVO rev. 3: sesgo vertical constante del rig actual (`90 - Distance` frente a la realidad) [V]+[D]+[C]

Lecturas en vivo [V] (CDO de `BP_ThirdPersonCharacter`): `CollisionCylinder` `capsuleHalfHeight 90`, `capsuleRadius 35`; `CharacterMesh0` `relativeLocation z = -94.5`; CharacterMovement `walkableFloorAngle 44.765`, `maxStepHeight 30`, `maxWalkSpeed 600`, `maxAcceleration 1500`. El rig asume `90` y el mesh esta a `-94.5`, no `-90`.

Datos de huesos ANIMADOS ya medidos por la ronda 5/6 [D] (`evidencia/sweep_OFF.json` y `sweep_LOCX12.json`, mundo, cm; suelo z=0 deducido abajo):

| Escena | Config | Foot z (mediana / min) | ToeBase z (mediana / min) |
|---|---|---|---|
| idle izq. | rig OFF | 5.04 / 4.99 | -1.52 / -1.56 |
| idle izq. | rig ON (Location X=12) | 2.85 / 2.84 | **-3.71** / -3.72 |
| walk izq. (min = apoyo) | OFF | 9.39 / 5.48 | 1.80 / -1.24 |
| walk izq. (min = apoyo) | ON | 7.24 / 3.33 | -0.35 / **-3.39** |
| run izq. (min = apoyo) | OFF | 20.34 / 4.73 | 11.88 / -2.09 |
| run izq. (min = apoyo) | ON | 18.19 / 2.58 | 9.73 / **-4.24** |

`ActorLoc.z = 92.15` en todas las muestras. Derivacion [C]: con capsula de 90, la capsula flota 2.15 cm sobre el suelo (holgura normal de CharacterMovement), suelo en z=0. El rig ON baja todo ~2.15 cm (idle 5.04 -> 2.85; ya anotado por la ronda 6 como 'el rig baja el cuerpo ~2.15 cm') porque `offset = 90 - Distance = 90 - 92.15 = -2.15`: confunde la holgura de la capsula con una necesidad de bajar el pie. Ademas, con el mesh a -94.5 el origen del mesh queda en z = 92.15 - 94.5 = -2.35 y el ToeBase (ideal 0.78 sobre el suelo) aparece a -1.52 con el rig OFF, 2.3 cm bajo el suelo, coherente con -2.35. Formula del rig real en suelo plano [C]: `tobillo_final = (ActorZ - 94.5 + 7.34) + (90 - D) = suelo + 2.84` (medido 2.85, cuadra al decimo), cuando lo ideal es `suelo + 7.34`. **Sesgo = -4.5 cm** en todo el pie.

Alcance honesto: (a) el suelo z=0 del sweep se DEDUCE del algebra (D=92.15); los JSON no lo registran. (b) Es la posicion del HUESO; no se sabe cuanto sobresale la malla bajo el hueso, asi que el hundimiento visual en plano NO esta demostrado. (c) **Contradice parcialmente el sintoma de Franco**: un sesgo de -4.5 cm sumado al termino de pendiente daria al subir ~-9.3 cm en la bola y al bajar solo ~+0.3 cm (casi sin flote), pero Franco ve flotar al bajar. O la malla no sigue el hueso como se supone, o domina otro efecto (3.8). **No resuelto sin PIE.** Es un hallazgo de primera clase porque cambia el diseno: el objetivo del tobillo debe ser ABSOLUTO (`suelo_z + AnkleHeight`), no `90 - D`.

### 3.8 NUEVO rev. 3: retraso de `FInterpTo` en apoyo, cuantificado [C]

`FInterpTo` es un filtro de primer orden con constante de tiempo `tau = 1/InterpSpeed` = 83 ms (velocidad 12). Si el objetivo cambia a tasa constante `r` (cm/s), el error estacionario es `r/12`. En apoyo el pie esta quieto en el mundo mientras la capsula avanza a velocidad `v` por la rampa: el objetivo `90 - D` varia a `r = v*tan(theta)` [C, modelo: pie plantado]. Con theta = 28 grados (`tan` = 0.5317): v = 150 cm/s -> r = 80 cm/s -> **retraso 6.6 cm**; v = 250 -> 11.1 cm; v = 600 (maxWalkSpeed del CDO) -> 26.6 cm (el clamp -40/30 lo limitaria). Signo: al SUBIR el objetivo del offset disminuye, el filtro va retrasado (offset demasiado alto: el pie flota); al BAJAR el offset queda demasiado bajo (el pie se hunde). Es decir, da el signo CONTRARIO al del termino geometrico (3.4) en el pie completo y del mismo orden de magnitud o mayor; por eso no se puede descartar, y el resultado neto observado depende de la velocidad real, que NO se midio ([NO MEDIDO]). Para un retraso <= 0.5 cm a 80 cm/s haria falta `InterpSpeed >= 160/s`: en la practica NO interpolar el objetivo de apoyo (el suelo es determinista) y limitar solo la tasa para absorber saltos bruscos (bordes, gradas).

## 4. Que falta (punto 3) y comparacion con el enfoque estandar de UE5

| Falta | Estado actual | Necesario |
|---|---|---|
| Normal de la superficie por pie | no se lee (solo `Distance`) [D] | `ImpactNormal` de `BreakHitResult` por pie |
| Rotacion del pie hacia la normal (pitch/roll) con limites | no existe; `Effector.Rotation` = rotacion de animacion [D] | cuaternion de alineacion con limite (p. ej. +-35 grados pitch, +-20 roll) |
| Traza de bola/puntera independiente | no existe [D] | segundo trace en `LeftToeBase/RightToeBase` para pitch fino y para bordes/gradas |
| Solucion de pelvis | `Min(L,R)` sin rango, sin suavizado propio [D] | `min` para bajar, limite de extension de pierna (42.3 cm largo total de pierna [M-previo]) y suavizado propio |
| Interpolacion | `FInterpTo` 12 [D] | velocidad alta + limite de tasa; subir mas rapido que bajar |
| Apagar IK en el aire | solo el offset se pone a 0 con `IsFalling` [D] (el IK sigue evaluando) | `Alpha` del nodo por estado (suelo=1, aire=0..0.3), con inercializacion |
| Foot-planting | no hay [D]; el estudio previo notaba que el pie no se clava [M-previo] | bloquear XY/rotacion en apoyo si hay curva de contacto o velocidad de pie < umbral |
| Alpha del Control Rig en subida/bajada | pin Alpha=1 fijo [M-previo] | Alpha dinamico por variable (0 en salto/aterrizaje duro, 1 en suelo) |

### Comparacion con el enfoque estandar de Epic (honestidad sobre las fuentes)

- **Fuentes oficiales consultadas:** `dev.epicgames.com/.../control-rig-full-body-ik-in-unreal-engine` (si cargo) y `.../control-rig-in-unreal-engine` (no menciona foot IK). `.../foot-ik-in-unreal-engine` devolvio solo la tabla de contenidos (sin texto utilizable). La busqueda web no devolvio documentacion oficial de Epic sobre foot placement; solo guias de terceros (mocaponline, 80.lv, Vulkan tutorial generico). Context7 no se uso (herramienta no relevante para docs de motor).
- **Lo que dice la doc oficial de Full Body IK** (resumen de la pagina): se anade el nodo FBIK a `Forwards Solve`; hay que fijar `Root` (normalmente cadera) y un efector por control; `Root Behavior` tiene `Pre Pull`, `Pin to Input`, `Free`; para que la cadera no se mueva demasiado se usan Bone Settings (rigidez 0.8 en el ejemplo); describe FBIK como herramienta de "ground alignment" pero **no da una receta paso a paso de foot placement**; el ejemplo de tobillo limita la rotacion en Z a -70..70.
- **Enfoque estandar (conocimiento general, [S] sin cita oficial):** (1) trazas por pie desde el ABP o el rig; (2) offset vertical por pie; (3) cadera baja al pie mas bajo (`min`) con suavizado; (4) IK de 2 huesos (Basic IK / Leg IK) con polo; (5) **rotacion del pie a la normal** (el rig del Mannequin 5 `CR_Mannequin_FootIK`, ya incluido en el proyecto bajo `/Game/Characters/Mannequins/Rigs`, hace exactamente trazas + normal + pelvis + IK; no lo abri hoy, [NO MEDIDO]); (6) Alpha por estado. Es decir: lo que tenemos cubre (1)-(4) parcialmente y **falta (5)**, que es justo el sintoma.
- **FBIK vs Basic IK:** FBIK puede resolver pie+cadera+columna a la vez pero exige configurar efectores y rigidez; con 41 huesos, Hips escala 100/roll 90 [M-previo] y un solo rig de 2 piernas, **Basic IK + alineacion de efector es la via de menor riesgo**. Reservar FBIK para el rig final de Carlos (C-M3).

## 5. Causa raiz, por orden de probabilidad

| # | Causa | Probabilidad | Base |
|---|---|---|---|
| 1 | El efector del tobillo solo recibe traslacion Z; la rotacion es la de la animacion (suela plana) -> error `d*tan(theta)` en la bola | Alta: unica causa que explica el signo de AMBOS sintomas con geometria; NO demostrada en movimiento (sin porcentaje) | [D] pines + [C] geometria + [V] trazas reales en la rampa (3.5) + [V]+[F] `EffectorBone` set y `TransformC=Effector` (3.6). Falta solo PIE con huesos animados |
| 2 | Trazas ancladas al tobillo, sin traza de bola -> el rig no conoce la altura bajo la puntera | Alta, depende de #1 | [D] |
| 2b | Sesgo constante -4.5 cm por `90 - D` + mesh a -94.5 + holgura de capsula 2.15 (3.7) | Alta como hecho a nivel de hueso (medido en sweeps); su efecto visual y su encaje con el sintoma de bajada: no resuelto | [D] sweeps + [V] CDO + [C] |
| 3 | `FInterpTo` 12: retraso `v*tan(theta)/12` en apoyo (3.8), signo contrario al geometrico en el pie completo | Media; magnitud depende de `v`, no medida | [C] modelo, [S] supuestos |
| 4 | Desfase de `90` frente a la capsula/mesh reales. **Correccion rev. 3:** NO se cancela (el objetivo no es absoluto, es `anim + (90 - D)`); se traslada 1:1 y esta medido en 3.7. En pendiente el centro de capsula queda ~`r*(1/cos(theta)-1)` mas alto (r = 35 leido en vivo -> 4.7 cm a 28 grados) y eso entra en D | Media-alta | [V] hh 90, r 35, mesh -94.5; [C] |
| 5 | Alpha del CR / IK activo en transicion y pole fijo -> pequenos errores de rodilla/tobillo | Baja | [D] |
| 6 | Skin / escala 100 en Hips afectando offsets | Baja (la traslacion Z es global y se mide bien por huesos) | [M-previo] |

## 6. Diseno propuesto (punto 4)

### 6.1 Variables nuevas (ABP `_fix` y CR `_fix`)

| Variable | Tipo | Valor inicial | Uso |
|---|---|---|---|
| FootNormalL / FootNormalR | Vector | (0,0,1) | `ImpactNormal` del trace de tobillo, 0,0,1 si no hay hit |
| ToeGroundZL / ToeGroundZR | float | 0 | altura de suelo bajo la bola (para pitch fino) |
| FootPitchL / FootPitchR | float (grados) | 0 | pitch objetivo, clamp (-35, 35) |
| FootRollL / FootRollR | float (grados) | 0 | roll objetivo, clamp (-20, 20) |
| FootIKAlpha | float | 1 | `Alpha` del nodo CR; 0..0.3 en aire |
| FootRateUp / FootRateDown | float (cm/s) | 400 / 250 | limite de tasa del offset (sustituye a `FInterpTo`, ver 3.8) [S] |
| GroundRelZL / GroundRelZR | float (cm) | 0 | suelo bajo el tobillo relativo al origen del mesh (objetivo absoluto, 3.7) |
| FootTraceHalfUp / FootTraceDown | float (cm) | 50 / 80 | rango del trace relativo al tobillo |
| ToeBaseDistH | float | 9.1 | distancia horizontal tobillo->bola (de [C]) |
| AnkleHeight | float | 7.34 | altura del tobillo sobre la suela |

### 6.2 Cambios en UpdateProceduralVariables

1. Mover el origen del trace a `ankleWorld + (0,0,+50)` y el destino a `ankleWorld + (0,0,-80)` (hoy: `ActorZ` -> `ActorZ-150`). Sustituir el calculo `90 - Distance` por `FootOffset = (hit.Z + AnkleHeight) - ankle_anim_Z` **Rev. 3:** hacerlo ABSOLUTO es obligatorio (3.7): el ABP envia al rig `GroundRelZ = hit.Z - MeshComponent.WorldZ` (suelo relativo al origen del mesh) y el rig calcula `FootOffset = (GroundRelZ + AnkleHeight) - Get_Foot.Z_anim`, de modo que ni el 90, ni el -94.5, ni la holgura de 2.15 influyen. Riesgo: no leer la Z de animacion con `GetSocketLocation` en el ABP (devuelve la pose final del frame anterior, ya con IK: realimenta); leerla dentro del rig (`Get_Foot`, pre-IK).
2. Leer `ImpactNormal` del `BreakHitResult` y guardar `FootNormalL/R`.
3. Anadir segundo `LineTrace` en `LeftToeBase`/`RightToeBase` (mismo canal/ignora) -> `ToeGroundZ`. `pitch = atan2(ToeGroundZ - AnkleGroundZ, ToeBaseDistH)`, mezclado con el pitch de la normal.
4. Pelvis: `PelvisOffset = Min(offL, offR)` con tope de extension (`>= -(maxLegExtension - actual)`) y `FInterpTo` propio (subida 25, bajada 15).
5. `FootIKAlpha = IsFalling ? 0 : 1` con `FInterpTo` (6-10) -> pin `Alpha` del nodo.

### 6.3 Cambios en CR_Student_Procedural_fix

Insertar entre `Get_LeftFoot.Transform.Rotation` y `TwoBoneIK_Left.Effector.Rotation` (y lo mismo para la derecha):

Nombres de struct (UE 5.8) verificados en `Plugins/Runtime/RigVM/Source/RigVM/Public/RigVMFunctions/Math/RigVMFunction_MathQuaternion.h` [F]. Correccion: el prefijo `RigUnit_` de la rev. 1 era incorrecto (nombre viejo, solo redirigido por `StructRedirects`); el correcto es `RigVMFunction_`. `ControlRigTools` NO tiene `list_unit_types` (la rev. 1 lo citaba por error): sus metodos son `create_node`, `list_nodes`, `connect_pins`, `set_pin_value`, etc.; el nombre del struct se pasa a `create_node` y debe comprobarse con una creacion real en la copia `_fix` al implementar [pendiente, no se creo para no mutar].

1. `RigVMFunction_MathQuaternionFromTwoVectors` (DisplayName 'From Two Vectors'; pines `A`:FVector in, `B`:FVector in, `Result`:FQuat out; 'shortest rotation between the two vectors') con A = (0,0,1), B = `FootNormal` -> `q_align` [F]. Alternativa: `RigVMFunction_MathQuaternionFromAxisAndAngle` (linea 135 de la cabecera).
2. `RigVMFunction_MathQuaternionSlerp` (DisplayName 'Interpolate'; pines `A`,`B`:FQuat in, `T`:float in, `Result`:FQuat out) con A = identidad, B = `q_align`, T = clamp(35/angulo, 0, 1) para el limite [F].
3. `RigVMFunction_MathQuaternionMul` (aggregate binario 'Multiply', pines `A`,`B`,`Result` [F]) `q_align * Get_Foot.Rotation` -> `Effector.Rotation` (que `Effector.Rotation` gira el pie queda confirmado en 3.6). Orden: la alineacion se aplica en espacio mundo, para conservar el yaw de la animacion. Con Hips escala 100/roll 90 esto es seguro solo si el efector se evalua en espacio global; [S, verificar con una prueba].
4. Subir el Z del efector `N * (AnkleHeight/cos(angulo) - AnkleHeight)` para que la suela inclinada siga tocando el plano (a 28 grados: `7.339*(1/cos28 - 1) = +0.97 cm`; a 35: `7.339*(1/cos35 - 1) = +1.62 cm`) [C]. Correccion: la rev. 1 decia +0.70 y +1.5.
5. Pole: pasar a `Get_Foot.Transform` desplazado `+60 Y` en espacio del pie, o recalcularlo desde la rotacion del yaw del pie.
6. Opcional fase 2: `FRigUnit_SetRotation` (DisplayName 'Set Rotation', pines `Item`, `Space`, `Value`:FQuat, `Weight`, `bPropagateToChildren` [F]; cabecera `RigUnit_SetTransform.h`; este SI conserva el prefijo `RigUnit_` porque vive en ControlRig, no en RigVM) sobre `LeftToeBase`/`RightToeBase` con pitch `(ToeGroundZ - AnkleGroundZ)`, limite +-25 grados, `Weight` 1 (necesario para gradas/bordes).

### 6.4 Valores iniciales

Clamp pie (-10, 35); pitch +-35, roll +-20; Alpha aire 0.0-0.3; `ToeBaseDistH` 9.02 (izq.) / 9.19 (der.) y `AnkleHeight` 7.34 son [V] (leidos en vivo). Clamp, pitch/roll y Alpha son valores de partida [S] sin medicion (35 de pitch cubre la rampa mas empinada, 35 grados; el roll 20 es un margen). **Rev. 3, interpolacion:** los 25/15 de la rev. 2 se descartan por calculo (3.8: para <= 0.5 cm de retraso a 80 cm/s hace falta velocidad >= 160/s). Inicio: sin `FInterpTo` en apoyo; limitador de tasa 400 cm/s subiendo y 250 bajando [S], a calibrar con el plan de prueba.

## 7. Plan de prueba medible (punto 4 y 5)

### 7.1 Metrica

Para cada frame de la prueba, por pie: `err_bola = z_mundo(ToeBase) - z_suelo_bajo_ToeBase_XY - 0.8` (0.8 = altura de `ToeBase` sobre la suela). `err < 0` penetracion, `> 0` flotacion. Mismo calculo para `Foot` (tobillo, referencia 7.34) y, si se puede leer, `Toe_End`. Ground truth: `SceneTools.trace_world` (o `LineTrace` en el actor sonda) sobre el XY de cada hueso. Maximo, mediana y P95 por escenario.

### 7.2 Metodo (reutiliza el actor sonda de la Ronda 5)

`BP_ProbeDriver` en `/Game/_Test` leyendo `GetSocketLocation` de Foot/ToeBase por Tick (ya usado en `evidencia/scripts_medicion/lib.py`, `sweep.py`), y `AddMovementInput` por propiedades (inyeccion de teclas denegada). Añadir al sonda 2 traces por pie hacia abajo en el XY de cada hueso y exponer `GroundZ_*`. Escenarios: subir y bajar la Rampa de ThirdPerson (28 grados) y la Plataforma (35 grados), en idle, walk y run; mediciones en 3 configuraciones (rig OFF = Alpha 0, rig actual, rig nuevo).

**Medicion del defecto actual (punto 5): PARCIAL.** La medicion de huesos animados requiere PIE y arrancar la sonda (mutaria el nivel/camara/PIE), asi que NO se hizo. Lo que si se midio es la version estatica con colision real (3.5): suela -4.80 / +4.80 cm en 28 grados. (La rev. 1 dijo que el editor estaba apagado; ahora esta corriendo, y la unica razon para no medir en PIE es la regla de no tocarlo.) Prediccion testeable para PIE [C]: con el rig actual, `err_bola` en reposo sobre la rampa de 28 grados debe ser **-4.8 +/- 1 cm subiendo y +4.8 +/- 1 cm bajando** (y ~-6.4/+6.4 en 35 grados); en movimiento, mas el retraso del `FInterpTo`. Si el valor medido difiere mucho (< 2 cm o > 8 cm), la causa #1 no basta.

### 7.3 Criterios de aceptacion

| Criterio | Umbral |
|---|---|
| Bola en reposo (idle) en 28 y 35 grados, subiendo y bajando | `abs(err_bola) <= 0.5 cm` [S: umbral perceptual de partida] |
| Bola en apoyo durante walk/run | `abs(err_bola) <= 1.0 cm` P95, max 1.5 cm [S] |
| Sesgo en suelo plano (nuevo, 3.7) | idle sobre z=0: Foot z = 7.34 +/- 0.3 y ToeBase z = 0.78 +/- 0.3 [C] (hoy 2.85 y -3.71) |
| Tobillo (Foot) en apoyo | `abs(err_tobillo) <= 0.5 cm` |
| Giro del pie entre frames | <= 1.5 x el maximo de la propia animacion OFF en la misma escena (a medir en la fase D). El '15 grados/frame' de la rev. 2 era [S] sin base (900 grados/s a 60 fps, demasiado laxo) |
| Cadera | oscilacion vertical <= 1 cm en tramo recto de rampa |
| Rodilla | sin regresion respecto a Ronda 6 (`abs(lat)` mediana <= 1.25 cm en run) |
| Suelo plano | sin regresion (offsets ~0, pitch ~0) |

## 8. Esfuerzo, riesgos y automatizacion

| Fase | Contenido | Horas |
|---|---|---|
| A | Normal por pie + cuaternion de alineacion con limite en el efector (CR + ABP) | 4-6 |
| B | Traza de bola + pitch fino + compensacion de altura del tobillo | 2-3 |
| C | Pelvis con limite, interpolacion asimetrica, Alpha por estado, pole | 3-4 |
| D | Automatizar la medicion (sonda con traces, tablas A/B) y ajustar | 3-4 |
| **Total** | | **12-17 h** |

Riesgos: (1) ejes del rig (Hips escala 100, roll 90, ejes de pierna volteados [M-previo]) pueden invertir el signo del pitch -> probar con una rampa y desde ambos sentidos; (2) la rotacion del efector SI se aplica al hueso (3.6, codigo fuente + pines `EffectorBone`), pero el sentido de los ejes con Hips escala 100/roll 90 no esta probado: validar con un valor fijo de 20 grados y mirar el signo; (2b) el nodo Basic IK esta deprecado desde 4.25 (3.6 punto 3); (3) la rodilla puede girar al inclinar el pie (re-ajustar el pole); (4) la medicion en movimiento sigue pendiente de PIE; (5) otros agentes estan editando los mismos grafos: coordinar antes de implementar.

Automatizable por MCP/Python del editor [S, segun lo que hicieron las rondas previas]: crear variables y nodos en CR (`ControlRigTools`), crear/conectar nodos del ABP (`BlueprintTools`, `set_pin_value`), compilar, medir (sonda), tablas. A mano: elegir signos de eje por prueba visual, afinar limites, guardar (Ctrl+S) y revisar la rodilla.

## 9. Preguntas abiertas

1. Cual es la pendiente real de las rampas de AnimTest (necesita cargar ese nivel; hoy el editor tiene abierto `Lvl_ThirdPerson`)? y **en que rampa vio Franco el defecto** (28 grados de ThirdPerson o las de AnimTest)? No se puede deducir de los datos: pregunta abierta.
2. (Resuelta) El clamp real es `-40..30` [verificador, lectura en vivo].
3. (Resuelta en parte, rev. 3) Capsula del CDO: radio 35, semialtura 90 [V]; mesh a z=-94.5 [V]. Falta saber si la instancia en el nivel/PIE lo sobreescribe y cuanto sobresale la malla bajo el hueso `Foot`/`ToeBase` (define si el sesgo de 3.7 se ve).
4. Toe_End: existe, pero `LeftToe_End` esta mal posicionado en bind (Y=1.9, detras de ToeBase, seccion 3.4): corregirlo o ignorarlo? El talon no es un hueso.
5. Se quiere resolver gradas ademas de rampas (requiere traza de bola obligatoria, fase B)?
7. (rev. 3) A que velocidad probaba Franco (walk o run) y mira el pie en apoyo o en vuelo? El balance entre 3.4, 3.7 y 3.8 depende de eso.
6. Se acepta usar `RigVMFunction_MathQuaternionFromTwoVectors` (nombre confirmado en cabeceras, creacion real por probar) o se prefiere el rig `CR_Mannequin_FootIK` como plantilla?

## 10. Registro de lo verificado y lo supuesto

- **Verificado con lectura real (disco):** pines/conexiones de `UpdateProceduralVariables` (trace origen/destino/canal/clamp/interp) y de `CR_Student_Procedural_fix`; poses/escala/rotacion de todas las rampas de ThirdPerson (28 y 35 grados); nombres y escalas de las 3 rampas con nombre y de las SM_Ramp de AnimTest; PoleVector y ejes del TwoBoneIK.
- **Verificado EN VIVO en esta revision [V]:** pines de `TwoBoneIK_Left/Right` (EffectorBone, Weight, Pole, SecondaryAxisWeight); posiciones globales bind de Foot/ToeBase/Toe_End L/R; propiedades y colision de la rampa de 28 grados; angulo 28.0 por 13 trazas con impacto (releido rev. 3); simulacion estatica del error de suela; PIE apagado; nivel activo = ThirdPerson. Clamp -40/30, FInterpTo 12 y canal de trace releidos en vivo en la rev. 3.
- **Verificado en codigo fuente [F]:** `TransformC = Effector` y `SetGlobalTransform(Effector)`; nombres/pines de `RigVMFunction_MathQuaternion{FromTwoVectors,Slerp,Mul}` y `FRigUnit_SetRotation`; deprecacion de `FRigUnit_TwoBoneIKSimple`.
- **Heredado de mediciones previas (no re-medido):** rotacion de pie ON vs OFF (informe ronda 6, linea 125).
- **Verificado EN VIVO en la rev. 3 [V]** (cliente Python, editor corriendo): ABP `_fix` en memoria: Clamp -40/30, FInterpTo 12, TraceTypeQuery1, bTraceComplex false, DrawDebugType None; pines de TwoBoneIK_Left/Right (EffectorBone LeftFoot/RightFoot, Weight 1, SecondaryAxisWeight 0, PoleVector (+-12, 60, 28.1), Location, bPropagateToChildren True); huesos Foot/ToeBase/Toe_End (Foot z 7.339, ToeBase z 0.782, horizontal 9.02 / 9.19, 3D 11.15 / 11.29); rampa de 28 grados: en y=-540, 13 trazas con impacto cada 30 cm (x -450..-90) dan pendiente -0.5317 constante = 28.0 grados, sin escalones, suelo plano z=0 fuera de la rampa; CDO capsula 90/35, mesh z -94.5, walkable 44.765, maxWalkSpeed 600; nivel activo ThirdPerson.
- **Sigue NO verificado / suposicion:** angulos de AnimTest; geometria nativa de SM_Ramp; si la instancia de PIE sobreescribe capsula/mesh; sesgo visual de 3.7 (solo hueso); velocidad real en rampa; magnitud real del defecto (prediccion `d*tan(theta)` por contrastar en PIE); creacion real de los nodos de cuaternion via `create_node` (nombres solo en cabeceras); estructura de docs oficiales de Epic (solo FBIK leida); el talon estimado (4.5 cm); rampa de 35 grados en vivo (su nivel no esta cargado); huesos animados en PIE.

Scripts de apoyo (solo lectura, en el scratchpad de la sesion, no en el proyecto): `t2.py` (pines TwoBoneIK), `t5.py`/`t6.py` (actores y propiedades de rampa), `t7.py` (huesos), `t8.py`/`t9.py` (trazas y simulacion).

### 10.1 Mutaciones (respuesta al punto 6 del verificador)

Rev. 3: tampoco guardo nada. Se hicieron solo lecturas por el cliente Python (`get_*`, `list_*`, `find_*`, `trace_world`, `describe_toolset`); no se llamo a `set_*`, `create_*`, `connect_*`, compilar, guardar, PIE ni `load_level`. Un `find` posterior (17:00) no halla `.uasset`/`.umap`/Config modificados despues de las 16:44; las copias `_fix` siguen en 16:43:14. No puedo atribuir quien las guardo a las 16:43 (la regla dice que los agentes de graph no guardan; la rev. 1 y esta no lo hicieron, el resto lo sabe el orquestador). Rev. 2: esta revision hizo solo llamadas de lectura. No llamo a `set_*`, `create_*`, `connect_*`, `StartPIE`, `load_level`, ni compilo ni guarda nada. `mtime` observados al inicio de la revision (16:46-16:49): `CR_Student_IK` y `CR_Student_Procedural` originales 15:27; ABP original 2026-10-27 22:48; `_Backup_v5` 2026-10-10; `Lvl_AnimTest.umap` 15:27; `Lvl_ThirdPerson.umap` 2026-07-29. Las copias `CR_Student_IK_fix` y `CR_Student_Procedural_fix` se guardaron a las 16:43:14, **antes** de esta revision y no por ella. De la rev. 1 no puedo demostrar quien guardo a las 16:43. El nivel activo del editor (`Lvl_ThirdPerson`) no lo cambio esta revision.

Fuentes: <https://dev.epicgames.com/documentation/en-us/unreal-engine/control-rig-full-body-ik-in-unreal-engine>, <https://dev.epicgames.com/documentation/en-us/unreal-engine/control-rig-in-unreal-engine>, <https://docs.vulkan.org/tutorial/latest/Advanced_glTF/Procedural_Animation_IK/04_foot_placement.html>.
