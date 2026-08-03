from typing import Type,TypeVar,Optional
from requests import Response
from pydantic import BaseModel

T = TypeVar("T",bound=BaseModel)

class ResponseValidator:
    """Utility class to centralize HTTP response and schema validations"""

    @staticmethod
    def assert_status_code(response:Response,expected_code:int=200)->None:
        """Asserts that the response HTTP status code matches expectations."""
        actual_code = response.status_code
        assert actual_code ==  expected_code, (
            f"Expected status code {expected_code}, but got {actual_code}"
            f"Response Body:{response.text}"
        )

    
    @staticmethod
    def assert_response_time(response:Response,max_allowed_ms:float=1.5) ->None:
        """Assume that API response time is within acceptable SLA limits"""
        elapsed_ms = response.elapsed.total_seconds()
        assert elapsed_ms <= max_allowed_ms,(
            f"API repsonse time ({elapsed_ms:.2f}s) exceeded SLA limit ({max_allowed_ms}ms)"
        )

    @staticmethod
    def validate_schema(response:Response,model_class:Type[T])->T:
        """Parse and validates the response JSON against a Pydantic model,Returns the parsed model instance for futher assurations"""
        try:
            json_data = response.json()
            return model_class(**json_data)

        except Exception as e:
            raise AssertionError(
                f"Failed to validate response body against {model_class.__name__}.\n"
                f"Raw Response:{response.text}\n"
                f"Error Details:{e}"
            )

    @classmethod
    def validate_response(
        cls,
        response:Response,
        expected_code:int = 200,
        model_class:Optional[Type[T]] = None,
        max_allowed_ms: Optional[float] = 1.5,
    ) -> Optional[T]:
        """
        Executes status code, response time, and optional schema validation in a single call
        """
        cls.assert_status_code(response=response,expected_code=expected_code)
        cls.assert_response_time(response=response,max_allowed_ms=max_allowed_ms)

        if model_class:
            return cls.validate_schema(response=response,model_class=model_class)
        return None 