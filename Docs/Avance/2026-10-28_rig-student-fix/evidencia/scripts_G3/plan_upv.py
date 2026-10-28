import sys; sys.path.insert(0,"D:/Dev/Computacion_Grafica/Rumi 5.8/Docs/Avance/2026-10-28_rig-student-fix/evidencia/scripts_G3")
from g3layout import *
EV="D:/Dev/Computacion_Grafica/Rumi 5.8/Docs/Avance/2026-10-28_rig-student-fix/evidencia/"
P=lambda *a:['K2Node_'+x for x in a]
GROUPS={
 'ENTRADA':   dict(color='ent', text='ENTRADA - UpdateProceduralVariables (DeltaTime) y Secuencia', n=P('FunctionEntry_0','ExecutionSequence_0')),
 'LP_CALC':   dict(color='lean',text='LEAN PITCH - calculo del objetivo (GroundSpeed)', n=P('VariableGet_1','PromotableOperator_0','PromotableOperator_1','CallFunction_0')),
 'LP_OUT':    dict(color='sal', text='LEAN PITCH - interpolacion y salida', n=P('VariableGet_2','CallFunction_1','VariableSet_0')),
 'LR_CALC':   dict(color='lean',text='LEAN ROLL - calculo del objetivo (cambio de Yaw)', n=P('VariableGet_6','CallFunction_12','CallFunction_13','VariableGet_7','PromotableOperator_6','PromotableOperator_7','PromotableOperator_8','CallFunction_14')),
 'LR_OUT':    dict(color='sal', text='LEAN ROLL - interpolacion y salida (+ PreviousYaw)', n=P('VariableGet_8','CallFunction_15','VariableSet_3','VariableSet_4')),
 'PI_TRAZA':  dict(color='pies',text='PIE IZQ - posicion de inicio y fin de la traza', n=P('CallFunction_22','CallFunction_23','CallFunction_47','CallFunction_48','CallFunction_49','VariableGet_20','MakeArray_0')),
 'UBICACION': dict(color='ref',text='REFERENCIAS - ubicacion y direccion del Character (para trazas y mirada)', n=P('VariableGet_19','CallFunction_37','CallFunction_38','CallFunction_46','PromotableOperator_27')),
 'DBG_I':     dict(color='debug',text='DEBUG - traza pie izquierdo (DrawDebugType None)', n=P('CallFunction_26')),
 'PI_OFF':    dict(color='pies',text='PIE IZQ - calculo de offset (distancia al suelo)', n=P('CallFunction_27','PromotableOperator_13','Select_1','CallFunction_28','CallFunction_53','CommutativeAssociativeBinaryOperator_5')),
 'PI_OUT':    dict(color='sal', text='PIE IZQ - interpolacion y salida FootOffsetL', n=P('VariableGet_9','CallFunction_29','VariableSet_5')),
 'PD_TRAZA':  dict(color='pies',text='PIE DER - posicion de inicio y fin de la traza', n=P('CallFunction_30','CallFunction_50','CallFunction_51','CallFunction_52')),
 'DBG_D':     dict(color='debug',text='DEBUG - traza pie derecho (DrawDebugType None)', n=P('CallFunction_31')),
 'PD_OFF':    dict(color='pies',text='PIE DER - calculo de offset (distancia al suelo)', n=P('CallFunction_32','PromotableOperator_16','Select_2','CallFunction_33','CommutativeAssociativeBinaryOperator_6')),
 'PD_OUT':    dict(color='sal', text='PIE DER - interpolacion y salida FootOffsetR', n=P('VariableGet_10','CallFunction_34','VariableSet_6')),
 'PELVIS':    dict(color='pies',text='PELVIS - PelvisOffset = min(FootOffsetL, FootOffsetR)', n=P('CommutativeAssociativeBinaryOperator_1','VariableSet_7')),
 'AT_CALC':   dict(color='aterr',text='ATERRIZAJE - calculo del objetivo (TimeToImpact / PeakFallSpeed)', n=P('VariableGet_15','VariableGet_16','VariableGet_17','PromotableOperator_18','CommutativeAssociativeBinaryOperator_2','PromotableOperator_19','CallFunction_35','PromotableOperator_20','PromotableOperator_21','PromotableOperator_22','Select_3')),
 'AT_OUT':    dict(color='sal', text='ATERRIZAJE - interpolacion y salida LandCrouch', n=P('VariableGet_18','CallFunction_36','VariableSet_8')),
 'MI_CALC':   dict(color='mira',text='MIRADA - calculo del punto LookTarget', n=P('PromotableOperator_23','PromotableOperator_24','CallFunction_39','PromotableOperator_25')),
 'MI_OUT':    dict(color='sal', text='MIRADA - salida LookTarget y LookAlpha', n=P('VariableSet_9','VariableSet_10')),
 'ORFANOS':   dict(color='orf', text='ORFANOS - nodos con salida sin usar (no se borran)', n=P('CallFunction_24','CallFunction_25','CallFunction_41','PromotableOperator_11','PromotableOperator_12','PromotableOperator_14','PromotableOperator_15')),
}
SPEC={
 'ENTRADA':{'center_rows':(1,3),'x':0,'ord':1},
 'LP_CALC':{'row':1,'after':['ENTRADA'],'ord':2},'LP_OUT':{'row':1,'after':['LP_CALC'],'ord':3},
 'LR_CALC':{'row':2,'after':['ENTRADA'],'ord':2},'LR_OUT':{'row':2,'after':['LR_CALC'],'ord':3},
 'UBICACION':{'row':3,'after':['ENTRADA'],'ord':2},'PI_TRAZA':{'row':3,'after':['UBICACION'],'ord':3},'DBG_I':{'row':3,'after':['PI_TRAZA'],'ord':3},
 'PI_OFF':{'row':3,'after':['DBG_I'],'ord':4},'PI_OUT':{'row':3,'after':['PI_OFF'],'ord':5},
 'PD_TRAZA':{'row':4,'after':['PI_TRAZA'],'ord':6},
 'DBG_D':{'row':3,'after':['PI_OUT','PD_TRAZA'],'ord':7},'PD_OFF':{'row':3,'after':['DBG_D'],'ord':8},
 'PD_OUT':{'row':3,'after':['PD_OFF'],'ord':9},'PELVIS':{'row':3,'after':['PD_OUT'],'ord':10},
 'AT_CALC':{'row':5,'after':['ENTRADA'],'ord':2},'AT_OUT':{'row':5,'after':['AT_CALC'],'ord':3},
 'MI_CALC':{'row':6,'after':['UBICACION'],'ord':3},'MI_OUT':{'row':6,'after':['MI_CALC'],'ord':3},
 'ORFANOS':{'row':4,'after':['PD_TRAZA'],'ord':7},
}
if __name__=='__main__':
    d=json.load(open(EV+'G3b_full_antes.json',encoding='utf8'))['UpdateProceduralVariables']
    dd=json.load(open(EV+'G3_dump_antes.json',encoding='latin-1'))['UpdateProceduralVariables']
    sizes={m:est_size(n,(dd[m]['w'],dd[m]['h'])) for m,n in d.items()}
    pos0={m:(n['x'],n['y']) for m,n in d.items()}
    m0=metrics(d,pos0,sizes)
    pos,boxes,loc=place(d,sizes,GROUPS,SPEC)
    m1=metrics(d,pos,sizes)
    print('ANTES',{k:v for k,v in m0.items() if not k.startswith('_')})
    print('DESPUES',{k:v for k,v in m1.items() if not k.startswith('_')})
    print(m1['_largos']); print(m1['_solapes'])
    for gn,b in boxes.items(): print(gn,b)
