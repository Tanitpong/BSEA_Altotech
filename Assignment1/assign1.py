# !pip install mysql-connector-python fastapi uvicorn[standard]
# how to run this file: uvicorn assign1:app --reload

import mysql.connector
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# Configure database connection (MySQL)
database = "assignment1"
user = "-"
password = "-"
host = "-"
port = "3306"
conn = mysql.connector.connect(
    host=host, port=port, user=user, password=password, database=database
)

# Pydantic models class for request and response in operations
class CreateWorkOrderRequest(BaseModel):
    work_order_number: str
    created_by: str
    assigned_to: str
    room: str
    started_at: datetime
    finished_at: datetime
    type: str
    status: str


class UpdateWorkOrderRequest(BaseModel):
    created_by: str = None
    assigned_to: str = None
    room: str = None
    started_at: datetime = None
    finished_at: datetime = None
    type: str = None
    status: str = None


class CheckWorkOrderRequest(BaseModel):
    id: int
    work_order_number: str
    created_by: str
    assigned_to: str
    room: str
    started_at: datetime
    finished_at: datetime
    type: str
    status: str
    
###===================================================================================================###
# API endpoints for operations
# Create work-orders
@app.post("/work-orders", response_model=CheckWorkOrderRequest)
def create_work_order(work_order: CreateWorkOrderRequest):
    
    try:
        # Check if work order number is duplicate
        cursor = conn.cursor()
        query = "SELECT id FROM work_orders WHERE work_order_number = %s"
        cursor.execute(query, (work_order.work_order_number,))
        if cursor.fetchone():
            cursor.close()
            raise HTTPException(
                status_code=400, detail="Work order number already exists"
            )
        cursor.close()

        # Create work order
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO work_orders (
            work_order_number, created_by, assigned_to, room,
            started_at, finished_at, type, status
        ) VALUES (
            %(work_order_number)s, %(created_by)s, %(assigned_to)s, %(room)s,
            %(started_at)s, %(finished_at)s, %(type)s, %(status)s
        )
        """
        cursor.execute(insert_query, work_order.dict())
        conn.commit()
        work_order_id = cursor.lastrowid
        cursor.close()
        return {
            "id": work_order_id,
            **work_order.dict(),
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Failed to create work order")

###===================================================================================================###
#  Update work-orders by id
@app.put("/work-orders/{work_order_id}", response_model=CheckWorkOrderRequest)
def update_work_order(work_order_id: int, work_order: UpdateWorkOrderRequest):
    
    try:
        cursor = conn.cursor()
        query = """
        UPDATE work_orders
        SET
            created_by = COALESCE(%(created_by)s, created_by),
            assigned_to = COALESCE(%(assigned_to)s, assigned_to),
            room = COALESCE(%(room)s, room),
            started_at = COALESCE(%(started_at)s, started_at),
            finished_at = COALESCE(%(finished_at)s, finished_at),
            type = COALESCE(%(type)s, type),
            status = COALESCE(%(status)s, status)
        WHERE id = %(work_order_id)s
        """
        work_order_dict = work_order.dict()
        work_order_dict["work_order_id"] = work_order_id
        cursor.execute(query, work_order_dict)
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Work order is not found")
        cursor.close()
        return {
            "id": work_order_id,
            **work_order.dict(exclude_unset=True),
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Failed to update the work order")

###===================================================================================================###
# Get work-orders by id
@app.get("/work-orders/{work_order_id}", response_model=CheckWorkOrderRequest)
def get_work_order(work_order_id: int):
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM work_orders WHERE id = %s"
        cursor.execute(query, (work_order_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            work_order_dict = {
                "id": result[0],
                "work_order_number": result[1],
                "created_by": result[2],
                "assigned_to": result[3],
                "room": result[4],
                "started_at": result[5],
                "finished_at": result[6],
                "type": result[7],
                "status": result[8],
            }
            return CheckWorkOrderRequest(**work_order_dict)
        else:
            raise HTTPException(status_code=404, detail="Work order not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to get work order")



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
