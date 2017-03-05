#!/usr/bin/python
# ========= HASHBANG LINE ABOVE IS MAGIC! =========
# ========= (Must be first line of file.) =========

"""
Team Public Relations - Gilvir Gill, Henry Zheng
IntroCS2 pd8
FINAL PROJECT
END OF SEMESTER
"""

# ======================================================
# ================== ADD COMMENTS FOR ==================
# =================== quickLinePatch ===================
# ======================================================

import math
import cgi
import cgitb
import urllib2
#import googlemaps
#from datetime import datetime
cgitb.enable()  #diag info --- comment out once full functionality achieved
#gmaps = googlemaps.Client(key='AIzaSyD7g6o2aIIo3ZlXtYbc4LjhcUaRizS1DKU')
#google maps is hereby referred to as gmaps



# ~~~~~~~~~~~~~~~ Settings ~~~~~~~~~~~~~~~ #
printed_info = ['SSID', 'City', 'Type', 'Provider', 'Location_T', 'Remarks']

def ulElements(D): #returns an unordered html list of info from the dictionary using the settings in printed_info global
    html = '<ul> \n'
    for infotype in printed_info:
        if infotype == 'Location_T':
            html += '<li><b>%s</b>: %s</li> \n' % ('Location Type', D[infotype])  #changes front-end of 'Location_T' to 'Location Type'
        else:
            if D[infotype] != "":
                html += '<li><b>%s</b>: %s</li> \n' % (infotype, D[infotype])
    html += '</ul>'
    return html


# ~~~~~~~~~~~~~~~ support functions ~~~~~~~~~~~~~~~
def FStoD():
    '''
    Converts cgi.FieldStorage() return value into a standard dictionary
    '''
    d = {}
    formData = cgi.FieldStorage()
    for k in formData.keys():
        if type(formData[k]) is list:
            d[k] = formData.getfirst(k)
        else:
            d[k] = formData[k].value
    return d

query = FStoD()
def getCoords():  #returns the map of the latitude/longitude of the user inputted address so far
    keys = query.keys()
    try:
        address = query["address"]  #gets the address value
    except KeyError:
        print 'Location: index.html'
        print #blank print    
    address = address.replace(' ',"+")  #replaces spaces in user inputted address value with +'s in order to comply with gmap's API
    url="https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=AIzaSyD7g6o2aIIo3ZlXtYbc4LjhcUaRizS1DKU" % address  #geocodes the address
    response = urllib2.urlopen(url)
    info = response.read() #these past few lines basically assign a json formatted file from google api to info
    info = info.replace('true','True') #puts booleans in proper format
    exec "info =" + info #executes a string that sets variable "info" equal to the python formatted stuff
    try:
        lat = info["results"][0]['geometry']['location']['lat']  #gets latitude
    except IndexError:
        print 'Location: index.html'
        print #blank print
    lng = info["results"][0]['geometry']['location']['lng']  #gets longitude
    return {'Long_': lng, 'Lat': lat}


def crtEmbedDict(origLoc,destLoc,mode): #returns a dictionary to be used in getDirections function. Accepts dict form for coords, and string for mode.
    D = {}
    orig = str(origLoc['Lat']) + ',' + str(origLoc['Long_'])  #gets latitude,longitude of user-inputted data
    dest = str(destLoc['Lat']) + ',' + str(destLoc['Long_'])  #gets latitude,longitude of closest hotspot
    D['origin'] =  orig
    D['destination'] = dest
    D['mode'] = mode
    return D


def getDirections(dct): #takes dictionary in format {'origin': googlereadyorigin, 'destination': googlereadydestination, 'mode': driving,walking,bicycling,transit,flying}
    userquerys = ""
    for param in dct:
        userquerys+= '&' + param + '=' + str(dct[param])  #adds in each param to the address for additional parameters
    maps = '''
<iframe
  width="900px"
  height="500px"
  frameborder="0" style="border:0"
  src="https://www.google.com/maps/embed/v1/directions?key=AIzaSyDq-niy82jWRr3FZj3BE7FpyLiIeoLtO6w
'''+userquerys+'''"allowfullscreen>
</iframe>
'''  #embeds the map within the website of the latitude,longitude pair
    return maps
def getDirectionsText(dct): #takes same formatted dictionary:
    htmlStr = ""
    userquerys = ""
    for param in dct:
        userquerys+= '&' + param + '=' + str(dct[param])  #adds in each param to the address for additional parameters
    url="https://www.google.com/maps/api/directions/json?key=AIzaSyD7g6o2aIIo3ZlXtYbc4LjhcUaRizS1DKU"+userquerys
    response = urllib2.urlopen(url)
    info = response.read()
    info = info.replace('true','True')
    exec "info =" + info
    try:
        steps = info['routes'][0]['legs'][0]['steps']
    except IndexError:
        return ""
    for num in range(0,len(steps)): #for every element in D
        step = steps[num]['html_instructions']
        step = step.replace('\u003c', '<')
        step = step.replace('\u003e', '>')
        htmlStr += str(num+1) + '. ' + step + '\n<br>\n'
    return htmlStr


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




# ========= DATAPROCCESSING FUNCTIONS  =========== #
def readL(filename):  #reads file
    inStream = open(filename,'r')
    data = inStream.readlines()
    inStream.close()
    return data

def quickLinePatch(lines):
    newlines = [lines[0]]
    for num in range(1,len(lines),2): #for lines 1,3,5,etc.
        newlines.append(lines[num]+lines[num+1])
    return newlines

#Turns data into a 2D list.
def ListGen(lines):
    list = []
    for line in lines:
        line = line.replace('""', "15NfzYl2Yw") #replace double quotes which reprsent quotation marks within a quote  with a string
        line = line.split('"') #split every line into parts with and without quotes, then loop through those blocks in the next part:
        counter = 0
        newline = []
        for quote_block in line:
            if counter % 2 == 0: #if it is outside of a quotation mark:
                if quote_block == ',':
                    quote_block = "L4hkE0NNLY"
                if quote_block != '' and quote_block[-1] == ',' and quote_block != ',': #if it ends or starts with a comma remove the comma
                    quote_block = quote_block[:-1]
                if quote_block != '' and quote_block[0] == ',' and quote_block != ',':
                    quote_block = quote_block[1:]
                quote_block = quote_block.split(',') #split it into columns based on commas
            else:
                quote_block = quote_block.replace("15NfzYl2Yw", '""')
                quote_block = [quote_block] #else if it's a quote just add it in the list to append to.
            for column_item in quote_block:
                if column_item != "L4hkE0NNLY":
                    newline.append(column_item)
            counter += 1
        list.append(newline[:-1]) #append all but the last element, which is just a newline anyways
    return list

# takes 2D list and turns into a list of dictionaries
def ListToDict(L):
    #define an empty dictionary to be populated
    D = {}
    for row in L[1:]: #for every row after the header row:
        D[row[0]] = {}
        for num in range(1,len(L[0])): #for every element in the header row except the first one:
            (D[row[0]])[L[0][num]] = row[num]
    return D

def rmExclusions(removeD, L): #takes dictionary and removes any key/value combos wherethe value dictionary contains a location or type value in L
    keys = removeD.keys()
    for hotspot in keys:
        if removeD[hotspot]['Type'] not in L or removeD[hotspot]['Location_T'] not in L:
            del removeD[hotspot]

def distance(sx,sy,ex,ey): #gives the distance between two points using the haversine formula
    lateral_distance = sx-ex
    longitudal_distance = sy-ey
    a = math.sin(math.radians(lateral_distance/2))**2 + math.cos(math.radians(sx)) * math.cos(math.radians(ex)) * math.sin(math.radians(longitudal_distance/2))**2
    c = 2 * math.atan2((a**0.5 ),(1-a**0.5))
    d = 3959 * c
    return d

#adds distance to starting point to all elements of the dictionary
def addDist(dict,sx,sy):
    for hotspot in dict:
        lati = dict[hotspot]['Lat']
        longi = dict[hotspot]['Long_']
        dict[hotspot]['Distance'] = distance(sx,sy,float(lati),float(longi))



def minDist(D): #returns the key of the dictionary element with the lowest "Distance" value
    objects = D.keys()
    values = D.values()
    distances = [] #list of distances parallel to the values and objects
    for dct in values:
        distances.append(float(dct['Distance']))
    return objects[(distances.index(min(distances)))] #return the object id of the object with the lowest distance value

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#Note: query variable was defined earlier and is the dictionary output


#----CSV Hotspot database proccessing----
data = readL('hotspotdata.csv') #reads CSV file into lines
data = quickLinePatch(data) #fixes lines to be properly formated
listHotspots = ListGen(data) #generates a 2D table
dictHotspots = ListToDict(listHotspots) #turns 2D table into dictionary where first row servers as keys
rmExclusions(dictHotspots, query.keys()) #removes variables to be excluded for location and hotspot
#----------------------------------------
add_info = "" #this is the variable that will eventually hold extra informaiton
coords = getCoords() # {'Long_': longcoord, 'Lat': 'lat coord'}
if dictHotspots != {}: #if the hotspots dictionary is not empty:
    addDist(dictHotspots,float(coords['Lat']),float(coords['Long_']))
    closest = dictHotspots[minDist(dictHotspots)] #returns the dictionary of the closest hotspot

    params = crtEmbedDict(coords,closest,query['mode']) #gets the parameters ready for google maps api

    closest_info = ulElements(closest)
    gmap = getDirections(params) + '\n<br>' + '<h3> Text Directions</h3><br>\n' + getDirectionsText(params)
    add_info += '\n<h3>Hotspot Information:</h3>\n'
    add_info += "<h4>%s</h4>" % (closest['Name'])
    add_info += closest_info
else: #otherwise, that means none work so return this:
    gmap = """<h3>Uh oh</h3>
    Looks like there are no hotspots that fit the given parameters. Please try again <a href="index.html">here</a> giving different restrictions. Generally, include libraries and free hotspots for the most results.
    """






def userHTML(D): #takes a dictionary and turns it html list
    info = D #makes destructable variable that stores info from query
    htmlStr = '<ul> \n'
    for setting in ['mode', 'address']:
        htmlStr += '<li><b>%s</b>: %s</li> \n' % (setting, info.pop(setting))
    hotspot_types = ""
    location_types = ""
    typesList = info.keys()
    for elem in typesList:
        if info[elem] == 'includeH':
            hotspot_types += "%s, " % elem #pops includeH
        if info[elem] == 'includeL':
            location_types += "%s, " % elem #pops includeH
    htmlStr += '\n<li><b>Included Location Types</b>: ' +  location_types[:-2] + '</li>'
    htmlStr += '\n<li><b>Included Hotspot Types</b>: ' + hotspot_types[:-2] + '</li>'
    return htmlStr
userinputHTML = userHTML(query)


# ========= CONTENT-TYPE LINE REQUIRED. ===========
# ======= Must be beginning of HTML string ========
htmlStr = "Content-Type: text/html\n\n" #NOTE there are 2 '\n's !!!
htmlStr += '<html>\n<head>\n<title> Handy Hotspot NYC</title>\n<link rel="icon" href="logo1.gif">\n<link rel="stylesheet" type="text/css" href="style.css">\n</head>\n</html>\n'
htmlStr += "<body>\n"

# ~~~~~~~~~~~~~ HTML-generating code ~~~~~~~~~~~~~~
htmlStr += '<div class="container">'
htmlStr += "<h1>Handy Hotspot NYC</h1>\n"
htmlStr += '<div class="body_section" id="data_input">\n'
htmlStr += "<h3>Data Input:</h4>\n"
htmlStr += userinputHTML
htmlStr += '\n</div>\n'
htmlStr += '<div class="body_section" id="data_output">\n'
htmlStr += "\n<h3>Data Output:</h4>\n"
htmlStr += gmap
htmlStr += add_info
htmlStr += '\n</div>\n'
htmlStr += '<div class="body_section" id="link">\n'
htmlStr += '<a href="index.html">Back to Homepage</a>\n'
htmlStr += '</div>\n'
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
htmlStr += "<br>\n"
htmlStr += "</body>\n"
htmlStr += "<footer>\n\
&copy; Handy Hotspot NYC\n\
<br>\n\
<br>\n\
Handy Hotspot NYC isn't endorsed by Google Inc. and doesn't reflect the views or opinions of Google Inc.\
or anyone officially involved in producing or managing Google Maps. Google Maps and Google Inc. are trademarks\
or registered trademarks of Alphabet, Inc.\n\
</footer>"
htmlStr += "</html>"

print htmlStr
