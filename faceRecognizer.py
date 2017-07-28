# coding=utf-8
# please keep the comment line above if you enter any non-English characters

# This program take an image via webcam.py, upload the image to the Azure server, and decides if it can recognizes the face
# If the face is recognized, personalized greetings will be vocalized and door lock will be unlocked (will be locked again in 3 secs)
# Authors: Nancy Xiao & Ayumi Mizuno
import httplib, urllib, base64, json, requests,os,sys,time
import cognitive_face as CF
from os.path import expanduser, join, dirname
from webcam import *
from watson_developer_cloud import TextToSpeechV1,SpeechToTextV1

# Enter a valid subscription key (keeping the quotes in place).
KEY = '' #Enter subscription key here

#detect face
params = urllib.urlencode({
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
})


headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': KEY,
}

params = urllib.urlencode({
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes':'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
})

url = 'https://api.projectoxford.ai/face/v1.0/detect?%s' % params

# get the image file from webcam.py
img = open(expanduser(file), 'rb')

response = requests.post(url, data=img, headers=headers)

# extracting key infos from the response given by Microsoft Azure
raw_text = str(response.json())

cooked_text = raw_text.replace('u\'', " ")
cooked_text = cooked_text.replace("':", ":")
cooked_text = cooked_text.replace("'","")
cooked_text = cooked_text.replace("'","")
cooked_text = cooked_text.replace("[","")
cooked_text = cooked_text.replace("]","")


final_text = cooked_text.split(",")


# initalizing the variables that will be redefined by the data in the response
age = ""
happy = 0.0
sad = 0.0
anger = 0.0
surprise = 0.0
neutral = 0.0
lipmakeup = False
eyemakeup = False
makeup = False
# search through response and find corresponding info
for line in final_text:
    if line.find("age")!=-1:
        age = line
    if line.find("happiness")!=-1:
        happy = eval(line[line.find(":")+2:-1])
    if line.find("anger")!=-1:
        anger = eval(line[line.find(":")+2:])
    if line.find("surprise")!=-1:
        surprise = eval(line[line.find(":")+2:])
    if line.find("neutral")!=-1:
        neutral = eval(line[line.find(":")+2:])
    if line.find("sadness")!=-1:
        sad = eval(line[line.rfind("s")+2:])
    if line.find("lipMakeup")!=-1:
        lipmakeup = eval(line[line.rfind(":")+1:])
    if line.find("eyeMakeup")!=-1:
        eyemakeup = eval(line[line.rfind(":")+1:-1])

# finding the most probable emotion the user gives        
emotionValue = [happy,anger,surprise,neutral,sad]
emotions = ["happy","angry","surprised","cool","sad"]
highest = 0.0
targetIndex = 0
for i in range(len(emotionValue)):
    if emotionValue[i] > highest:
        highest = emotionValue[i]
        targetIndex = i

highestEmotion = emotions[targetIndex]

# if the person wears makeup, will add one more sentence in the greeting part
if(lipmakeup or eyemakeup):
    makeup = True

space = ""

'''
#do not delete it parr, if program is still in testing phase
#this part prints out the reformatted report sent by the server
for line in final_text: 
    line = line.replace("}", "")
    if "{" in line:
        print("\t")
        str1 = line[line.find("{")+1:]
        line = line[0:line.find("{")]
        if "{" in str1:
            str2 = str1[str1.find("{")+1:]
            str1 = str1[0:str1.find("{")]
            print(line)
            print(" "+str1)
            print(" "+str2)
        else:
            print(line)
            print(" "+str1)
    else:
        print(line)

print(" ")
'''

# if face not detected, emit corrsponding greeting
finalList = final_text[0].split(":")
try:
    target=finalList[1].strip()
except IndexError:
    speech = "Cannot detect face, try again."
    text_to_speech = TextToSpeechV1(
        username='', #Enter username here
        password='',
        x_watson_learning_opt_out=True)
    with open(join(dirname(__file__), './output2.mp3'),
              'wb') as audio_file:
        audio_file.write(
        text_to_speech.synthesize(speech, accept='audio/wav',
                                      voice="en-US_MichaelVoice"))
        
    os.startfile('C:/Users/Admin/Desktop/spinachEgg/output2.mp3') # path may needed to be changed
    sys.exit(0)

if response.status_code != 200:
    raise ValueError(
        'Request to Azure returned an error %s, the response is:\n%s'
        % (response.status_code, response.text)
    )


# recognize face
params = urllib.urlencode({
})

headers = {
    #'Content-Type': 'application/octet-stream',
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': KEY,
}

targetList = []
targetList.append(target)

body1 = {'personGroupID':'su-ilab', 'confidenceThreshold': 0.0, 'faceIds': targetList }
body = str(body1)

try:
    conn = httplib.HTTPSConnection('api.projectoxford.ai')
    #'westus.api.cognitive.microsoft.com'
    #'api.projectoxford.ai'
    conn.request("POST", "/face/v1.0/identify?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    dataList = data.split(":")
    #print(data)

    idList = dataList[3].split(",")
    personID = idList[0].replace('"',"")
    confidence = eval(dataList[4][ :-4])
   
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
    
# the Azure server only tells the face ID, we loop it up in the local directory to find out this person's name
f = open("directory.txt",'r')
s = f.readlines()
f.close()
print('\n')

# Personalized greeting based on IBM watson API
text_to_speech = TextToSpeechV1(
    username='', #Enter username here
    password='',
    x_watson_learning_opt_out=True)  # Optional flag


speech = ""
# if the confidence level given by Azure is lower than 0.5. we think this person is not a visitor that the lab knows
if confidence < 0.5:
    speech = "Confidence level:"+str(confidence)+"   "+"Sorry, you have no permission to enter. Go away!"
    with open(join(dirname(__file__), './output.mp3'),
                  'wb') as audio_file:
            audio_file.write(
            text_to_speech.synthesize(speech, accept='audio/wav',
                                      voice="ja-JP_EmiVoice"))
    os.startfile('C:/Users/Admin/Desktop/spinachEgg/output.mp3')

# if the person is a recognized vistor, greeting part starts
else:
    from getLanguage import transcript
    #extract key info
    name = ""

    # look through "directory.txt" to find out the person's name
    for item in s:
        if item.startswith(personID):
            item = item.replace("\n",'')
            name = item[item.find(':')+1:]
            # reformat age part
            ageList = age.split(":")
            age = ageList[1]


    
    f = open("timesheet.txt",'r')
    content = f.readlines()
    f.close()
    
    # if this person has never entered into the lab, this person will be greeted in full name
    # else this person will be greeted by the first name
    fullName = name
    for line in content:
        if name in line:
            #print("found name, yeah!")
            nameList = name.split(" ")      
            name = nameList[0]
            #print("changed name:"+name)
            break

    # record the name and time of this person into "timesheet.txt"
    date = time.strftime("%m-%d-%y %H:%M:%S")
    f = open("timesheet.txt",'a')
    line = fullName + " entered into the lab at " + date
    print(line)
    f.write(line)
    f.write("\n")
    f.close()
    


    #greeting part         
    if "skip" in transcript:
        print("Welcome to iLab " + name+" !")
        
    # greeting in German
    elif "man" in transcript:
        speech = "Herzliche Wilkommen zu Innovation Labor! "+ name +"!  "
        speech += "Heute unsere Gesichts erkennungs software denkt dass Sie"+age+" Jahres alt! "
        if(makeup):
            speech +=" übrigens, Ihr Make-up sieht gut aus!"
        with open(join(dirname(__file__), './output.mp3'),
              'wb') as audio_file:
            audio_file.write(
            text_to_speech.synthesize(speech, accept='audio/wav',
                                      voice="de-DE_BirgitVoice"))
        os.startfile('C:/Users/Admin/Desktop/spinachEgg/output.mp3')

    # greeting in Japanese
    elif "Jap" in transcript:
        speech = name + 'さん、アイラボへようこそ！'
        speech += '今日は、フェースレコグナイザーでは、'+ age + '歳に見えます。'
        if(makeup):
            speech += '今日のメイク、いい感じですよ！'
        with open(join(dirname(__file__), './output.mp3'),
                  'wb') as audio_file:
            audio_file.write(
            text_to_speech.synthesize(speech, accept='audio/wav',
                                      voice="ja-JP_EmiVoice"))
        os.startfile('C:/Users/Admin/Desktop/spinachEgg/output.mp3')

    # greeting in French   
    elif "Fr" in transcript:
        speech = " Bienvenue a Laboratoire d'innovation " + name +"!  "
        speech += " Aujourd'hui, notre identificateur des visages pense que vous êtes" +age +"ans!   "
        if(makeup):
            speech += "D'ailleurs, votre maquillage parait impeccable!  "
        with open(join(dirname(__file__), './output.mp3'),
                  'wb') as audio_file:
            audio_file.write(
            text_to_speech.synthesize(speech, accept='audio/wav',
                                      voice="fr-FR_ReneeVoice"))
        os.startfile('C:/Users/Admin/Desktop/spinachEgg/output.mp3')
        
    # greeting in English (default)
    else:
        speech = "Welcome to iLab, "+name+"!   "
        speech += "Today, our face recognizer thinks your face looks " + highestEmotion+" and"+age+" years old!   "
        if(makeup):
            speech += "By the way, your makeup looks fab!"  
            #print("By the way, your makeup looks fab!")

        with open(join(dirname(__file__), './output.mp3'),
              'wb') as audio_file:
            audio_file.write(
            text_to_speech.synthesize(speech, accept='audio/wav',
                                      voice="en-US_MichaelVoice"))

        os.startfile('C:/Users/Admin/Desktop/spinachEgg/output.mp3')

    time.sleep(3)



    
    #Control the lock by using Lockitron API            
    url = "https://api.lockitron.com/v2/locks/2096c5b1-f2ec-49a3-875f-a879b3410b26"

    access_token = '' #Enter token here


    data = {
            'access_token': access_token,
            'state': 'unlock'
            }

    headers = {"Content-Type": "application/json"}

    response = requests.put(url, data=json.dumps(data), headers=headers)

    time.sleep(5)


    data = {
            'access_token': access_token,
            'state': 'lock'
            }

    headers = {"Content-Type": "application/json"}


    response = requests.put(url, data=json.dumps(data), headers=headers)

    #remove greeting file
    if "skip" not in transcript:
        os.remove('output.mp3')


