from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class LoginLogQueryParam(BaseModel):
    status: int | None = Field(None, ge=1, le=2, description="登录状态(1成功 2失败)")
    username: str | None = Field(None, max_length=64, description="用户名")

    def to_dict(self) -> dict | None:
        """转换为字典，仅包含非空字段"""
        return self.model_dump(exclude_none=True)


class LoginLogOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    status: int
    login_ip: str | None = None
    login_location: str | None = None
    request_os: str | None = None
    request_browser: str | None = None
    msg: str | None = None
    created_at: datetime


class LoginLogDetailOutSchema(LoginLogOutSchema):
    pass


class LoginLogCreateSchema(BaseModel):
    username: str = Field(..., min_length=1, max_length=64, description="用户名")
    status: int = Field(1, ge=1, le=2, description="登录状态(1成功 2失败)")
    login_ip: str | None = Field(None, max_length=50, description="登录IP地址")
    login_location: str | None = Field(None, max_length=255, description="登录位置")
    request_os: str | None = Field(None, max_length=64, description="操作系统")
    request_browser: str | None = Field(None, max_length=64, description="浏览器")
    msg: str | None = Field(None, max_length=255, description="提示消息")

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: int) -> int:
        if value not in [1, 2]:
            raise ValueError("登录状态只能为1(成功)或2(失败)")
        return value
