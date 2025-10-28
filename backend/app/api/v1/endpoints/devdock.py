"""
API endpoints for interacting with the DevDock blockchain.
"""

from fastapi import APIRouter
from ..... import models
from .....services.devdock_service import devdock_service

router = APIRouter()

@router.post("/verify", response_model=models.schemas.VerificationResponse)
def verify_credential(credential: models.schemas.Credential):
    """
    Verify a credential on the DevDock blockchain.
    """
    verified = devdock_service.verify_credential(credential)
    return {"verified": verified}
