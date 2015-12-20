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
from numpy import *
from time import *
# the updateVisualization(centerViews = True) function can be called
# during script execution to update the opened views

# the pauseScript() function can be called to pause the script execution.
# To resume the script execution, you will have to click on the "Run script " button.

# the runGraphScript(scriptFile, graph) function can be called to launch another edited script on a tlp.Graph object.
# The scriptFile parameter defines the script name to call (in the form [a-zA-Z0-9_]+.py)

# the main(graph) function must be defined 
# to run the script on the current graph


def kmeans(k, properties) :
	ClustersList = []
	BaryList = []
	NodesList = []
	
	print "Initialisation des clusters"

	for n in graph.getNodes():
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
		square = sqrt(total)
		DistanceEuclidienne.append(square)
	Tab = array(DistanceEuclidienne)
	
	for i in range (len(DistanceEuclidienne)) :
		if DistanceEuclidienne[i] == Tab.min() :
			return i

def ColorOfCluster(cluster, nb):
	if nb == 0 :
		color = tlp.Color(0,100,0)
	elif nb == 1 :
		color = tlp.Color(0,191,255)
	elif nb == 2 :
		color = tlp.Color(0,0,255)
	elif nb == 3 :
		color = tlp.Color(0,0,0) 
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
		viewLayout[n] = tlp.Coord(x, y, 0)
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
	
def detecteCheckin(graph):
	X = graph.getIntegerProperty("X")
	Y = graph.getIntegerProperty("Y")
	Timestamp = graph.getStringProperty("Timestamp")
	graph.addSubGraph("test")
	Coordo=graph.getIntegerProperty("Coordo")
	type_ = graph.getStringProperty("type")
	boolentre= graph.getIntegerProperty("boolentre")
	viewColor=graph.getColorProperty("viewColor")

	for i in graph.getNodes():
		#if type_[i]!="movement":
		viewColor[i]=tlp.Color(0,0,0)
		
		if (X[i]>=94 or X[i]<2 or Y[i]>94 or Y[i]<16) and type_[i]!="movement":
			viewColor[i]=tlp.Color(255,255,0)

			graph.getSubGraph("test").addNode(i)
			
		elif type_[i]!="movement" :
			viewColor[i]=tlp.Color(255,255,0)

			
			
			#print str(Timestamp[i][10:12])+str((Timestamp[i][13:15]))
		 
		#if int(Timestamp[i][11])==8 and int(Timestamp[i][13]+Timestamp[i][14])==06:
		if type_[i]!="movement":
			boolentre[i]=1
			
			
	return graph
	
def personCount(graph):
	#renvoi tous les id differents
	person=tlp.newGraph()
	id_ = graph.getIntegerProperty("id")
	graph.addSubGraph("persons")

	IDP= []
	for i in graph.getNodes():

		if id_[i] not in IDP:
			IDP.append(id_[i])
			graph.getSubGraph("persons").addNode(i)
			
	print(len(IDP))

	return (person)
	
def place(graph ):
	print graph.numberOfNodes()
	t=graph.getLayoutProperty("viewLayout")
	X=graph.getIntegerProperty("X")
	Y = graph.getIntegerProperty("Y")
	for i in graph.getNodes():
		t[i]=tlp.Coord(X[i],Y[i],0)
	#graph.setAttribute("viewLayout",t)
	

	
def verif(graph):
	t=personCount(graph)
	id_ = graph.getIntegerProperty("id")

	for i in graph.getSubGraph("test").getNodes():
		if (id_[i]) in t:
			t.pop(t.index(id_[i]))
	print t
	
	
def getTemps(graph):
	Time = graph.getIntegerProperty("Time")
	Timestamp = graph.getStringProperty("Timestamp")

	for i in graph.getNodes():
		a=Timestamp[i][10:12] + Timestamp[i][13:15]
		Time[i]=int(a)
	print "fin gettemps"
	return graph

def representeTemps(graph):
	Stayed=graph.getIntegerProperty("Stayed")
	entre={}
	sortie={}
	Time = graph.getIntegerProperty("Time")
	id_ = graph.getIntegerProperty("id")
	t=graph.getLayoutProperty("viewLayout")
	X=graph.getIntegerProperty("X")
	Y = graph.getIntegerProperty("Y")
	viewColor=graph.getColorProperty("viewColor")

	for i in graph.getNodes():
		if id_[i] not in entre.keys():
			entre[id_[i]]=9999
		if id_[i] not in sortie.keys():
			sortie[id_[i]]=0
		if entre[id_[i]]>Time[i]:
			entre[id_[i]]=Time[i]
			
		if sortie[id_[i]]<Time[i]:
			sortie[id_[i]]=Time[i]
	print "debut ccc"
	ccc=personCount(graph)
	print len(ccc)
	for iii in ccc:
		X[iii]=entre[id_[iii]]
		Y[iii]=sortie[id_[iii]]		
		c = t[iii]
		c.setX(X[iii])
		t[iii]=c
		viewColor[iii]=tlp.Color(255,100,155)


		cc = t[iii]
		cc.setY(Y[iii])
		t[iii]=cc		
	graph.setAttribute("viewColor",viewColor)

	graph.setAttribute("viewLayout",t)
	return graph


#
def cptCheckIn(graph, subgraph):
	type_ = graph.getStringProperty("type")
	id_ = graph.getIntegerProperty("id")
	nbCheckIn=subgraph.getIntegerProperty("nbCheckIn")
	mapPersonNbCheckIn={}
	for i in subgraph.getNodes():
		mapPersonNbCheckIn[id_[i]]=0
	
	for j in graph.getNodes():
		if type_[j]=="check-in" :#and mapPersonNbCheckIn.has_key(id_[j]):
			mapPersonNbCheckIn[id_[j]]=mapPersonNbCheckIn[id_[j]]+1
			
	for k in subgraph.getNodes():
		nbCheckIn[k]=mapPersonNbCheckIn[id_[k]]
		
	return graph

def convertGraph(graph):
	graphe=tlp.newGraph()	
	graphe = personCount(graph)
	return graphe
	
def subgraphperperson(graph):
	id_ = graph.getIntegerProperty("id")

	
	for i in graph.getNodes():
		tmp=str(id_[i])
		if not graph.isSubGraph(graph.getSubGraph(tmp)):
			graph.addSubGraph(tmp)
		graph.getSubGraph(tmp).addNode(i)
		
def subgraphCheckInMovement(graph):
	id_ = graph.getIntegerProperty("id")
	type_ = graph.getStringProperty("type")
	for i in graph.getNodes():
		tmpId=str(id_[i])
		tmp=str(type_[i])
		if not graph.isSubGraph(graph.getSubGraph(tmpId)):
			graph.addSubGraph(tmpId)
		if not graph.getSubGraph(tmpId).isSubGraph(graph.getSubGraph(tmpId).getSubGraph(tmp)):
			graph.getSubGraph(tmpId).addSubGraph(tmp)
		graph.getSubGraph(tmpId).getSubGraph(tmp).addNode(i)

def detectSecurite(graph):
	type_ = graph.getStringProperty("type")
	graph.addSubGraph("Security")
	secu=tlp.newGraph()
	for i in graph.getSubGraphs():
		Timestamp = graph.getStringProperty("Timestamp")
		if graph.getSubGraph(i.getName()).getSubGraph((("check-in")))!=None:
			if graph.getSubGraph(i.getName()).getSubGraph((("check-in"))).numberOfNodes()<4:


				t=graph.getSubGraph(i.getName())
				graph.getSubGraph("Security").addCloneSubGraph(t.getName(),True)
			#graph.getSubGraph("Security").inducedSubGraph(tmp)#i.getName(),False)
			#graph.delSubGraph(graph.getSubGraph(i.getName()))

def afficheCheckInMovement(graph):
	y=0
	viewColor=graph.getColorProperty("viewColor")
	t=graph.getLayoutProperty("viewLayout")
	a=tri(graph)
	for i in a:
		y=y+1
		x=0

		if graph.getSubGraph(i.getName()).isSubGraph(graph.getSubGraph(i.getName()).getSubGraph("movement")):
			for j in graph.getSubGraph(i.getName()).getSubGraph("movement").getNodes():
				
				x=x+1
				viewColor[j]=tlp.Color(255,0,0)
				t[j]=tlp.Coord(x,y,0)

		if graph.getSubGraph(i.getName()).isSubGraph(graph.getSubGraph(i.getName()).getSubGraph("check-in")):
			for k in graph.getSubGraph(i.getName()).getSubGraph("check-in").getNodes():
				x=x+1
				viewColor[k]=tlp.Color(0,255,0)
				t[k]=tlp.Coord(x,y,0)
				
				
	graph.setAttribute("viewLayout",t)

def tri(graph):
	#tri non optimise
	t=[]
	tmp=[]
	mini=graph.getSubGraphs().next()
	for ui in graph.getSubGraphs():
		tmp.append(ui)
		
	for k in range(len(tmp)):		
		mini=tmp[0]
		for j in range(len(tmp)):
			
			if mini.numberOfNodes()>=(tmp[j]).numberOfNodes():
				mini=tmp[j]
		tmp.pop(tmp.index(mini))
		t.append(mini)

	return t
def main(graph): 
	Stayed=graph.getIntegerProperty("Stayed")
	Timestamp = graph.getStringProperty("Timestamp")
	Time = graph.getIntegerProperty("Time")

	X = graph.getIntegerProperty("X")
	Y = graph.getIntegerProperty("Y")
	t= graph.getIntegerProperty("id")
	id_ = graph.getIntegerProperty("id")
	state= graph.getIntegerProperty("state")

	type_ = graph.getStringProperty("type")
	Coordo=graph.getIntegerProperty("Coordo")
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

	#graph=createCoord(graph)
	#detecteCheckin(graph)
	#place(graph)
	#verif(graph)
	#graph=getTemps(graph)
	#graph=representeTemps(graph)
	#graph=place(graph,"e")

	#subgraphperperson(graph)
	subgraphCheckInMovement(graph)
	afficheCheckInMovement(graph)
	#detectSecurite(graph)
	#graph=cptCheckIn(graph)
	#graph=cptCheckIn(graph,graph.getSubGraph("persons"))
	#verif(graph.getSubGraph("persons"))
	
	
		
