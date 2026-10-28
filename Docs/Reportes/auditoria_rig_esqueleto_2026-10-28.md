# Auditoria de factibilidad: rig procedural y esqueleto Student (2026-10-28)

Alcance: SOLO LECTURA. No se edito, guardo, movio ni compilo ningun asset. Leyenda de evidencia:
- **[M]** medido por mi con lectura real del editor via MCP en esta sesion (ControlRigTools: get_all_bones / get_local_transform / get_global_transform con `initial=True`, list_nodes / list_pins / get_pin_value; SkeletalMeshTools: get_bone_names, get_bounds, etc.).
- **[D]** leido del disco (cadenas del .uasset, tamanos de archivo) o de documentos del proyecto (`Docs/Avance/2026-10-28_rig-student-fix/informe.md`), NO re-verificado por mi.
- **[G]** conocimiento general de UE / suposicion. Debe verificarse antes de decidir.

Nota de honestidad: no pude medir el esqueleto del Mannequin (la lectura de `CR_Mannequin_Body` tardo mas de 2 min y la cancele para no cargar el editor mientras el otro equipo trabaja). Todo lo dicho del Mannequin es **[G]**. Tampoco pude leer los pesos de skin: `get_vertex_count(LOD0)` devolvio 0 (la herramienta no expone datos de vertices), asi que el punto "pesos de skin" queda sin medir.

## 1. Resumen ejecutivo

1. **Posible: SI.** Todo el trabajo de diagnostico y el 60-70% de la construccion de un Control Rig nuevo se puede automatizar por MCP (crear CR, nodos, pines, variables). Un esqueleto nuevo exige DCC (Blender) o el editor a mano, porque el MCP no edita huesos de un SkeletalMesh.
2. **Conviene: CONDICIONAL.** Rehacer el esqueleto placeholder NO conviene ahora; rehacer el Control Rig como modulo procedural reusable SI conviene (Opcion B), disenado para sobrevivir al retarget al rig final de Carlos (C-M3).
3. **Esqueleto Student: usable pero sucio** [M]: Hips escala 100 y roll 90 heredados a los 41 huesos, sin Root, sin huesos IK/twist, sin sockets; el defecto de import es de unidades (m a cm), no de proporciones.
4. **Control Rig actual: parcheable pero fragil** [M]: TwoBoneIK sin control de rotacion de tobillo, polo fijo (Direction 0,1,0), offsets de pie sin consumidor. Ya "se ve bien" en camara alta tras el fix; no hay prueba a ras de suelo.
5. **Recomendacion:** B ahora (8-14 h), mas una prueba piloto de retarget (IK Rig/Retargeter Student -> Mannequin, 2-3 h) para decidir el esqueleto con datos; NO construir esqueleto nuevo hasta que llegue C-M3.

## 2. Hallazgos medidos del esqueleto Student_Skeleton / mesh Student

| # | Hallazgo | Evidencia | Gravedad |
|---|---|---|---|
| 1 | 41 huesos, sin hueso Root: Hips es la raiz (parent=None) | [M] get_all_bones, get_parent | Media: root motion y retarget piden root |
| 2 | Hips: escala local/global (100,100,100); rotacion roll 90 (pitch 0, yaw 0). Pos (0.15, 0.29, 52.72) | [M] get_local_transform initial | Alta |
| 3 | La escala 100 se hereda: los 41 huesos tienen escala GLOBAL 100; sus escalas locales son 1 y las traslaciones locales son pequenas (p. ej. UpLeg->Leg = 0.21 locales = 21 cm reales) | [M] Gs=100 en todos | Alta: todo calculo en espacio local de hueso esta a 1/100; pines Location/Direction en Hips-space se rompen |
| 4 | Eje del hueso hijo = -Y local (spine, brazos, piernas: el offset dominante del hijo es -Y). Confirmado en spine (0,-0.06..-0.09,0), arm (0,-0.09), leg (0,-0.21,0) | [M] | Media: ya contemplado en `_fix` (PrimaryAxis 0,-1,0) |
| 5 | Nomenclatura Mixamo SIN prefijo (`mixamorig_` ya eliminado): Hips, Spine, Spine1, Spine2, LeftUpLeg, LeftLeg, LeftFoot, LeftToeBase, LeftToe_End... | [M] get_bone_names | Baja: facilita IK Rig chain mapping automatico "Mixamo" |
| 6 | Sin huesos twist, sin ik_foot/ik_hand, sin huesos de socket; `get_socket_names` = [] | [M] | Media: sin sockets no hay donde anclar props (martillo/yunque) |
| 7 | Longitudes reales (cm): muslo L 21.43 / R 21.46; espinilla L 20.83 / R 20.83; pie->punta L 11.15 / R 11.29; ancho de cadera 10.49; Hips->Neck 28.6; brazo 11.6, antebrazo 10.7 | [M] calculado de posiciones globales | Dato clave |
| 8 | Altura: HeadTop_End z=113.6; bounds mesh centro z=58.2, extension z=58.2 (0..116.4), x +-46.5 (T-pose) | [M] get_bounds, global | Personaje de ~1.14 m (proporcion infantil) |
| 9 | Tobillo (LeftFoot/RightFoot) a z=7.34 cm en bind pose; ToeBase z=0.8; cadera (UpLeg) z=49.5; pierna recta teorica = 42.3 (muslo+espinilla); bind pose NO es perfectamente recta (distancia directa 42.2) | [M] | Sin margen de "extension": IK sin estirar |
| 10 | Muslo ~ espinilla (ratio 1.03): con la pierna casi recta el plano de flexion es inestable sin polo explicito | [M] ratio; efecto [G] | Media |
| 11 | Huesos fin de dedo anomalos: LeftHandThumb4 local (-0.26,0.11,0.26) y global (12.1,10.7,47.9), a ~30 cm de la mano (34,0.8,75); idem Index4 L/R y RightThumb4. Tienen rotaciones locales raras (p. ej. 35.9,-64.8,38.6) | [M] valores; causa [G] | Baja/ruido: parece basura del end-site Mixamo; verificar contra la ref pose del SkeletalMesh (puede ser artefacto de la jerarquia del CR) |
| 12 | Hombros con rotacion local extrema (LeftShoulder -89,-178.6,-71.5): orientacion de clavicula torcida (arrastrada por el roll 90 del padre) | [M] | Media para IK de brazos / look-at |
| 13 | Eje X local lateral, Y local vertical-del-hueso, Z frontal en Hips segun el equipo; los hijos tienen rotaciones globales de yaw ~180 en piernas (UpLeg Grot yaw -179.9, roll -92), es decir ejes de piernas volteados respecto al Hips | [M] Grot de las piernas | Alta para cualquier IK basado en ejes locales |
| 14 | Mesh: 1 LOD, 0 sockets, PhysicsAsset `Student_PhysicsAsset` (9.7 KB) asignado | [M] get_lod_count, get_physics_asset | Info |
| 15 | Skeleton asset 15.8 KB; mesh `Student.uasset` 8.7 MB; no hay curvas ni slots personalizados salvo `DefaultSlot` | [D] | Info |
| 16 | Pesos de skin | NO MEDIDO (get_vertex_count devuelve 0; no hay API de pesos) | Desconocido. El A/B (alpha 0 vs 1) del informe del equipo sugiere residuo por skin/esqueleto "pantalon delgado" [D] |

Interpretacion [G]: Hips con escala 100 + roll 90 es el tipico artefacto de FBX en metros importado con "Convert Scene / Force Front X axis" desactivado, o de un Mixamo exportado a 0.01. Las animaciones existentes estan horneadas con ese mismo esqueleto, por lo que las posiciones de raiz que importan ya compensan la escala 100.

## 3. Hallazgos de los Control Rigs y el AnimBP

### 3.1 Arquitectura actual

| Asset | Contenido leido [M] | Estado |
|---|---|---|
| `CR_Student_Procedural_fix` (45 nodos) | BeginExecution -> Set_Spine1 -> Set_Spine2 -> Set_Neck_Lean (lean con LeanRoll/LeanPitch repartido 1 / 0.5 / 0.333, multiplicando quats locales) -> Set_Hips (offset Z = PelvisOffset + LandCrouch*25) -> TwoBoneIK_Left -> TwoBoneIK_Right. PrimaryAxis (0,-1,0), SecondaryAxis (0,0,1), PoleVector (0,1,0) kind **Direction** (fijo, sin control de polo), Weight 1 | Funcional en idle/walk/run segun capturas del equipo [D] |
| Inerte / huerfano [M] + [D] | `Add_HipsZ`, `Add_LeftFootZ`, `Add_RightFootZ` sin consumidor; `Mul_Hips_Offset_1` sin conexiones. FootOffsetL/R solo llegan via `Sub_FootOffset -> Clamp -> Make_*Foot_Offset -> Mul_*Foot_Offset` (esa rama SI esta conectada al efector); el "offset sin conectar" es la rama `Add_*FootZ`. LandCrouch*25 y offsets en cm sobre un espacio donde Hips tiene escala 100: verificar si Set_Hips en LocalSpace aplica 25 cm o 25*100 | Parcial |
| `CR_Student_IK_fix` (15 nodos) | SetTransform_Hips <- ctrl_hips; 4 IK de dos huesos (piernas + brazos) con efector `ctrl_*_ik` y polo `ctrl_pole_*` (PoleVectorKind Location) | Es un rig de controles para animar a mano; usa PrimaryAxis (0,-1,0) tras el fix, el original `CR_Student_IK` tenia (1,0,0)/(0,1,0), que estaba mal [M diff] |
| Original vs `_fix` | Original IK: ejes X/Y; `_fix`: -Y/Z. Procedural `_fix`: lean rewired, SecondaryAxisWeight 0, sin Set_*Foot_Rot (probados y eliminados) [D] | |

### 3.2 Por que TwoBoneIK da rodillas/tobillos mal (causas, con evidencia)

| Causa | Evidencia | Peso |
|---|---|---|
| TwoBoneIK solo resuelve cadena BoneA-BoneB-Effector; **no controla la rotacion del tobillo**: el pie hereda la rotacion de la espinilla. El intento Set_*Foot_Rot fue un no-op porque Get_*Foot se evaluaba tras el IK | [D] informe Ronda 3-4; [G] comportamiento de RigUnit_TwoBoneIKSimple | Alta |
| Polo fijo `Direction (0,1,0)` en espacio global/componente, sin relacion con el eje de flexion real (que con roll 90 y yaw 180 de las piernas no es Y) | [M] pin values, rotaciones globales de pierna | Alta |
| SecondaryAxis (0,0,1) con peso 1 forzaba torsion -> cruce de piernas; se mitigo poniendo peso 0 | [D] Ronda "SecondaryAxisWeight 0" | Resuelto parcial |
| Escala 100 en Hips/jerarquia: transform de efector tomado en GlobalSpace mezcla cm reales con locales/100; cualquier offset en espacio local de Hips queda x100 o /100 | [M] Gs=100; efecto [G] | Alta (latente) |
| Rodilla casi recta (pierna 42.3 vs 42.2) y muslo~espinilla: sin stretch (`bEnableStretch False`), objetivos mayores a 42 cm no alcanzables | [M] longitudes + pins | Media |
| Sin raycast -> pelvis -> pie coherente en el rig: el trace vive en el AnimBP y pasa FootOffsetL/R/PelvisOffset al rig; no hay "foot lock" ni alineacion al normal del suelo | [D] orden_graph.md | Media |
| Sin pesos/twist: deformacion residual del pantalon con alpha 0 | [D] Ronda 2 | No medido |

Nota: el equipo concluye que con camara alta y alpha 1 no se ve defecto; falta prueba a ras de suelo con polo y pesos. Mi lectura coincide: el sintoma esta mitigado, no resuelto de raiz.

### 3.3 AnimBP vs arquitectura acordada

- ABP original [D, cadenas del uasset]: 10 `AnimStateNode` (0-9), 3 conduits, 30 transiciones, 2 state machines (Main y Locomotion), BlendSpacePlayer + `AnimGraphNode_BlendSpaceGraph_0`, `DefaultSlot`, Inertialization, `AnimNode_ControlRig`. Estados nombrados en `_fix`: Locomotion, JumpStart, LandPrep/LandCrouch, SoftLand, HardLanding, Fall (BS_Fall), Swing (IsSwinging), etc. (el equipo habla de 9 estados).
- Arquitectura acordada (CLAUDE.md): Locomotion simple (Idle/Walk/Run en Blend Space) + estado Busy; interaccion/feedback como Montages en Slots.
- Diferencia: la SM actual absorbe aire y aterrizaje en estados (correcto para plataformas); lo que NO esta aun es Busy y la jerarquia de montages por Slot (hay `DefaultSlot` + Slot node en cadena: SM -> Slot -> Inertialization -> ControlRig). Es compatible: **el Control Rig va al final de la cadena, despues de Slot e Inertialization**, lo que es correcto para IK de pies.
- 9-10 estados no contradicen el plan siempre que Busy y Montages se anadan; no es un bloqueo para el rig.

## 4. Comparativa de opciones

Horas = estimacion [G] para Franco asistido por MCP; incluyen verificacion.

| Opcion | Descripcion | Esfuerzo | Riesgo | Reversibilidad | Que requiere | Automatizable por MCP |
|---|---|---|---|---|---|---|
| A | Corregir lo actual (`_fix`): polo con control, rotacion de tobillo con nodo propio ordenado, normalizar escala en calculos, limpiar huerfanos | 3-6 h | Bajo | Alta (son copias) | Solo editor | Si, ~80% |
| B | Control Rig nuevo modular (Setup/Construction + Forward Solve): Leg IK 2 huesos o FBIK ligero, foot placement desde traces del ABP, rotacion de tobillo alineada a normal, lean, look-at, polo en espacio de pierna, todo parametrizado por nombres de hueso (variables) para reusar con otro esqueleto | 8-14 h | Medio-bajo | Alta (asset nuevo, ABP `_fix` apunta al nuevo) | Editor; Python MCP para crear nodos | Si, ~70% (crear CR, variables, nodos, conexiones); afinado de ejes/valores a mano |
| C | Esqueleto nuevo (Root, pelvis escala 1, IK bones, twist) + rig nuevo + retarget de las animaciones (Student x5, Rumi ~12) via IK Rig/Retargeter | 25-45 h (modelado/skin en DCC 8-15 h, retarget y ajuste de 17 clips 8-15 h, rehacer ABP/BS/PhysicsAsset/BP 5-10 h) | Alto: rompe referencias; registro de assets de esta sesion roto; re-skin; retarget con pie deslizando | Media (hay que conservar el viejo) | Blender (o Maya), reimport Interchange, IK Rig/Retargeter manual | Solo parcialmente: `import_file` de SkeletalMesh existe [M, herramienta listada]; IK Rig/Retargeter no tiene toolset visto en la lista que consulte |
| D | Base oficial: rig del Mannequin UE5 (`CR_Mannequin_Body`, `CR_Mannequin_FootIK`, `CR_Mannequin_Procedural` ya en el proyecto, `/Game/Characters/Mannequins/Rigs`) copiado/adaptado, o IK Rig + FBIK nativo; Pose Search/Motion Matching solo si se justifica | 6-12 h para adaptar (si el esqueleto fuera el del Mannequin) ; 3-5 h para un piloto de retarget Student->Mannequin | Medio: el Mannequin tiene huesos IK/twist que Student no; usar sus nodos obliga a retargetear o a mapear | Alta | Editor | Lectura SI; adaptacion parcial |
| E | Auto-rigger (Epic MetaHuman/Mixamo re-rig) o rehacer en DCC y reimportar | Mixamo: 2-4 h y reproduce los mismos defectos; DCC: = Opcion C | Mixamo: bajo pero no corrige escala; MetaHuman no aplica (personaje estilizado infantil) | Alta | Mixamo web / Blender | No |

Nota sobre Motion Matching / Pose Search [G]: requiere base de datos amplia de animacion; con 5 clips Student + ~12 Rumi es sobredimensionado. No recomendado para la PoC.

Que SE puede hacer desde MCP (lista verificada de herramientas en `describe_toolset`) [M]:
- Control Rig: crear (`create`), variables, nodos (`create_node`), pines, conexiones, eventos/grafos, transformadas de jerarquia, `import_bones_from_asset`, add_control/null/bone.
- Skeletal Mesh: leer huesos, sockets (add/remove/rename/transform), asignar PhysicsAsset/material, `import_file` (FBX con `skeleton`, `import_animations`).
- Lo que NO vi en las herramientas: editar huesos del esqueleto, pesos de skin, IK Rig / IK Retargeter, retarget masivo de animaciones. Eso = Blender o editor a mano.

## 5. Viabilidad concreta del esqueleto mejorado

- **Corregir escala/roll de Hips sin romper animaciones:** no es seguro. Cambiar el bind pose del esqueleto actual cambia la interpretacion de las pistas de las 5 animaciones Student y las ~12 de Rumi (estan horneadas contra esos valores) [G]. Tres caminos: (i) reexportar mesh y anims juntos desde Blender con Hips escala 1 y reimportar todo (reimporta clips, rompe referencias del BS y del ABP si cambian nombres); (ii) dejar el esqueleto y retargetear con IK Rig/Retargeter a un esqueleto limpio nuevo; (iii) dejar tal cual y neutralizarlo en el rig (la escala 100 afecta solo si se opera en espacio local de Hips).
- **Retarget en UE 5.8:** el flujo oficial es IK Rig en origen y destino (chains Spine/Legs/Arms, retarget root = Hips/pelvis), IK Retargeter con poses de referencia alineadas (T/A), exportar animaciones. Para pies deslizantes, Epic recomienda Speed Planting + FBIK en el retargeter (fuente: documentacion "fix foot sliding with IK Retargeter" que consulte hoy) [fuente web]. Con proporciones de nino (pierna 42 cm) vs Mannequin (~90 cm) se espera deslizamiento notable [G].
- **Compatibilidad de esqueleto:** `Student_Skeleton_BlendSpace`, el ABP (`Student_Skeleton_AnimBlueprint`, `_fix`, `_Backup_v5`), `Student_PhysicsAsset` y los 5+12 clips estan atados a `Student_Skeleton`. Un esqueleto nuevo obliga a recrearlos o retargetearlos. Una alternativa de bajo riesgo es "Compatible Skeletons" en Skeleton para reusar clips sin copiar [G, verificar].
- **Registro de assets roto en esta sesion:** exists/get_referencers/move/save fallan [D]; los .uasset no se renombran en disco. Cualquier migracion con renombres es de alto riesgo hasta reiniciar editor/MCP y comprobar referencias con "Reference Viewer" a mano.
- **BP_ThirdPersonCharacter:** referenciado con asterisco (cambios sin guardar) [D]; no se toco ni lei.

## 6. Relacion con el plan (C-M3 de Carlos)

El rig final de Carlos tendra proporciones estilizadas y llegara con su propio esqueleto, casi seguro con nomenclatura y ejes distintos [CLAUDE.md]. Consecuencias:
- Un esqueleto Student "mejorado desde cero" se vuelve descartable en pocas semanas; el trabajo vale solo como piloto de retarget, no como activo final.
- Lo que SI se reutiliza: (a) la logica procedural (lean, foot placement, pelvis, land crouch), (b) la integracion ABP <-> CR (variables, traces), (c) el flujo IK Rig + Retargeter.
- Por tanto: **invertir en un Control Rig modular parametrizado por nombres de hueso** (Opcion B), probarlo contra Mannequin (que ya tiene Root/IK/twist) como segundo esqueleto para asegurar portabilidad, y esperar C-M3 para decidir el esqueleto de produccion. Pedir a Carlos desde ya: Root en origen, escala 1, pelvis eje consistente, IK bones (ik_foot_l/r, ik_hand_l/r), twist y sockets.

## 7. Recomendacion y plan por fases

Recomendacion: **Opcion B (con piloto de D) ahora; C solo si el piloto falla o cuando llegue C-M3.**

| Fase | Tarea | Criterio de aceptacion verificable | Quien |
|---|---|---|---|
| 0 | Preparar: reiniciar MCP/editor, confirmar que get_referencers y exists funcionan; guardar estado de originales (Ctrl+S o copia) | `exists` devuelve true para `/Game/Characters/Student/Student_Skeleton`; backup del ABP y CR existentes | Franco manual + MCP |
| 1 | Medir lo pendiente (solo lectura): ref pose real del SkeletalMesh (no la del CR), esqueleto del Mannequin (huesos, longitudes), huesos fin de dedo anomalos | Tabla Student vs Mannequin completa con longitudes de muslo/espinilla/pie y ejes; confirmar si las posiciones de Thumb4/Index4 estan en el mesh | MCP automatizable |
| 2 | Piloto de retarget: IK Rig `Student` + IK Rig `Mannequin` + IK Retargeter; retargetear `Student_Idle` y `Student_Running` a un esqueleto limpio de prueba (o al reves) | Captura a 3 vistas (frente, perfil, espalda) sin deslizamiento > 2 cm del pie en apoyo y sin torsion visible | Franco manual (UI del Retargeter) |
| 3 | Control Rig nuevo `CR_Student_Leg_v2` en copia (no sobre originales): variables de nombres de hueso; Leg IK con polo calculado en espacio de pierna; rotacion de tobillo = alineacion al normal del suelo (trace del ABP) con peso; pelvis offset; lean; look-at | Compila sin errores en log; en PIE a ras de suelo (camara baja) rodillas apuntan al frente en idle/walk/run/jump/aterrizaje; pie plano en rampa; alpha 0 vs 1 comparado en 4 poses | MCP crea el 70%; ajuste de ejes y valores Franco |
| 4 | Probar portabilidad: asignar el mismo CR_v2 al Mannequin (solo cambiando nombres de variables) | Funciona sin cambios de nodos | MCP |
| 5 | Integrar en ABP `_fix` (nodo ControlRig tras Slot/Inertialization); anadir estado Busy y montages por Slot segun acuerdo | ABP compila; Busy bloquea input; un montage de prueba se reproduce sin tocar la SM | Franco manual |
| 6 | Decidir esqueleto de produccion cuando llegue C-M3 (checklist de requisitos para Carlos: Root, escala 1, IK/twist/sockets) | Documento firmado/aprobado por Jhasmani | Equipo |

## 8. Riesgos y reversibilidad

| Riesgo | Mitigacion | Reversible |
|---|---|---|
| Registro de assets roto: movimientos/renombres pueden romper referencias | No renombrar ni mover hasta reiniciar y comprobar; trabajar con copias `_v2` | Si |
| Alterar bind pose de Hips rompe 17 clips | No tocar el esqueleto actual; usar retarget | Si si se conserva el original |
| Otro equipo edita el editor ahora | Mi trabajo fue solo lectura; coordinar antes de la fase 3 | n/a |
| Retarget con proporciones de nino produce deslizamiento | Speed Planting + FBIK en Retargeter [fuente web] | Si |
| Estimaciones de horas son [G] | Revisar tras fase 1-2 | n/a |
| Mis mediciones de globales dependen de la jerarquia del CR (preview mesh); posible desfase con la ref pose del mesh | Fase 1 las cruza | n/a |

## 9. Preguntas abiertas para Franco

1. El objetivo es solo "piernas bien" o tambien brazos (IK de manos para el yunque)? Cambia el alcance de B.
2. Cuando llega C-M3 de Carlos (fecha real)? Si es en menos de 2 semanas, B solo vale como logica reusable.
3. Tienes Blender en D:? Y quien escribe/reexporta FBX (tu o Carlos)?
4. Las ~12 animaciones de Rumi comparten `Student_Skeleton`? (leyendo el ABP/BS de Rumi lo veria; no lo verifique).
5. Aceptas que reinicie MCP/editor para reparar el registro de assets antes de la fase 3?
6. Prioridad: estabilidad visual a camara de juego (alta, isometrica) o calidad a ras de suelo (cinematicas)?

## 10. Registro tecnico de lecturas

- Esqueleto/jerarquia: `animation_toolset...ControlRigTools.get_all_bones/get_parent/get_local_transform/get_global_transform(initial=True)` sobre `/Game/Characters/Student/Rig/CR_Student_Procedural` (datos guardados en el scratchpad, `stu.json`).
- Mesh: `SkeletalMeshTools.get_bone_names/get_bounds/get_physics_asset/get_socket_names/get_lod_count` sobre `/Game/Characters/Student/Student`.
- Rigs: list_nodes/list_pins/get_pin_value/get_connected_pins sobre `CR_Student_IK`, `CR_Student_IK_fix`, `CR_Student_Procedural_fix`. La lectura de `CR_Student_Procedural` (original) no termino y no se usa.
- Disco: tamanos de .uasset y cadenas de `Student_Skeleton_AnimBlueprint(.fix)`.
- Web: documentacion de Epic "fix foot sliding with IK Retargeter" (consultada hoy).
- Efecto colateral: escribi scripts auxiliares en el scratchpad compartido (`r.py`, `a1.py`..`a4.py`, `d.py`, `n.py`, `an.py`); si el otro equipo tenia archivos con esos nombres, pudieron sobrescribirse (solo scratchpad, no el proyecto).
