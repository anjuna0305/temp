from typing import List

from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile, Request
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
import os
import shutil
import uuid
from urllib.parse import urlencode

from app.database import get_db
from app.models import User as UserModel
from app.schemas import UserAPIRequest
from app.exeptions_handlers import InternalServerError
from .. import crud
import requests

router = APIRouter()


# @router.post("/{api_id}")
# async def outlet_funct(
#     api_id: int, request: Request, db: AsyncSession = Depends(get_db)
# ):
#     try:
#         print("try callled \n\n\n\n\n\n\n\n\n\n")
#         local_server_url = f"http://localhost:3000/{api_id}"
#         payload = await request.body()
#         encoded_paload = urlencode({"key1": "value1", "key2": "value2"})
#         print(payload)
#         print("try callled \n\n\n\n\n\n\n\n\n\n")

#         async with httpx.AsyncClient() as client:
#             response = await client.post(
#                 local_server_url, data={"key1": "value1", "key2": "value2"}
#             )
#         print("try callled \n\n\n\n\n\n\n\n\n\n")

#         if response.status_code == 200:
#             return response
#         else:
#             raise HTTPException(status_code=response.status_code, detail=response.text)

#     except Exception as e:
#         raise InternalServerError(detail={str(e)})


@router.post("/test")
async def outlet_funct():
    try:
        local_server_url = f"http://localhost:3000/123"
        encoded_paload = urlencode({"key1": "value1", "key2": "value2"})
        # payload = {"key1": "value1", "key2": "value2"}

        async with httpx.AsyncClient() as client:
            response = await client.post(local_server_url, data=encoded_paload)
            response.raise_for_status()
            return response.json()

    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/tmp")
async def send_request():
    url = "http://localhost:3000/tmp"  # The URL to which you want to send a request
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Raise an exception for 4xx/5xx responses
            return response.json()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/test2")
async def submit_form(request: Request):
    url = (
        "http://localhost:3000/endpoint"  # The URL to which you want to send a request
    )

    # Read the form data and files
    # form = await request.form()
    # print(form)

    # Prepare the form data for forwarding
    # form_data = {}
    # files = []
    # for field, value in form.multi_items():
    #     if isinstance(value, UploadFile):
    #         content = await value.read()  # Await the read operation
    #         files.append((field, (value.filename, content, value.content_type)))
    #     else:
    #         form_data[field] = value

    try:
        async with httpx.AsyncClient() as client:
            # Send the POST request with multipart/form-data
            response = await client.post(url, data=await request.body())
            response.raise_for_status()  # Raise an exception for 4xx/5xx responses
            return response.json()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/test3")
async def send_data(data=Form(...), files: list[UploadFile] = File(...)):
    # Replace with the actual URL of the other server's endpoint
    url = "http://localhost:3000/endpoint"

    # Prepare data to send (optional):
    # If the other server expects custom data format, manipulate it here

    # Prepare files for sending:
    file_data = {}
    for file in files:
        file_data[file.filename] = (file.content_type, file.file)

    # Send the POST request (handle potential errors)
    try:
        response = requests.post(url, data=data, files=file_data)
        response.raise_for_status()  # Raise exception for non-2xx status codes
        return {"message": "Data and files sent successfully!"}
    except requests.exceptions.RequestException as e:
        print(f"Error sending POST request: {e}")
        return {"error": "Failed to send data and files"}
