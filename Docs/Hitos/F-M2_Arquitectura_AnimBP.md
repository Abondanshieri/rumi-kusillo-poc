# F-M2 — Arquitectura del Animation Blueprint de Rumi (ABP_Rumi_Provisional)

**Verificado en vivo contra el editor** (llamadas MCP frescas, no repetidas de memoria) el
2026-09-14. Todos los `refPath` citados abajo se confirmaron existentes en ese momento con
`find_nodes` / `get_node_infos` / `list_graphs` reales.

## 0. Respuesta directa a la duda de Franco

> "no me diras que todo esta ligado a locomotion, no creo"

**Sí, literalmente todo lo que llega a los Slots depende en cada instante de qué sub-estado esté
activo dentro de la FSM anidada de Locomotion.** No es una suposición ni una simplificación mía —
es la estructura real del Blueprint, verificada así:

- `AnimGraph.AnimGraphNode_StateMachine_0.Main` (la state machine "Main") tiene **un único estado
  hijo**: `AnimStateNode_0.Locomotion`. Lo confirmé con `list_graphs`: solo aparece ese estado bajo
  `Main`, ninguno más. Main no tiene ramas alternativas — es un contenedor de un solo estado.
- Ese único estado "Locomotion" **es** la FSM anidada `AnimGraphNode_StateMachine_1.Locomotion`,
  que sí tiene 4 estados reales: `Idle`, `Move/Run`, `Fall`, `HardLanding`, unidos por 7
  transiciones.
- Como Main no tiene otra rama, la pose que sale de `StateMachine_0` (pin `Pose`) **es, en cada
  frame, exactamente la pose que la FSM anidada esté produciendo en ese instante** — Idle, o
  Move/Run, o Fall (nunca HardLanding hoy, ver §3.1). No hay ningún punto donde eso se "fije" a un
  solo estado.
- Esa pose dinámica es la que conecté como `Source` del nodo `AnimGraphNode_Slot_0` (`FullBodySlot`).
  Lo verifiqué de nuevo ahora mismo con `get_node_infos`: el pin `Source` de `Slot_0` tiene como
  único `connected_pin` la salida `Pose` de `StateMachine_0`. Confirmado, no fabricado.

Cadena real, verificada en vivo (AnimGraph raíz de `ABP_Rumi_Provisional`):

```
StateMachine_0 "Main"  (único estado interno: Locomotion → FSM anidada Idle/Move-Run/Fall/HardLanding)
        │ Pose
        ▼
AnimGraphNode_Slot_0  "FullBodySlot"   (renombrado desde el DefaultSlot original del template)
        │ Pose  ──────────────┐
        ▼                     ▼
AnimGraphNode_LayeredBoneBlend_1        AnimGraphNode_Slot_1  "UpperBodySlot"
  BasePose  = Slot_0.Pose                 Source = Slot_0.Pose
  BlendPoses_0 = Slot_1.Pose ◄─────────────── Pose
  Branch filter: hueso "Spine1", BlendDepth -1
        │ Pose
        ▼
AnimGraphNode_Root_0  (Output Pose)
```

Esto también responde la otra parte de la duda: **no es "solo una copia del Blueprint"**. La copia
(`ABP_Rumi_Provisional`, duplicado de `Student_Skeleton_AnimBlueprint`) fue el punto de partida no
destructivo, pero encima de esa copia se crearon y cablearon 2 nodos nuevos reales
(`AnimGraphNode_Slot_1`, `AnimGraphNode_LayeredBoneBlend_1`), se renombró el slot existente a
`FullBodySlot`, se rompió el link viejo `Slot_0 → Root_0` y se reconstruyó la cadena de arriba, se
configuró el branch filter por hueso, se agregó la variable `IsInteracting` (categoría
"Interaction"), y todo compila sin errores nuevos (`compile_blueprint` limpio salvo 2 warnings
preexistentes del template original, ver §3.1). Nada de esto es texto — es el estado real
verificable ahora mismo en Persona abriendo `ABP_Rumi_Provisional`.

## 1. Por qué esto no requirió tocar las sub-FSM (y lo que sí las requiere)

El Slot/Montage system de Unreal ya resuelve **qué animación se ve** sin tocar la state machine:
mientras un Montage está sonando en `FullBodySlot` o `UpperBodySlot`, ese nodo reemplaza la pose de
Locomotion automáticamente, sin importar en qué sub-estado esté Idle/Move-Run/Fall. Eso ya está
construido y funcionando hoy.

Lo que el Slot/Montage system **no resuelve**, y por lo que la arquitectura original pedía un
"estado Busy/Interacting", es el **input de movimiento**: si el jugador sigue empujando el stick
mientras Rumi golpea el yunque, el `CharacterMovementComponent` lo va a seguir desplazando aunque la
animación de arriba se vea distinta (deslizamiento clásico). Ese bloqueo de input **no vive en el
AnimGraph** — vive en el Character/Controller. Por eso separo la recomendación en dos partes abajo.

## 2. Gate de Busy/Interacting — dos opciones concretas

No pude tocar `Main` ni la FSM anidada `Locomotion` por el bloqueo de tooling ya reportado
(`find_node_types`/`get_graph` fallan con "Cannot cast ... to 'Blueprint'" en cualquier subgrafo de
state machine). Lo que sigue es la receta exacta para hacerlo a mano en Persona.

### Opción A — Recomendada: sin estado nuevo en la FSM

**No crear ningún estado "Busy/Interacting" en el grafo.** Razón: el propósito real de ese gate
(según la propia arquitectura acordada) es bloquear input de movimiento, no cambiar qué animación se
ve — eso último ya lo resuelven `FullBodySlot`/`UpperBodySlot`. Un estado de FSM no tiene autoridad
sobre el input del jugador; meterlo ahí sería resolver un problema de gameplay dentro del grafo de
animación, más difícil de mantener que resolverlo donde vive el input.

Pasos exactos:

1. **En el Character (o en la mecánica del yunque de Jhasmani, J-M3):** al iniciar la interacción,
   poner `IsInteracting = true` (ya existe como variable bool en `ABP_Rumi_Provisional`, categoría
   "Interaction" — se lee, no se escribe, desde el AnimGraph) y bloquear el procesamiento de input de
   movimiento (ej. no llamar a `AddMovementInput` mientras `IsInteracting == true`, o
   `DisableInput` del eje de movimiento). Al terminar el Montage de interacción
   (callback `OnCompleted`/`OnMontageEnded` de `PlaySlotAnimationAsDynamicMontage`), poner
   `IsInteracting = false` y reactivar el input.
2. **Refuerzo defensivo dentro de la FSM anidada `Locomotion`** (abrir en Persona:
   `AnimGraph → Main → Locomotion`): en la transición `Idle → Move/Run`
   (`AnimStateTransitionNode_1` o `_2`, verificar cuál es cuál al abrirla), agregar
   `AND NOT IsInteracting` a la regla booleana existente (la que hoy probablemente compara
   `ShouldMove` o `GroundSpeed`). Esto evita que la FSM salga de Idle visualmente si queda algún
   residuo de velocidad mientras se interactúa, aunque el input ya esté bloqueado en el paso 1.
   No tocar las transiciones de `Move/Run`, `Fall` ni `HardLanding` — la interacción solo debería
   poder empezar desde reposo.

### Opción B — Solo si quieren un estado visible en Persona

Si Franco/Jhasmani prefieren ver explícitamente un estado "interactuando" en el grafo (por
claridad de diseño, no por necesidad técnica):

1. Abrir `AnimGraph → Main → Locomotion` (la FSM anidada de 4 estados).
2. Crear un estado nuevo llamado **`InteractIdle`** (no `Busy` — mantener el nombre describiendo la
   pose, no el gameplay, para que un animador que abra el grafo entienda qué anima).
3. Transición `Idle → InteractIdle`: condición `IsInteracting == true`.
4. Transición `InteractIdle → Idle`: condición `IsInteracting == false`.
5. **No conectar `InteractIdle` a `Move/Run`, `Fall` ni `HardLanding`** — solo es alcanzable desde
   `Idle` y solo vuelve a `Idle`.
6. Dentro de `InteractIdle`, reproducir temporalmente el mismo clip que `Idle` (no hace falta un
   clip nuevo todavía) — es solo un punto de anclaje visual; `FullBodySlot`/`UpperBodySlot` siguen
   siendo quienes realmente muestran golpear/tomar/colocar/feedback por encima, sin cambios.

Mi recomendación sigue siendo A: B agrega un estado y dos transiciones a mantener sin cambiar
ningún comportamiento observable, porque los Slots ya hacen el trabajo visual.

## 3. Otras piezas de la FSM que hay que preparar para que F-M1 encaje

### 3.1 Reparar `Fall → HardLanding` y `HardLanding → Idle` (bug preexistente, no introducido por mí)

El log de compilación de `ABP_Rumi_Provisional` (heredado tal cual de
`Student_Skeleton_AnimBlueprint`, no lo toqué) marca:

```
[Compiler] Fall to HardLanding will never be taken, please connect something to Can Enter Transition
[Compiler] HardLanding to Idle will never be taken, please connect something to Can Enter Transition
```

Es decir: el estado `HardLanding` existe pero es inalcanzable — cubre el hueco de "aterrizaje" que
marcamos como falta en el inventario F-M1 (MOV-07), pero está muerto. Por los nombres de variables
que ya existen en el Blueprint (`IsFalling` bool, `PeakFallSpeed` float — típicos del patrón Epic),
la regla que probablemente falta conectar es del estilo `IsFalling == false AND PeakFallSpeed >
<umbral de aterrizaje duro>` en `Fall → HardLanding`, y en `HardLanding → Idle` normalmente basta
marcar "Automatic Rule Based on Sequence Player in State" (que la transición dispare sola cuando el
clip de aterrizaje casi termina). Hay que abrir esas dos transiciones en Persona y verificar qué
regla parcial tienen hoy antes de asumir que está vacía.

### 3.2 Turn in Place (MOV-04 del inventario, imprescindible)

No existe ninguna infraestructura hoy, ni en `Main` ni en la FSM anidada. Cuando lleguen los clips
de Mixamo, va a hacer falta un estado (o dos, izquierda/derecha) alcanzable solo desde `Idle`,
con una condición basada en la diferencia entre la orientación del personaje y la del input/cámara
superando un umbral con velocidad ~0. No lo diseño en detalle todavía porque depende de qué clips
salgan elegidos en Mixamo (un solo clip con mirror, o dos clips separados).

### 3.3 Interacción y Feedback (INT-*, FBK-* del inventario)

Ya resueltos arquitectónicamente — no requieren ningún cambio adicional en la FSM. Cuando lleguen
los clips: los de golpear/tomar/colocar se reproducen como Montage en `FullBodySlot`; los de
acierto/error se reproducen como Montage en `UpperBodySlot`. Ambos slots y el layered blend ya están
construidos y verificados (§0).

## 4. Qué está construido y verificado hoy vs. qué falta a mano

| Pieza | Estado |
|---|---|
| `ABP_Rumi_Provisional`, `BS_Rumi_Provisional_Locomotion` (duplicados no destructivos) | Hecho, verificado en vivo |
| `FullBodySlot` (renombrado), `UpperBodySlot` (nuevo), `LayeredBoneBlend` (branch en Spine1) | Hecho, verificado en vivo, compila sin errores nuevos |
| Variable `IsInteracting` (bool, categoría Interaction) | Hecho, pero nadie la escribe todavía (le corresponde al Character/J-M3) |
| Gate de Busy/Interacting dentro de la FSM anidada (Opción A, §2) | Pendiente — 5 minutos en Persona, receta exacta arriba |
| Reparar `Fall→HardLanding`/`HardLanding→Idle` | Pendiente — bug preexistente, no mío, receta aproximada arriba |
| Turn in Place | Pendiente de diseño — depende de qué clips salgan de Mixamo |
| Comment boxes de categorización en el AnimGraph | Pendiente — bug del plugin MCP al crear nodos de comentario, hay que agregarlos a mano (cosmético) |
