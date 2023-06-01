from datetime import datetime, time, timedelta
from enum import Enum
import time
from typing import Literal, Union
from uuid import UUID

from fastapi import (
    Body,
    Depends,
    FastAPI,
    Query,
    Path,
    Cookie,
    Header,
    status,
    Form,
    File,
    UploadFile,
    HTTPException,
    Request,
)


from pydantic import BaseModel
from typing import Optional, Text
from datetime import datetime, time, timedelta
from uuid import uuid4 as uuid
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import HTMLResponse
import uvicorn
import cv2
import requests
import io
import json
import openai

app = FastAPI()

posts = []

# Post model
class Post(BaseModel):
    id: Optional[str]
    title: str
    author: str
    content: Text
    created_at: datetime =  datetime.now()
    published_at: Optional[datetime] 
    published: Optional[bool] = False


## class MyMiddleware(BaseHTTPMiddleware):
#    async def dispatch(self, request: Request, call_next):
#        start_time = time.time
#        response = await call_next(request)
#        process_time = time.time() - start_time
#        response.headers["X-Process-Time"] = str(process_time)
##        return response

##origins = ["http://localhost:8000", "http://localhost:3000"]
##app.add_middleware(MyMiddleware)
##app.add_middleware(CORSMiddleware, allow_origins=origins)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def read_root():
    return {"welcome": "Horizon API"}

async def leerDocumentoOCR(Archivo):
    vStrApiOCRKey = "e318ddff0488957"
    vStrApiOCRUrl = "https://api.ocr.space/parse/image"

    vImgDocumento = cv2.imread("files/EstadoDeSituacionFinanciera.jpg")

    vNumAlturaImg , vNumAnchoImg , _  = vImgDocumento.shape 

    roi = vImgDocumento[0:vNumAlturaImg,0:vNumAnchoImg]

    _, compressedimage = cv2.imencode(".jpg", roi, [1, 90])
    file_bytes = io.BytesIO(compressedimage)

    resultado = requests.post(vStrApiOCRUrl ,
                  files={"EstadoDeSituacionFinanciera.jpg":file_bytes},
                  data={"apikey":vStrApiOCRKey})

   # resultado = resultado.content.decode()
   # resultado = json.loads(resultado)

   # parsed_results = resultado.get("ParsedResults")[0]
   # text_detected = parsed_results.get("ParsedText")
    return resultado


@app.post('/')
def save_post(post):
    post.id = str(uuid())
    posts.append(post.dict())
    return posts[-1]

@app.post('/posts')
def save_post(post: Post):
    post.id = str(uuid())
    posts.append(post.dict())
    return posts[-1] 


@app.post("/uploadfile/")
async def create_upload_file(files: list[UploadFile] = File(..., description="A file read as UploadFile") ):
    ##return {"filename": [file.filename for file in files]}
    vStrApiOCRKey = "e318ddff0488957"
    vStrApiOCRUrl = "https://api.ocr.space/parse/image"

    vImgDocumento = cv2.imread("files/EstadoDeSituacionFinanciera.jpg")

    vNumAlturaImg , vNumAnchoImg , _  = vImgDocumento.shape 

    roi = vImgDocumento[0:vNumAlturaImg,0:vNumAnchoImg]

    _, compressedimage = cv2.imencode(".jpg", roi, [1, 90])
    file_bytes = io.BytesIO(compressedimage)

    resultado = requests.post(vStrApiOCRUrl ,
                  files={"EstadoDeSituacionFinanciera.jpg":file_bytes},
                  data={"apikey":vStrApiOCRKey,
                        "isTable":True})

    return resultado.content.decode()
    #return resultado.content


@app.post("/AnalizarDocumento/")
async def AnalizarDocumento(textoAnalizarapi:str="johan"):
    #if not textoAnalizar:
    #    raise HTTPException(status_code=400, detail="El campo 'textoAnalizar' es requerido")
    
    
    openai.api_key = "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"

    completion = openai.Completion.create(engine= "text-davinci-003",
                                          prompt= "¿Que podriamos concluir de la operacion de una empresa en base siguiente reporte: ? "+"COMPANIA ABC, C.A.\t\r\nESTADO DE SITUACIÖN FINANCIERA O BALANCE GENERAL\t\r\nAL 31/12/2020 (en miles de dölares)\t\r\nACTIVOS\t\r\nACTIVOS CORRIENTES\t\r\nEfectivo y equivalentes\t322,90\t\r\nCuentas por cobrar\t110,80\t\r\nInventarios\t132,50\t\r\nOtros activos corrientes\t12,54\t\r\nTOTAL DE ACTIVOS CORRIENTES\t578,74\t\r\nACTIVOS NO CORRIENTES\t\r\nPropiedad, planta y equipos\t360,02\t\r\nPatentes\t91,20\t\r\nOtros activos intangibles\t227,47\t\r\nInversiones en asociados\t110,77\t\r\nInversiones a largo plazo\t156,00\t\r\nTOTAL DE ACTIVOS NO CORRIENTES\t945,46\t\r\nTOTAL ACTIVOS\t1.524,20\t\r\nPASIVO Y CAPITAL\t\r\nPASIVOS CORRIENTES\t\r\nCuentas por pagar\t187,62\t\r\nPréstamos a corto plazo\t200,00\t\r\nPorciön actual de préstamos a largo plazo\t20,00\t\r\nImpuesto por pagar\t42,00\t\r\nProvisiones a corto plazo\t4,80\t\r\nTOTAL DE PASIVOS CORRIENTES\t454,42\t\r\nPASIVOS NO CORRIENTES\t\r\nPréstamos a largo plazo\t160,00\t\r\nImpuestos diferidos\t26,04\t\r\nProvisiones a largo plazo\t52,24\t\r\nTOTAL DE PASIVOS NO CORRIENTES\t238,28\t\r\nTOTAL DE PASIVOS\t692,70\t\r\nCAPITAL CONTABLE\t\r\nCapital s«ial\tmoo\t\r\nGanancias retenidas\t210,30\t\r\na legal\t21,20\t\r\nTOTAL CAPITAL CONTABLE\t831,50\t\r\nTOTAL PASIVO Y CAPITAL\t1.524,20\t\r\n",
                                          max_tokens=2048  )

    return  completion.choices[0].text


#@app.post("/AnalizarDocumento/")
#async def AnalizarDocumento(textoAnalizar):

    #openai.api_key = "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"

    #completion = openai.Completion.create(engine= "text-davinci-003",
    #                                      prompt= "¿Que podriamos concluir de la operacion de una empresa en base siguiente reporte: ? "+textoAnalizar,
    #                                      max_tokens=2048  )


    #return completion.choices[0].text
    #return textoAnalizar


    #return resultado.content.decode()
    #return resultado.content


@app.get('/posts/{post_id}')
def get_post(post_id: str):
    for post in posts:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete('/posts/{post_id}')
def delete_post(post_id: str):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts.pop(index)
            return {"message": "Post has been deleted succesfully"}
    raise HTTPException(status_code=404, detail="Item not found")

@app.put('/posts/{post_id}')
def update_post(post_id: str, updatedPost: Post):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts[index]["title"]= updatedPost.dict()["title"]
            posts[index]["content"]= updatedPost.dict()["content"]
            posts[index]["author"]= updatedPost.dict()["author"]
            return {"message": "Post has been updated succesfully"}
    raise HTTPException(status_code=404, detail="Item not found")
