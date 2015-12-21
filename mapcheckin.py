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
		
def checkinjour(graph,subgraph):
	if  graph.getSubGraph(subgraph).isDescendantGraph(graph.getSubGraph(subgraph).getSubGraph("map")):
		graph.getSubGraph(subgraph).delSubGraph(graph.getSubGraph(subgraph).getSubGraph("map"))
	graph.getSubGraph(subgraph).addSubGraph("map")

	viewLayout = graph.getLayoutProperty("viewLayout")
	viewSize = graph.getSizeProperty("viewSize")

	X = graph.getIntegerProperty("X")
	Y = graph.getIntegerProperty("Y")
	graph.delNodes(graph.getSubGraph(subgraph).getSubGraph("map").getNodes())
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
						
					if bb==None:
						bb=graph.getSubGraph(subgraph).getSubGraph("map").addNode()
						X[bb]=X[b]
						Y[bb]=Y[b]
						viewLayout[bb]=tlp.Coord(X[bb],Y[bb],0)

					if aa==None:
						aa=graph.getSubGraph(subgraph).getSubGraph("map").addNode()
						X[aa]=X[a]
						Y[aa]=Y[a]
						viewLayout[aa]=tlp.Coord(X[aa],Y[aa],0)

					yy=False
					for f in graph.getInOutEdges(aa)	:
						for g in graph.getInOutEdges(bb):
							if f==g:
								viewSize[f]=viewSize[f]+0.1
								yy=True
					if not yy :

						graph.getSubGraph(subgraph).getSubGraph("map").addEdge(bb,aa)
					
				b=n

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
	classementjour(graph)
	checkinjour(graph, "Friday")


