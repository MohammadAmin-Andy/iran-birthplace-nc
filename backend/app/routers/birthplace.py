# backend/app/routers/birthplace.py

from fastapi import APIRouter, HTTPException, status, Path
from typing import Dict

# Import the service that contains the business logic
from app.services.birthplace_service import BirthplaceService

# Create an instance of the service
birthplace_service = BirthplaceService()

# Create a new router
router = APIRouter()

@router.get(
    "/validate/{national_code}",
    response_model=Dict[str, str],
    summary="Validate a national code and get its birthplace",
    tags=["Birthplace Validation"]
)
def validate_national_code(
    national_code: str = Path(
        ...,
        min_length=10,
        max_length=10,
        regex="^[0-9]{10}$",
        title="Iranian National Code",
        description="A 10-digit Iranian national code."
    )
):
    """
    Validates the first three digits of an Iranian national code to find the
    corresponding birthplace (city/region).

    - **national_code**: A 10-digit string containing the national code.
    - **Returns**: A dictionary with the birthplace information if found.
    - **Raises**: An HTTPException with status 404 if the code prefix is not found.
    """
    try:
        # Extract the first 3 digits
        code_prefix = national_code[:3]
        
        # Call the service to get the city
        city = birthplace_service.get_city_by_code(code_prefix)
        
        if city:
            return {"code_prefix": code_prefix, "birthplace": city}
        else:
            # If the service returns None, the code was not found
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Birthplace for code prefix '{code_prefix}' not found."
            )
    except Exception as e:
        # General error handler for unexpected issues
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.get(
    "/all",
    response_model=Dict[str, str],
    summary="Get the entire dataset of codes and birthplaces",
    tags=["Dataset"]
)
def get_all_codes():
    """
    Returns the complete dataset mapping all known code prefixes to their
    corresponding birthplaces.
    """
    try:
        return birthplace_service.get_all_data()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not load the dataset: {str(e)}"
        )
