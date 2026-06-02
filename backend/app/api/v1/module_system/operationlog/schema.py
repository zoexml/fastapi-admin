from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

ALLOWED_REQUEST_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]


class OperationLogQueryParam(BaseModel):
    request_path: str | None = Field(None, max_length=255, description="请求路径")
    request_method: str | None = Field(None, description="请求方式")
    username: str | None = Field(None, max_length=64, description="用户名")

    @field_validator("request_method")
    @classmethod
    def validate_request_method(cls, value: str | None) -> str | None:
        if value and value.upper() not in ALLOWED_REQUEST_METHODS:
            raise ValueError(f"请求方式必须是: {', '.join(ALLOWED_REQUEST_METHODS)}")
        return value.upper() if value else None

    def to_dict(self) -> dict | None:
        """转换为字典，仅包含非空字段"""
        return self.model_dump(exclude_none=True)


class OperationLogOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    tenant_id: int
    request_path: str
    request_method: str
    request_ip: str | None = None
    request_os: str | None = None
    request_browser: str | None = None
    response_code: int
    process_time: str | None = None
    created_at: datetime


class OperationLogDetailOutSchema(OperationLogOutSchema):
    request_payload: str | None = None
    response_json: str | None = None


class OperationLogCreateSchema(BaseModel):
    request_path: str = Field(..., min_length=1, max_length=255, description="请求路径")
    request_method: str = Field(..., description="请求方式")
    request_payload: str | None = Field(None, description="请求体")
    request_ip: str | None = Field(None, max_length=50, description="请求IP地址")
    request_os: str | None = Field(None, max_length=64, description="操作系统")
    request_browser: str | None = Field(None, max_length=64, description="浏览器")
    response_code: int = Field(200, ge=100, le=599, description="响应状态码")
    response_json: str | None = Field(None, description="响应体")
    process_time: str | None = Field(None, max_length=20, description="处理时间")

    @field_validator("request_method")
    @classmethod
    def validate_request_method(cls, value: str) -> str:
        upper_value = value.upper()
        if upper_value not in ALLOWED_REQUEST_METHODS:
            raise ValueError(f"请求方式必须是: {', '.join(ALLOWED_REQUEST_METHODS)}")
        return upper_value
