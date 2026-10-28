# Borrador de mensaje para Jhasmani (F-M1-06 + validación técnica)

Diferencia clave con el reporte para el docente: a Jhasmani no le basta con que "suena bien" —
como **aprobador** y dueño de mecánicas/arquitectura, necesita el contrato técnico exacto para
poder disparar las animaciones desde su sistema (J-M3, la mecánica del yunque) sin tener que
adivinar nombres de variables o de slots. Este borrador cubre eso.

---

Hola Jhasmani, te paso el avance de F-M1 (inventario de animación) para que lo revises — es
borrador porque D-M4 de Diego sigue sin empezar, así que lo adelanté con supuestos razonables en
vez de quedarme bloqueado. Apenas confirmemos, lo cerramos como F-M1-06.

**Ya está categorizado** en Movimiento / Interacción / Feedback, con prioridad imprescindible vs
deseable — está completo en `Docs/Hitos/F-M1_Inventario_Animacion.md`.

**Cómo va a funcionar cada categoría (esto es lo que te toca a ti para engancharlo):**

- **Movimiento** (idle/caminar/correr/girar/salto/caída): vive dentro de la Locomotion State
  Machine, manejada por Blend Space según la velocidad del personaje. No necesitas dispararla vos
  — corre sola con el movimiento del jugador.

- **Interacción** (acercarse al yunque, golpear, tomar/colocar objeto): son Montages reproducidos
  por el slot **`FullBodySlot`**. Estas SÍ las tenés que disparar vos desde tu sistema de mecánica
  del yunque, en el momento en que el jugador ejecuta la acción. Mientras se reproducen, la
  variable booleana **`IsInteracting`** (ya existe en el Animation Blueprint) debe estar en `true`
  para bloquear el input de movimiento — te toca setearla vos desde el Character/Controller antes
  de disparar el Montage, y volverla a `false` al terminar.

- **Feedback** (acierto/error/reintento): son Montages reproducidos por el slot
  **`UpperBodySlot`** (con layered bone blend desde la columna hacia arriba, así no pisa la pose de
  piernas). Estas las disparás vos cuando tu sistema evalúe la respuesta del jugador —
  correcta/incorrecta — no requieren tocar `IsInteracting` porque no bloquean locomoción.

Ambos slots y la variable ya están construidos y verificados en `ABP_Rumi_Provisional`
(duplicado de `Student_Skeleton_AnimBlueprint`, no toqué nada del original). El detalle técnico
completo de la arquitectura está en `Docs/Hitos/F-M2_Arquitectura_AnimBP.md` si querés meterte más a
fondo — ahí también documenté una limitación de la herramienta que usé (no pude tocar el interior
de la state machine, solo el AnimGraph raíz) y cómo la resolví sin agregar un estado nuevo.

¿Me confirmás si el inventario categorizado te sirve así, y si el contrato de slots/variable
(`FullBodySlot`, `UpperBodySlot`, `IsInteracting`) te funciona para engancharlo desde J-M3, o
preferís otros nombres/otra forma de disparo?
