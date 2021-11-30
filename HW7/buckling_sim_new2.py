"""
Description:
This script solves the ABAQUS portion of HW5

Script by:
Ying-Kuan (Rick) Tsai & Peter Myers
Dept. of Aerospace Engineering
Texas A&M University
November 29, 2021
"""

from abaqus import *
from abaqusConstants import *
import __main__
import section
import odbSection
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import job
import sketch
import visualization
import xyPlot
import connectorBehavior
import displayGroupOdbToolset as dgo
import time
from math import atan, sin, cos, tan
from EigenvalueExtraction import findEigenValue
# from DOEmethods import LHS
# from Post_P_Script import getResults

######################################
# Variable and Fixed Design Parameters
######################################

##########################
# FEA Modeling Parameters
# (e.g., mesh seeds, step times, etc)
##########################

session.journalOptions.setValues(replayGeometry=COORDINATE,recoverGeometry=COORDINATE)

####################################
### Calculated Properties/Values ###
####################################

filename = 'PostData_HW7_buckling_eigenVal.txt'
filename_time = 'PostData_HW7_time.txt'

# ### Write data file column headings
# DataFile = open(filename,'w')
# DataFile.write('Buckling\n')
# DataFile.close()

###############################
### Generation of FEA Model ###
###############################

### Note: If you create a loop, START it here 
### (i.e., the contents of the loop below are intended)
tic = time.time()

## Taguchi
# nS = 18
# Orth_array_file = 'Orth_array_L18.txt'
# ### Write data file column headings
# DataFile = open(Orth_array_file,'r')
# A = [[0]*nV]*nS
# contents = []
# contents = DataFile.read()
# for i in range(nS):
	# A_tmp = [0]*nV
	# for j in range(nV):
		# A_tmp[j] = int(contents[i*12+j*2])
	# A[i] = A_tmp
	# # print(A[i])
# DataFile.close()

### Design variables
# t_skin = 0.1
# t_stiff = 0.2
# h_stiff = 5
# w_stiff = 5

nV = 5 # number of design variables
DV_file = 'DesignVariables.txt'
### Write data file column headings
# DataFile = open(DV_file,'r')
# A = [0]*nS
# contents = []
# contents = DataFile.read()
# for i in range(nS):
	# A[i] = contents[i]
	# print(A[i])

A = [0]*nV
i = 0
file_in = open(DV_file, 'r')
for y in file_in.read().split('\n'):
	if i<nV:
		A[i] = (float(y))
		i = i+1


file_in.close()
t_skin, t_stiff, h_stiff, w_stiff, n_stiff = A
# n_stiff = 5
w_domain = 60/n_stiff

type_bc = (XSYMM, XASYMM)

## Optimal design
nS = 1
# xDesign = [[0.100905, 2.588353, 0.289071, 0.673110, 0.856545, 0.052998]]
for i in range(nS):
	
	for j in type_bc:
		### Scripting the entire model allows its entire
		### contents to be packaged into this single file. 
		  
		# Sketch Geometry and Create Parts
		# Skin
		print 'Sketching/Creating the part'
		s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
			sheetSize=200.0)
		g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
		s.setPrimaryObject(option=STANDALONE)
		s.rectangle(point1=(0.0, 0.0), point2=(90.0, w_domain))
		p = mdb.models['Model-1'].Part(name='Skin', dimensionality=THREE_D, 
			type=DEFORMABLE_BODY)
		p = mdb.models['Model-1'].parts['Skin']
		p.BaseShell(sketch=s)
		s.unsetPrimaryObject()
		p = mdb.models['Model-1'].parts['Skin']
		session.viewports['Viewport: 1'].setValues(displayedObject=p)
		del mdb.models['Model-1'].sketches['__profile__']
		
		# Stiffener
		s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
			sheetSize=200.0)
		g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
		s1.setPrimaryObject(option=STANDALONE)
		s1.Line(point1=(0.0, h_stiff), point2=(0.0, 0.0))
		s1.VerticalConstraint(entity=g[2], addUndoState=False)
		s1.Line(point1=(0.0, 0.0), point2=(w_stiff, 0.0))
		s1.HorizontalConstraint(entity=g[3], addUndoState=False)
		s1.PerpendicularConstraint(entity1=g[2], entity2=g[3], addUndoState=False)
		p = mdb.models['Model-1'].Part(name='Stiff', dimensionality=THREE_D, 
			type=DEFORMABLE_BODY)
		p = mdb.models['Model-1'].parts['Stiff']
		p.BaseShellExtrude(sketch=s1, depth=90.0)
		s1.unsetPrimaryObject()
		p = mdb.models['Model-1'].parts['Stiff']
		session.viewports['Viewport: 1'].setValues(displayedObject=p)
		
		# Force
		s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
			sheetSize=200.0)
		g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
		s1.setPrimaryObject(option=STANDALONE)
		s1.Line(point1=(0.0, 0.0), point2=(0.0, w_domain))
		s1.VerticalConstraint(entity=g.findAt((0.0, w_domain/2)), addUndoState=False)
		p = mdb.models['Model-1'].Part(name='Force', dimensionality=THREE_D, 
			type=ANALYTIC_RIGID_SURFACE)
		p = mdb.models['Model-1'].parts['Force']
		p.AnalyticRigidSurfExtrude(sketch=s1, depth=w_domain)
		s1.unsetPrimaryObject()
		p = mdb.models['Model-1'].parts['Force']
		session.viewports['Viewport: 1'].setValues(displayedObject=p)
		del mdb.models['Model-1'].sketches['__profile__']
		
		

		# Defining the face partitions
		# First partition
		print 'Partitioning part'
		session.viewports['Viewport: 1'].view.setValues(session.views['Right'])
		p = mdb.models['Model-1'].parts['Force']
		f = p.faces
		pickedFaces = f.findAt(((0.0, w_domain/2, 0.0), ))
		v1, e, d1 = p.vertices, p.edges, p.datums
		p.PartitionFaceByShortestPath(faces=pickedFaces, point1=p.InterestingPoint(
			edge=e.findAt(coordinates=(0.0, w_domain/2, w_domain/2)), rule=MIDDLE), 
			point2=p.InterestingPoint(edge=e.findAt(coordinates=(0.0, w_domain/2, -w_domain/2)), 
			rule=MIDDLE))
		# Second partition
		p = mdb.models['Model-1'].parts['Force']
		f = p.faces
		pickedFaces = f.findAt(((0.0, 4.0, -2.0), ), ((0.0, 2.0, 2.0), ))
		v2, e1, d2 = p.vertices, p.edges, p.datums
		p.PartitionFaceByShortestPath(faces=pickedFaces, point1=p.InterestingPoint(
			edge=e1.findAt(coordinates=(0.0, 0.0, 0.0)), rule=MIDDLE), 
			point2=p.InterestingPoint(edge=e1.findAt(coordinates=(0.0, w_domain, 0.0)), 
			rule=MIDDLE))
		
		# Add a reference point
		p = mdb.models['Model-1'].parts['Force']
		v1, e, d1, n = p.vertices, p.edges, p.datums, p.nodes
		p.ReferencePoint(point=v1.findAt(coordinates=(0.0, w_domain/2, 0.0)))
		

		# Create Material
		print 'Creating the Materials'
		mdb.models['Model-1'].Material(name='Aluminum')
		mdb.models['Model-1'].materials['Aluminum'].Elastic(table=((10400000.0, 0.3), 
			))
		mdb.models['Model-1'].materials['Aluminum'].Density(table=((0.0975, ), ))
		
		#Create/Assign Section
		print 'Creating the Sections'
		print 'Assigning the Sections'
		# Skin
		p = mdb.models['Model-1'].parts['Skin']
		session.viewports['Viewport: 1'].setValues(displayedObject=p)
		mdb.models['Model-1'].HomogeneousShellSection(name='skin', preIntegrate=OFF, 
			material='Aluminum', thicknessType=UNIFORM, thickness=t_skin, 
			thicknessField='', nodalThicknessField='', idealization=NO_IDEALIZATION, 
			poissonDefinition=DEFAULT, thicknessModulus=None, temperature=GRADIENT, 
			useDensity=OFF, integrationRule=SIMPSON, numIntPts=5)
		p = mdb.models['Model-1'].parts['Skin']
		f = p.faces
		faces = f.findAt(((1.0, 1.0, 0.0), ))
		region = p.Set(faces=faces, name='Set-1')
		p = mdb.models['Model-1'].parts['Skin']
		p.SectionAssignment(region=region, sectionName='skin', offset=0.0, 
			offsetType=TOP_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
		
		
		# Stiff
		p = mdb.models['Model-1'].parts['Stiff']
		session.viewports['Viewport: 1'].setValues(displayedObject=p)
		mdb.models['Model-1'].HomogeneousShellSection(name='sitff', preIntegrate=OFF, 
			material='Aluminum', thicknessType=UNIFORM, thickness=t_stiff, 
			thicknessField='', nodalThicknessField='', idealization=NO_IDEALIZATION, 
			poissonDefinition=DEFAULT, thicknessModulus=None, temperature=GRADIENT, 
			useDensity=OFF, integrationRule=SIMPSON, numIntPts=5)
		p = mdb.models['Model-1'].parts['Stiff']
		f = p.faces
		faces = f.findAt(((0.1, 0.0, 60.0), ), ((0.0, 0.1, 60.0), ))
		region = p.Set(faces=faces, name='Set-1')
		p = mdb.models['Model-1'].parts['Stiff']
		p.SectionAssignment(region=region, sectionName='sitff', offset=0.0, 
			offsetType=TOP_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

		#Assemble Parts
		print('Placing Parts in Space')
		#Create Instances here
		a = mdb.models['Model-1'].rootAssembly
		session.viewports['Viewport: 1'].setValues(displayedObject=a)
		session.viewports['Viewport: 1'].assemblyDisplay.setValues(
			optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
		a = mdb.models['Model-1'].rootAssembly
		a.DatumCsysByDefault(CARTESIAN)
		p = mdb.models['Model-1'].parts['Force']
		a.Instance(name='Force-1', part=p, dependent=ON)
		p = mdb.models['Model-1'].parts['Skin']
		a.Instance(name='Skin-1', part=p, dependent=ON)
		p = mdb.models['Model-1'].parts['Stiff']
		a.Instance(name='Stiff-1', part=p, dependent=ON)
		
		# rotate
		a = mdb.models['Model-1'].rootAssembly
		a.rotate(instanceList=('Skin-1', 'Force-1'), axisPoint=(0.0, 0.0, 0.0), 
			axisDirection=(90.0, 0.0, 0.0), angle=90.0)
		
		# rotate
		a = mdb.models['Model-1'].rootAssembly
		a.rotate(instanceList=('Force-1', 'Skin-1'), axisPoint=(0.0, 0.0, 0.0), 
			axisDirection=(0.0, 1.0, 0.0), angle=-90.0)
		
		# translate the stiff to the reference point
		a = mdb.models['Model-1'].rootAssembly
		a.translate(instanceList=('Stiff-1', ), vector=(-w_domain/2.0, 0.0, 0.0))
		session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
		

		#Define Steps
		print 'Defining Steps'
		# Buckling, NOT static
		session.viewports['Viewport: 1'].assemblyDisplay.setValues(
			adaptiveMeshConstraints=ON)
		mdb.models['Model-1'].BuckleStep(name='Step-1', previous='Initial', numEigen=1, 
			eigensolver=LANCZOS, minEigen=None, blockSize=DEFAULT, maxBlocks=DEFAULT)
		session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
		
		# Define Interaction
		print 'Defining Interaction'
		# Constraint 1: Skin + Stiff
		session.viewports['Viewport: 1'].assemblyDisplay.setValues(interactions=ON, 
			constraints=ON, connectors=ON, engineeringFeatures=ON, 
			adaptiveMeshConstraints=OFF)
		a = mdb.models['Model-1'].rootAssembly
		f1 = a.instances['Skin-1'].faces
		faces1 = f1.findAt(((-1.0, 0.0, 30.0), ))
		leaf = dgm.LeafFromGeometry(faceSeq=faces1)
		session.viewports['Viewport: 1'].assemblyDisplay.displayGroup.remove(leaf=leaf)
		session.viewports['Viewport: 1'].view.setValues(nearPlane=161.178, 
			farPlane=282.478, width=112.721, height=57.2827, cameraPosition=(54.0495, 
			-93.2195, 234.093), cameraUpVector=(-0.0696417, 0.990725, 0.116681), 
			cameraTarget=(-15.693, -3.11763, 48.8106))
		a = mdb.models['Model-1'].rootAssembly
		s1 = a.instances['Skin-1'].faces
		side2Faces1 = s1.findAt(((-10.0/n_stiff*2, 0.0, 30.0), ))
		region1=a.Surface(side2Faces=side2Faces1, name='m_Surf-1')
		a = mdb.models['Model-1'].rootAssembly
		s1 = a.instances['Stiff-1'].faces
		side1Faces1 = s1.findAt(((-11.666667/n_stiff*2, 0.0, 30.0), ))
		region2=a.Surface(side1Faces=side1Faces1, name='s_Surf-1')
		mdb.models['Model-1'].Tie(name='Constraint-1', master=region1, slave=region2, 
			positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)
		leaf = dgm.Leaf(leafType=DEFAULT_MODEL)
		session.viewports['Viewport: 1'].assemblyDisplay.displayGroup.replace(
			leaf=leaf)
		session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
		
		
		# Constraint 2: rigid body
		a = mdb.models['Model-1'].rootAssembly
		s1 = a.instances['Force-1'].faces
		side2Faces1 = s1.findAt(((-w_domain/2-1, 1, 0.0), ), ((-w_domain/2-1, -1, 0.0), ), ((-w_domain/2+1, 
			-1, 0.0), ), ((-w_domain/2+1, 1, 0.0), ))
		region5=a.Surface(side2Faces=side2Faces1, name='Surf-3')
		a = mdb.models['Model-1'].rootAssembly
		r1 = a.instances['Force-1'].referencePoints
		refPoints1=(r1[4], )
		region1=regionToolset.Region(referencePoints=refPoints1)
		mdb.models['Model-1'].RigidBody(name='Constraint-2', refPointRegion=region1, 
			surfaceRegion=region5)
		
		# Constraint 3: force plate + skin
		session.viewports['Viewport: 1'].view.setValues(nearPlane=182.356, 
			farPlane=247.896, width=127.533, height=64.8094, cameraPosition=(163.718, 
			119.824, 45.7924), cameraUpVector=(-0.748718, 0.491965, -0.444288), 
			cameraTarget=(-15.6929, -3.11761, 48.8106))
		session.viewports['Viewport: 1'].view.setValues(nearPlane=149.893, 
			farPlane=273.383, width=104.829, height=53.272, cameraPosition=(54.7877, 
			51.7334, -148.004), cameraUpVector=(-0.690163, 0.657251, 0.302815), 
			cameraTarget=(-14.4845, -2.36225, 50.9605))
		a = mdb.models['Model-1'].rootAssembly
		f1 = a.instances['Force-1'].faces
		faces1 = f1.findAt(((-w_domain/2-1, 1, 0.0), ), ((-w_domain/2-1, -1, 0.0), ), ((-w_domain/2+1, 
			-1, 0.0), ), ((-w_domain/2+1, 1, 0.0), ))
		leaf = dgm.LeafFromGeometry(faceSeq=faces1)
		session.viewports['Viewport: 1'].assemblyDisplay.displayGroup.remove(leaf=leaf)
		session.viewports['Viewport: 1'].view.setValues(nearPlane=159.986, 
			farPlane=262.045, width=44.2285, height=22.476, viewOffsetX=10.041, 
			viewOffsetY=-0.0978743)
		leaf = dgm.Leaf(leafType=DEFAULT_MODEL)
		session.viewports['Viewport: 1'].assemblyDisplay.displayGroup.replace(
			leaf=leaf)
		session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
		a = mdb.models['Model-1'].rootAssembly
		f1 = a.instances['Force-1'].faces
		faces1 = f1.findAt(((-w_domain/2-1, 1, 0.0), ), ((-w_domain/2-1, -1, 0.0), ), ((-w_domain/2+1, 
			-1, 0.0), ), ((-w_domain/2+1, 1, 0.0), ))
		leaf = dgm.LeafFromGeometry(faceSeq=faces1)
		session.viewports['Viewport: 1'].assemblyDisplay.displayGroup.remove(leaf=leaf)
		session.viewports['Viewport: 1'].view.setValues(nearPlane=168.306, 
			farPlane=263.833, width=117.707, height=59.816, viewOffsetX=12.3327, 
			viewOffsetY=4.13871)
		session.viewports['Viewport: 1'].view.setValues(nearPlane=168.837, 
			farPlane=282.849, width=118.078, height=60.0049, cameraPosition=(45.9678, 
			75.3674, -160.968), cameraUpVector=(-0.899557, 0.335955, 0.279163), 
			cameraTarget=(5.26608, 12.5061, 43.2464), viewOffsetX=12.3716, 
			viewOffsetY=4.15177)
		session.viewports['Viewport: 1'].view.setValues(nearPlane=176.447, 
			farPlane=275.239, width=35.7993, height=18.1924, viewOffsetX=25.5599, 
			viewOffsetY=7.50309)
		a = mdb.models['Model-1'].rootAssembly
		region1=a.surfaces['Surf-3']
		a = mdb.models['Model-1'].rootAssembly
		s1 = a.instances['Skin-1'].edges
		side1Edges1 = s1.findAt(((-w_domain/2, 0.0, 0.0), ))
		s2 = a.instances['Stiff-1'].edges
		side1Edges2 = s2.findAt(((-w_domain/2, 0.1, 0.0), ), )
		region2=a.Surface(side1Edges=side1Edges1+side1Edges2, name='s_Surf-4')
		mdb.models['Model-1'].Tie(name='Constraint-3', master=region1, slave=region2, 
			positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)
		session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
		leaf = dgm.Leaf(leafType=DEFAULT_MODEL)
		session.viewports['Viewport: 1'].assemblyDisplay.displayGroup.replace(
			leaf=leaf)
		session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
		
		

		#Create Loads
		print 'Defining Loads and BCs'
		session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
			predefinedFields=ON, interactions=OFF, constraints=OFF, 
			engineeringFeatures=OFF)
		a = mdb.models['Model-1'].rootAssembly
		r1 = a.instances['Force-1'].referencePoints
		refPoints1=(r1[4], )
		region = a.Set(referencePoints=refPoints1, name='Set-3')
		mdb.models['Model-1'].ConcentratedForce(name='Load-1', createStepName='Step-1', 
			region=region, cf3=1.0, distributionType=UNIFORM, field='', localCsys=None)
		session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Initial')
		a = mdb.models['Model-1'].rootAssembly
		region = a.sets['Set-3']
		mdb.models['Model-1'].DisplacementBC(name='BC-1', createStepName='Initial', 
			region=region, u1=SET, u2=SET, u3=UNSET, ur1=SET, ur2=SET, ur3=SET, 
			amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
		a = mdb.models['Model-1'].rootAssembly
		e1 = a.instances['Skin-1'].edges
		edges1 = e1.findAt(((-22.5/n_stiff*2, 0.0, 90.0), ))
		e2 = a.instances['Stiff-1'].edges
		edges2 = e2.findAt(((-w_domain/2, 1.25, 90.0), ))
		region = a.Set(edges=edges1+edges2, name='Set-4')
		mdb.models['Model-1'].EncastreBC(name='BC-2', createStepName='Initial', 
			region=region, localCsys=None)
		
		# Asymmetric and Symmetric
		a = mdb.models['Model-1'].rootAssembly
		e1 = a.instances['Skin-1'].edges
		edges1 = e1.findAt(((0.0, 0.0, 67.5), ), ((-w_domain, 0.0, 22.5), ))
		region = a.Set(edges=edges1, name='Set-5')
		mdb.models['Model-1'].XsymmBC(name='BC-3', createStepName='Initial', 
			region=region, localCsys=None)
		mdb.models['Model-1'].boundaryConditions['BC-3'].setValues(typeName=j)
		
		
		#Mesh Parts
		print 'Meshing the Part'
		# Mesh the skin
		# session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON, loads=OFF, 
			# bcs=OFF, predefinedFields=OFF, connectors=OFF)
		# session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
			# meshTechnique=ON)
		# p = mdb.models['Model-1'].parts['Stiff']
		# session.viewports['Viewport: 1'].setValues(displayedObject=p)
		# session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
			# engineeringFeatures=OFF, mesh=ON)
		# session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
			# meshTechnique=ON)
		# p = mdb.models['Model-1'].parts['Skin']
		# session.viewports['Viewport: 1'].setValues(displayedObject=p)
		# p = mdb.models['Model-1'].parts['Skin']
		# f = p.faces
		# pickedRegions = f.findAt(((30.0, 10.0, 0.0), ))
		# p.setMeshControls(regions=pickedRegions, technique=STRUCTURED)
		# p = mdb.models['Model-1'].parts['Skin']
		# p.seedPart(size=1.0, deviationFactor=0.1, minSizeFactor=0.1)
		# elemType1 = mesh.ElemType(elemCode=S4R, elemLibrary=STANDARD, 
			# secondOrderAccuracy=OFF, hourglassControl=DEFAULT)
		# elemType2 = mesh.ElemType(elemCode=S3, elemLibrary=STANDARD)
		# p = mdb.models['Model-1'].parts['Skin']
		# f = p.faces
		# faces = f.findAt(((30.0, 10.0, 0.0), ))
		# pickedRegions =(faces, )
		# p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
		# p = mdb.models['Model-1'].parts['Skin']
		# p.generateMesh()
		
		
		# # Mesh the stiff
		# p = mdb.models['Model-1'].parts['Stiff']
		# session.viewports['Viewport: 1'].setValues(displayedObject=p)
		# p = mdb.models['Model-1'].parts['Stiff']
		# f = p.faces
		# pickedRegions = f.findAt(((3.333333, 0.0, 60.0), ), ((0.0, 1.666667, 60.0), ))
		# p.setMeshControls(regions=pickedRegions, technique=STRUCTURED)
		# p = mdb.models['Model-1'].parts['Stiff']
		# p.seedPart(size=1.0, deviationFactor=0.1, minSizeFactor=0.1)
		# p = mdb.models['Model-1'].parts['Stiff']
		# p.generateMesh()
		
		p = mdb.models['Model-1'].parts['Skin']
		session.viewports['Viewport: 1'].setValues(displayedObject=p)
		p = mdb.models['Model-1'].parts['Skin']
		p.seedPart(size=1.0, deviationFactor=0.1, minSizeFactor=0.1)
		p = mdb.models['Model-1'].parts['Skin']
		p.generateMesh()
		p = mdb.models['Model-1'].parts['Stiff']
		session.viewports['Viewport: 1'].setValues(displayedObject=p)
		p = mdb.models['Model-1'].parts['Stiff']
		p.seedPart(size=1.0, deviationFactor=0.1, minSizeFactor=0.1)
		p = mdb.models['Model-1'].parts['Stiff']
		p.generateMesh()

		#####################################
		### Creation/Execution of the Job ###
		#####################################
		print 'Creating/Running Job'

		ModelName='Model-1'

		mdb.Job(name=ModelName, model=ModelName, description='', type=ANALYSIS, 
			atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
			memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
			explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
			modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
			scratch='', multiprocessingMode=DEFAULT, numCpus=1, numGPUs=0)

		job=mdb.jobs[ModelName]

		# delete lock file, which for some reason tends to hang around, if it exists
		if os.access('%s.lck'%ModelName,os.F_OK):
			os.remove('%s.lck'%ModelName)
			
		# Run the job, then process the results.		
		job.submit()
		job.waitForCompletion()
		print 'Completed job'
		
		# mdb.Job(name='Job-1', model='Model-1', description='', type=ANALYSIS, 
			# atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
			# memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
			# explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
			# modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
			# scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
			# numGPUs=0)
		# del mdb.jobs['Model-1']
		# mdb.jobs['Job-1'].submit(consistencyChecking=OFF) 
		# o3 = session.openOdb(
			# name='C:/Users/yktsai0121/Desktop/AERO604_abaqus/HW7_script/Job-1.odb')
		# session.viewports['Viewport: 1'].setValues(displayedObject=o3)
		# session.viewports['Viewport: 1'].makeCurrent()

		toc = time.time()
		elapsedTime = toc - tic
		print elapsedTime
		
		
		print 'Extract the eigenvalue for buckling'
		eigenVal = findEigenValue(ModelName,'Step-1')
		print eigenVal
		
		print(eigenVal)
		DataFile = open(filename, 'a')
		DataFile.write('%10f\n' %(eigenVal))
		DataFile.close()
		
		print(elapsedTime)
		DataFile = open(filename_time, 'w')
		DataFile.write('elapsed time = %4f seconds\n' % elapsedTime)
		DataFile.close()

print 'DONE!!'

