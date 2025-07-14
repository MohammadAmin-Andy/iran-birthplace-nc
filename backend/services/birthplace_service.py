# backend/app/services/birthplace_service.py

import json
from typing import Dict, Optional, Tuple

# Import the centralized settings to get the dataset path
from app.config import settings

class BirthplaceService:
    """
    A service class to handle the business logic for birthplace data
    and national code validation, using a structured dataset (Province -> City).
    """
    _data: Dict[str, Dict[str, str]] = {}

    def __init__(self):
        """
        Initializes the service by loading the structured dataset from the JSON file.
        """
        if not BirthplaceService._data:
            try:
                with open(settings.DATASET_PATH, 'r', encoding='utf-8') as f:
                    BirthplaceService._data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"FATAL ERROR: Could not load or parse the dataset at {settings.DATASET_PATH}. Error: {e}")
                BirthplaceService._data = {}

    def _find_location_by_code(self, code_prefix: str) -> Optional[Tuple[str, str]]:
        """
        Finds the province and city for a given 3-digit code prefix by iterating
        through the structured data.
        """
        for province, cities in self._data.items():
            if code_prefix in cities:
                return (province, cities[code_prefix])
        return None

    def _is_valid_national_code_algorithm(self, national_code: str) -> bool:
        """
        Validates an Iranian national code using the control digit algorithm.
        """
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
        Performs a full, step-by-step validation of the national code using the structured dataset.
        """
        # Step 1: Validate the national code algorithm
        if not self._is_valid_national_code_algorithm(national_code):
            return {
                "is_valid": False,
                "status": "Invalid National Code Algorithm",
                "reason": "The control digit does not match the first 9 digits."
            }

        # Step 2: Find the location (province and city) using the new structured data
        code_prefix = national_code[:3]
        location = self._find_location_by_code(code_prefix)

        if not location:
            return {
                "is_valid": False,
                "status": "Birthplace Code Not Found",
                "reason": f"The birthplace code prefix '{code_prefix}' does not exist in the dataset, although the code's algorithm is valid."
            }
        
        province, city = location
        
        # Step 3: Success - All checks passed
        return {
            "is_valid": True,
            "status": "National Code is Valid",
            "details": {
                "national_code": national_code,
                "code_prefix": code_prefix,
                "province": province,
                "city": city
            }
        }

    def get_all_data(self) -> Dict[str, Dict[str, str]]:
        """
        Returns the entire cached structured dataset.
        """
        return self._data