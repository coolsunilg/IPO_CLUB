from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def dashboard():

    return {

        "software": "IPO CLUB",

        "version": "1.0.0",

        "broker": "Angel One",

        "clients": 0,

        "active_ipo": 0,

        "applications": 0,

        "status": "Ready"

    }