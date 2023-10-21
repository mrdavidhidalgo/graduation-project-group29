from controllers import management_service_facade

from fastapi import HTTPException
import enum
import pydantic

class ErrorCode(enum.Enum):
    ABC00 = "ABC00"
    ABC01 = "ABC01"

class MapperException(pydantic.BaseModel):
    status_code : int
    error_code : ErrorCode
    
    def to_dict(self):
        return {
            "status_code": self.status_code,
            "error_code": self.error_code.value
        }
    

    
_EXCEPTION_MAPPING = {
    management_service_facade.ProfessionalDoesNotExistError: MapperException(status_code = 404, error_code = ErrorCode.ABC01)
}

def _get_exception_code(
    exception: Exception,
) -> MapperException:
    try:
        return _EXCEPTION_MAPPING[type(exception)]
    except Exception as e:
        return MapperException(http_status_code = 500, error_code = ErrorCode.ABC00)
    

def process_error_response(exception: Exception)->None:
    exception_result = _get_exception_code(exception)
    
    raise HTTPException(status_code=exception_result.status_code, detail=exception_result.to_dict())