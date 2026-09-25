from fastapi import APIRouter, HTTPException

from backend.services.case_service import get_case, list_cases

router = APIRouter()


@router.get("/cases")
def get_all_cases():
    return [case.model_dump() for case in list_cases().values()]


@router.get("/cases/{case_id}")
def get_case_by_id(case_id: str):
    try:
        case = get_case(case_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Case not found")
    return case.model_dump()
