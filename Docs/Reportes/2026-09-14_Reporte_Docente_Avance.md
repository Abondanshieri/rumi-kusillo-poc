# Reporte de avance — para el docente

## 1. Sobre la máquina de estados de animación (AnimBP)

Se construyó la arquitectura de animación de Rumi sobre un Animation Blueprint (el sistema de
Unreal que decide qué animación se reproduce en cada momento), con dos partes:

- **Una state machine de locomoción** (ya existía como base funcional, heredada de un personaje de
  prueba del proyecto: quieto/caminar/correr/saltar/caer) que decide sola qué animación de
  movimiento mostrar según la velocidad del personaje.
- **Un sistema de "slots" para interacción y feedback** (golpear el yunque, tomar un objeto,
  celebrar un acierto, mostrar error) que se reproduce por encima de la locomoción sin agregar más
  estados a la máquina — evita que el sistema crezca sin control a medida que se suman acciones del
  juego.

La parte de slots ya está **construida y verificada funcionando en el editor**: 2 canales de
reproducción (cuerpo completo, y solo parte superior — así el feedback de acierto/error no
interrumpe la postura de interacción) más una variable de control para bloquear el movimiento
mientras Rumi interactúa.

Queda documentado, con instrucciones exactas, un ajuste pendiente de 5-10 min de trabajo manual en
el editor (agregar una condición a una transición existente) para terminar de conectar ese bloqueo
— no se pudo automatizar por una limitación técnica de la herramienta usada, no del diseño. También
se detectó, auditando el sistema heredado, un error preexistente (una animación de aterrizaje que
existe pero nunca se activa), no introducido en este trabajo pero documentado para corregirlo.

## 2. Hitos casi listos

- **F-M1 (Inventario de animación) — borrador completo**, cubre las 4 tareas de contenido
  (F-M1-02 a F-M1-05: movimiento, interacción, feedback, prioridad). **No cerrado formalmente**:
  F-M1-01 depende de una entrega previa de un compañero (D-M4, especificación de actividades) que
  según el tracker del proyecto aún no empezó — por eso se adelantó como borrador razonado en vez
  de quedar bloqueado, y falta F-M1-06 (envío a revisión) hasta confirmar contra la spec real.
- **F-M2 (Blockout y timing) — arrancado, no completo.** F-M2-01 (montar rig provisional) resuelto
  reutilizando el personaje de prueba ya existente; la arquitectura del punto 1 ya está construida
  sobre ese rig. Falta descargar/importar los clips reales y hacer el bloqueo de timing (F-M2-02 a
  F-M2-06) — ya se identificaron las fuentes gratuitas a usar, pero ningún clip fue descargado
  todavía.

## 3. Avance por iniciativa propia

- Adelantar el borrador de F-M1 en vez de esperar bloqueado al compañero de narrativa.
- Auditar el proyecto antes de proponer trabajo nuevo: se encontró una base de personaje/animación
  de prueba ya utilizable, evitando duplicar esfuerzo creando un rig desde cero.
- Detectar un error preexistente no reportado (animación de aterrizaje inalcanzable).
- Documentar con precisión una limitación real de la herramienta usada, en vez de forzar una
  solución poco confiable o quedar bloqueado sin explicación.

## 4. Cómo funcionará cada animación

- **Movimiento** (quieto/caminar/correr/girar/saltar/caer): dentro de la state machine de
  locomoción, se disparan solas según velocidad y orientación — el jugador no las activa
  directamente.
- **Interacción** (acercarse, golpear, tomar/colocar): animaciones puntuales por el canal de cuerpo
  completo, disparadas cuando el jugador ejecuta la acción de interactuar (botón cerca del yunque);
  una variable bloquea el movimiento mientras dura.
- **Feedback** (acierto/error/reintento): animaciones puntuales por el canal de solo-parte-superior,
  disparadas cuando el sistema de mecánica del yunque (de otro compañero) evalúa la respuesta — se
  ven aunque el personaje siga en postura de interacción, sin cortarla.
- **Origen de los clips:** mayoría de una biblioteca gratuita estándar (Mixamo); para el golpe del
  yunque, sin match perfecto ahí, se identificó una biblioteca alternativa gratuita de licencia
  abierta (Quaternius) como respaldo. Sin gasto contemplado.
