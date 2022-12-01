from fastapi import FastAPI
from licenseManager import checkLicense, generateLicense, licenses
import sys, os

app = FastAPI()

generateLicense({"id": 5412, "name": "John Doe"})

@app.get("/")
async def root():
    return {"license": str(licenses[0])}

@app.get("/verify")
async def verify(license: str, id: int, name: str):
    licenseData = checkLicense(license)
    isValid = (licenseData=={'id': id, 'name': name})
    return {"valid": isValid}