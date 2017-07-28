#This is the program that you add new people and their photos to Microsoft Azure
#Reminder: after you upload new people to the server, do use the program "trainPersonGroup.py" to train the person group
#Authors: Nancy Xiao & Ayumi Mizuno
import httplib, urllib, base64

KEY = '' #Enter subscription key here
headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': KEY,
}
params = urllib.urlencode({
    'personGroupId':'su-ilab'
})

#create person
name = '' # please enter name in this format (i.e. vincent-david), because this name will be automatically reformatted and written into "directory.txt"
tempDict = {'name': name}
body = str(tempDict)

try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/persongroups/{personGroupId}/persons?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print(e)
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

#get the response from the server and extract correspoonding person ID
dataList = data.split(":")
personID = dataList[1][1:-2]
#format the string to write into local directory
nameList = name.split("-")
newName = nameList[0].capitalize()
newName +=" "+nameList[1].capitalize()
line = personID+" :"+newName

f = open("directory.txt",'a')
print(line)
f.write(line)
f.write("\n")
f.close()


#add image and link it to the newly-created personID
params = urllib.urlencode({
    'personGroupId':'su-ilab',
    'personId': personID,
    
})

#enter image url here (we've tried to use local images, but to no avail.
#One way that we converted local images into url format is to upload it to a github account, get the url, and take down the image)
body = "{'url':''}"

try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/persongroups/{personGroupId}/persons/{personId}/persistedFaces?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
