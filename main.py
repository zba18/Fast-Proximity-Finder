import h3
import redis
import time
import hashlib
import cachetools
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, Request

from models import FindJobRequest, AddJobRequest, EditJobRequest
from h3_services import H3RedisService

load_dotenv()
secret = os.getenv('SECRET_KEY')
### redis auth keys here.
###

r = redis.Redis('localhost') # make sure this is running, port default is 6379

h3service = H3RedisService(r)

app = FastAPI()

### to do: test these, use os.environ 



salt_cache = cachetools.TTLCache(10000, 5)

async def verify_user(req: Request):  
    try:
        time_token = int(req.headers["time-token"])
        h = req.headers["auth-key"]
    except KeyError:
        raise HTTPException(status_code=401, detail="Unauthorized 1")
    except TypeError:
        raise HTTPException(status_code=412, detail="Precondition Failed") 
        
    #no reusing old tokens
    if not (time.time_ns() - 5 * 1000000000 < time_token < time.time_ns()): 
        raise HTTPException(status_code=401, detail="Unauthorized 2")
        
    #no using tokens more than once
    if salt_cache.get(time_token, None): # cache return None if hash is fresh, so disallow when True
        raise HTTPException(status_code=401, detail="Unauthorized 3")
    
    #confirm auth: test integrity of hash
    valid_h = hashlib.new('sha512')
    valid_h.update(f'{time_token}-{secret}'.encode())
    
    if h != valid_h.hexdigest():
        raise HTTPException(status_code=401, detail="Unauthorized 4")
        
    else: 
        salt_cache[time_token] = True #no using tokens more than once
        return True
    

@app.post("/add_job")
async def add_job_service( ajr : AddJobRequest, authorized: bool = Depends(verify_user)):
    resp = h3service.add_job(ajr.id_, (ajr.lat,ajr.lng))
    return {"message": resp}

@app.post("/find_jobs")
async def find_job_service(fjr : FindJobRequest, authorized: bool = Depends(verify_user)):
    resp = h3service.find_jobs((fjr.lat,fjr.lng))
    return {"job_ids": resp}

@app.post("/edit_job")
async def edit_job_service(ejr : EditJobRequest, authorized: bool = Depends(verify_user)):
    resp = h3service.edit_job_loc(ejr.id_, (ejr.lat_old,ejr.lng_old), (ejr.lat_new,ejr.lng_new) )
    return {"message": resp}

@app.get("/")
async def home(authorized: bool = Depends(verify_user)):
     if authorized:
        return {"detail": "Authorised"}

