# backend/app/routers/birthplace.py

from fastapi import APIRouter, HTTPException, status
from typing import Dict

# Import the service that contains the business logic
from app.services.birthplace_service import BirthplaceService

# Create an instance of the service
birthplace_service = BirthplaceService()

# Create a new router
router = APIRouter()

@router.post(
    "/validate",
    response_model=Dict,
    summary="Validate a national code and get its details",
    tags=["Birthplace Validation"]
)
def validate_national_code(payload: Dict[str, str]):
    """
    Performs a full, step-by-step validation of an Iranian national code.

    - **Receives**: A JSON payload like `{"national_code": "0012345678"}`.
    - **Returns**: A detailed dictionary with the validation status and details.
    """
    national_code = payload.get("national_code")
    
    # Step 1: Check if the 'national_code' key exists in the payload.
    if not national_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'national_code' key is missing from the request payload."
        )

    # Step 2: Check if the length is exactly 10.
    if len(national_code) != 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The national code must be exactly 10 digits long."
        )

    # Step 3: Check if all characters are digits.
    if not national_code.isdigit():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The national code must only contain digits."
        )

    try:
        # Call the service method to get the full validation details
        validation_result = birthplace_service.get_validation_details(national_code)
        return validation_result
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
