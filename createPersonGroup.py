#This program create a person group (in which you can add multiple new people
#should only run it when you want to create a whole new person group
#Authors: Nancy Xiao & Ayumi Mizuno
import cognitive_face as CF
import httplib, urllib, base64

# Enter a valid subscription key (keeping the quotes in place).
KEY = '564a789479fe4d99ab424c3e9174b0e7'

CF.Key.set(KEY)


uri_base = 'westus.api.cognitive.microsoft.com'

headers = {
    # Request headers.
    'Content-Type': 'application/json',

    'Ocp-Apim-Subscription-Key':KEY,
}

# Enter an ID you haven't used for creating a group before.
# The valid characters for the ID include numbers, English letters in lower case, '-' and '_'. 
# The maximum length of the ID is 64.
personGroupId = 'su-ilab'

# The userData field is optional. The size limit for it is 16KB.
body = "{ 'name':'su-ilab'}"

try:
    # NOTE: You must use the same region in your REST call as you used to obtain your subscription keys.
    #   For example, if you obtained your subscription keys from westus, replace "westcentralus" in the 
    #   URL below with "westus".
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("PUT", "/face/v1.0/persongroups/%s" % personGroupId, body, headers)
    response = conn.getresponse()

    # 'OK' indicates success. 'Conflict' means a group with this ID already exists.
    # If you get 'Conflict', change the value of personGroupId above and try again.
    # If you get 'Access Denied', verify the validity of the subscription key above and try again.
    print(response.reason)

    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

