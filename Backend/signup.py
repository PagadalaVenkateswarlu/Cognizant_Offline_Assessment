import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from Backend import database_model as models, schemas
from sqlalchemy import select, or_
from Backend.database_model import init_models, get_db
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Event Slots API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.on_event("startup")
async def on_startup():
    await init_models()


@app.post("/slots/create")
async def create_slots(slot: schemas.SlotCreate, db: AsyncSession = Depends(get_db)):
    # checking admin or not if admin creating slots
    if not slot.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can create slots")
    # stmt = select(models.EventSlot).where(
    #     models.EventSlot.category_id == slot.category_id,
    #     models.EventSlot.week == slot.week
    # )
    #
    # result = await db.execute(stmt)
    # existing_slot = result.scalars().first()
    #
    # if existing_slot:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Slot already exists for this user in the same category and week"
    #     )

    new_slot = models.EventSlot(start_time=slot.start_time,
                                end_time=slot.end_time,
                                week=slot.week,
                                category_id=slot.category_id,
                                is_booked=False,
                                is_admin=True
                                )

    db.add(new_slot)
    await db.commit()
    await db.refresh(new_slot)
    return {"detail": "Slot created successfully", "slot_id": new_slot.id}


@app.post("/booking-flow")
async def booking_flow(user: schemas.UserCreate, category_id: int, week: int, db: AsyncSession = Depends(get_db)):
    stmt = select(models.User).where(or_(models.User.email == user.email, models.User.username == user.username))
    result = await db.execute(stmt)
    db_user = result.scalars().first()

    if not db_user:
        db_user = models.User(email=user.email, username=user.username, category_id=category_id, week=week,
                              user_id=user.user_id)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

    stmt = select(models.EventSlot).where(
        models.EventSlot.category_id == category_id,
        models.EventSlot.week == week,
        models.EventSlot.is_booked == False
    )

    result = await db.execute(stmt)
    available_slots = result.scalars().all()

    if not available_slots:
        raise HTTPException(status_code=404, detail="No slots available")
    stmt = select(models.User).where(models.User.user_id == user.user_id).with_for_update()
    result = await db.execute(stmt)
    user_locked = result.scalars().first()
    if not user_locked:
        user_update = models.User(category_id=category_id,
                                  username=user.username,
                                  email=user.email,
                                  week=week,
                                  is_booked=user.is_booked,
                                  user_id=user.user_id)
        db.add(user_update)
        await db.commit()
        await db.refresh(user_update)

    booking = models.Booking(
        user_id=user.user_id,
        slot_id=category_id
    )

    booking.is_booked = True

    db.add(booking)
    await db.commit()
    await db.refresh(booking)

    return {
        "message": "Slot successfully booked",
        "user_id": user.user_id
    }


@app.get("/admin/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    stmt = select(models.EventSlot)
    results = await db.execute(stmt)
    users = results.scalars().all()

    result = []
    for user in users:
        # booked = [slot.id for slot in users]
        result.append({"user_id": user.id, "start_time": user.start_time, "end_time": user.end_time, "week": user.week,
                       "is_booked": user.is_booked})
    return result


@app.post("/slots/{slot_id}/cancel")
async def cancel_slot(slot_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(models.User).where(models.User.user_id == user_id,
                                     models.User.category_id == slot_id).with_for_update()
    result = await db.execute(stmt)
    slot = result.scalars().first()

    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")

    if slot.user_id != user_id:
        raise HTTPException(status_code=403, detail=" You did not book the slot")

    slot.user_id = None
    await db.commit()

    return {"detail": "Slot successfully cancelled"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
