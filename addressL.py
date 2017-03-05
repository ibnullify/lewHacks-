#!/usr/bin/python
# ========= HASHBANG LINE ABOVE IS MAGIC! =========
# ========= (Must be first line of file.) =========

"""
Team Public Relations - Gilvir Gill, Henry Zheng
IntroCS2 pd8
FINAL PROJECT
END OF SEMESTER
"""

import math
import cgi
import cgitb
import urllib2
#import googlemaps
#from datetime import datetime
cgitb.enable()  #diag info --- comment out once full functionality achieved
query = cgi.FieldStorage()
#gmaps = googlemaps.Client(key='AIzaSyD7g6o2aIIo3ZlXtYbc4LjhcUaRizS1DKU')
#google maps is hereby referred to as gmaps

# ~~~~~~~~~~~~~~~ Settings ~~~~~~~~~~~~~~~ #
printed_info = ['SSID', 'Location', 'City', 'Type', 'Provider', 'Location_T', 'Remarks']

def ulElements(D): #returns an unordered html list of info from the dictionary using the settings in printed_info global
    html = '<ul> \n'
    for infotype in printed_info:
        html += '<li>%s: %s</li> \n' % (infotype, D[infotype])
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

def getCoords():  #returns the list of addresses
    keys = query.keys()
    address = query["address"]  #gets the address value
    address = address.replace(' ',"+")  #replaces spaces in user inputted address value with +'s in order to comply with gmap's API
    url="https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=AIzaSyD7g6o2aIIo3ZlXtYbc4LjhcUaRizS1DKU" % address  #geocodes the address
    response = urllib2.urlopen(url)
    info = response.read() #these past few lines basically assign a json formatted file from google api to info
    info = info.replace('true','True') #puts booleans in proper format
    exec "info =" + info #executes a string that sets variable "info" equal to the python formatted stuff
    return info


def listaddresses(dictInfo): #takes the dictionary containing all the information and extracts the list of addresses in order
    L = []
    for location in info['results']:
        L.append(location["formatted_address"])
    return L


def formCreator(L,query,areManyAddresses): #creates a dropdown form in html with it's choices being elements in the given list, also takes already available query info string
    formHTML = '<form name="input" method="GET" action="addressL.py"> \n'
    missing_queries = 'includeL' not in query.values() or 'includeH' not in query.values()
    if missing_queries:
        for key in query.keys():
            if query[key] == 'includeH' or query[key] == 'includeL':
                query.pop(key)
    if areManyAddresses:
        del query['address']
        formHTML += 'There are multiple addresses. Please select your address\n<br>'
        formHTML += '\t <select name = "address"> size="1">\n'
        formHTML += '\t\t <option selected> %s </option><br>\n' % L[0]
        for element in L[1:]: #for every elment after the first one:
            formHTML+= '\t\t <option> %s </option>\n' % element
        for element in query: #for all the query elements from the old query that still need to be shown:
            formHTML+= '\t<input type="hidden" name=%s value = %s>' % (element.replace(' ', '+'), query[element].replace(' ', '+'))
        formHTML += '\t</select>'
    if missing_queries:
        formHTML+= """<br>You did not specify a single hotspot and/or location type. Please do so now. If you ever need to go back, do so <a href="index.html">here</a>.
        <br>
              Types of Hotspots:  <br>
              <input type="checkbox" name="Free" value="includeH" checked="checked">Free
              <input type="checkbox" name="Limited Free" value="includeH" checked="checked">Limited Free
              <input type="checkbox" name="Partner Site" value="includeH" checked="checked">Partner Site
              <br>
              Different Types of Locations:<br>
              <input type="checkbox" name="Indoor" value="includeL" checked="checked">Indoor
              <input type="checkbox" name="Library" value="includeL" checked="checked">Library
              <input type="checkbox" name="Outdoor" value="includeL" checked="checked">Outdoor
              <input type="checkbox" name="Outdoor Kiosk" value="includeL" checked="checked">Outdoor Kiosk
              <input type="checkbox" name="Outdoor TWC Aerial" value="includeL" checked="checked">Outdoor TWC Aerial
              <input type="checkbox" name="Outdoor Subway" value="includeL" checked="checked">Subway Station<br>"""
        if not areManyAddresses:
            for element in query: #for all the query elements from the old query that still need to be shown:
                formHTML+= '\t<input type="hidden" name=%s value = %s>' % (element.replace(' ', '+'), query[element].replace(' ', '+'))
    formHTML += '\n\t<center><input type="submit" value="Submit"></center>'
    formHTML += '</form>'
    return formHTML




def FStoString(D): #takes query dictionary and returns it's query string
    query_string = "?"
    for element in D:
        query_string += "%s=%s&" % (element.replace(' ', '+'), str(D[element]).replace(' ', '+'))
    return query_string[:-1] #returns all ands minus the last one

query = FStoD()
info = getCoords()
addresses = listaddresses(info)
doRedirect = '' #this is the string added in the header, depending on if its filled or not determines whether the redirect happens
form = 'Looks like the redirect didnt work! Please go to <a href = "hotspot.py' + str(FStoString(query)) + '"> this link</a> for the map!' #this is the form element




if len(addresses) < 1:
    print 'Location: index.html'
    print #blank print
if len(addresses) == 1: #if there is only one address given, just redirect straight to the page
    if 'includeL' not in query.values() or 'includeH' not in query.values(): #if they didnt specify all info, make them submit another form
        form = formCreator(addresses,query,False)
    else:
        print 'Location: hotspot.py%s' % FStoString(query)
        print # blank print to finish redirect
else:
    form = formCreator(addresses,query,True)


# ========= CONTENT-TYPE LINE REQUIRED. ===========
# ======= Must be beginning of HTML string ========
htmlStr = "Content-Type: text/html\n\n" #NOTE there are 2 '\n's !!!
htmlStr += '<html><head><title> Handy Hotspot NYC </title><link rel="icon" href="logo1.gif">\n<link rel="stylesheet" type="text/css" href="style.css">\n</head>\n</html>\n'
htmlStr += "<body>\n"

# ~~~~~~~~~~~~~ HTML-generating code ~~~~~~~~~~~~~~
htmlStr += '<div class="container">'
htmlStr += "<h1>Handy Hotspot NYC</h1>\n"
htmlStr += '<div class="body_section" id="form">'
htmlStr +=  form
htmlStr += '\n</div>\n'
htmlStr += "<footer>\n\
&copy; Handy Hotspot NYC\n\
<br>\n\
<br>\n\
Handy Hotspot NYC isn't endorsed by Google Inc. and doesn't reflect the views or opinions of Google Inc.\
or anyone officially involved in producing or managing Google Maps. Google Maps and Google Inc. are trademarks\
or registered trademarks of Alphabet, Inc.\n\
</footer>"
htmlStr += '\n</div>\n'
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

htmlStr += "</body>\n"
htmlStr += "</html>"

print htmlStr
