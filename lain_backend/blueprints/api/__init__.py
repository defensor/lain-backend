from fastapi import APIRouter

from . import domain, host, organization, project, service

router = APIRouter()

router.include_router(project.router, tags=["projects"], prefix="/projects")
router.include_router(
    organization.router, tags=["organizations"], prefix="/organizations"
)
router.include_router(host.router, tags=["hosts"], prefix="/hosts")
router.include_router(domain.router, tags=["domains"], prefix="/domains")
router.include_router(service.router, tags=["services"], prefix="/services")
