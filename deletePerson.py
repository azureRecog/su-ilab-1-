#This program enables you to delete people and their images from the server
#Authors: Nancy Xiao & Ayumi Mizuno
import httplib, urllib, base64

KEY = '564a789479fe4d99ab424c3e9174b0e7'
headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': KEY,
}

params = urllib.urlencode({
'personGroupId':'su-ilab',
#Enter the person ID here, can get it from "diretory.txt"
'personId': "e26815bb-762c-4005-8857-a4b88fd1f3b4",
})

try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("DELETE", "/face/v1.0/persongroups/{personGroupId}/persons/{personId}?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

#After you run this program and get response that you've successfully
#deleted this person from the server, please manually delete this person's info from "directory.txt" as well
