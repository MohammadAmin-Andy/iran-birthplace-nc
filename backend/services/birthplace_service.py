# backend/app/services/birthplace_service.py

import json
from typing import Dict, Optional

# Import the centralized settings to get the dataset path
from app.config import settings

class BirthplaceService:
    """
    A service class to handle the business logic for birthplace data
    and national code validation.
    """
    _data: Dict[str, str] = {}

    def __init__(self):
        """
        Initializes the service by loading the dataset from the JSON file.
        The data is loaded only once and cached in the _data attribute for performance.
        """
        if not BirthplaceService._data:
            try:
                with open(settings.DATASET_PATH, 'r', encoding='utf-8') as f:
                    BirthplaceService._data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                # This is a critical error. The service cannot function without the data.
                print(f"FATAL ERROR: Could not load or parse the dataset at {settings.DATASET_PATH}. Error: {e}")
                BirthplaceService._data = {}

    def _is_valid_national_code_algorithm(self, national_code: str) -> bool:
        """
        Validates an Iranian national code using the control digit algorithm.
        Assumes the input is a 10-digit string.
        """
        # A national code where all digits are the same is invalid.
        if len(set(national_code)) == 1:
            return False

        control_digit = int(national_code[9])
        s = sum(int(national_code[i]) * (10 - i) for i in range(9))
        remainder = s % 11

        if remainder < 2:
            return control_digit == remainder
        else:
            return control_digit == 11 - remainder

    def get_validation_details(self, national_code: str) -> Dict:
        """
        Performs a full, step-by-step validation of the national code.
        1. Validates the control digit algorithm.
        2. Checks if the birthplace code exists in the dataset.
        3. Returns detailed results at each step.
        """
        # Step 1: Validate the national code algorithm (control digit)
        if not self._is_valid_national_code_algorithm(national_code):
            return {
                "is_valid": False,
                "status": "Invalid National Code Algorithm",
                "reason": "The control digit does not match the first 9 digits."
            }

        # Step 2: Check for the birthplace code in our dataset
        code_prefix = national_code[:3]
        city = self._data.get(code_prefix)

        if not city:
            return {
                "is_valid": False,
                "status": "Birthplace Code Not Found",
                "reason": f"The birthplace code prefix '{code_prefix}' does not exist in the dataset, although the code's algorithm is valid."
            }
        
        # Step 3: Success - All checks passed
        return {
            "is_valid": True,
            "status": "National Code is Valid",
            "details": {
                "national_code": national_code,
                "code_prefix": code_prefix,
                "birthplace": city
            }
        }

    def get_all_data(self) -> Dict[str, str]:
        """
        Returns the entire cached dataset.
        """
        return self._data