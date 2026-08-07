from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import encrypt
from app.models.user import Member
from app.schemas.user import (
    MemberCreate,
    MemberUpdate,
    MemberResponse,
)
from app.services.auth_service import MemberService

router = APIRouter(
    prefix="/api/v1/members",
    tags=["Members"],
)


@router.get("/", response_model=list[MemberResponse])
def get_members(db: Session = Depends(get_db)):
    return MemberService.get_all(db)


@router.post("/", response_model=MemberResponse)
def create_member(
    data: MemberCreate,
    db: Session = Depends(get_db),
):

    if MemberService.get_by_client_id(db, data.client_id):
        raise HTTPException(
            status_code=400,
            detail="Client ID already exists"
        )

    member = Member(
        member_name=data.member_name,
        client_id=data.client_id,
        password=encrypt(data.password),
        api_key=encrypt(data.api_key),
        totp_secret=encrypt(data.totp_secret),
    )

    return MemberService.create(db, member)


@router.get("/{member_id}", response_model=MemberResponse)
def get_member(
    member_id: int,
    db: Session = Depends(get_db),
):
    member = MemberService.get_by_id(db, member_id)

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    return member


@router.put("/{member_id}", response_model=MemberResponse)
def update_member(
    member_id: int,
    data: MemberUpdate,
    db: Session = Depends(get_db),
):

    member = MemberService.get_by_id(
        db,
        member_id,
    )

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found",
        )

    member.member_name = data.member_name

    member.password = encrypt(
        data.password
    )

    member.api_key = encrypt(
        data.api_key
    )

    member.totp_secret = encrypt(
        data.totp_secret
    )

    member.is_active = data.is_active

    MemberService.save(db)

    return member


@router.delete("/{member_id}")
def delete_member(
    member_id: int,
    db: Session = Depends(get_db),
):

    member = MemberService.get_by_id(
        db,
        member_id,
    )

    if member is None:

        raise HTTPException(
            status_code=404,
            detail="Member not found",
        )

    MemberService.delete(
        db,
        member,
    )

    return {

        "success": True,

        "message": "Member Deleted"

    }