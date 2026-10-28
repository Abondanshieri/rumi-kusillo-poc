# Informe de avance - Correccion del rig del Student (piernas deformes)

Fecha: 2026-10-28 | Hito: F-M2 (blockout sobre rig provisional)

## Objetivo
Encontrar y corregir por que las piernas del personaje Student se ven deformes en Unreal 5.8, trabajando solo sobre copias `_fix` sin tocar los originales.

## Que se hizo
**Problema.** Piernas deformes. Los bloques rojos que se veian no son zapatos: son debug de LineTrace.

**Hallazgos medidos.**
- El eje del hueso es -Y.
- Hips tiene escala 100 y roll 90.
- Los ejes IK se verificaron y son correctos.
- Los offsets de pie estan inertes porque los nodos Add_*FootZ quedaron huerfanos.

**Cambios (solo en copias).**
- `CR_Student_Procedural_fix`: lean recableado a Euler.X / Euler.Z.
- `CR_Student_IK_fix`: PrimaryAxis (0,-1,0) y SecondaryAxis (0,0,1).
- `Student_Skeleton_AnimBlueprint_fix`: apunta al rig `_fix`.

**Prueba A/B (D0).** Se comparo alpha 1 vs alpha 0 del nodo ControlRig en el ABP `_fix`. Resultado: NO CONCLUYENTE. Personaje en idle visto de perfil, sin diferencia visible y sin deformacion visible desde ese angulo. No se puede culpar ni absolver al rig. El alpha quedo en 1, compilado y sin guardar.

**Orden de carpetas (Archivista).** No se movio nada: `get_referencers` y `exists` fallan con "Asset does not exist" para assets validos, asi que no se pudo re-verificar los 34 assets SIN_USO de `/Game/Characters/Rumi`. Inventario por escaneo de disco (398 assets): Student 20 (12 intocables, 5 en uso, 3 a revisar); Rumi 53 (12 en uso, 7 a revisar, 34 sin uso). Ver `evidencia/movimientos_archivo.txt`.

## Evidencia
Recortes del muneco en `capturas/` (01 y 02: idle de perfil alpha 1 y alpha 0; 03 y 04: prueba previa; 05 y 06: recortes adicionales). Manifiesto en `evidencia/movimientos_archivo.txt`.

## Decisiones
- No borrar ni mover ningun asset; los 34 SIN_USO solo son candidatos a una carpeta de archivo.
- Originales (`CR_Student_*`, ABP, Backup_v5, BP_ThirdPersonCharacter) sin modificar.

## Pendientes
- Guardar con Ctrl+S el orden del graph.
- Decidir que hacer con los originales que tienen cambios sin guardar (BP_ThirdPersonCharacter, CR_Student_IK, CR_Student_Procedural aparecen con asterisco).
- Validar el sentido del lean.
- Repetir la prueba A/B con vista frontal.
- Reintentar el archivado tras reiniciar el MCP/editor, o con autorizacion explicita.

## Bloqueos
- Herramientas de registro de AssetTools rotas (get_referencers, exists, list_folders).
- La vista de perfil no permite ver el cruce de piernas.

## Prueba A/B de frente (rig activo vs. desactivado)

- `capturas/06_frente_rig_on.png`: Alpha del Control Rig = 1. Las piernas se cruzan hacia adentro y las rodillas quedan juntas.
- `capturas/07_frente_rig_off.png`: Alpha = 0. Las piernas quedan más rectas y separadas, aunque el pantalón sigue viéndose delgado.
- Conclusión provisional: el rig aporta parte de la deformación (cruce hacia adentro). Queda una parte residual que parece venir del esqueleto o del skin (Hips con escala 100 y roll 90). No es concluyente: las dos capturas están en fases distintas del idle.
- Alpha restaurado a 1 y ABP `_fix` recompilado; se verificó con lectura de `node.alpha`.
- Siguiente prueba: `SecondaryAxisWeight = 0` en los dos `TwoBoneIK` de `CR_Student_Procedural_fix`.

## Corrección aplicada: SecondaryAxisWeight = 0

- En `CR_Student_Procedural_fix`, `TwoBoneIK_Left` y `TwoBoneIK_Right` pasaron de `SecondaryAxisWeight` 1 a 0 (leído de vuelta: 0.0 en ambos).
- `capturas/08_frente_secondaryweight0.png`: con el rig activo las piernas quedan rectas y paralelas, sin el cruce hacia adentro.
- Causa probable: el eje secundario (0,0,1) contra el pole forzaba una torsión de la pierna en el esqueleto Mixamo con Hips escala 100 y roll 90.
- Falta validar en movimiento (walk, run, jump) y revisar el sentido del lean.

## Ronda 3 - Pulido de piernas (tobillos) y debug

- Antes/despues `UpdateProceduralVariables` (ABP `_fix`, nodos `K2Node_CallFunction_26` y `_31`, LineTraceByChannel): `DrawDebugType` ForOneFrame -> None (leido de vuelta: None). Ya no aparecen las lineas rojas en los pies (`capturas/09_idle_espalda_footrot_debugoff.png`).
- Hipotesis 1 (rotacion del tobillo): TwoBoneIK solo traslada el efector; el pie solo hereda la rotacion de la pantorrilla. En `CR_Student_Procedural_fix` se anadieron `Set_LeftFoot_Rot` y `Set_RightFoot_Rot` (RigUnit_SetRotation, GlobalSpace, Weight 1, bPropagate True) en cadena tras `TwoBoneIK_Right` (Set_Hips -> IK_Left -> IK_Right -> Set_LeftFoot_Rot -> Set_RightFoot_Rot). `Value` = `Get_*Foot.Transform.Rotation` (la rotacion del pie de la pose de animacion, leida antes del IK). Conexiones leidas de vuelta OK. Rig y ABP `_fix` compilados sin errores en el log.
- Resultado en idle (espalda): piernas rectas, pies paralelos, sin regresion (09). Alpha del nodo `AnimGraphNode_ControlRig_1` = 1 (leido).
- NO verificado en movimiento: el control por teclado automatico (inyeccion de teclas) fue denegado por el sistema de permisos, asi que walk/run/jump/aterrizaje y la vista de perfil quedan pendientes de prueba manual (ver pendientes).
- Pendiente de validar: que `Get_*Foot` conserve el valor pre-IK en la ejecucion (si el pie queda mal en movimiento, revertir borrando los dos nodos Set_*Foot_Rot).

## Ronda 4 (movimiento real, A/B)

Metodo de movimiento permitido: actor temporal BP_TestDriver (en /Game/_Test, sin guardar) que llama AddMovementInput cada tick sobre el personaje en PIE; salto con MovementMode=Falling + Velocity.Z=450 por propiedades. Capturas via CaptureEditorImage (solo ventana de Unreal), recortadas al muneco. Camara alta (~25 grados) por el boom del juego; no se pudo bajarla (el BP la restablece).

> AVISO (Ronda 6): las capturas 01-24 y los cmp_* se movieron a `capturas/_descartadas_invalidas/` (archivado en `Archivo_No_Proyecto/2026-10-28/Capturas_descartadas/_descartadas_invalidas/`) (comparaban Alpha 1 vs Alpha 1 por el pin ignorado, o mostraban caida). NO son evidencia. La tabla siguiente se conserva solo como historial.

| Captura | Escena | Alpha | Resultado |
|---|---|---|---|
| 10 | walk perfil | 1 | piernas/rodillas/pies naturales |
| 11 | run perfil | 1 | natural, inclinacion hacia delante |
| 12 | walk frente | 1 | piernas rectas, pies paralelos |
| 13 | salto perfil | 1 | linea roja de debug visible (EventGraph) |
| 14 | run frente | 1 | sin torsion visible |
| 15 | aterrizaje perfil | 1 | sin deformacion visible |
| 17 | run perfil | 0 | comparable; diferencia solo de fase |
| 18, 19 | walk/run frente | 0 | comparable |
| 20, 21 | salto/aterrizaje | 0 | comparable (fase distinta) |
| 22-24 | alpha 1 sin Set_*Foot_Rot | 1 | iguales a 10/12 (24 invalida: cayo) |

Cambios: (1) EventGraph K2Node_CallFunction_24 (LineTraceByChannel, 2208,-400) DrawDebugType ForOneFrame -> None (era la linea roja que seguia viendose). (2) Set_LeftFoot_Rot y Set_RightFoot_Rot: probados desconectados, sin diferencia visible (probable no-op porque Get_*Foot se evalua despues del IK); ELIMINADOS del rig _fix. Cadena final: Set_Hips -> TwoBoneIK_Left -> TwoBoneIK_Right. Alpha=1 restaurado y ABP _fix compilado.
Conclusion honesta: en estas vistas (camara alta) no se observa defecto de rodillas/tobillos con Alpha 1; no se pudo demostrar mejora ni empeoramiento respecto a Alpha 0. Pendiente: vista a ras de suelo, pole vector, pesos de skin.

## Ronda 5 - Rodillas y tobillos: causa encontrada y corregida (2026-10-28)

**Hallazgo critico sobre el metodo anterior:** `node.alpha` del nodo `AnimGraphNode_ControlRig_1` NO afecta al runtime. El valor efectivo lo manda el pin `Alpha` del nodo (pin default 1.0). Todas las comparaciones "Alpha 0 vs 1" de las rondas 1-4 (capturas 01-24) eran en realidad Alpha 1 vs Alpha 1: eso explica que "no se viera diferencia". Esas capturas no prueban nada sobre rig on/off. Ahora se fija con `BlueprintTools.set_pin_value` sobre el pin `Alpha` (se mantiene tambien `node.alpha`), compilando el ABP y releyendo el pin ('1.0').

**Instrumento (medicion, no adivinanza):** actor temporal `BP_ProbeDriver` (en `/Game/_Test`, solo en memoria; ya retirado del nivel) que en cada Tick lee con `GetSocketLocation/Rotation` las posiciones mundo de cadera, rodilla, tobillo y puntera de ambas piernas del personaje en PIE; las leo con `ObjectTools.get_properties`. Camara de captura: `CameraActor` temporal con `autoActivateForPlayer=Player0` (ya retirado), puesto a ras de rodilla (z actor -66), vistas frente/perfil, FOV 40. Pose congelada con `customTimeDilation=0.0001` del personaje (fase identica entre configuraciones: en run, flex 20.4/114.3 en las tres). Suelo plano: x=-3500..-2400, y=0 (las rampas invalidaron la primera tanda: el personaje subia a Rampa_Ascenso_1).
Metricas por pierna: flexion de rodilla (angulo muslo-espinilla), desviacion lateral de la rodilla respecto a la linea cadera-tobillo (|lat|, eje Y mundo; el personaje avanza en +X), desviacion frontal (fwd), yaw/pitch del pie (vector tobillo->puntera).

**Tabla (8 fases por escena, 3 en idle; detalle en `evidencia/tabla_medicion_rodillas.txt`)** - |lat| media/max en cm, muslo 21.4 cm:

| Escena | Rig OFF (anim original) | Rig ON, pole Direction (estado anterior) | Rig ON, pole Location (fix) |
|---|---|---|---|
| idle I/D | 0.49/0.59 y 0.74/0.94 | 2.26/3.45 y 2.89/3.46 | 0.10/0.23 y 0.08/0.10 |
| walk I/D | 1.65 y 0.76 | 5.75/7.99 y 2.05/2.54 | 0.06/0.11 y 0.15/0.19 |
| run I/D | 2.06/2.46 y 1.05/1.27 | 1.59/6.86 y 13.67/17.67 | 0.09/0.10 y 0.22 |
| jump I/D | 1.06/1.61 y 0.59/0.71 | 2.00/8.91 y 3.74/5.41 | 0.08/0.13 y 0.07/0.11 |

Conclusion: la animacion original (Rig OFF) tiene las rodillas en el plano sagital (lat <= 2.5 cm). El defecto lo introducia el rig: el pole vector `Direction (0,1,0)` con `PoleVectorSpace None` no se interpreta como "adelante" y empuja las rodillas de lado hasta 17.7 cm en run (rodilla casi a 90 grados fuera del plano; en captura 27/28 la pierna se dobla hacia adentro y se cruza). Las pruebas de polo +X/-X/+Y/+Z en Direction no movian la rodilla de forma coherente (efecto casi nulo); en cambio `Location` si controla el plano.

**Cambio aplicado (hipotesis 1, pole como Location):** en `CR_Student_Procedural_fix`:
- `TwoBoneIK_Left`: `PoleVectorKind` Direction -> Location; `PoleVector` (0,1,0) -> (X=6.07, Y=60, Z=28.1). Leido de vuelta OK.
- `TwoBoneIK_Right`: idem con (X=-5.78, Y=60, Z=28.1).
(Coordenadas en espacio global del rig = espacio componente: +Y adelante, +X izquierda; 6.07/-5.78 = x de la rodilla en pose de referencia; Y=60 delante; Z=28.1 altura de rodilla.)
Antes/despues con captura: `capturas/25_idle_front_off_dir_loc.png`, `26_idle_side_...`, `27_run_front_...`, `28_run_side_...` (izquierda Rig OFF, centro antes, derecha despues; misma fase congelada). Resultado (corregido en Ronda 6): Location elimina los cruces, pero NO es identico a la animacion original: aplana la rodilla al plano sagital (ver Ronda 6 para la diferencia medida). No hay hiperextension: la desviacion frontal (fwd) es positiva (rodilla adelante) en todas las fases.

**Tobillos/pies:** el IK no altera la rotacion del pie; yaw/pitch del pie identicos entre OFF/Direction/Location en idle (-17.8/-36.0 vs -17.8/-36.0 vs -17.9/-36.5). El "tobillo raro" se debia a que la rodilla torcida dejaba el pie girado respecto a la espinilla; con la rodilla en el plano desaparece. Los Set_*Foot_Rot siguen retirados (no hacen falta).

**Hallazgo adicional (no cambiado, a decidir):** en el grafo, `Set_Hips` (propaga a hijos) se ejecuta antes de leer `Get_LeftFoot/RightFoot`, de modo que el efector IK se calcula con el pie ya movido por la cadera: el IK de pies no clava el pie al suelo (solo corrige la rodilla). Ademas el offset de pelvis se aplica en eje local de Hips (roll 90, escala 100), no en vertical mundo. Con suelo plano (offsets ~0) no se nota; si se quiere foot-planting real habria que leer los pies antes de `Set_Hips` y expresar el offset en espacio mundo/componente.

**Estado final:** Alpha pin = 1.0 (node.alpha 1), `DrawDebugType` = None en los 3 LineTrace (UpdateProceduralVariables x2, EventGraph x1), ABP `_fix` compilado sin errores, nivel sin actores temporales (ProbeDriver y LegCam retirados; sin guardar el nivel). Scripts y datos: `evidencia/scripts_medicion/`, `evidencia/meas_phases_off_dir_loc.json`. `meas_INVALIDA_alpha_nodo_ignorado.json` es la tanda con el alpha mal aplicado (no usar).

## Ronda 6 - A/B a fase igualada, tobillos en movimiento y ajuste del pole (2026-10-28)

**Correcciones a la Ronda 5:** (1) `tabla_medicion_rodillas.txt` NO comparaba a fase igualada (renombrada a `evidencia/tabla_medicion_rodillas_fases_NO_igualadas.txt`; no usar). (2) Capturas 01-24 y cmp_* movidas a `capturas/_descartadas_invalidas/` (archivado en `Archivo_No_Proyecto/2026-10-28/Capturas_descartadas/_descartadas_invalidas/`) (no borradas). (3) Se retira la frase "Location indistinguible de la original".

**Metodo nuevo (fase igualada de verdad):** barrido continuo en camara lenta (`customTimeDilation` 0.03-0.05, 90 muestras walk/run, 70 jump, 6 idle) con el mismo script en tres configuraciones: rig OFF (pin Alpha 0), Direction (antes) y Location (fix). Cada muestra del rig ON se empareja con la muestra OFF de la misma escena cuyos tobillos L+R relativos a la cadera sean mas cercanos; solo se aceptan pares con residuo <= 1 cm. La cobertura de fase es completa: flexion de rodilla cubierta walk 14-70, run 10-144, jump 7-88 grados (antes una sola fase). Datos: `evidencia/sweep_OFF.json` y `evidencia/sweep_LOCX12.json` (los demas `sweep_*` archivados en `Archivo_No_Proyecto/2026-10-28/Evidencia_intermedia/evidencia/`); tabla: `evidencia/tabla_AB_fase_igualada.txt`; scripts: `evidencia/scripts_medicion/` (sweep.py, an3b.py, an5b.py). Lateral = eje Y mundo (el personaje avanza en +X). Hallazgo lateral: el rig baja todo el cuerpo ~2.15 cm en Z (pelvis y pies) respecto a OFF; se quita para emparejar.

**Resultado, rotacion del pie (requisito 4), a fase igualada** (angulo entre rotaciones del hueso Foot, rig ON vs OFF, mediana/max en grados): Direction idle/walk 0, run 0.56/2.2, jump 0/0.6. Location (final) idle 0.07/0.16, walk 0/1.35, run 0/0, jump 0/0.64. Vector tobillo-puntera igual de bajo. Es decir, el IK NO gira el tobillo ni en walk, run ni jump: las diferencias de yaw/pitch de la tabla anterior eran solo diferencia de fase, no del rig. Los valores de yaw cerca de +-90 deg del vector tobillo-puntera son una propiedad del eje del hueso ToeBase de Mixamo (aparecen igual con rig OFF) y no son un defecto.

**Diferencia de la rodilla frente a la animacion original (|lat ON - lat OFF| por pierna y par, cm):**

| Escena | Direction (antes) mediana / max | Location X=+-6 (Ronda 5) mediana / max | Location X=+-12 (FINAL) mediana / max |
|---|---|---|---|
| idle | 3.34 / 4.07 | 0.71 / 0.93 | 0.46 / 0.60 |
| walk | 2.66 / 12.43 | 0.82 / 1.75 | 0.22 / 0.94 |
| run | 3.05 / 16.40 | 1.25 / 6.29 | 1.24 / 3.51 |
| jump | 4.45 / 14.76 | 0.58 / 2.08 | 0.21 / 1.07 |

**Hipotesis del pole X (una a la vez, mismo metodo):** X=0 empeoro (run max 8.9, walk mediana 1.47); X=+-12 mejoro (tabla); X=+-20 empeoro frente a 12 (run 5.65). Se adopta X=+-12 (Y=60, Z=28.1 sin cambio). Residual honesto: Location sigue sin ser identico a la original (en run mediana 1.2 cm, max 3.5 cm cuando la pierna trasera esta muy flexionada, 100-144 deg); la animacion original tiene 0.5-3.7 cm de desviacion natural y el rig la reemplaza por una rodilla mas alineada al plano sagital. Direction (estado que veia el usuario) la desviaba hasta 17.7 cm.

**Capturas (fase congelada, misma pose en ambas, camara a ras de pierna, pies visibles, sin caida):** `capturas/29_OFF_*` (rig OFF) y `30_FIX_*` (fix), montajes `31_cmp_walk_OFF_vs_FIX.png` y `31_cmp_run_OFF_vs_FIX.png` (izq OFF, der FIX; arriba frente, abajo perfil). Residuo de pose congelada walk/run 0.00 cm, rotacion de pie 0.00 deg. Visualmente walk y run son equivalentes entre OFF y FIX. Jump: NO se logro captura A/B valida (la trayectoria del salto en camara lenta no es reproducible entre corridas y la camara atravesaba la rampa); las capturas intentadas estan en `_descartadas_invalidas/`. Jump queda cubierto solo por la medicion numerica (66 de 70 pares emparejados, rotacion de pie max 0.64 deg, |lat| diferencia mediana 0.21 cm). 27/28 (run) siguen validas pero 27 corta los pies; usar 31.

**Estado final leido del editor:** pole Location (X=12 / X=-12, Y=60, Z=28.1) en TwoBoneIK_Left/Right, SecondaryAxisWeight 0, pin Alpha del ABP `_fix` = 1.0, node.alpha 1, ABP compilado sin errores, PIE detenido, actores temporales ProbeDriver y LegCam retirados (nivel sin guardar; paredes Limites_Mapa intactas). Sin cambios en los originales.

**Limites:** no hubo prueba con teclado manual en la camara normal (la inyeccion de teclas esta denegada); todo se midio con entrada simulada via actor temporal. Nada esta guardado en disco: Ctrl+S sobre `CR_Student_Procedural_fix`, `Student_Skeleton_AnimBlueprint_fix` y `Lvl_AnimTest`.

---
Nota de archivo (2026-10-28): las capturas 01-24/cmp_* (`_descartadas_invalidas/`), los barridos intermedios `sweep_DIR/LOC/LOCX0/LOCX20`, `frozen_*.json`, snapshots intermedios y scripts de una sola vez se movieron a `Archivo_No_Proyecto/2026-10-28/` (ver `Archivo_No_Proyecto/INDEX.md`). Las capturas 06, 07, 08 y 09 se conservan en `capturas/` porque este informe las cita como evidencia vigente.
