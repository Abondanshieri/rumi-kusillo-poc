# Propuesta: estructura ideal de Content/ (NO aplicada)

Motivo de no aplicarla: renombrar/mover .uasset en disco rompe referencias y el registro de assets esta roto en esta sesion. Se hace desde el Content Browser del editor (crea redirectors) y despues "Fix Up Redirectors".

## Estructura objetivo (por personaje)
```
Content/Characters/<Personaje>/
  Mesh/          (SK_*, Student, Student_PhysicsAsset)
  Rig/           (Skeleton, CR_*  Control Rigs, IK Rig/Retargeter)
  Animations/    (Idle, Walk, Run, Jump, Fall... ; subcarpetas Locomotion/ Interaction/ Feedback/)
  BlendSpaces/
  Montages/
  AnimBlueprints/(ABP_*)
  Materials/ Textures/
Content/Characters/_Archive/   (ya existe; Rumi_Unused con 26 assets)
```
Convencion de prefijos: `SK_`, `SKEL_`, `CR_`, `ABP_`, `BS_`, `AM_`, `AS_`/`A_` para clips, `M_`/`MI_`, `T_`.

## Plan (desde el editor)
1. Cerrar copias de trabajo; guardar todo (Ctrl+S).
2. NO tocar originales `CR_Student_Procedural`, `CR_Student_IK`, `Student_Skeleton_AnimBlueprint`, `_Backup_v5` hasta validar las copias `_fix`.
3. Arrastrar y mover en Content Browser (no en el Explorador); renombrar solo desde el editor.
4. Click derecho en Content > Fix Up Redirectors in Folder.
5. Resolver las copias `_fix` (CR_*_fix, ABP_fix): adoptar o archivar a `_Archive` segun resultado del A/B (ver `Docs/Avance/2026-10-28_rig-student-fix/informe.md`).
6. Mover los 8 assets no archivados (6 con referencias, 2 bloqueados) solo tras re-comprobar referencias con Reference Viewer.
7. Verificar: abrir mapa, PIE, sin warnings de assets faltantes; commit en git.
