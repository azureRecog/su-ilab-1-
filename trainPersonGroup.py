#This program train the person group. so that when you use "faceRecognizer.py,"
#it can recognize the faces of newly added people
#Authors: Nancy Xiao & Ayumi Mizuno
import cognitive_face as CF
import httplib, urllib, base64

KEY = '564a789479fe4d99ab424c3e9174b0e7'

CF.Key.set(KEY)


uri_base = 'westus.api.cognitive.microsoft.com'

#train
headers = {
    # Request headers.
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key':KEY,
}

params = urllib.urlencode({
    'personGroupId':'su-ilab'
})

try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/persongroups/{personGroupId}/train?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

#get training status
params = urllib.urlencode({
    #Enter person group id here
    'personGroupId':'su-ilab'
})

try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("GET", "/face/v1.0/persongroups/{personGroupId}/training?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
