# main.py

from fastapi import FastAPI, HTTPException
import asyncpg

# Initialize FastAPI app
app = FastAPI()

# PostgreSQL connection pool
pool = None


# Function to create connection pool
async def create_pool():
    global pool
    pool = await asyncpg.create_pool(
        user='mkasana',
        password='kkasanacoder',
        database='postgres',
        host='localhost'
    )


# Function to get a database connection from the pool
async def get_connection():
    return await pool.acquire()


# Function to close connection
async def close_connection(connection):
    await pool.release(connection)


# Define CRUD operations

# Create operation
async def create_item(connection, name):
    query = 'INSERT INTO items(name) VALUES($1) RETURNING id, name;'
    return await connection.fetchrow(query, name)


# Read operation
async def read_item(connection, item_id):
    query = 'SELECT id, name FROM items WHERE id = $1;'
    return await connection.fetchrow(query, item_id)


# Update operation
async def update_item(connection, item_id, new_name):
    query = 'UPDATE items SET name = $1 WHERE id = $2 RETURNING id, name;'
    return await connection.fetchrow(query, new_name, item_id)


# Delete operation
async def delete_item(connection, item_id):
    query = 'DELETE FROM items WHERE id = $1;'
    await connection.execute(query, item_id)


# API Endpoints

# Create item
@app.post("/items/", response_model=dict)
async def create_item_api(name: str):
    connection = await get_connection()
    item = await create_item(connection, name)
    await close_connection(connection)
    return item


# Read item
@app.get("/items/{item_id}", response_model=dict)
async def read_item_api(item_id: int):
    connection = await get_connection()
    item = await read_item(connection, item_id)
    await close_connection(connection)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# Update item
@app.put("/items/{item_id}", response_model=dict)
async def update_item_api(item_id: int, name: str):
    connection = await get_connection()
    item = await update_item(connection, item_id, name)
    await close_connection(connection)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# Delete item
@app.delete("/items/{item_id}", response_model=dict)
async def delete_item_api(item_id: int):
    connection = await get_connection()
    await delete_item(connection, item_id)
    await close_connection(connection)
    return {"message": "Item deleted successfully"}


# # Initialize the connection pool when the app starts
# @app.on_event("startup")
# async def startup():
#     await create_pool()


# # Close the connection pool when the app stops
# @app.on_event("shutdown")
# async def shutdown():
#     await pool.close()
