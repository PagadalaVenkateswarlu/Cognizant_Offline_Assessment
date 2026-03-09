# from fastapi import APIRouter
# from Backend import schemas
# from typing import List
#
# router = APIRouter(prefix = "/categories", tags = ["Categories"])
#
# @router.get("/admin/slots", response_model=List[schemas.Category])

a = [1,2,3,4]
b=a
b.append(5)
a= a+[5]
print(b)