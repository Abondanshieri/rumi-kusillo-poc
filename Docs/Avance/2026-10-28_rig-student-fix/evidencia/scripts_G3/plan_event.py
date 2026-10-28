import sys; sys.path.insert(0,"D:/Dev/Computacion_Grafica/Rumi 5.8/Docs/Avance/2026-10-28_rig-student-fix/evidencia/scripts_G3")
from g3layout import *
EV="D:/Dev/Computacion_Grafica/Rumi 5.8/Docs/Avance/2026-10-28_rig-student-fix/evidencia/"
P=lambda *a:['K2Node_'+x for x in a]
GROUPS={
 'INIT':       dict(color='ref',  text='INIT - referencias iniciales (Character / MovementComponent / PlayerCharacter)',
                    n=P('Event_1','DynamicCast_0','CallFunction_1','VariableSet_0','VariableSet_1','VariableGet_1','DynamicCast_1','VariableSet_10')),
 'ENTRADA':    dict(color='ent',  text='ENTRADA - evento BlueprintUpdateAnimation y reparto en Secuencia',
                    n=P('Event_0','VariableGet_0','ExecutionSequence_0')),
 'VELOCIDAD':  dict(color='proc', text='VELOCIDAD - Velocity y GroundSpeed',
                    n=P('VariableSet_2','VariableSet_3','VariableGet_2','VariableGet_4','CallFunction_7')),
 'DIRECCION':  dict(color='proc', text='DIRECCION - CalculateDirection y Clamp (+/-45 si no hay strafing)',
                    n=P('VariableSet_4','VariableGet_5','CallFunction_3','VariableGet_6','CallFunction_5','CallFunction_6','VariableGet_7','VariableGet_8','CallFunction_8')),
 'MOVIMIENTO': dict(color='proc', text='ESTADO DE MOVIMIENTO - ShouldMove',
                    n=P('Knot_0','VariableGet_9','CallFunction_9','PromotableOperator_2','VariableGet_10','PromotableOperator_0','CommutativeAssociativeBinaryOperator_0','VariableSet_5')),
 'LLAMADA':    dict(color='sal',  text='LLAMADA - UpdateProceduralVariables',
                    n=P('CallFunction_0')),
 'CAIDA':      dict(color='caida',text='CAIDA / SALTO - IsFalling, PeakFallSpeed, VerticalSpeed, IsSwinging',
                    n=P('Knot_1','VariableGet_11','CallFunction_10','VariableSet_6','VariableSet_7','VariableGet_3','CallFunction_12','CallFunction_13','VariableGet_12','CallFunction_14','VariableSet_13','MacroInstance_0','VariableSet_12','VariableGet_19','VariableSet_9','VariableGet_14','VariableGet_18')),
 'FALLSPEED':  dict(color='caida',text='CAIDA - FallSpeed',
                    n=P('VariableSet_14','VariableGet_16','PromotableOperator_3','CallFunction_2')),
 'DECISION':   dict(color='data', text='DATOS PROCEDURALES - decision: cae o no cae',
                    n=P('IfThenElse_3','VariableGet_15')),
 'SIN_CAIDA':  dict(color='data', text='DATOS PROCEDURALES - rama sin caida (reinicio de valores)',
                    n=P('VariableSet_11','VariableSet_15','VariableSet_16','VariableSet_17')),
 'TRAZA_IN':   dict(color='data', text='DATOS PROCEDURALES - inicio y fin de la traza',
                    n=P('VariableGet_17','CallFunction_22','VariableGet_20','PromotableOperator_9','CallFunction_23','PromotableOperator_10')),
 'DEBUG':      dict(color='debug',text='DEBUG - LineTraceByChannel (DrawDebugType None)',
                    n=P('CallFunction_24')),
 'TRAZA_OUT':  dict(color='data', text='DATOS PROCEDURALES - resultado de la traza y DistanceToGround',
                    n=P('CallFunction_25','VariableSet_18','PromotableOperator_11','CommutativeAssociativeBinaryOperator_2','CallFunction_26','VariableSet_19')),
 'IMPACTO':    dict(color='data', text='DATOS PROCEDURALES - TimeToImpact y LandPrep (interpolacion)',
                    n=P('VariableGet_21','CommutativeAssociativeBinaryOperator_3','PromotableOperator_12','VariableGet_22','PromotableOperator_13','CallFunction_27','VariableSet_20','PromotableOperator_14','PromotableOperator_15','CallFunction_28','CallFunction_29','VariableGet_23','CallFunction_30','VariableSet_21')),
}
SPEC={
 'INIT':{'row':0,'x':0},
 'ENTRADA':{'center_rows':(1,4),'x':0,'ord':1},
 'LLAMADA':{'row':5,'after':['ENTRADA'],'ord':2},
 'VELOCIDAD':{'row':1,'after':['ENTRADA'],'ord':3},
 'DIRECCION':{'row':1,'after':['VELOCIDAD'],'ord':4},
 'MOVIMIENTO':{'row':2,'after':['ENTRADA'],'ord':3},
 'CAIDA':{'row':3,'after':['ENTRADA'],'ord':3},
 'FALLSPEED':{'row':4,'after':['ENTRADA'],'ord':3},
 'TRAZA_IN':{'row':4,'after':['FALLSPEED'],'ord':4},
 'DECISION':{'row':4,'after':['TRAZA_IN'],'ord':5},
 'DEBUG':{'row':4,'after':['DECISION'],'ord':7},
 'TRAZA_OUT':{'row':4,'after':['DEBUG'],'ord':8},
 'IMPACTO':{'row':4,'after':['TRAZA_OUT'],'ord':9},
 'SIN_CAIDA':{'row':5,'after':['DECISION','LLAMADA'],'ord':10},
}
if __name__=='__main__':
    d=json.load(open(EV+'G3b_full_antes.json',encoding='utf8'))['EventGraph']
    rep={}
    dd=json.load(open(EV+'G3_dump_antes.json',encoding='latin-1'))['EventGraph']
    sizes={m:est_size(n,(dd[m]['w'],dd[m]['h'])) for m,n in d.items()}
    pos0={m:(n['x'],n['y']) for m,n in d.items()}
    m0=metrics(d,pos0,sizes)
    pos,boxes,loc=place(d,sizes,GROUPS,SPEC)
    m1=metrics(d,pos,sizes)
    print('ANTES',{k:v for k,v in m0.items() if not k.startswith('_')})
    print('DESPUES',{k:v for k,v in m1.items() if not k.startswith('_')})
    print(m1['_largos']); print(m1['_solapes'])
    for gn,b in boxes.items(): print(gn,b)
    json.dump({'pos':pos,'boxes':boxes},open(SPp:=EV+'G3b_plan_event.json','w'))
