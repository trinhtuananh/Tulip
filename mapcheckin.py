# Powered by Python 2.7

# To cancel the modifications performed by the script
# on the current graph, click on the undo button.

# Some useful keyboards shortcuts : 
#   * Ctrl + D : comment selected lines.
#   * Ctrl + Shift + D  : uncomment selected lines.
#   * Ctrl + I : indent selected lines.
#   * Ctrl + Shift + I  : unindent selected lines.
#   * Ctrl + Return  : run script.
#   * Ctrl + F  : find selected text.
#   * Ctrl + R  : replace selected text.
#   * Ctrl + Space  : show auto-completion dialog.

from tulip import *
from tulipgui import *
import math
from numpy import *
from time import *

def kmeans(k, properties,subgraph) :
	ClustersList = []
	BaryList = []
	NodesList = []
	
	print "Initialisation des clusters"

	for n in graph.getSubGraph(subgraph).getSubGraph("map").getEdges():
		NodesList.append(n)
	print ClustersList
	for i in range (0, k) :
		l = []
		l.append(NodesList.pop())
		ClustersList.append(l)

	print ClustersList
	print "Calcul du Barycentre pour chaque Cluster"

	for i in range (0, len(ClustersList)) :
		bary_list = CalculBarycentre(ClustersList[i], properties)
		BaryList.append(bary_list)

	print "Ajout des noeuds dans les Clusters \n"

	
	for i in range (len(NodesList)) :
		ListeBarycentre = []
		indice = CalculEuclidienne(NodesList[i], BaryList, properties) 
		ClustersList[indice].append(NodesList[i])
		for cluster in ClustersList :
			bary_list = CalculBarycentre(cluster, properties)
			ListeBarycentre.append(bary_list)
			
		BaryList = ListeBarycentre

	for i in range (len(ClustersList)) :
		ColorOfCluster(ClustersList[i], i);
		PositionOfCluster(ClustersList[i], i);

	print "rpartition dans les clusters..."
	repartition(ClustersList, BaryList, properties)	
	print "Fin du Kmeans"

def CalculBarycentre(cluster, properties) :
	bary_list = []
	for p in properties:
		val = []
		for n in cluster :
			val.append(p[n])
		v = array(val)	
		barycentre = v.mean() 
		bary_list.append(barycentre)

	return bary_list


def CalculEuclidienne(node, BaryList, properties) :
	DistanceEuclidienne = []

	for i in range (len(BaryList)) :
		total = 0
		for j in range (len(properties)) :
			carre = (properties[j][node] - BaryList[i][j])**2
			total += carre
		square = math.sqrt(total)
		DistanceEuclidienne.append(square)
	Tab = array(DistanceEuclidienne)
	
	for i in range (len(DistanceEuclidienne)) :
		if DistanceEuclidienne[i] == Tab.min() :
			return i

def ColorOfCluster(cluster, nb):
	if nb == 0 :
		color = tlp.Color(255,0,0)
	elif nb == 1 :
		color = tlp.Color(0,0,255)
	elif nb == 2 :
		color = tlp.Color(0,255,0)
	elif nb == 3 :
		color = tlp.Color(255,255,0) 
	viewColor = graph.getColorProperty("viewColor")

	for n in cluster :
		viewColor[n] = color


def PositionOfCluster(cluster, nb) :
	if nb == 0 :
		x = 0
	elif nb == 1 :
		x = 15
	elif nb == 2 :
		x = 30
	elif nb == 3 :
		x = 45

	viewLayout = graph.getLayoutProperty("viewLayout")
	y = 0
	for n in cluster :
		#viewLayout[n] = tlp.Coord(x, y, 0)
		y += 1
		sleep(0.1)
		updateVisualization()


def repartition(ClustersList, BaryList, properties):
	a = 0
	abis = 0
	while a == 0 :
		for i in range (len(ClustersList)):
			for n in ClustersList[i] :
				indice = CalculEuclidienne(n, BaryList, properties)
				if indice != i :
					ClustersList[indice].append(n)
					ClustersList[i].remove(n)	
					BaryP = CalculBarycentre(ClustersList[i], properties) 
					BaryList[i] = BaryP
					baryIndice = CalculBarycentre(ClustersList[indice], properties)
					BaryList[indice] = baryIndice
					for j in range (len(ClustersList)) :
						ColorOfCluster(ClustersList[j], j);
						PositionOfCluster(ClustersList[j], j);
					 
				else :
					abis += 1
				
				if abis > 6: 
					a = 1
					
					
def createCoord(graph):
	Coordo=graph.getIntegerProperty("Coordo")

	X = graph.getIntegerProperty("X")
	Y = graph.getIntegerProperty("Y")
	for i in graph.getNodes():
		Coordo[i]=(int(str(X[i])+str(Y[i])))
	print "fin createcoord"
		
	return graph
	
# the updateVisualization(centerViews = True) function can be called
# during script execution to update the opened views

# the pauseScript() function can be called to pause the script execution.
# To resume the script execution, you will have to click on the "Run script " button.

# the runGraphScript(scriptFile, graph) function can be called to launch another edited script on a tlp.Graph object.
# The scriptFile parameter defines the script name to call (in the form [a-zA-Z0-9_]+.py)

# the main(graph) function must be defined 
# to run the script on the current graph
def classementjour(graph):
	Timestamp = graph.getStringProperty("Timestamp")
	id_ = graph.getIntegerProperty("id")

	p=0.0
	graph.addSubGraph("Friday")
	graph.addSubGraph("Saturday")
	graph.addSubGraph("Sunday")
	for i in graph.getNodes():
		p=p+1
		if p%round(graph.numberOfNodes()/100)==0:
			print (p/graph.numberOfNodes()*100 , "%")
		if 		p==graph.numberOfNodes()-1:
			print Timestamp[i]

		if Timestamp[i][8]=="6" :
			subgraph="Friday"
		elif Timestamp[i][8]=="7":
			subgraph="Saturday"
		elif Timestamp[i][8]=="8":
			subgraph="Sunday"
			
		if not graph.getSubGraph(subgraph).isDescendantGraph(graph.getSubGraph(subgraph).getSubGraph(str(id_[i]))):
			graph.getSubGraph(subgraph).addSubGraph(str(id_[i]))
		
		graph.getSubGraph(subgraph).getSubGraph(str(id_[i])).addNode(i)

			
def subgraphperson(graph,subgraph):
	graph.getSubGraph(subgraph).addSubGraph("map")
	id_ = graph.getIntegerProperty("id")
	for i in graph.getSubGraph(subgraph).getNodes():
		if not graph.getSubGraph(subgraph).isDescendantGraph(graph.getSubGraph(subgraph).getSubGraph(str(id_[i]))):
			graph.getSubGraph(subgraph).addSubGraph(str(id_[i]))
		graph.getSubGraph(subgraph).getSubGraph(str(id_[i])).addNode(i)
		
		
#Incremente freq d'une arete à chaque deplacement entre 2 attractions
def checkinjour(graph,subgraph):
	viewColor = graph.getColorProperty("viewColor")
	freq=graph.getIntegerProperty("freq")


	viewLayout = graph.getLayoutProperty("viewLayout")
	viewSize = graph.getSizeProperty("viewSize")

	X = graph.getIntegerProperty("X")
	Y = graph.getIntegerProperty("Y")
	graph.delEdges(graph.getSubGraph(subgraph).getSubGraph("map").getEdges())

	p=0.0
	for sub in graph.getSubGraph(subgraph).getSubGraphs():
		p=p+1
		if p%round(graph.getSubGraph(subgraph).numberOfSubGraphs()/100)==0:
			print (p/graph.getSubGraph(subgraph).numberOfSubGraphs()*100 , "%")
		if sub.getName()!="map":
			a=None
			b=None
			for n in graph.getSubGraph(subgraph).getSubGraph(sub.getName()).getNodes():
				a=b
				b=n
			
				if a!=None:
					aa=None
					bb=None
					for i in graph.getSubGraph(subgraph).getSubGraph("map").getNodes():
						if X[i]==X[a] and Y[i]==Y[a] :
							aa=i
						if X[i]==X[b] and Y[i]==Y[b] :
							bb=i
						if aa!=None and bb!=None:
							break


					yy=False
					for f in graph.getSubGraph(subgraph).getSubGraph("map").getInOutEdges(aa)	:
						for g in graph.getSubGraph(subgraph).getSubGraph("map").getInOutEdges(bb):
							if f==g:
								freq[f]=freq[f]+1
							

								yy=True
								break
					if not yy :

						tmpedge=graph.getSubGraph(subgraph).getSubGraph("map").addEdge(aa,bb)
						freq[tmpedge]=0
				b=n
			
				
def colorEdges(graph,subgraph):
	freq=graph.getIntegerProperty("freq")
	viewColor = graph.getColorProperty("viewColor")

	r=0	
	for g in graph.getEdges():
		if r<freq[g]:
			r=freq[g]
	
	pas=765.0/r
	for e in graph.getSubGraph(subgraph).getSubGraph("map").getEdges():
		x=int(freq[e]*pas)
		if freq[e]<(256/pas) and freq[e]>10:
			viewColor[e]=tlp.Color(0,255,0)
		elif freq[e]<(511/pas)  and freq[e]>10:
			x=x-256
			viewColor[e]=tlp.Color(0,0,255)
		elif   freq[e]>510 :
			x=x-510
			viewColor[e]=tlp.Color(255,0,0)

def colorSpecificEdges(graph,subgraph,limit):
	freq=graph.getIntegerProperty("freq")
	viewColor = graph.getColorProperty("viewColor")

	r=0	
	for g in graph.getEdges():
		if r<freq[g]:
			r=freq[g]
	
	pas=765.0/r
	for e in graph.getSubGraph(subgraph).getSubGraph("map").getEdges():
		if freq[e]>limit :
			viewColor[e]=tlp.Color(0,0,0)
		else :
			viewColor[e]=tlp.Color(255,255,255,0)


def placementAttractions(graph,subgraph):
	viewLayout = graph.getLayoutProperty("viewLayout")
	X = graph.getIntegerProperty("X")
	Y = graph.getIntegerProperty("Y")
	for i in graph.getSubGraph(subgraph).getSubGraph("map").getNodes():
		viewLayout[i]=tlp.Coord(X[i],Y[i],0)
		
def countFreqPerAttraction(graph,subgraph):
	X = graph.getIntegerProperty("X")
	Y = graph.getIntegerProperty("Y")
	freqAttraction=graph.getIntegerProperty("FreqAttraction")
	for i in graph.getSubGraph(subgraph).getNodes():
		for j in graph.getSubGraph(subgraph).getSubGraph("map").getNodes():
			if X[i]==X[j] and Y[i]==Y[j]:
				freqAttraction[j]=freqAttraction[j]+1

def countFreqPerAttractionWE(graph):
	X = graph.getIntegerProperty("X")
	Y = graph.getIntegerProperty("Y")
	freqAttraction=graph.getIntegerProperty("FreqAttraction")
	for subgraph in graph.getSubGraphs():
		if subgraph.getName()!="mapWE":
			for i in graph.getSubGraph(subgraph.getName()).getNodes():
				for j in graph.getSubGraph("mapWE").getNodes():
					if X[i]==X[j] and Y[i]==Y[j]:
						freqAttraction[j]=freqAttraction[j]+1	
							
def generationColor(graph,subgraph):
	dico={}
	X = graph.getIntegerProperty("X")
	zone=graph.getStringProperty("zone")

	type_=graph.getSubGraph("Sunday").getSubGraph("map").getStringProperty("type")
	couleurs=[tlp.Color(125,0,0),tlp.Color(0,125,0),tlp.Color(255,0,0),tlp.Color(125,0,125),tlp.Color(0,0,255),tlp.Color(0,255,0)]
	for i in graph.getSubGraph(subgraph).getSubGraph("map").getNodes():
		print zone[i]

		if type_[i] not in dico.keys():
			dico[type_[i]]=couleurs.pop(0)
		
		if len(dico)==6:
			break
	return dico					
def colorAttractionperType(graph, subgraph,dico):
	viewColor = graph.getColorProperty("viewColor")
	type_=graph.getSubGraph(subgraph).getSubGraph("map").getStringProperty("type")

	for i in graph.getSubGraph(subgraph).getSubGraph("map").getNodes():
		viewColor[i]=dico[type_[i]]
		viewColor[i]=dico[type_[i]]

def freqCreightonPavilionperHour(graph,subgraph):
	id_ = graph.getIntegerProperty("id")

	graph.delNodes(graph.getSubGraph(subgraph).getSubGraph("creightonPavilion").getNodes())
	Timestamp = graph.getStringProperty("Timestamp")
	heure = graph.getIntegerProperty("heure")
	X = graph.getIntegerProperty("X")
	Y = graph.getIntegerProperty("Y")
	p=0
	for n in graph.getSubGraph(subgraph).getNodes():
		p=p+1
		if p%(graph.getSubGraph(subgraph).numberOfNodes()/100)==0:
			print (float(p)/graph.getSubGraph(subgraph).numberOfNodes()*100.0 , "%")
		if n not in graph.getSubGraph(subgraph).getSubGraph("creightonPavilion").getNodes() and n not in graph.getSubGraph(subgraph).getSubGraph("map").getNodes():
			if X[n]==32 and Y[n]==33:
				tmp=graph.getSubGraph(subgraph).getSubGraph("creightonPavilion").addNode()
				Timestamp[tmp]=Timestamp[n]
				t=str(Timestamp[n][10:12])
				heure[tmp]=float(t)
				id_[tmp]=id_[n]
def AttractionWE(graph):

	X = graph.getIntegerProperty("X")
	Y = graph.getIntegerProperty("Y")
	freqAttractionFriday=graph.getIntegerProperty("FreqAttractionFriday")
	freqAttractionSaturday=graph.getIntegerProperty("FreqAttractionSaturday")
	freqAttractionSunday=graph.getIntegerProperty("FreqAttractionSunday")
	for subgraph in graph.getSubGraphs():

		if subgraph.getName()!="mapWE":

			for subsubgraph in graph.getSubGraph(subgraph.getName()).getSubGraphs():

				if subsubgraph.getName()!="map":
					for n in graph.getSubGraph(subgraph.getName()).getSubGraph(subsubgraph.getName()).getNodes():
						for m in graph.getSubGraph("mapWE").getNodes():			
							if X[n]==X[m] and Y[n]==Y[m]:
								if subgraph.getName()=="Friday":
									freqAttractionFriday[m]=freqAttractionFriday[m]+1
								elif subgraph.getName()=="Saturday":
									freqAttractionSaturday[m]=freqAttractionSaturday[m]+1
								elif subgraph.getName()=="Sunday":
									freqAttractionSunday[m]=freqAttractionSunday[m]+1


def main(graph): 
	Timestamp = graph.getStringProperty("Timestamp")
	X = graph.getIntegerProperty("X")
	Y = graph.getIntegerProperty("Y")
	id_ = graph.getIntegerProperty("id")
	viewBorderColor = graph.getColorProperty("viewBorderColor")
	viewBorderWidth = graph.getDoubleProperty("viewBorderWidth")
	viewColor = graph.getColorProperty("viewColor")
	viewFont = graph.getStringProperty("viewFont")
	viewFontAwesomeIcon = graph.getStringProperty("viewFontAwesomeIcon")
	viewFontSize = graph.getIntegerProperty("viewFontSize")
	viewLabel = graph.getStringProperty("viewLabel")
	viewLabelBorderColor = graph.getColorProperty("viewLabelBorderColor")
	viewLabelBorderWidth = graph.getDoubleProperty("viewLabelBorderWidth")
	viewLabelColor = graph.getColorProperty("viewLabelColor")
	viewLabelPosition = graph.getIntegerProperty("viewLabelPosition")
	viewLayout = graph.getLayoutProperty("viewLayout")
	viewMetric = graph.getDoubleProperty("viewMetric")
	viewRotation = graph.getDoubleProperty("viewRotation")
	viewSelection = graph.getBooleanProperty("viewSelection")
	viewShape = graph.getIntegerProperty("viewShape")
	viewSize = graph.getSizeProperty("viewSize")
	viewSrcAnchorShape = graph.getIntegerProperty("viewSrcAnchorShape")
	viewSrcAnchorSize = graph.getSizeProperty("viewSrcAnchorSize")
	viewTexture = graph.getStringProperty("viewTexture")
	viewTgtAnchorShape = graph.getIntegerProperty("viewTgtAnchorShape")
	viewTgtAnchorSize = graph.getSizeProperty("viewTgtAnchorSize")
	freqAttraction=graph.getIntegerProperty("FreqAttraction")
	type_=graph.getSubGraph("Sunday").getSubGraph("map").getStringProperty("type")
	zone=graph.getStringProperty("zone")
	freq=graph.getSubGraph("Saturday").getSubGraph("map").getIntegerProperty("freq")

	dicoCouleur=generationColor(graph,"Sunday")
	print dicoCouleur
	#countFreqPerAttractionWE(graph)
	freqCreightonPavilionperHour(graph,"Friday")
	#AttractionWE(graph)
	#colorAttractionperType(graph,"Saturday",dicoCouleur)
	#colorAttractionperType(graph,"Friday",dicoCouleur)

	#colorAttractionperType(graph,"Sunday",dicoCouleur)

	#classementjour(graph)
	#checkinjour(graph, "Sunday")
	#colorSpecificEdges(graph,"Friday",700)
	#colorSpecificEdges(graph,"Saturday",900)
	#colorSpecificEdges(graph,"Sunday",1100)

	#countFreqPerAttraction(graph,"Sunday")
	#kmeans(3,[freq],"Saturday")
