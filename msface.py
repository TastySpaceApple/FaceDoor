import urllib2
import json
from threading import Thread

key1 = "d8731dcbe24341e695cefb9ca06e440b";
key2 = "7710709d37e64624ae15c3a9d93c9a43";

class FaceRecognizer:
    STAGE_WAITING = 1
    STAGE_APPROVED = 2
    STAGE_DENIED = 3
    STAGE_IDLE = 0
    def __init__(self):
        self.faces = []
        self.stage = 0;

    def clean(self):
        self.stage = self.STAGE_IDLE;
        
    def addFace(self, imgData):
        faceId = self.postDetect(imgData)
        if faceId != None:
            self.faces.append(faceId)

    def recognizeFace(self, imgData):
        self.stage = self.STAGE_WAITING
	if len(self.faces) > 0:
            faceId = self.postDetect(imgData)
        for knownFaceId in self.faces:
            res = self.postVerify(faceId, knownFaceId)
	    print res
            if res['isIdentical']:
                self.stage = self.STAGE_APPROVED
                return True
            else:
                self.stage = self.STAGE_DENIED
        self.stage = self.STAGE_DENIED
        return False

    def recognizeFaceAsync(self, imgData):
        thread = Thread(target = self.recognizeFace, args = [imgData])
        thread.start()

    def postDetect(self, imgData, dataFormat='octet-stream'):
        params = "returnFaceId=true&returnFaceLandmarks=false&returnFaceAttributes=age"
        url = "https://api.projectoxford.ai/face/v1.0/detect?" + params

        headers = {}
        headers['Content-Type'] = 'application/'+dataFormat
        headers['Ocp-Apim-Subscription-Key'] = key1
        
        req = urllib2.Request(url, imgData, headers)
        response = urllib2.urlopen(req)
        faces = json.loads(response.read())
        if len(faces) > 0:
            return faces[0]['faceId']
        else:
            return None
        
    def postVerify(self, faceId1, faceId2):
        data = json.dumps(
                {'faceId1': faceId1, 'faceId2': faceId2}
            )
        url = "https://api.projectoxford.ai/face/v1.0/verify"

        headers = {}
        headers['Content-Type'] = 'application/json'
        headers['Ocp-Apim-Subscription-Key'] = key1
        
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)
        return json.loads(response.read())
        
    
