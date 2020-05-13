from fastapi import APIRouter

from . import project
from . import organization
from . import host
from . import domain
from . import service

router = APIRouter()

router.include_router(project.router, prefix="/projects")
router.include_router(organization.router, prefix="/organizations")
router.include_router(host.router, prefix="/hosts")
router.include_router(domain.router, prefix="/domains")
router.include_router(service.router, prefix="/services")
