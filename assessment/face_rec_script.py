import os
import requests

face_api_url = "https://face-detect-arghyasahoo.cloud.okteto.net"

def faceRec(original_img, current_img):
    orig_img = open(original_img, 'rb')
    curr_img = open(current_img, 'rb')
    files = {
        'file1': curr_img,
        'file2': orig_img
    }
    rec = requests.post(face_api_url+'/recognize', files=files)
    curr_img.close()
    orig_img.close()
    # os.unlink(current_img)
    rec = rec.json()
    print(rec)
    return rec