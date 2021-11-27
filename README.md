# Fast Proximity Finder
Built in python with (Uber's H3 Geohashing Library)[https://github.com/uber/h3]

## To run: 

Need to have Redis running on localhost with default port (6379)

1. Create and activate virtual env. (tested with 3.8.5)
2. `pip install -r "requirements.txt"`
3. `uvicorn main:app`

Endpoints:
1. `/add_location`
2. `/find_nearby_locations`
3. `/delete_location`


### Deprec
instructions on endpoints available at http://127.0.0.1:8000/docs 

notes on redis: 
1. `CONFIG GET dir` to know where the dump file is. (Persistence)
2. `CONFIG SET appendfsync always` to keep all data safe
