# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__


#BPL Scripts: EXPLICIT MODE 
#Autor: Saint Clair
#Objetivo: Este código tem por objetivo replicar a simulação do BPL via script para que assim possa ser utilizado na GA.
#Data: 01/10/2024

import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior
import random
import numpy as np
import os
import argparse
import sys

def Create_Bolt():
    
    # Criando o modelo do Parafuso (aqui ainda não seccionado)
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
    s.FixedConstraint(entity=g[2])
    s.Line(point1=(0.0, 70.0), point2=(9.53, 70.0))
    s.HorizontalConstraint(entity=g[3], addUndoState=False)
    s.Line(point1=(9.53, 70.0), point2=(9.53, 0.0))
    s.VerticalConstraint(entity=g[4], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[3], entity2=g[4], addUndoState=False)
    s.Line(point1=(-20.0, 0.0), point2=(20.0, 0.0))
    s.HorizontalConstraint(entity=g[5], addUndoState=False)
    s.setAsConstruction(objectList=(g[5], ))
    s.copyMirror(mirrorLine=g[5], objectList=(g[3], g[4]))
    s.Line(point1=(0.0, 70.0), point2=(0.0, -70.0))
    s.PerpendicularConstraint(entity1=g[6], entity2=g[8], addUndoState=False)
    s.sketchOptions.setValues(constructionGeometry=ON)
    s.assignCenterline(line=g[2])
    p = mdb.models['Model-1'].Part(name='Bolt', dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['Bolt']
    p.BaseSolidRevolve(sketch=s, angle=360.0, flipRevolveDirection=OFF)
    s.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['Bolt']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']

def Create_Nut():
    
    # Criando a geometria da porca 

    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
    s.FixedConstraint(entity=g[2])
    s.Line(point1=(9.63, 9.32), point2=(18.79, 9.32))
    s.HorizontalConstraint(entity=g[3], addUndoState=False)
    s.Line(point1=(18.79, 9.32), point2=(18.79, 0.0))
    s.VerticalConstraint(entity=g[4], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[3], entity2=g[4], addUndoState=False)
    s.Line(point1=(-20.0, 0.0), point2=(20.0, 0.0))
    s.HorizontalConstraint(entity=g[5], addUndoState=False)
    s.setAsConstruction(objectList=(g[5], ))
    s.copyMirror(mirrorLine=g[5], objectList=(g[3], g[4]))
    s.Line(point1=(9.63, 9.32), point2=(9.63, -9.32))
    s.VerticalConstraint(entity=g[8], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[3], entity2=g[8], addUndoState=False)
    s.sketchOptions.setValues(constructionGeometry=ON)
    s.assignCenterline(line=g[2])
    p = mdb.models['Model-1'].Part(name='Nut', dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['Nut']
    p.BaseSolidRevolve(sketch=s, angle=360.0, flipRevolveDirection=OFF)
    s.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['Nut']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']

def Nut_Round():
    
    # Aplicando um 'ROUND' na porca 

    p = mdb.models['Model-1'].parts['Nut']      # p contém todo o modelo da porca (arestas, pontos, superfícies e dentre outros)
    e1 = p.edges                                # e1 contém todas as arestas da porca obtidos através da chamada de 'p.edges'
    p.Round(radius=1.0, edgeList=(e1[2], ))     # e1[2] é a aresta em que foi aplicado o round
    p = mdb.models['Model-1'].parts['Nut']
    e = p.edges
    p.Round(radius=1.0, edgeList=(e[5], ))

def Create_Claw():
    
    # Criando a geometria da Garra

    s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=800.0)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=STANDALONE)
    s1.Line(point1=(0.0, 0.0), point2=(30.0, 0.0))
    s1.HorizontalConstraint(entity=g[2], addUndoState=False)
    s1.Line(point1=(30.0, 0.0), point2=(70.4, 70.0))
    s1.Line(point1=(70.4, 70.0), point2=(70.4, 198.0))
    s1.VerticalConstraint(entity=g[4], addUndoState=False)
    s1.Line(point1=(70.4, 198.0), point2=(30.0, 268.0))
    s1.Line(point1=(30.0, 268.0), point2=(0.0, 268.0))
    s1.HorizontalConstraint(entity=g[6], addUndoState=False)
    s1.Line(point1=(0.0, 44.0), point2=(32.31, 44.0))
    s1.HorizontalConstraint(entity=g[7], addUndoState=False)
    s1.Line(point1=(32.31, 44.0), point2=(50.4, 76.43))
    s1.Line(point1=(50.4, 76.43), point2=(50.4, 191.57))
    s1.VerticalConstraint(entity=g[9], addUndoState=False)
    s1.Line(point1=(50.4, 191.57), point2=(32.31, 224.0))
    s1.Line(point1=(32.31, 224.0), point2=(0.0, 224.0))
    s1.HorizontalConstraint(entity=g[11], addUndoState=False)
    s1.Line(point1=(0.0, 300.0), point2=(0.0, -300.0))
    s1.VerticalConstraint(entity=g[12], addUndoState=False)
    s1.setAsConstruction(objectList=(g[12], ))
    s1.copyMirror(mirrorLine=g[12], objectList=(g[2], g[3], g[4], g[5], g[6], g[7], 
        g[8], g[9], g[10], g[11]))
    p = mdb.models['Model-1'].Part(name='Claw', dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['Claw']
    p.BaseSolidExtrude(sketch=s1, depth=48.0)
    s1.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['Claw']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']

def Plane_Hole():
    
    # Criando um furo superior na Garra que permitirá passar o parafuso

    p = mdb.models['Model-1'].parts['Claw']
    f = p.faces
    p.DatumPlaneByOffset(plane=f[3], flip=SIDE1, offset=0.0)
    p = mdb.models['Model-1'].parts['Claw']
    f1, e = p.faces, p.edges
    t = p.MakeSketchTransform(sketchPlane=f1[3], sketchUpEdge=e[14], 
        sketchPlaneSide=SIDE1, sketchOrientation=TOP, origin=(0.0, 268.0, 
        24.0))
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=557.59, gridSpacing=13.93, transform=t)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models['Model-1'].parts['Claw']
    p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
    s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(9.63, 0.0))
    p = mdb.models['Model-1'].parts['Claw']
    f, e1 = p.faces, p.edges
    p.CutExtrude(sketchPlane=f[3], sketchUpEdge=e1[14], sketchPlaneSide=SIDE1, 
        sketchOrientation=TOP, sketch=s, depth=46.0, flipExtrudeDirection=OFF)
    s.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__profile__']

def Claw_Fixer():
    
    # Criando a parte cilíndrica inferior a Garra onde será aplicada posteriormente as CC de fixação e aplicação da carga

    p = mdb.models['Model-1'].parts['Claw']
    f1 = p.faces
    p.DatumPlaneByOffset(plane=f1[8], flip=SIDE1, offset=0.0)
    p = mdb.models['Model-1'].parts['Claw']
    f, e = p.faces, p.edges
    t = p.MakeSketchTransform(sketchPlane=f[8], sketchUpEdge=e[29], 
        sketchPlaneSide=SIDE1, sketchOrientation=BOTTOM, origin=(0.0, 0.0, 
        24.0))
    s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=557.59, gridSpacing=13.93, transform=t)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models['Model-1'].parts['Claw']
    p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)
    s1.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(7.5, 0.0))
    p = mdb.models['Model-1'].parts['Claw']
    f1, e1 = p.faces, p.edges
    p.SolidExtrude(sketchPlane=f1[8], sketchUpEdge=e1[29], sketchPlaneSide=SIDE1, 
        sketchOrientation=BOTTOM, sketch=s1, depth=80.0, 
        flipExtrudeDirection=OFF)
    s1.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__profile__']

    # Aplicando um 'ROUND' entre a Garra e o fixador criado acima
    p = mdb.models['Model-1'].parts['Claw']
    e = p.edges
    p.Round(radius=10.0, edgeList=(e[1], ))
    p = mdb.models['Model-1'].parts['Claw']
    e1 = p.edges
    p.Round(radius=1.0, edgeList=(e1[9], ))
    p = mdb.models['Model-1'].parts['Claw']
    e = p.edges
    p.Round(radius=1.0, edgeList=(e[2], ))

def Material_Property():

    # Criando as propriedades do material (Steel)
    mdb.models['Model-1'].Material(name='Steel')
    mdb.models['Model-1'].materials['Steel'].Density(table=((7.85e-06, ), ))    # Densidade
    mdb.models['Model-1'].materials['Steel'].Elastic(table=((210000.0, 0.3), )) # Propriedades Elásticas
    mdb.models['Model-1'].HomogeneousSolidSection(name='Steel-Section', 
        material='Steel', thickness=None)
    
    # Aplicando o material no parafuso
    p = mdb.models['Model-1'].parts['Bolt']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    region = regionToolset.Region(cells=cells)
    p = mdb.models['Model-1'].parts['Bolt']
    p.SectionAssignment(region=region, sectionName='Steel-Section', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    p1 = mdb.models['Model-1'].parts['Claw']
    
    # Aplicando o material na Garra
    p = mdb.models['Model-1'].parts['Claw']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    region = regionToolset.Region(cells=cells)
    p = mdb.models['Model-1'].parts['Claw']
    p.SectionAssignment(region=region, sectionName='Steel-Section', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    
    # Aplicando o material na Porca
    p1 = mdb.models['Model-1'].parts['Nut']
    p = mdb.models['Model-1'].parts['Nut']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    region = regionToolset.Region(cells=cells)
    p = mdb.models['Model-1'].parts['Nut']
    p.SectionAssignment(region=region, sectionName='Steel-Section', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)

def Assembly():

    # Montagem das Garras
    a = mdb.models['Model-1'].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
        optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
    a = mdb.models['Model-1'].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models['Model-1'].parts['Claw']
    a.Instance(name='Claw-1', part=p, dependent=ON)
    a = mdb.models['Model-1'].rootAssembly
    p = mdb.models['Model-1'].parts['Claw']
    a.Instance(name='Claw-2', part=p, dependent=ON)
    p1 = a.instances['Claw-2']
    p1.translate(vector=(170.368, 0.0, 0.0))
    session.viewports['Viewport: 1'].view.fitView()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=560.673, 
        farPlane=1272.1, width=506.709, height=229.744, viewOffsetX=23.4124, 
        viewOffsetY=80.2522)
    a = mdb.models['Model-1'].rootAssembly
    a.rotate(instanceList=('Claw-2', ), axisPoint=(140.368, 268.0, 24.0), 
        axisDirection=(60.0, 0.0, 0.0), angle=180.0)
    a = mdb.models['Model-1'].rootAssembly
    a.translate(instanceList=('Claw-2', ), vector=(-170.368, 0.0, 0.0))

    # Montagem das Porcas
    a = mdb.models['Model-1'].rootAssembly
    p = mdb.models['Model-1'].parts['Nut']
    a.Instance(name='Nut-1', part=p, dependent=ON)
    p1 = a.instances['Nut-1']
    p1.translate(vector=(99.988, 0.0, 0.0))
    session.viewports['Viewport: 1'].view.fitView()
    a = mdb.models['Model-1'].rootAssembly
    a.translate(instanceList=('Nut-1', ), vector=(-99.988, 321.32, 24.0))
    a = mdb.models['Model-1'].rootAssembly
    p = mdb.models['Model-1'].parts['Nut']
    a.Instance(name='Nut-2', part=p, dependent=ON)
    p1 = a.instances['Nut-2']
    p1.translate(vector=(99.988, 0.0, 0.0))
    session.viewports['Viewport: 1'].view.fitView()
    a = mdb.models['Model-1'].rootAssembly
    f1 = a.instances['Nut-2'].faces
    f2 = a.instances['Claw-1'].faces
    a.FaceToFace(movablePlane=f1[4], fixedPlane=f2[2], flip=ON, clearance=0.0)
    a = mdb.models['Model-1'].rootAssembly
    f1 = a.instances['Nut-2'].faces
    f2 = a.instances['Claw-1'].faces
    a.Coaxial(movableAxis=f1[1], fixedAxis=f2[1], flip=OFF)

    # Montagem do parafuso
    p = mdb.models['Model-1'].parts['Claw']
    p.DatumPointByCoordinate(coords=(0.0, 268.0, 24.0))
    p = mdb.models['Model-1'].parts['Bolt']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    p = mdb.models['Model-1'].parts['Bolt']
    p.DatumPointByCoordinate(coords=(0.0, 0.0, 0.0))
    a1 = mdb.models['Model-1'].rootAssembly
    a1.regenerate()
    a = mdb.models['Model-1'].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    a1 = mdb.models['Model-1'].rootAssembly
    p = mdb.models['Model-1'].parts['Bolt']
    a1.Instance(name='Bolt-1', part=p, dependent=ON)
    p1 = a1.instances['Bolt-1']
    p1.translate(vector=(88.876, 0.0, 0.0))
    session.viewports['Viewport: 1'].view.fitView()
    a1 = mdb.models['Model-1'].rootAssembly
    a1.translate(instanceList=('Bolt-1', ), vector=(-88.876, 268.0, 24.0))

def Step():
    
    #Tirando o Mass Scaling como um parâmetro de variável e definindo como 0.014
    # Definição do primeiro step onde será aplicada a 'BOLT LOAD'
    mdb.models['Model-1'].ExplicitDynamicsStep(name='Bolt-Load', 
        previous='Initial', massScaling=((SEMI_AUTOMATIC, MODEL, 
        THROUGHOUT_STEP, 0.0, 0.014, BELOW_MIN, 1, 0, 0.0, 0.0, 0, None), ), 
        improvedDtMethod=ON)
    
    # Definição do segundo step onde será aplicada a 'DYNAMIC LOAD' ou carga cíclica no modelo
    mdb.models['Model-1'].ExplicitDynamicsStep(name='Dynamic-Load', timePeriod =1000.0, 
        previous='Bolt-Load', massScaling=((SEMI_AUTOMATIC, MODEL, 
        #THROUGHOUT_STEP, 0.0, mass_Scaling, BELOW_MIN, 1, 0, 0.0, 0.0, 0, None), ), 
        THROUGHOUT_STEP, 0.0, 0.014, BELOW_MIN, 1, 0, 0.0, 0.0, 0, None), ), 
        improvedDtMethod=ON)

def Defining_Surfaces():

    # Criando as surperfícies de cada geometria para poder referenciá-las durante as definições de contato posteriormente. As superfícies são:
    #   . Nut: Face Superior
    #          Parte interna da porca
    #          Face Inferior
    # 
    #   . Claw: Face Superior
     
    # Superfícies da Porca
    p = mdb.models['Model-1'].parts['Nut']
    s = p.faces
    side1Faces = s.getSequenceFromMask(mask=('[#10 ]', ), )
    p.Surface(side1Faces=side1Faces, name='Nut-Superior-Surface')

    p = mdb.models['Model-1'].parts['Nut']
    s = p.faces
    side1Faces = s.getSequenceFromMask(mask=('[#2 ]', ), )
    p.Surface(side1Faces=side1Faces, name='Nut-Interior-Surface')

    a1 = mdb.models['Model-1'].rootAssembly
    a1.regenerate()
    a = mdb.models['Model-1'].rootAssembly

    p = mdb.models['Model-1'].parts['Nut']
    p = mdb.models['Model-1'].parts['Nut']
    s = p.faces
    side1Faces = s.getSequenceFromMask(mask=('[#4 ]', ), )
    p.Surface(side1Faces=side1Faces, name='Nut-Inferior-Surface')

    # Superfícies da Garra
    p = mdb.models['Model-1'].parts['Claw']
    p = mdb.models['Model-1'].parts['Claw']
    s = p.faces
    side1Faces = s.getSequenceFromMask(mask=('[#10 ]', ), )
    p.Surface(side1Faces=side1Faces, name='Claw-Superior-Surface')

    p = mdb.models['Model-1'].parts['Claw']
    s = p.faces
    side1Faces = s.getSequenceFromMask(mask=('[#4 ]', ), )
    p.Surface(side1Faces=side1Faces, name='Claw-Inferior-Surface')

def Claw_interactions():

    # Cria-se o tipo de contato a ser imposto no tipo 'GARRA - GARRA'.
    # 
    mdb.models['Model-1'].ContactProperty('Claw-Claw-Property')
    mdb.models['Model-1'].interactionProperties['Claw-Claw-Property'].NormalBehavior(
        pressureOverclosure=HARD, allowSeparation=OFF, 
        constraintEnforcementMethod=DEFAULT)                # Para permitir separação modifique 'allowSeparation = ON'. Caso contrário, 'allowSeparation = OFF' 
    
    # Instanciando as superícies que estarão entre contato e o tipo de propriedade de contato a ser imposto a elas. Neste caso, 
    # 'Claw-Claw' 
    #
    a = mdb.models['Model-1'].rootAssembly
    region1=a.instances['Claw-1'].surfaces['Claw-Superior-Surface']
    a = mdb.models['Model-1'].rootAssembly
    region2=a.instances['Claw-2'].surfaces['Claw-Superior-Surface']
    mdb.models['Model-1'].SurfaceToSurfaceContactExp(name ='Claw-Claw', 
        createStepName='Initial', master = region1, slave = region2, 
        mechanicalConstraint=KINEMATIC, sliding=FINITE, 
        interactionProperty='Claw-Claw-Property', initialClearance=OMIT, 
        datumAxis=None, clearanceRegion=None)

def Nut_Claw_interactions():

    # # Cria-se o tipo de contato a ser imposto no tipo 'Nut - Claw'.
    # Foi definido inicialmente um contato do tipo Tangencial e um do tipo Normal
    #
    mdb.models['Model-1'].ContactProperty('Nut-Claw-Property')
    mdb.models['Model-1'].interactionProperties['Nut-Claw-Property'].TangentialBehavior(
        formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, 
        pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, 
        table=((0.1, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION, 
        fraction=0.005, elasticSlipStiffness=None)      # Para alterar o coef. de atrito basta alterar o valor presente em 'table'
    
    mdb.models['Model-1'].interactionProperties['Nut-Claw-Property'].NormalBehavior(
        pressureOverclosure=HARD, allowSeparation=ON, 
        constraintEnforcementMethod=DEFAULT)            # Para permitir separação modifique 'allowSeparation = ON'. Caso contrário, 'allowSeparation = OFF' 
    
    # Instanciando as superícies que estarão entre contato e o tipo de propriedade de contato a ser imposto a elas. Neste caso, 
    # 'Nut-Claw-Upper' 
    #
    a = mdb.models['Model-1'].rootAssembly
    region1=a.instances['Nut-1'].surfaces['Nut-Inferior-Surface']
    a = mdb.models['Model-1'].rootAssembly
    region2=a.instances['Claw-2'].surfaces['Claw-Inferior-Surface']
    mdb.models['Model-1'].SurfaceToSurfaceContactExp(name ='Nut-Claw-Upper', 
        createStepName='Initial', master = region1, slave = region2, 
        mechanicalConstraint=KINEMATIC, sliding=FINITE, 
        interactionProperty='Nut-Claw-Property', initialClearance=OMIT, 
        datumAxis=None, clearanceRegion=None)

    # Instanciando as superícies que estarão entre contato e o tipo de propriedade de contato a ser imposto a elas. Neste caso, 
    # 'Nut-Claw-Lower' 
    #
    a = mdb.models['Model-1'].rootAssembly
    region1=a.instances['Nut-2'].surfaces['Nut-Superior-Surface']
    a = mdb.models['Model-1'].rootAssembly
    region2=a.instances['Claw-1'].surfaces['Claw-Inferior-Surface']
    mdb.models['Model-1'].SurfaceToSurfaceContactExp(name ='Nut-Claw-Lower', 
        createStepName='Initial', master = region1, slave = region2, 
        mechanicalConstraint=KINEMATIC, sliding=FINITE, 
        interactionProperty='Nut-Claw-Property', initialClearance=OMIT, 
        datumAxis=None, clearanceRegion=None)

def RP():

    # Criando o Reference Point Superior do modelo 'ASSEMBLY' onde será aplicada a carga cíclica
    a = mdb.models['Model-1'].rootAssembly
    e1 = a.instances['Claw-2'].edges
    a.DatumPointByMidPoint(point1=a.instances['Claw-2'].InterestingPoint(
        edge=e1[18], rule=CENTER), 
        point2=a.instances['Claw-2'].InterestingPoint(edge=e1[16], 
        rule=CENTER))
    a = mdb.models['Model-1'].rootAssembly
    d11 = a.datums
    a.ReferencePoint(point=d11[14])
    mdb.models['Model-1'].rootAssembly.features.changeKey(fromName='RP-1', 
        toName='Top-RP')

    # Criando o Reference Point Inferior do modelo 'ASSEMBLY' onde será aplicada a CC 'ENCASTRE'
    a = mdb.models['Model-1'].rootAssembly
    e11 = a.instances['Claw-1'].edges
    a.DatumPointByMidPoint(point1=a.instances['Claw-1'].InterestingPoint(
        edge=e11[16], rule=CENTER), 
        point2=a.instances['Claw-1'].InterestingPoint(edge=e11[18], 
        rule=CENTER))
    a = mdb.models['Model-1'].rootAssembly
    d21 = a.datums
    a.ReferencePoint(point=d21[16])
    mdb.models['Model-1'].rootAssembly.features.changeKey(fromName='RP-1', 
        toName='Base-RP')

def RP_Nut_Bolt_Upper():

    # 'Reference Point' da 
    # Nut-Superior
    #
    a = mdb.models['Model-1'].rootAssembly
    e1 = a.instances['Nut-1'].edges
    a.DatumPointByMidPoint(point1=a.instances['Nut-1'].InterestingPoint(edge=e1[6], 
        rule=CENTER), point2=a.instances['Nut-1'].InterestingPoint(edge=e1[0], 
        rule=CENTER))
    a = mdb.models['Model-1'].rootAssembly
    d11 = a.datums
    a.ReferencePoint(point=d11[18])
    mdb.models['Model-1'].rootAssembly.features.changeKey(fromName='RP-1', 
        toName='RP-Nut-Upper')
    
    # 'Reference Point' da 
    # Bolt-Superior
    #
    a = mdb.models['Model-1'].rootAssembly
    r1 = a.referencePoints
    a.DatumPointByOffset(point=r1[19], vector=(0.0, 2.0, 0.0))      # 'Datum-Point' espaçado de 2 mm do 'RP' da porca
    a = mdb.models['Model-1'].rootAssembly
    d21 = a.datums
    a.ReferencePoint(point=d21[20])
    mdb.models['Model-1'].rootAssembly.features.changeKey(fromName='RP-1', 
        toName='RP-Bolt-Upper')

def RP_Nut_Bolt_Lower():

    # 'Reference Point' da 
    # Nut-Inferior
    #
    a = mdb.models['Model-1'].rootAssembly
    e11 = a.instances['Nut-2'].edges
    a.DatumPointByMidPoint(point1=a.instances['Nut-2'].InterestingPoint(
        edge=e11[0], rule=CENTER), 
        point2=a.instances['Nut-2'].InterestingPoint(edge=e11[6], rule=CENTER))
    a = mdb.models['Model-1'].rootAssembly
    d11 = a.datums
    a.ReferencePoint(point=d11[22])
    mdb.models['Model-1'].rootAssembly.features.changeKey(fromName='RP-1', 
        toName='RP-Nut-Lower')
    
    # 'Reference Point' da 
    # Bolt-Inferior
    #
    a = mdb.models['Model-1'].rootAssembly
    r11 = a.referencePoints
    a.DatumPointByOffset(point=r11[23], vector=(0.0, -2.0, 0.0))    # 'Datum-Point' espaçado de -2 mm do 'RP' da porca
    a = mdb.models['Model-1'].rootAssembly
    d21 = a.datums
    a.ReferencePoint(point=d21[24])
    mdb.models['Model-1'].rootAssembly.features.changeKey(fromName='RP-1', 
        toName='RP-Bolt-Lower')

def Bolt_Section():

    # Particionando o parafuso
    #

    # Criando dois 'Datum-Point' na parte superior do parafuso de acordo com a parte em contato com a porca no modelo
    #
    p = mdb.models['Model-1'].parts['Bolt']
    e = p.edges
    p.DatumPointByOffset(point=p.InterestingPoint(edge=e[0], rule=CENTER), vector=(
        0.0, -5.36, 0.0))                                               # Alterar a posição do 'Datum-Point' nas coordenadas se desejado
    p = mdb.models['Model-1'].parts['Bolt']
    e2, d1 = p.edges, p.datums
    p.DatumPointByOffset(point=d1[4], vector=(0.0, -18.64, 0.0))        # Alterar a posição do 'Datum-Point' nas coordenadas se desejado

    # Particionamento da região superior do parafuso 
    p = mdb.models['Model-1'].parts['Bolt']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    e, v1, d3 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(point=d3[4], normal=e[3], cells=pickedCells)
    p = mdb.models['Model-1'].parts['Bolt']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#2 ]', ), )
    e2, v2, d1 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(point=d1[5], normal=e2[1], cells=pickedCells)

    # Criando dois 'Datum-Point' na parte inferior do parafuso de acordo com a parte em contato com a porca no modelo
    #
    p = mdb.models['Model-1'].parts['Bolt']
    e = p.edges
    p.DatumPointByOffset(point=p.InterestingPoint(edge=e[5], rule=CENTER), vector=(
        0.0, 5.36, 0.0))                                                # Alterar a posição do 'Datum-Point' nas coordenadas se desejado
    p = mdb.models['Model-1'].parts['Bolt']
    e2, d3 = p.edges, p.datums
    p.DatumPointByOffset(point=d3[8], vector=(0.0, 18.64, 0.0))         # Alterar a posição do 'Datum-Point' nas coordenadas se desejado

    # Particionamento da região inferior do parafuso
    p = mdb.models['Model-1'].parts['Bolt']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#4 ]', ), )
    e, v1, d1 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(point=d1[8], normal=e[4], cells=pickedCells)
    p = mdb.models['Model-1'].parts['Bolt']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    e2, v2, d3 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(point=d3[9], normal=e2[1], cells=pickedCells)

def Bolt_Section_Surfaces():

    # Criando a superfície superior do parafuso referente a parte seccionada do parafuso criada em 'Bolt_Section()'
    #
    p = mdb.models['Model-1'].parts['Bolt']
    s = p.faces
    side1Faces = s.getSequenceFromMask(mask=('[#20 ]', ), )
    p.Surface(side1Faces=side1Faces, name='Bolt-Section-Surface-Upper')

    # Criando a superfície inferior do parafuso 
    #
    p = mdb.models['Model-1'].parts['Bolt']
    s = p.faces
    side1Faces = s.getSequenceFromMask(mask=('[#2 ]', ), )
    p.Surface(side1Faces=side1Faces, name='Bolt-Section-Surface-Lower')

def Define_Constraints():

    # Constaint do tipo 'COUPLING' entre o 'RP-Upper' e a Garra 
    #
    a = mdb.models['Model-1'].rootAssembly
    r1 = a.referencePoints
    refPoints1=(r1[15], )
    region1=regionToolset.Region(referencePoints=refPoints1)
    a = mdb.models['Model-1'].rootAssembly
    s1 = a.instances['Claw-2'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#40 ]', ), )
    region2=regionToolset.Region(side1Faces=side1Faces1)
    mdb.models['Model-1'].Coupling(name='Top-RP-Constraint', controlPoint=region1, 
        surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC, 
        localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)

    # Constaint do tipo 'COUPLING' entre o 'RP-Lower' e a Garra
    #
    a = mdb.models['Model-1'].rootAssembly
    r1 = a.referencePoints
    refPoints1=(r1[17], )
    region1=regionToolset.Region(referencePoints=refPoints1)
    a = mdb.models['Model-1'].rootAssembly
    s1 = a.instances['Claw-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#40 ]', ), )
    region2=regionToolset.Region(side1Faces=side1Faces1)
    mdb.models['Model-1'].Coupling(name='Base-RP-Constraint', controlPoint=region1, 
        surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC, 
        localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)
    
    # Constaint do tipo 'COUPLING' entre o 'RP-Nut-Upper' e a parte interna da Porca superior
    #
    a = mdb.models['Model-1'].rootAssembly
    r1 = a.referencePoints
    refPoints1=(r1[19], )
    region1=regionToolset.Region(referencePoints=refPoints1)
    a = mdb.models['Model-1'].rootAssembly
    region2=a.instances['Nut-1'].surfaces['Nut-Interior-Surface']
    mdb.models['Model-1'].Coupling(name='Nut-Upper-Constraint', 
        controlPoint=region1, surface=region2, influenceRadius=WHOLE_SURFACE, 
        couplingType=KINEMATIC, localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, 
        ur2=ON, ur3=ON)
    
    # Constaint do tipo 'COUPLING' entre o 'RP-Nut-Lower' e a parte interna da Porca inferior
    #
    a = mdb.models['Model-1'].rootAssembly
    r1 = a.referencePoints
    refPoints1=(r1[23], )
    region1=regionToolset.Region(referencePoints=refPoints1)
    a = mdb.models['Model-1'].rootAssembly
    region2=a.instances['Nut-2'].surfaces['Nut-Interior-Surface']
    mdb.models['Model-1'].Coupling(name='Nut-Lower-Constraint', 
        controlPoint=region1, surface=region2, influenceRadius=WHOLE_SURFACE, 
        couplingType=KINEMATIC, localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, 
        ur2=ON, ur3=ON)
    
    # Constaint do tipo 'COUPLING' entre o 'RP-Bolt-Upper' e a parte da superfície externa do parafuso criada em 'Bolt_Section_Surfaces'
    #
    a = mdb.models['Model-1'].rootAssembly
    r1 = a.referencePoints
    refPoints1=(r1[21], )
    region1=regionToolset.Region(referencePoints=refPoints1)
    a = mdb.models['Model-1'].rootAssembly
    region2=a.instances['Bolt-1'].surfaces['Bolt-Section-Surface-Upper']
    mdb.models['Model-1'].Coupling(name='Bolt-Upper-Constraint', 
        controlPoint=region1, surface=region2, influenceRadius=WHOLE_SURFACE, 
        couplingType=KINEMATIC, localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, 
        ur2=ON, ur3=ON)

    # Constaint do tipo 'COUPLING' entre o 'RP-Bolt-Lower' e a parte da superfície externa do parafuso criada em 'Bolt_Section_Surfaces'
    #
    a = mdb.models['Model-1'].rootAssembly
    r1 = a.referencePoints
    refPoints1=(r1[25], )
    region1=regionToolset.Region(referencePoints=refPoints1)
    a = mdb.models['Model-1'].rootAssembly
    region2=a.instances['Bolt-1'].surfaces['Bolt-Section-Surface-Lower']
    mdb.models['Model-1'].Coupling(name='Bolt-Lower-Constraint', 
        controlPoint=region1, surface=region2, influenceRadius=WHOLE_SURFACE, 
        couplingType=KINEMATIC, localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, 
        ur2=ON, ur3=ON)

def Connector_Builder():

    # Definindo o tipo de 'Connector Builder' que irá atuar entre os dois RP
    #
    mdb.models['Model-1'].ConnectorSection(name='Connector_Type', 
        assembledType=CYLINDRICAL)
    
    # Criando um 'axys' ou eixo que servirá de referência para os deslocamentos do connector force, ou seja, o deslocamento entre os RP será referente a esse novo eixo criado.
    #
    a = mdb.models['Model-1'].rootAssembly
    r1 = a.referencePoints
    dtm1 = a.DatumCsysByThreePoints(origin=r1[19], point1=r1[21], 
        coordSysType=CARTESIAN)
    dtmid1 = a.datums[dtm1.id]

    # Criando 'Connector-Force' da parte superior 
    #
    a = mdb.models['Model-1'].rootAssembly
    r11 = a.referencePoints
    wire = a.WirePolyLine(points=((r11[19], r11[21]), ), mergeType=IMPRINT, 
        meshable=False)
    oldName = wire.name
    mdb.models['Model-1'].rootAssembly.features.changeKey(fromName=oldName, 
        toName='Wire-Upper')
    a = mdb.models['Model-1'].rootAssembly
    e1 = a.edges
    edges1 = e1.getSequenceFromMask(mask=('[#1 ]', ), )
    a.Set(edges=edges1, name='Wire-Upper-Set-1')
    region = mdb.models['Model-1'].rootAssembly.sets['Wire-Upper-Set-1']
    csa = a.SectionAssignment(sectionName='Connector_Type', region=region)
    a.ConnectorOrientation(region=csa.getSet(), localCsys1=dtmid1)

    # Criando um 'axys' para a parte inferior
    #
    dtm1 = a.DatumCsysByThreePoints(origin=r11[23], point1=r11[25], 
        coordSysType=CARTESIAN)
    dtmid1 = a.datums[dtm1.id]

    # Criando 'Connector-Force' da parte inferior 
    #
    a = mdb.models['Model-1'].rootAssembly
    r1 = a.referencePoints
    wire = a.WirePolyLine(points=((r1[23], r1[25]), ), mergeType=IMPRINT, 
        meshable=False)
    oldName = wire.name
    mdb.models['Model-1'].rootAssembly.features.changeKey(fromName=oldName, 
        toName='Wire-Lower')
    a = mdb.models['Model-1'].rootAssembly
    e1 = a.edges
    edges1 = e1.getSequenceFromMask(mask=('[#1 ]', ), )
    a.Set(edges=edges1, name='Wire-Lower-Set-1')
    region = mdb.models['Model-1'].rootAssembly.sets['Wire-Lower-Set-1']
    csa = a.SectionAssignment(sectionName='Connector_Type', region=region)
    a.ConnectorOrientation(region=csa.getSet(), localCsys1=dtmid1)

def Amplitudes(amplitude_file):

    # Definindo o nome do arquivo de entrada
    arquivo_txt = amplitude_file 

    # Inicializando a lista onde os dados serão 
    data = []

    # Abrindo e lendo o arquivo .txt
    with open(arquivo_txt, 'r') as file:
        for line in file:

            # Divide cada linha em dois valores (tempo e magnitude)
            tempo = float(line.split(',')[0])
            magnitude = float(line.split(',')[1].strip())

            data.append((tempo,magnitude))

    # Convertendo a lista de dados em uma tupla de tuplas (para usar no ABAQUS)
    data = tuple(data)
    
    # Definindo a amplitude do tipo 'Tabular'
    mdb.models['Model-1'].TabularAmplitude(name='Amp-1000', timeSpan=STEP, 
        smooth=0.0, data=data)

    #Definindo a amplitude do tipo 'Decay'
    mdb.models['Model-1'].DecayAmplitude(name='Decay_Curve', timeSpan=TOTAL, 
        initial=0.0, maximum=1.0, start=0.0, decayTime=250.0)

def Load_Apply():

    # Aplicando a força no 'Wire-Upper' do tipo 'Connector Force'
    #
    a = mdb.models['Model-1'].rootAssembly
    region=a.sets['Wire-Upper-Set-1']
    mdb.models['Model-1'].ConnectorForce(name='Bolt-Load-Upper', 
        createStepName='Bolt-Load', region=region, f1=81000.0, 
        amplitude='Decay_Curve')
    
    # Aplicando a força no 'Wire-Lower' do tipo 'Connector Force'
    #
    a = mdb.models['Model-1'].rootAssembly
    region=a.sets['Wire-Lower-Set-1']
    mdb.models['Model-1'].ConnectorForce(name='Bolt-Load-Lower', 
        createStepName='Bolt-Load', region=region, f1=81000.0, 
        amplitude='Decay_Curve')
    
    # Aplicando a força cíclica no 'Top-RP'
    #
    a = mdb.models['Model-1'].rootAssembly
    r1 = a.referencePoints
    refPoints1=(r1[15], )
    region = regionToolset.Region(referencePoints=refPoints1)
    mdb.models['Model-1'].ConcentratedForce(name='Dynamic-Load', 
        createStepName='Dynamic-Load', region=region, cf2=24000.0, 
        amplitude='Amp-1000', distributionType=UNIFORM, field='', 
        localCsys=None)

def Change_Load_Step():

    # Caso necessário alternar entre as curvas de frequência entre os steps (se quiser aplicar instantânea no começo e decay na dinâmica)
    #
    mdb.models['Model-1'].loads['Bolt-Load-Upper'].setValuesInStep(
        stepName='Dynamic-Load', amplitude='Decay_Curve')

def Sets():

    # Criando Set do Parafuso
    #
    p = mdb.models['Model-1'].parts['Bolt']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1f ]', ), )
    p.Set(cells=cells, name='Bolt-Set')

    # Criando Set da Porca
    #
    p = mdb.models['Model-1'].parts['Nut']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    p.Set(cells=cells, name='Nut-Set')

    # Criando Set da Garra
    #
    p1 = mdb.models['Model-1'].parts['Claw']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p = mdb.models['Model-1'].parts['Claw']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    p.Set(cells=cells, name='Claw-Set')

def BC():

    # Criando o ENCASTRE na parte inferior do modelo
    a = mdb.models['Model-1'].rootAssembly
    r1 = a.referencePoints
    refPoints1=(r1[17], )
    region = regionToolset.Region(referencePoints=refPoints1)
    mdb.models['Model-1'].EncastreBC(name='ENCASTRE', createStepName='Initial', 
        region=region, localCsys=None)

def BC_Bolt(u1,u3,ur1,ur3):

    u1=SET if u1==1 else UNSET 
    u3=SET if u3==1 else UNSET 
    ur1=SET if ur1==1 else UNSET 
    ur3=SET if ur3==1 else UNSET

    # Criando BC da parafuso
    # As regiões definidas como 'SET' serão travadas no modelo
    a = mdb.models['Model-1'].rootAssembly
    region = a.instances['Bolt-1'].sets['Bolt-Set']
    mdb.models['Model-1'].DisplacementBC(name='Bolt_BC', createStepName='Initial', 
        region=region, u1=u1, u2=UNSET, u3=u3, ur1=ur1, ur2=UNSET, ur3=ur3, 
        amplitude=UNSET, distributionType=UNIFORM, fieldName='', 
        localCsys=None)

def BC_Nut(u1,u3,ur1,ur3):

    # Criando BC da porca superior
    # As regiões definidas como 'SET' serão travadas no modelo
    #
    u1=SET if u1==1 else UNSET 
    u3=SET if u3==1 else UNSET 
    ur1=SET if ur1==1 else UNSET 
    ur3=SET if ur3==1 else UNSET

    a = mdb.models['Model-1'].rootAssembly
    region = a.instances['Nut-1'].sets['Nut-Set']
    mdb.models['Model-1'].DisplacementBC(name='Nut-Upper', 
        createStepName='Initial', region=region, u1=u1, u2=UNSET, u3=u3, 
        ur1=ur1, ur2=UNSET, ur3=ur3, amplitude=UNSET, 
        distributionType=UNIFORM, fieldName='', localCsys=None)
    
    # Criando BC da porca inferior
    #
    a = mdb.models['Model-1'].rootAssembly
    region = a.instances['Nut-2'].sets['Nut-Set']
    mdb.models['Model-1'].DisplacementBC(name='Nut-Lower', 
        createStepName='Initial', region=region, u1=u1, u2=UNSET, u3=u3, 
        ur1=ur1, ur2=UNSET, ur3=ur3, amplitude=UNSET, 
        distributionType=UNIFORM, fieldName='', localCsys=None)
    
def BC_Claw(u2,ur2):

    # Criando BC da Garra inferior
    # As regiões definidas como 'SET' serão travadas no modelo
    #
    u2=SET if u2==1 else UNSET
    ur2=SET if ur2==1 else UNSET 

    a = mdb.models['Model-1'].rootAssembly
    region = a.instances['Claw-1'].sets['Claw-Set']
    mdb.models['Model-1'].DisplacementBC(name='Claw-Lower', 
        createStepName='Initial', region=region, u1=SET, u2=u2, u3=SET, 
        ur1=UNSET, ur2=ur2, ur3=UNSET, amplitude=UNSET, 
        distributionType=UNIFORM, fieldName='', localCsys=None)
    #Todas as rotações da garra estão livres, verificar isso
    
    # Criando BC da Garra superior
    #
    a = mdb.models['Model-1'].rootAssembly
    region = a.instances['Claw-2'].sets['Claw-Set']
    mdb.models['Model-1'].DisplacementBC(name='Claw-Upper', 
        createStepName='Initial', region=region, u1=SET, u2=u2, u3=SET, 
        ur1=UNSET, ur2=ur2, ur3=UNSET, amplitude=UNSET, 
        distributionType=UNIFORM, fieldName='', localCsys=None)
    
def Mesh_Bolt():

    # Definindo a malha do Parafuso
    #
    p = mdb.models['Model-1'].parts['Bolt']
    c = p.cells
    pickedRegions = c.getSequenceFromMask(mask=('[#1f ]', ), )
    p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
    elemType1 = mesh.ElemType(elemCode=UNKNOWN_HEX, elemLibrary=EXPLICIT)
    elemType2 = mesh.ElemType(elemCode=UNKNOWN_WEDGE, elemLibrary=EXPLICIT)
    elemType3 = mesh.ElemType(elemCode=C3D10M, elemLibrary=EXPLICIT)
    p = mdb.models['Model-1'].parts['Bolt']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1f ]', ), )
    pickedRegions =(cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
        elemType3))
    elemType1 = mesh.ElemType(elemCode=UNKNOWN_HEX, elemLibrary=EXPLICIT)
    elemType2 = mesh.ElemType(elemCode=UNKNOWN_WEDGE, elemLibrary=EXPLICIT)
    elemType3 = mesh.ElemType(elemCode=C3D10M, elemLibrary=EXPLICIT, 
        secondOrderAccuracy=OFF, distortionControl=DEFAULT)
    p = mdb.models['Model-1'].parts['Bolt']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1f ]', ), )
    pickedRegions =(cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
        elemType3))
    p = mdb.models['Model-1'].parts['Bolt']
    p.seedPart(size=2.5, deviationFactor=0.1, minSizeFactor=0.1)
    p = mdb.models['Model-1'].parts['Bolt']
    p.generateMesh()

def Mesh_Nut():

    # Definindo a malha da Porca
    #
    p = mdb.models['Model-1'].parts['Nut']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    p = mdb.models['Model-1'].parts['Nut']
    c = p.cells
    pickedRegions = c.getSequenceFromMask(mask=('[#1 ]', ), )
    p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
    elemType1 = mesh.ElemType(elemCode=UNKNOWN_HEX, elemLibrary=EXPLICIT)
    elemType2 = mesh.ElemType(elemCode=UNKNOWN_WEDGE, elemLibrary=EXPLICIT)
    elemType3 = mesh.ElemType(elemCode=C3D10M, elemLibrary=EXPLICIT)
    p = mdb.models['Model-1'].parts['Nut']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    pickedRegions =(cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
        elemType3))
    elemType1 = mesh.ElemType(elemCode=UNKNOWN_HEX, elemLibrary=EXPLICIT)
    elemType2 = mesh.ElemType(elemCode=UNKNOWN_WEDGE, elemLibrary=EXPLICIT)
    elemType3 = mesh.ElemType(elemCode=C3D10M, elemLibrary=EXPLICIT, 
        secondOrderAccuracy=OFF, distortionControl=DEFAULT)
    p = mdb.models['Model-1'].parts['Nut']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    pickedRegions =(cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
        elemType3))
    p = mdb.models['Model-1'].parts['Nut']
    p.seedPart(size=2.5, deviationFactor=0.1, minSizeFactor=0.1)
    p = mdb.models['Model-1'].parts['Nut']
    p.generateMesh()

def Mesh_Claw():

    # Definindo a malha da Garra
    #
    p = mdb.models['Model-1'].parts['Claw']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    p = mdb.models['Model-1'].parts['Claw']
    c = p.cells
    pickedRegions = c.getSequenceFromMask(mask=('[#1 ]', ), )
    p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
    elemType1 = mesh.ElemType(elemCode=UNKNOWN_HEX, elemLibrary=EXPLICIT)
    elemType2 = mesh.ElemType(elemCode=UNKNOWN_WEDGE, elemLibrary=EXPLICIT)
    elemType3 = mesh.ElemType(elemCode=C3D10M, elemLibrary=EXPLICIT)
    p = mdb.models['Model-1'].parts['Claw']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    pickedRegions =(cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
        elemType3))
    elemType1 = mesh.ElemType(elemCode=UNKNOWN_HEX, elemLibrary=EXPLICIT)
    elemType2 = mesh.ElemType(elemCode=UNKNOWN_WEDGE, elemLibrary=EXPLICIT)
    elemType3 = mesh.ElemType(elemCode=C3D10M, elemLibrary=EXPLICIT, 
        secondOrderAccuracy=OFF, distortionControl=DEFAULT)
    p = mdb.models['Model-1'].parts['Claw']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    pickedRegions =(cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
        elemType3))
    p = mdb.models['Model-1'].parts['Claw']
    p.seedPart(size=15.0, deviationFactor=0.1, minSizeFactor=0.1)
    
    # Refinando a malha na região do furo
    p = mdb.models['Model-1'].parts['Claw']
    e = p.edges
    pickedEdges = e.getSequenceFromMask(mask=('[#207 ]', ), )
    p.seedEdgeBySize(edges=pickedEdges, size=2.5, deviationFactor=0.1, 
        minSizeFactor=0.1, constraint=FINER)
    p = mdb.models['Model-1'].parts['Claw']
    p.generateMesh()
    
def Job_Create(nome_simulacao):

    # Criando o 'Job' da simulação
    #
    a1 = mdb.models['Model-1'].rootAssembly
    a1.regenerate()
    a = mdb.models['Model-1'].rootAssembly
    mdb.Job(name=nome_simulacao, model='Model-1', description='', 
        type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, 
        memory=90, memoryUnits=PERCENTAGE, explicitPrecision=SINGLE, 
        nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF, 
        contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='', 
        resultsFormat=ODB, parallelizationMethodExplicit=DOMAIN, numDomains=10, 
        activateLoadBalancing=False, multiprocessingMode=DEFAULT, numCpus=10)
    mdb.jobs[nome_simulacao].submit(consistencyChecking=OFF)

def History_Output():
     
    # Extraindo os valores de Energia interna e cinética durante o step 'Bolt-Load'
    #
    mdb.models['Model-1'].HistoryOutputRequest(name='Energy', 
        createStepName='Bolt-Load', variables=('ALLIE', 'ALLKE'), frequency=1)      # frequency representa em quantas quantidades de incremento você deseja salvar esses dados. O passo de captura dos dados.

    # Extraindo os valores de Energia interna e cinética durante o step 'Bolt-Load'
    #
    mdb.models['Model-1'].HistoryOutputRequest(name='Energy_3', 
        createStepName='Dynamic-Load', variables=('ALLIE', 'ALLKE'), 
        frequency=1)
    

# Recebendo os parâmetros passados para dentro da simulação
#
# Criando um objeto do tipo Parser() para receber os argumentos passados

parser = argparse.ArgumentParser()
parser.add_argument("--nome_da_simulacao", type=str, required=True, help="Nome da simulação a ser executada")
parser.add_argument("--garra_S_T_Y", type=int, required=True, help="Garra superior: translação no eixo Y")
parser.add_argument("--garra_I_T_Y", type=int, required=True, help="Garra inferior: translação no eixo Y")
parser.add_argument("--garra_S_R_Y", type=int, required=True, help="Garra superior: rotação no eixo Y")
parser.add_argument("--garra_I_R_Y", type=int, required=True, help="Garra inferior: rotação no eixo Y")
parser.add_argument("--rosca_S_R_X", type=int, required=True, help="Rosca superior: rotação no eixo X")
parser.add_argument("--rosca_S_R_Z", type=int, required=True, help="Rosca superior: rotação no eixo Z")
parser.add_argument("--rosca_I_R_X", type=int, required=True, help="Rosca inferior: rotação no eixo X")
parser.add_argument("--rosca_I_R_Z", type=int, required=True, help="Rosca inferior: rotação no eixo Z")
parser.add_argument("--parafuso_T_X", type=int, required=True, help="Parafuso: translação no eixo X")
parser.add_argument("--parafuso_T_Z", type=int, required=True, help="Parafuso: translação no eixo Z")
parser.add_argument("--parafuso_R_X", type=int, required=True, help="Parafuso: rotação no eixo X")
parser.add_argument("--parafuso_R_Z", type=int, required=True, help="Parafuso: rotação no eixo Z")

# Como o Abaqus passa inúmeros args para dentro da simulação, vamos pegar apenas aqueles que são do nosso problema, instanciados na chamada da função
idx = sys.argv.index("--nome_da_simulacao")
args = parser.parse_args(sys.argv[idx:])

# Recebendo os valores a cada um dos 'parser'
nome_Simulacao = args.nome_da_simulacao
garra_S_u2 = args.garra_S_T_Y
garra_I_u2 = args.garra_I_T_Y
garra_S_ur2 = args.garra_S_R_Y
garra_I_ur2 = args.garra_I_R_Y
rosca_S_ur1 = args.rosca_S_R_X
rosca_S_ur3 = args.rosca_S_R_Z
rosca_I_ur1 = args.rosca_I_R_X
rosca_I_ur3 = args.rosca_I_R_Z
parafuso_u1 = args.parafuso_T_X
parafuso_u3 = args.parafuso_T_Z
parafuso_ur1 = args.parafuso_R_X
parafuso_ur3 = args.parafuso_R_Z

# Printando na tela os parâmetros lidos para verificar se estão todos ok
print >> sys.__stdout__, "O nome da simulacao e: " , nome_Simulacao
print >> sys.__stdout__, "O valor adotado para a garra superior com translação no eixo Y e: ", garra_S_u2
print >> sys.__stdout__, "O valor adotado para a garra inferior com translação no eixo Y e: ", garra_I_u2
print >> sys.__stdout__, "O valor adotado para a garra superior com rotação no eixo Y e: ", garra_S_ur2
print >> sys.__stdout__, "O valor adotado para a garra inferior com rotação no eixo Y e: ", garra_I_ur2
print >> sys.__stdout__, "O valor adotado para a rosca superior com rotação no eixo X e: ", rosca_S_ur1
print >> sys.__stdout__, "O valor adotado para a rosca superior com rotação no eixo Z e: ", rosca_S_ur3
print >> sys.__stdout__, "O valor adotado para a rosca inferior com rotação no eixo X e: ", rosca_I_ur1
print >> sys.__stdout__, "O valor adotado para a rosca inferior com rotação no eixo Z e: ", rosca_I_ur3
print >> sys.__stdout__, "O valor adotado para o parafuso com translação no eixo X e: ", parafuso_u1
print >> sys.__stdout__, "O valor adotado para o parafuso com translação no eixo Z e: ", parafuso_u3
print >> sys.__stdout__, "O valor adotado para o parafuso com rotação no eixo X e: ", parafuso_ur1
print >> sys.__stdout__, "O valor adotado para o parafuso com rotação no eixo Z e: ", parafuso_ur3

# Criando o parafuso
Create_Bolt()

# Criando a Garra
Create_Claw()
Plane_Hole()    # Fazendo um corte na parte superior da garra
Claw_Fixer()    # Extrudando o fixador da garra e criando um 'radius' de 10 mm na base como também de 1 mm na parte superior

# Criando a porca
Create_Nut()
Nut_Round()     # Aplicando o Round da porca

# Definindo e aplicando as propriedades mecânicas no material
Material_Property()

# Criando a montagem do modelo
Assembly()

# Definindo os steps
Step(mass_Scaling=0.014)

# Criando as superfícies de cada uma das geometrias do modelo
Defining_Surfaces()

# Definindo os tipos de contato do meu modelo
Claw_interactions()
Nut_Claw_interactions()

# Criando todos os 'Reference Points' 
RP()
RP_Nut_Bolt_Upper()
RP_Nut_Bolt_Lower()

# Realizando o particionamento do parafuso
# ESTA ETAPA É OPTATIVA E PODE SER DESABILITADA SE NECESSÁRIO. PORÉM, DEVE-SE ATENTAR QUE AS 'CONSTRAINTS' DO MODELO DEVERÃO SER ALTERADAS TAMBÉM 
Bolt_Section()
Bolt_Section_Surfaces() 

# CONSTRAINTS
Define_Constraints()

# Criação dos 'CONNECTOR-FORCE' entre os RP do parafuso e a porca
Connector_Builder()

# Definindo as curvas de amplitude do modelo (Parâmetro de entrada)
# Passar para a simulação o arquivo de entrada que será utilizado para definir a frequência da curva para aplicação da carga cíclica
Amplitudes(amplitude_file=amplitude_file)

# Aplicando as forças impostas ao modelo
Load_Apply()
#Change_Load_Step()     # Ativar se necessário e modificar a função conforme desejado

# Criando 'Sets' da Porca e da Garra para referenciá-las durante os BC's aplicados
Sets()

# BC's
BC()
BC_Bolt()
BC_Nut()
BC_Claw()

# Aplicando a malha 
Mesh_Bolt()
Mesh_Nut()
Mesh_Claw()

# Rodar a simulação
Job_Create(nome_simulacao=nome_Simulacao)