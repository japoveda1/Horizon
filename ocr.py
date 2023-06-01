import cv2  
#import requests
#import io
#import json

#vStrApiOCRKey = "e318ddff0488957"
#vStrApiOCRUrl = "https://api.ocr.space/parse/image"

#vImgDocumento = cv2.imread("EstadoDeSituacionFinanciera.jpg")

#vNumAlturaImg , vNumAnchoImg , _  = vImgDocumento.shape 

#roi = vImgDocumento[0:vNumAlturaImg,0:vNumAnchoImg]

#_, compressedimage = cv2.imencode(".jpg", roi, [1, 90])
#file_bytes = io.BytesIO(compressedimage)

#resultado = requests.post(vStrApiOCRUrl ,
#              files={"EstadoDeSituacionFinanciera.jpg":file_bytes},
#              data={"apikey":vStrApiOCRKey})

#resultado = resultado.content.decode()
#resultado = json.loads(resultado)

#parsed_results = resultado.get("ParsedResults")[0]
#text_detected = parsed_results.get("ParsedText")
#print(text_detected)

#cv2.imshow("ROI",roi)
#cv2.imshow("Documento para analisis",vImgDocumento)
#cv2.waitKey(0)
#cv2.destroyWindow()