# Fast Proximity Finder
Built in python with [Uber's H3 geospatial indexing](https://github.com/uber/h3) and FastAPI. 

## Purpose
Searching for nearby locations using stored latitude and longitude is **highly inefficient**. This python API provides a *fast, efficient* drop-in solution by interfacing with the highly efficient H3 library. For speed, it can either utilize sqlite3 (built-in with python) or Redis as a backend for indexing H3 geohashes.

## Use
Need to have Redis running on localhost with default port (6379)

1. Create and activate virtual env. (tested with 3.8.5)
2. `pip install -r "requirements.txt"`
3. `uvicorn main:app`

Endpoints:
1. `/add_location`
2. `/find_nearby_locations`
3. `/delete_location`


#### Deprec
instructions on endpoints available at http://127.0.0.1:8000/docs 

notes on redis: 
1. `CONFIG GET dir` to know where the dump file is. (Persistence)
2. `CONFIG SET appendfsync always` to keep all data safe
