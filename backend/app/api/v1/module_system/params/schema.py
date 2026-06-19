from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.common.enums import QueueEnum
from app.core.base_params import BaseQueryParam, TenantByQueryParam, UserByQueryParam
from app.core.base_schema import BaseSchema, TenantBySchema, UserBySchema


class ParamsCreateSchema(BaseModel):
    """配置创建模型"""

    config_name: str = Field(..., min_length=1, max_length=64, description="参数名称")
    config_key: str = Field(..., min_length=1, max_length=500, description="参数键名")
    config_value: str | None = Field(default=None, max_length=500, description="参数键值")
    config_type: bool = Field(default=False, description="是否系统内置")
    status: int = Field(default=0, ge=0, le=1, description="状态(0:正常 1:停用)")
    description: str | None = Field(default=None, max_length=500, description="描述")

    @field_validator("config_key")
    @classmethod
    def _validate_config_key(cls, v: str) -> str:
        v = v.strip().lower()
        import re

        if not re.match(r"^[a-z][a-z0-9_.-]*$", v):
            raise ValueError("参数键名必须以小写字母开头，仅允许小写字母、数字、_ . -")
        return v

    @field_validator("status")
    @classmethod
    def _validate_status(cls, v: int) -> int:
        if v not in {0, 1}:
            raise ValueError("状态仅支持 0(正常) 或 1(停用)")
        return v


class ParamsUpdateSchema(ParamsCreateSchema):
    """配置更新模型"""


class ParamsOutSchema(ParamsCreateSchema, BaseSchema, UserBySchema, TenantBySchema):
    """配置响应模型"""

    model_config = ConfigDict(from_attributes=True)


class ParamsQueryParam(BaseQueryParam, UserByQueryParam, TenantByQueryParam):
    """配置管理查询参数"""

    def __init__(
        self,
        config_name: str | None = Query(None, description="配置名称"),
        config_key: str | None = Query(None, description="配置键名"),
        config_type: bool | None = Query(None, description="系统内置((True:是 False:否))"),
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.config_name = (QueueEnum.like.value, config_name)
        self.config_key = (QueueEnum.like.value, config_key)
        self.config_type = (QueueEnum.eq.value, config_type)
