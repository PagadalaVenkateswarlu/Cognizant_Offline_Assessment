# @app.post("/signup")
# async def login_or_signup(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
#     stmt = select(models.User).where((models.User.email == user.email)| (models.User.username == user.username))
#     result = await db.execute(stmt)
#     db_user = result.scalars().first()
#     if db_user:
#         raise HTTPException(status_code=400, detail="User already exists")
#     db_user = models.User(email=user.email, username=user.username)
#     db.add(db_user)
#     await db.commit()
#     await db.refresh(db_user)
#     return db_user
#
#
# @app.post("/login")
# async def get_slots(slot:UserCreate, week: int, db: AsyncSession = Depends(get_db)):
#     stmt = select(models.User).where(models.User.username == slot.username,
#                                           models.User.email == slot.email)
#     result = await db.execute(stmt)
#     slots = result.scalars().all()
#     if not slots:
#         raise HTTPException(status_code=404, detail="Slots not found")
#     return {"message": "Login successful", "user_id": slot.user_id}
#
# @app.get("/slots")
# async def get_available_slots(category_id: int, week: int, db: AsyncSession = Depends(get_db)):
#     stmt = select(models.EventSlot).where(models.EventSlot.category_id == category_id,models.EventSlot.week==week,models.EventSlot.is_booked==False)
#     return stmt
#
# @app.post("/slots/book_slot")
# async def book_slot(slot_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
#     stmt = select(models.User).where(models.User.user_id == user_id).with_for_update()
#     result = await db.execute(stmt)
#     user = result.scalars().first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     if user.is_booked:
#         raise HTTPException(status_code=400, detail="User already booked")
#     booking = Booking(user_id=user_id, slot_id=slot_id)
#
#     user.is_booked = True
#     await db.add(booking)
#     await db.commit()
#     return {"detail": "slot successfully booked"}


# @app.post("/booking-flow")
# async def booking_flow(user: schemas.UserCreate,category_id: int,week: int,slot_id: int,db: AsyncSession = Depends(get_db)):
#     stmt = select(models.User).where(or_(models.User.email == user.email,models.User.username == user.username))
#     result = await db.execute(stmt)
#     db_user = result.scalars().first()
#
#     if not db_user:
#         db_user = models.User(email=user.email,username=user.username)
#         db.add(db_user)
#         await db.commit()
#         await db.refresh(db_user)
#
#     stmt = select(models.User).where(models.User.email == user.email,models.User.username == user.username)
#     result = await db.execute(stmt)
#     login_user = result.scalars().first()
#
#     if not login_user:
#         raise HTTPException(status_code=404, detail="Login failed")
#
#     stmt = select(models.EventSlot).where(
#         models.EventSlot.category_id == category_id,
#         models.EventSlot.week == week,
#         models.EventSlot.is_booked == False
#     )
#
#     result = await db.execute(stmt)
#     available_slots = result.scalars().all()
#
#     if not available_slots:
#         raise HTTPException(status_code=404, detail="No slots available")
#     stmt = select(models.User).where(
#         models.User.id == login_user.user_id
#     ).with_for_update()
#
#     result = await db.execute(stmt)
#     user_locked = result.scalars().first()
#
#     if user_locked.is_booked:
#         raise HTTPException(status_code=400, detail="User already booked")
#
#     # STEP 6 — Book slot
#     booking = models.Booking(
#         user_id=user_locked.user_id,
#         slot_id=slot_id
#     )
#
#     user_locked.is_booked = True
#
#     db.add(booking)
#     await db.commit()
#
#     return {
#         "message": "Slot successfully booked",
#         "user_id": user_locked.user_id,
#         "slot_id": slot_id
#     }
#
# @app.get("/admin/users")
# async def get_users(db: AsyncSession = Depends(get_db)):
#     stmt = select(models.User).options(selectinload(models.User.booked_slots))
#     results = await db.execute(stmt)
#     users = results.scalars().all()
#
#     result = []
#     for user in users:
#         booked = [slot.id for slot in user.booked_slots]
#         result.append({"user_id": user.id, "username": user.username, "booked_slots": booked})
#     return result
#
#
# @app.post("/slots/{slot_id}/cancel")
# async def cancel_slot(slot_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
#     stmt = select(models.EventSlot).where(models.EventSlot.user_id == user_id,models.EventSlot.category_id==slot_id).with_for_update()
#     result = await db.execute(stmt)
#     slot = result.scalars().first()
#
#     if not slot:
#         raise HTTPException(status_code=404, detail="Slot not found")
#
#     if slot.user_id != user_id:
#         raise HTTPException(status_code=403, detail=" You did not book the slot")
#
#     slot.user_id = None
#     await db.commit()
#
#     return {"detail": "Slot successfully cancelled"}
