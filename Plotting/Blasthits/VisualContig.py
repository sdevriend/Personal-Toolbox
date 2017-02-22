#!/usr/bin/python
"""
This script plots data onto a scatterplot for labels and rectangle object for
each blast hit per file. 

THIS SCRIPT IS USED BY VisualSamples.sh!

This script has the following input:
    Argument 1: Filelocation: Example: C:/user/data.txt
    Argument 2: Contigname: Example: Contig_2
    Argument 3: Length of contig: Example: 54332
Please make sure that the inputfile is a blast output with tabular and no 
headers.

The script requires plotly to be installed on the local machine.
"""

import sys
import plotly.graph_objs as go
import plotly.offline as pyo


def get_data(filename):
    """
    Input:
        filename: string containing filelocation and filename.
    
        The function opens a file that is set on the variable filename.
        It then reads the lines into the variable data and automatic 
        closes the file.
        
        After that the function loops through the data list and appends a
        temporary list with the first, sixth and seventh element.
        Position 1: Familyname
        Position 6: Startposition
        Position 7: Endposition
        The loop adds the temporary list into a large list with lists.
        
        The function then returns the multi-dimensional list
        
    Output:
        datanew: multi-dimensional list.
    """
    with open(filename, "r") as f:
        data = f.readlines()
    datanew = []
    for row in data:
        rowsplit = row.split("\t")
        templist = []
        templist.append(rowsplit[1])
        templist.append(rowsplit[6])
        templist.append(rowsplit[7])
        datanew.append(templist)
    return datanew

    
def processData(RAWData):
    """
    Input:
        RAWData: multi-dimensional list
    
        The function loops through the raw data and creates a dictionary in
        each loop iteration. 
        In the loop the start position of the data will be checken with the
        end positiion. If the blast hit is reversed, then the data will be
        inserted in the dictionary in reversed order with a labelspace and
        strand orientation. at the end of each iteration, the dictionary is
        added to a list.
        
        After the loop the list will be sorted on elements by the first
        position.
        
    Output:
        lstAllData: multidimensional list that is being processed by
                    the function processSorted.
    """
    lstAllData = [] # list with dictionaries
    for line in RAWData:
        dictTemp = dict(name=line[0])
        if int(line[1]) > int(line[2]):
            dictTemp['strand'] = "REV"
            dictTemp['lblPos'] = (int(line[2]) + int(line[1])) / 2
            dictTemp['start'] = int(line[2])
            dictTemp['stop'] = int(line[1])
            dictTemp['lblSpace'] = -0.1 # margin for lbl position
        else:
            dictTemp['strand'] = "FWD"
            dictTemp['lblSpace'] = 0.1 # negativ margin for reversed
            dictTemp['lblPos'] = (int(line[1]) + int(line[2])) / 2
            dictTemp['start'] = int(line[1])
            dictTemp['stop'] = int(line[2])
        lstAllData.append(dictTemp)
    lstAllData.sort(key=lambda x: x['start'])
    return processSorted(lstAllData)


def processSorted(lstAllData):
    """
    Input: lstAllData: multi-dimensional list that contains dictionaries.
        
        The function iterates through the length of the list by indexes.
        If the integer is zero, than the iteration is running for the first
        time. The function treats the iteration as a unique hit.
        
        After the first iteration, the value of the previous loop is stored
        in the y variable. This is done by taking i minus 1.
        
        The function then checks if the range of the current hit is in the 
        range of the previous hit. It that's true, than the heigth will be 
        increased by 0.2. The positive or negative value will be added to the
        dictionary based on the strand orientation. If the strand is 
        reversed, then the heigth will be added as negative value.
        If the hit is not in the range of the previous item, then it will be
        displayed as a new hit. The heigth value will then be set to 1.0.
        
        Output: The input list with updated values.
    """
    for i in range(len(lstAllData)):
        if i == 0:
            ht = 1.0
            if lstAllData[i]['strand'] == "FWD":
                lstAllData[i]['height'] = ht
            else:
                lstAllData[i]['height'] = -abs(ht)
        else:
            y = i -1
            if lstAllData[i]['start'] in range(lstAllData[y]['start'], lstAllData[y]['stop']):
                ht += 0.2
                if lstAllData[i]['strand'] == "FWD":
                    lstAllData[i]['height'] = ht
                else:
                    lstAllData[i]['height'] = -abs(ht)
            else:
                ht = 1.0
                if lstAllData[i]['strand'] == "FWD":
                    lstAllData[i]['height'] = ht
                else:
                    lstAllData[i]['height'] = -abs(ht)
    return lstAllData


def formShapes(lstAllData):
    """
        Input: Multidimensional list.
        
        The function creates the shapes for each element in lstAllData.
        This is done in the loop. In each iteration the height is checked.
        If the heigth is 1.0, then the color of the graphelement is
        coloured as a dark red. If the heigth is -1.0, then the graph element is
        coloured as a light blue. If the heigth doesn't match the 1.0 values,
        then the line is colloured as grey.
        
        After checken the heigth. The loop sets a graph shape. It used the
        start and stop positions as x values. 0 as y0 value. This makes sure
        that the rectangle looks like bars. The y[1] is determined by the
        heigth. After setting the graph element, the element is added to a list
        for shapes. 
        
        Output: lstShapes: multidimensional list containing all the shapes for
                           the plot.
        """
    # Data is now ready for shapeforming.
    lstShapes = [] # list with shape elements
    for item in lstAllData:
        if item['height'] == 1.0:
            dctColor = dict(color = 'rgba(159, 0, 15, 1)')
            flcolor = dctColor['color']
        elif item['height']== -1.0:
            dctColor = dict(color = 'rgba(0, 158, 142, 1)')
            flcolor = dctColor['color']
        else:
            dctColor=dict(color = 'rgba(86, 80, 81, 1)')
            flcolor = 'rgba(0, 0, 0, 0)'
        dictShape = dict(
            type='rect',
            x0=item['start'],
            y0=0,
            x1=item['stop'],
            y1=item['height'],
            line=dctColor,
            fillcolor=flcolor
            )
        lstShapes.append(dictShape)
    return lstShapes


def plot_data(data, lstShapes, contigname, length, filename):
    """
    Input: 5
        data: object for scatterploting the labels.
        lstShapes: list containing all graph object for plotting.
        contigname: string with contigname.
        length: integer: basepairlength of the contig.
        filename: Outputfilename for plot.
    
        The function create a string for the title. In it the contigname and
        the number of hits is displayed. There is some added html to create a
        smooth layout title.
        
        After that the layout of the plot is created.
        The X-axis has a range of 0 to the contig length. It is also set to
        display a line.
        The Y-axis is set to have an autorange. This way the plot package will
        determine the best heigth automaticly, and it is also very accurate.
        The Y-axis also doesn't show a line, because that is not needed. The
        y-axis is for visual usage only and the datapoint do not have an y-
        value. 
        
        After that the shapes for the graph is being set with the list of all
        shapes.
        
        Then the layout and data will be plotted by the package. It uses an
        offline option. This is needed to use the package localy. The ploti is
        saved as an html document. The auto_open option is set to false to
        prevent terminal errors. 
        """
    titlestr = "<b>" + contigname + "</b><br>Total hits: " + str(len(lstShapes))
    layout = {
        'title' : titlestr,
        'xaxis' : {  # x-axis options
            'range' : [0, length],
            'showgrid' : False,
            'showline' : True,
            },
        'yaxis' : {  # y-axis options
            'autorange' : True,
            'showgrid' : False,
            'showline' : False,
            'autotick' : True,
            'ticks' : '',
            'showticklabels' : False,
            },
        'shapes' : lstShapes # end of shapes
        }
    pyo.plot( {"data" : data,  "layout": layout}, filename=filename + "_Hits-" + str(len(lstShapes)) + ".html",
            auto_open=False)

    
def setLblPos(lstAllData):
    """
    Input:
        lstAllData: multidimensional list.
    
        The function creates a scatterplot with the go.Scatter from plotly.
        The x-axis data is obtained from the lblpos from each data element.
        The labelpos is the position in the middle from the start and stop.
        The y-axis data is from the heigth and the lblspace. This way the
        negative values are stored up from the graph objects.
        
        The texts come from the name key from AllData.
        
        The function returns a scatterplot with labels.
    
    Output:
        trace0: Object for scatterplot.
    """
    trace0 = go.Scatter(
	x = [x['lblPos'] for x in lstAllData],
	y = [x['height'] + x['lblSpace'] for x in lstAllData],
	text = [x['name'] for x in lstAllData],
	mode = 'text',)
    return [trace0]


def visualData(filename, contigname, length):
    """
    input: 3
            filename: string.
            contigname: string
            length: string. length of contig specified by contigname.
    
        The function is a controller to get the data from raw to plot.
        This is done via opening the data in get_data. After that it is beign
        processed to useable data by processData. The processedData is formed
        into shapes by formShapes, and the labeldata is processed by setLblPos.
        After that the function sends everything to the plot function plot_data.
    """
    lstRAWData = get_data(filename)
    lstAllData = processData(lstRAWData)
    lstShapes = formShapes(lstAllData)
    data = setLblPos(lstAllData)
    plot_data(data, lstShapes, contigname, length, filename) # filename here
    
def main(argv):
    """
    Input: argv: Command line arguments.
        
        The function requires three arguments.
        
            Argument 1: Filelocation: Example: C:/user/data.txt
            Argument 2: Contigname: Example: Contig_2
            Argument 3: Length of contig: Example: 54332
    The function starts visualData.
    """     
    filename = argv[1]
    contigname = argv[2]
    length = int(argv[3])
    visualData(filename, contigname, length)

    
if __name__ == "__main__":
    main(sys.argv)
