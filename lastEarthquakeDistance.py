#-------------------------------------------------------------------------------
# Name:        Last Earthquake Distance ALPHA
#
# Author:      Luca Reverberi
#
# Created:     06/06/2012
# Copyright:   (c) Luca Reverberi 2012
# Licence:     GPL 3
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import httplib
import math
import time
from xml.dom.minidom import parseString

# position of uni/home:
latHome = 45.37 #
lonHome = 9.68  # Universita degli Studi di Milano - Crema

# update every:
timeUpdate = 60 #seconds. twitter: "Clients may not make more than 150 requests per hour."

def distanceOnUnitSphere(lat1, long1, lat2, long2):
    degrees_to_radians = math.pi/180.0
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
    return arc * 6378 # radianti terra

def readEarthquake():
    lastDate = ""
    earthQuakeInfo = {"lat":"","lon":"","ora":""}
    sendNotification = False
    giro = 0

    while True:
        # Open a connection to twitter.com.

        # with uni proxy:
#        twitterConn = httplib.HTTPConnection("prometeus.dti.unimi.it",8080)
#        twitterConn.request("GET", "http://www.twitter.com/statuses/user_timeline.xml?screen_name=INGVterremoti")

        # without uni proxy:
      	twitterConn = httplib.HTTPConnection("www.twitter.com")
      	twitterConn.request("GET", "/statuses/user_timeline.xml?screen_name=INGVterremoti")


        twitterResponse = twitterConn.getresponse()

    	# Check that everything went ok.
        if twitterResponse.status != 200:
    	  print("Failed to request tweets.")

    	# Read the response.
        tweets = twitterResponse.read()

    	# Close the connection.
        twitterConn.close()

    	#Parse the XML.
        twitterDom = parseString(tweets)

    	# Find last status tweet.
        try:
            tweet = twitterDom.getElementsByTagName("status")[0]
            for tweetParts in tweet.childNodes:
                # Find the date tag.
                if tweetParts.nodeName == "created_at":
                    for textNode in tweetParts.childNodes:
        		# Find the contents of the date tag.
                        if textNode.nodeType == textNode.TEXT_NODE:
                            if(lastDate != textNode.nodeValue):
                                lastDate = textNode.nodeValue
                                # define the action ... only print in this case
                                sendNotification = True
	                            #print textNode.nodeValue

                # Find the tweet tag.
                elif tweetParts.nodeName == "text":
                    for textNode in tweetParts.childNodes:
					# Find the contents of the tweet tag.
                        if textNode.nodeType == textNode.TEXT_NODE:
							#trovo posizione:

							# -- latitudine
                            latPosition = textNode.nodeValue.rfind("Lat")
                            earthQuakeInfo["lat"] = textNode.nodeValue[latPosition+4:latPosition+9]

							# -- longitudine
                            lonPosition = textNode.nodeValue.rfind("Lon")
                            earthQuakeInfo["lon"] = textNode.nodeValue[lonPosition+4:lonPosition+9]

							# -- ora:
                            oraPosition = textNode.nodeValue.rfind("UTC")
                            earthQuakeInfo["ora"] = textNode.nodeValue[oraPosition-9:oraPosition-1]


        except:
            pass

        if sendNotification == True:
            sendNotification = False
            print ("Ora: "+str(earthQuakeInfo["ora"]))
            print ("Distanza: "+str(distanceOnUnitSphere(float(earthQuakeInfo["lat"]),float(earthQuakeInfo["lon"]),latHome,lonHome)))

        time.sleep(timeUpdate)

if __name__ == '__main__':
    readEarthquake() 
