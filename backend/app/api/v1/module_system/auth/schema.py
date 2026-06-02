from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

# 从 core 模块导入基础认证 schema，避免循环导入
from app.core.auth_schema import (
    AuthSchema,
    JWTPayloadSchema,
    JWTOutSchema,
    RefreshTokenPayloadSchema,
    LogoutPayloadSchema,
)


class CaptchaOutSchema(BaseModel):
    """验证码响应模型"""

    model_config = ConfigDict(from_attributes=True)

    enable: bool = Field(default=True, description="是否启用验证码")
    key: str = Field(..., min_length=1, description="验证码唯一标识")
    img_base: str = Field(..., min_length=1, description="Base64编码的验证码图片")


class AutoLoginUserSchema(BaseModel):
    """免登录用户信息模型"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    name: str = Field(..., description="用户姓名")
    avatar: str | None = Field(default=None, description="头像")


class AutoLoginTokenSchema(BaseModel):
    """免登录Token响应模型"""

    model_config = ConfigDict(from_attributes=True)

    token: str = Field(..., description="免登录Token")
    user: AutoLoginUserSchema = Field(..., description="用户信息")


class TenantOptionSchema(BaseModel):
    """租户选项（用于登录后选择租户）"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="租户ID")
    name: str = Field(..., description="租户名称")
    code: str = Field(..., description="租户编码")


class SelectTenantSchema(BaseModel):
    """选择租户请求"""

    tenant_id: int = Field(..., gt=0, description="租户ID")


class SelectTenantOutSchema(BaseModel):
    """选择租户响应"""

    model_config = ConfigDict(from_attributes=True)

    access_token: str = Field(..., description="访问token（含租户上下文）")
    token_type: str = Field(default="Bearer", description="token类型")
    expires_in: int = Field(..., gt=0, description="过期时间(秒)")


class LoginWithTenantsSchema(JWTOutSchema):
    """登录响应（含租户列表）"""

    tenants: list[TenantOptionSchema] = Field(default_factory=list, description="可选租户列表")
    user_info: dict = Field(default_factory=dict, description="用户信息")
