from pydantic import BaseModel

class FindJobRequest(BaseModel):
    lat: float
    lng: float
        
class AddJobRequest(BaseModel):
    id_: int 
    lat: float
    lng: float
        
class EditJobRequest(BaseModel):
    id_: int 
    lat_old: float
    lng_old: float
    lat_new: float
    lng_new: float
        