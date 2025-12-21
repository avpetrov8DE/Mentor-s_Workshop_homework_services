from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from app.db import init_db, get_conn
from app.schemas import ItemCreate, ItemUpdate, ItemOut, ItemStatus
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    pass

app = FastAPI(title="TODO Service", version="1.0.0", lifespan=lifespan)

def _row_to_item(row) -> ItemOut:
    """Преобразует строку БД в объект ItemOut"""
    return ItemOut(
        id=row['id'],
        title=row['title'],
        description=row['description'],
        completed=bool(row['completed']),
        status=row['status'],
        created_at=row['created_at']
    )

@app.post("/items", response_model=ItemOut, status_code=201)
def create_item(payload: ItemCreate):
    """Создание новой задачи"""
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO items (title, description, completed, status) VALUES (?, ?, ?, ?)",
            (
                payload.title, 
                payload.description, 
                0,  # completed по умолчанию False
                payload.status.value if payload.status else ItemStatus.non_urgent.value
            ),
        )
        conn.commit()
        item_id = cur.lastrowid
        row = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        return _row_to_item(row)

@app.get("/items", response_model=List[ItemOut])
def list_items(
    status: Optional[ItemStatus] = Query(None, description="Фильтр по статусу: Неотложная или Несрочная")
):
    """Получение списка задач по заданному статусу"""
    with get_conn() as conn:
        if status:
            # Если указан статус - фильтруем по нему
            rows = conn.execute(
                "SELECT * FROM items WHERE status = ? ORDER BY id DESC", 
                (status.value,)
            ).fetchall()
        else:
            # Если статус не указан - все задачи
            rows = conn.execute("SELECT * FROM items ORDER BY id DESC").fetchall()
        
        return [_row_to_item(r) for r in rows]

@app.get("/items/{item_id}", response_model=ItemOut)
def get_item(item_id: int):
    """Получение задачи по ID"""
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Item not found")
        return _row_to_item(row)

@app.put("/items/{item_id}", response_model=ItemOut)
def update_item(item_id: int, payload: ItemUpdate):
    """Обновление задачи по ID"""
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Item not found")
        
        update_fields = []
        params = []
        
        if payload.title is not None:
            update_fields.append("title = ?")
            params.append(payload.title)
        
        if payload.description is not None:
            update_fields.append("description = ?")
            params.append(payload.description)
        
        if payload.completed is not None:
            update_fields.append("completed = ?")
            params.append(int(payload.completed))
        
        if payload.status is not None:
            update_fields.append("status = ?")
            params.append(payload.status.value)
        
        if not update_fields:
            return _row_to_item(row)
        
        params.append(item_id)
        
        sql = f"UPDATE items SET {', '.join(update_fields)} WHERE id = ?"
        conn.execute(sql, params)
        conn.commit()
        
        updated_row = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        return _row_to_item(updated_row)

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    """Удаление задачи по ID"""
    with get_conn() as conn:
        row = conn.execute("SELECT id FROM items WHERE id = ?", (item_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Item not found")
        
        conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()
        return None

@app.get("/")

def root():
    """Корневой эндпоинт"""
    return {
        "message": "TODO Service API", 
        "docs": "/docs",
        "status_values": ["Неотложная", "Несрочная"]
    }
