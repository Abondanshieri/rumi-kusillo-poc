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
