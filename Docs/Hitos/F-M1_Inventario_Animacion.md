# F-M1 — Inventario de animación (BORRADOR pre-D-M4)

**Estado:** D-M4 (especificación de actividades de Diego) figura "Sin empezar" en el tracker. Este
inventario es un adelanto especulativo para no bloquear a Franco: en cuanto llegue la spec real de
Diego, se ajusta esta lista (altas/bajas/repriorización) y se ejecuta F-M1-06 (envío a Diego y
Jhasmani para confirmación). No se debe empezar a producir clips sobre esto sin esa confirmación.

**Supuestos usados** (a validar con Diego/Jhasmani):
- Mecánica central = resolver problemas matemáticos golpeando/manipulando un yunque, sin combate.
- Cámara isométrica fija → prioridad baja para animaciones que solo se leen en primera persona o
  en ángulos cerrados; prioridad alta para siluetas claras a distancia media.
- No se confirma aún si hay verticalidad (salto/plataformas) más allá de lo heredado de Student.
- Un solo personaje jugable (Rumi), sin NPCs animados en el alcance de F-M1..F-M5.

## 1. Auditoría cruzada contra `Content/Characters/Student/`

Ya existe una base de locomoción completa, probablemente de Jhasmani (J-M1), aunque el tracker la
marque en 0%:

| Activo existente | Cubre | Reusable para Rumi |
|---|---|---|
| `Student_Idle` | Idle | Sí, como placeholder — reemplazar por clip final en F-M3 |
| `Student_walking_Anim` | Walk | Sí, placeholder |
| `Student_Running` | Run | Sí, placeholder — **confirmar si Rumi corre** (ver supuestos) |
| `Student_Jump` | Jump (despegue) | Sí, placeholder — confirmar si hay salto en el diseño final |
| `Student_FallLoop` | Loop de caída | Sí, placeholder — falta el **Land** (aterrizaje), no existe clip |
| `Student_Skeleton_BlendSpace` | Blend Idle/Walk/Run | Base directa para el estado Locomotion de la state machine acordada |
| `Student_Skeleton_AnimBlueprint` | Estructura de AnimBP | Punto de partida técnico; hay que sumarle el estado Busy/Interacting y los Slots de Montage |

**Huecos que Student NO cubre** (nada de esto existe hoy): giro en el lugar (turn in place),
aterrizaje, cualquier interacción con el yunque, y todo el feedback de acierto/error.

## 2. Inventario categorizado

Convención de nombre propuesta (compatible con Mixamo para F-M2): `AM_Rumi_<Categoria>_<Nombre>`.

### Movimiento

| ID | Nombre | Prioridad | Estado | Notas técnicas |
|---|---|---|---|---|
| F-M1-MOV-01 | Idle | Imprescindible | Cubierto (placeholder Student) | Blend Space, peso 0 |
| F-M1-MOV-02 | Caminar | Imprescindible | Cubierto (placeholder Student) | Blend Space |
| F-M1-MOV-03 | Correr | Deseable | Cubierto (placeholder Student) | Confirmar con Diego si el ritmo de puzzle necesita correr |
| F-M1-MOV-04 | Giro en el lugar (turn in place) | Imprescindible | Falta | Isométrico fijo hace muy visible el "moonwalk" sin esto |
| F-M1-MOV-05 | Salto (despegue) | Deseable | Cubierto (placeholder Student) | Depende de si D-M3/D-M4 confirman verticalidad |
| F-M1-MOV-06 | Loop de caída | Deseable | Cubierto (placeholder Student) | Solo si hay salto/verticalidad |
| F-M1-MOV-07 | Aterrizaje (land) | Deseable | Falta | Complemento del anterior; hoy Student solo tiene el loop, no el recovery |
| F-M1-MOV-08 | Idle variations (respiración, micro-gesto) | Deseable | Falta | Evita repetición en cámara fija; Additive sobre el Idle base |

### Interacción (con el yunque / objetos del puzzle)

| ID | Nombre | Prioridad | Estado | Notas técnicas |
|---|---|---|---|---|
| F-M1-INT-01 | Entrar a estado Interacting (transición Locomotion→Busy) | Imprescindible | Falta | Bloquea input de movimiento por diseño de AnimBP acordado |
| F-M1-INT-02 | Idle de interacción (parado frente al yunque) | Imprescindible | Falta | Pose base del estado Busy |
| F-M1-INT-03 | Golpear el yunque (gesto base) | Imprescindible | Falta | Montage vía Slot; overlap con F-M4 pero el borrador base nace en F-M1 |
| F-M1-INT-04 | Tomar / agarrar objeto | Imprescindible* | Falta | *Condicionado a que D-M4 confirme mecánica de "piezas" físicas |
| F-M1-INT-05 | Colocar objeto en el yunque | Imprescindible* | Falta | *Mismo condicionamiento que el anterior |
| F-M1-INT-06 | Salir de Interacting (retorno a Locomotion) | Imprescindible | Falta | Puede ser el mismo clip que INT-01 en reversa |
| F-M1-INT-07 | Variación de golpe (fuerte/suave por dificultad) | Deseable | Falta | Solo si Jhasmani diferencia feedback por nivel de dificultad |

### Feedback (acierto / error / reintento)

| ID | Nombre | Prioridad | Estado | Notas técnicas |
|---|---|---|---|---|
| F-M1-FBK-01 | Acierto (celebración corta) | Imprescindible | Falta | Montage, Slot UpperBody para no cortar Locomotion si aplica |
| F-M1-FBK-02 | Error (frustración/negación breve) | Imprescindible | Falta | Montage corto, no debe bloquear el reintento inmediato |
| F-M1-FBK-03 | Reintento (pose de "pensar") | Imprescindible | Falta | Podría ser Idle variation reusada en vez de clip nuevo |
| F-M1-FBK-04 | Progreso intermedio (ánimo a mitad de actividad) | Deseable | Falta | Solo si D-M4 define feedback incremental, no binario |
| F-M1-FBK-05 | Celebración de fin de nivel | Deseable | Falta | Alcance de pulido (F-M5), no bloquea la PoC mínima |

## 3. Encaje con la arquitectura de AnimBP acordada

- **Locomotion State Machine** (Idle/Walk/Run vía Blend Space): cubre toda la sección Movimiento
  salvo Turn in Place y Land, que son estados/lógica adicional dentro del mismo state machine, no
  Montages.
- **Estado Busy/Interacting**: cubre toda la sección Interacción como estado único, con las
  variaciones (golpear, tomar, colocar) resueltas dentro por Montages en Slot, tal como se acordó
  para evitar explosión de transiciones.
- **Feedback**: 100% Montages en Slots, disparables por Jhasmani desde eventos de gameplay sin
  tocar la state machine — no requieren estado nuevo.

## 4. Preguntas abiertas para Diego/Jhasmani (bloquean confirmar prioridades)

1. ¿Rumi corre, o el ritmo de puzzle es solo caminar? (afecta MOV-03)
2. ¿Hay verticalidad/salto en el diseño de nivel, o es solo movimiento en el plano? (afecta MOV-05/06/07)
3. ¿La interacción con el yunque involucra objetos físicos (tomar/colocar piezas) o es abstracta
   (acercarse + un solo gesto de "golpear")? (afecta INT-04/05)
4. ¿El feedback de error permite reintento inmediato o hay un estado de "bloqueo" temporal?
   (afecta FBK-02/03)

## 5. Candidatos de Mixamo (previsualizados en vivo sobre `Student`)

Se subió `Student` (exportado a FBX desde el editor) a Mixamo como personaje custom — el rig ya usa
nomenclatura de huesos Mixamo, así que no pidió mapeo manual. Cada clip de abajo se previsualizó
retargeteado sobre este rig real, no sobre el maniquí genérico. Importante: **Mixamo no tiene URL
propia por animación** (es un SPA sin deep-link por clip) — el link que se puede dar es el de la
búsqueda; el clip exacto hay que seleccionarlo de la lista por nombre.

| Categoría F-M1 | Opción A | Opción B | Link de búsqueda |
|---|---|---|---|
| Giro en el lugar (MOV-04) | **Turning** — paramétrico (Turn Angle ajustable -180 a 180, cubre izq/der/180 con un solo clip) | **Right Turn** — clip fijo de 31 frames, limpio | https://www.mixamo.com/#/?query=turn |
| Golpear el yunque (INT-03) | **Smash** — paramétrico (Direction/Violence, sirve para variar intensidad fuerte/suave) | **One Hand Club Combo** — combo de varios golpes caminando, recortar al primer golpe con el slider Trim | https://www.mixamo.com/#/?query=strike (buscar "One Hand Club Combo") / https://www.mixamo.com/#/?query=slam (buscar "Smash" ahí también aparece) |
| Tomar objeto (INT-04, condicional) | **Taking Item** — agacharse y tomar algo del suelo, encaja directo | — (no se buscó segunda opción, cubre bien el caso) | https://www.mixamo.com/#/?query=examining |
| Colocar objeto (INT-05, condicional) | **Putting Down** — paramétrico (incluye Object Weight), encaja directo | — (único resultado) | https://www.mixamo.com/#/?query=putting+down |
| Acierto (FBK-01) | **Cheering** — paramétrico (Energy Level), brazos arriba, celebración grande | **Standing Cheering** — gesto más corto/contenido (puño), mejor si no se quiere cortar mucho el flujo | https://www.mixamo.com/#/?query=cheering |
| Error (FBK-02) | **Disappointed** — paramétrico (Disappointment/Arms), único resultado, encaja perfecto | **Defeated** — variante más marcada (hombros caídos), único resultado también | https://www.mixamo.com/#/?query=disappointed y https://www.mixamo.com/#/?query=defeated |
| Reintento (FBK-03) | **Thinking** — mano al mentón, único resultado, encaja perfecto | Reusar `Student_Idle` (sin descargar nada nuevo) — así lo planteaba el inventario original | https://www.mixamo.com/#/?query=thinking |

No se encontraron resultados directos para "hammer"/"mining"/"sledge" — Mixamo no tiene un
verbo genérico de "golpear con martillo sobre yunque" en su catálogo; **Smash** y **One Hand Club
Combo** son los sustitutos más cercanos y gratuitos para el blockout de F-M2.

**Alternativa de pago encontrada en ActorCore (Reallusion)**, mejor ajuste de gesto pero no gratis:

| Opción | Link | Notas |
|---|---|---|
| **Pile Driving 01** (recomendada) | https://actorcore.reallusion.com/3d-motion?orderBy=Relevance&keyword=hammer&searchType=0&asset=pile-driving-01 | Golpe descendente de pie, tag `Looping` (repetible), mocap real de mazo a dos manos — el más parecido a golpear un yunque |
| **Hammer Wall 01** (respaldo) | https://actorcore.reallusion.com/3d-motion?orderBy=Relevance&keyword=hammer&searchType=0&asset=hammer-wall-01 | Golpe a una mano, trayectoria más diagonal, también loopeable |

Ambas son del pack "Motions for Construction" (~$2.25 USD c/u o $199 el pack completo) — no requieren
login para buscar/previsualizar, pero sí cuenta + compra para descargar. El rig de ActorCore no viene
pre-nombrado estilo Mixamo (usa su propio esquema vía AccuRIG), así que igual pasaría por el IK
Retargeter de UE5, sin diferencia real de esfuerzo contra usar Mixamo. **Franco pidió no pagar — se
descarta esta opción para F-M2**, queda anotada solo como referencia para F-M3 si hiciera falta.

**Alternativa gratuita encontrada: Quaternius — Universal Animation Library 2**
(https://quaternius.com/packs/universalanimationlibrary2.html) — 130+ animaciones, **licencia CC0**
(sin restricciones, ni atribución), formato FBX, rig humanoide pensado explícitamente para
retargetear en Unreal/Godot/Unity. Se puede explorar entero en su visor interactivo en vivo:
https://quaternius.com/animviewer.html → seleccionar "Universal Animation Library 2" y buscar.

No tiene un "golpe de martillo sobre yunque" literal (se probó "mining", "hammer", sin resultados),
pero sí tiene golpes descendentes de dos manos con impulso de cuerpo completo bajo la búsqueda
"attack": **Sword_Heavy_A/B/C/D** — swing pesado a dos manos con zancada hacia adelante. Es más
"combate" que "herramienta de trabajo" (trae desplazamiento hacia adelante que habría que recortar
o adaptar para que Rumi se quede fijo frente al yunque), pero es 100% gratis, ya compatible con el
proyecto, y el mejor sustituto real encontrado hasta ahora sin pagar. Recomendado para el blockout
de F-M2 mientras no haya nada mejor.

## 6. Próximo paso

Al confirmar D-M4, ejecutar F-M1-06: enviar esta lista (ya ajustada) a Diego (completitud) y
Jhasmani (aprobación de viabilidad). En la próxima sesión con MCP: crear las carpetas de destino en
`Content/Characters/Rumi/Animations/` reflejando estas tres categorías, y extender
`Student_Skeleton_AnimBlueprint` (o su equivalente para Rumi) con el estado Busy/Interacting y los
Slots de Montage descritos arriba.
