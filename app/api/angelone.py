from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import Member
from app.schemas.auth import BulkLoginRequest
from app.services.angel_service import AngelService

router = APIRouter(
    prefix="/api/v1/angel",
    tags=["Angel One"],
)


@router.post("/login/{member_id}")
def login_member(
    member_id: int,
    db: Session = Depends(get_db),
):

    member = (
        db.query(Member)
        .filter(
            Member.id == member_id,
            Member.is_active == True,
        )
        .first()
    )

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found",
        )

    result = AngelService.login(member)

    return result


@router.post("/login-all")
def login_all(
    db: Session = Depends(get_db),
):

    members = (
        db.query(Member)
        .filter(Member.is_active == True)
        .order_by(Member.member_name)
        .all()
    )

    result = AngelService.login_all(
        members
    )

    return result


@router.post("/login-selected")
def login_selected(
    data: BulkLoginRequest,
    db: Session = Depends(get_db),
):

    members = (
        db.query(Member)
        .filter(
            Member.id.in_(data.member_ids),
            Member.is_active == True,
        )
        .all()
    )

    return AngelService.login_selected(
        members
    )


@router.post("/logout/{member_id}")
def logout_member(
    member_id: int,
    db: Session = Depends(get_db),
):

    member = (
        db.query(Member)
        .filter(
            Member.id == member_id,
            Member.is_active == True,
        )
        .first()
    )

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found",
        )

    AngelService.logout(
        member.client_id
    )

    return {
        "success": True,
        "message": "Logout Successful",
    }


@router.post("/logout-all")
def logout_all():

    AngelService.logout_all()

    return {
        "success": True,
        "message": "All Members Logged Out",
    }


@router.get("/status")
def login_status():

    return {
        "online": AngelService.online_members(),
        "sessions": AngelService.ACTIVE_SESSIONS,
    }


@router.get("/profile/{member_id}")
def member_profile(
    member_id: int,
    db: Session = Depends(get_db),
):

    member = (
        db.query(Member)
        .filter(
            Member.id == member_id,
            Member.is_active == True,
        )
        .first()
    )

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found",
        )

    session = AngelService.get_session(
        member.client_id
    )

    if session is None:
        raise HTTPException(
            status_code=400,
            detail="Member is not logged in",
        )

    return session["profile"]