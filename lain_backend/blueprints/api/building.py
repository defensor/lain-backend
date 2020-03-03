from fastapi import APIRouter

from typing import List, Optional

from fastapi import HTTPException

from lain_backend.cruds import building as crud, organization
from lain_backend.schemas import (
    Building,
    BuildingIn,
    BuildingUpdateIn,
    BuildingFilter,
    Organization,
    OrganizationFilter,
)
from lain_backend.database import database as db

router = APIRouter()


@router.post("/", response_model=Building)
async def building_create(building: BuildingIn):
    return await crud.create(db=db, building=building)


@router.put("/", response_model=List[Building])
async def building_get_all(
    skip: int = 0, limit: int = 100, filter: Optional[BuildingFilter] = None
):
    buildings = await crud.get_all(db=db, skip=skip, limit=limit, filter=filter)
    return buildings


@router.get("/{building_id}/", response_model=Building)
async def building_get(building_id: int):
    db_building = await crud.get(db=db, building_id=building_id)
    if db_building is None:
        raise HTTPException(status_code=404, detail="Building not found")
    return db_building


@router.delete("/{building_id}/", response_model=Building)
async def building_delete(building_id: int):
    db_building = await crud.get(db=db, building_id=building_id)
    if db_building is None:
        raise HTTPException(status_code=404, detail="Building not found")

    await crud.delete(db=db, building_id=building_id)

    return


@router.put("/{building_id}/", response_model=Building)
async def building_update(building_id: int, building: BuildingUpdateIn):
    if not (await crud.check(db=db, building_id=building_id)):
        raise HTTPException(status_code=404, detail="Building not found")

    return await crud.update(db=db, building_id=building_id, building=building)


@router.get("/{building_id}/organizations", response_model=List[Organization])
async def building_get_organizations(building_id: int):
    if not (await crud.check(db=db, building_id=building_id)):
        raise HTTPException(status_code=404, detail="Building not found")

    return await organization.get_all(db=db, filter=OrganizationFilter(building_id=building_id))
