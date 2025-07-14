# backend/app/schemas/birthplace_schema.py

from pydantic import BaseModel, Field
from typing import Optional, Dict

class NationalCodePayload(BaseModel):
    """
    Schema for the request body of the /validate endpoint.
    """
    national_code: str = Field(
        ...,
        title="Iranian National Code",
        description="A 10-digit Iranian national code to be validated.",
        min_length=10,
        max_length=10,
        pattern="^[0-9]{10}$"
    )

class ValidationDetails(BaseModel):
    """
    Schema for the nested 'details' object in a successful response.
    """
    national_code: str
    code_prefix: str
    birthplace: str

class SuccessfulValidationResponse(BaseModel):
    """
    Schema for a successful validation response.
    """
    is_valid: bool = True
    status: str
    details: ValidationDetails

class FailedValidationResponse(BaseModel):
    """
    Schema for a failed validation response.
    """
    is_valid: bool = False
    status: str
    reason: str

# Although we return a Dict from the endpoint for simplicity,
# these schemas are useful for documentation and internal validation.