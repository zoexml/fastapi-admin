"""
平台级模块 - module_platform

包含平台级管理功能，不受租户隔离限制：
- 租户管理 (tenant)
- 套餐管理 (package)
- 插件管理 (plugin)
- 登录日志 (loginlog)
- 工单管理 (ticket)
"""
from fastapi import APIRouter

from app.api.v1.module_platform.loginlog.controller import LoginLogRouter
from app.api.v1.module_platform.package.controller import PackageRouter
from app.api.v1.module_platform.plugin.controller import PluginRouter
from app.api.v1.module_platform.tenant.controller import TenantRouter
from app.api.v1.module_platform.ticket.controller import TicketRouter

platform_router = APIRouter(prefix="/platform", tags=["平台管理"])

platform_router.include_router(TenantRouter, prefix="/tenant")
platform_router.include_router(PackageRouter, prefix="/package")
platform_router.include_router(PluginRouter, prefix="/plugin")
platform_router.include_router(LoginLogRouter)
platform_router.include_router(TicketRouter, prefix="/ticket")
