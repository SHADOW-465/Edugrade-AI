from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.v1 import dependencies
from app.services import approval_service
from app.models import schemas

router = APIRouter()

@router.post("/{submission_id}/approve", response_model=schemas.Submission)
def approve_submission(
    submission_id: int,
    approval_data: schemas.ApprovalCreate,
    db: Session = Depends(dependencies.get_db),
    current_user: schemas.User = Depends(dependencies.get_current_active_user),
):
    """
    Approve a submission.
    """
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Not authorized to approve submissions")
    submission = approval_service.approve_submission(
        db, submission_id=submission_id, user_id=current_user.id, notes=approval_data.notes
    )
    return submission

@router.post("/{submission_id}/reject", response_model=schemas.Submission)
def reject_submission(
    submission_id: int,
    rejection_data: schemas.ApprovalCreate,
    db: Session = Depends(dependencies.get_db),
    current_user: schemas.User = Depends(dependencies.get_current_active_user),
):
    """
    Reject a submission.
    """
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Not authorized to reject submissions")
    submission = approval_service.reject_submission(
        db, submission_id=submission_id, user_id=current_user.id, notes=rejection_data.notes
    )
    return submission
