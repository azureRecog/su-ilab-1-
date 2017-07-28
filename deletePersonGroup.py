# Only use this program when you want to wipe out the whole person group
# Authors: Nancy Xiao & Ayumi Mizuno
import httplib, urllib, base64

KEY = '564a789479fe4d99ab424c3e9174b0e7'
headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': KEY,
}

params = urllib.urlencode({
    #Enter person group ID here
    "personGroupId" : "su-ilab"
})

try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("DELETE", "/face/v1.0/persongroups/{personGroupId}?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
