from fastapi import APIRouter, Depends, HTTPException, status
from redis.asyncio import Redis
from src.models import Note
from src.auth import get_current_user
import uuid

router = APIRouter()

@router.post("/notes/", response_model=Note)
async def create_note(note: Note, redis: Redis = Depends(lambda: get_redis()), current_user: dict = Depends(get_current_user)):
    note_id = str(uuid.uuid4())
    note_data = note.dict()
    note_data['id'] = note_id
    note_data['owner_id'] = current_user['user_id']
    await redis.hset(f"note:{note_id}", mapping=note_data)
    return note_data

@router.get("/notes/{note_id}", response_model=Note)
async def get_note(note_id: str, redis: Redis = Depends(lambda: get_redis()), current_user: dict = Depends(get_current_user)):
    note_key = f"note:{note_id}"
    note_data = await redis.hgetall(note_key, encoding='utf-8')
    if not note_data:
        raise HTTPException(status_code=404, detail="Note not found")
    if note_data.get('owner_id') != current_user['user_id']:
        raise HTTPException(status_code=403, detail="Not authorized to access this note")
    return note_data

@router.delete("/notes/{note_id}")
async def delete_note(note_id: str, redis: Redis = Depends(lambda: get_redis()), current_user: dict = Depends(get_current_user)):
    note_key = f"note:{note_id}"
    note_data = await redis.hgetall(note_key, encoding='utf-8')
    if not note_data:
        raise HTTPException(status_code=404, detail="Note not found")
    if note_data.get('owner_id') != current_user['user_id']:
        raise HTTPException(status_code=403, detail="Not authorized to delete this note")
    await redis.delete(note_key)
    return {"detail": "Note deleted"}

# Additional routes for update, list, etc., can be added here
