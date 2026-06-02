from typing import Annotated

from fastapi import APIRouter, Depends, Path

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.response import ResponseSchema
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import BatchDelete
from app.core.dependencies import AuthPermission, get_current_user

from .schema import (
    LoginLogCreateSchema,
    LoginLogDetailOutSchema,
    LoginLogQueryParam,
)
from .service import LoginLogService

LoginLogRouter = APIRouter(prefix="/loginlog", tags=["登录日志"])


@LoginLogRouter.get(
    "/detail/{id}",
    summary="获取登录日志详情",
    description="根据ID获取登录日志详情",
    response_model=ResponseSchema[LoginLogDetailOutSchema],
    dependencies=[Depends(AuthPermission("module_platform:login_log:query"))],
)
async def detail(
    *,
    id: Annotated[int, Path(gt=0)],
    auth: AuthSchema = Depends(get_current_user),
):
    return await LoginLogService.detail_service(auth, id)


@LoginLogRouter.get(
    "/list",
    summary="获取登录日志列表",
    description="分页获取登录日志列表",
    response_model=ResponseSchema[dict],
    dependencies=[Depends(AuthPermission("module_platform:login_log:query"))],
)
async def list(
    *,
    page: Annotated[PaginationQueryParam, Depends()],
    search: LoginLogQueryParam,
    auth: AuthSchema = Depends(get_current_user),
):
    return await LoginLogService.page_service(
        auth,
        page.page,
        page.page_size,
        search.to_dict(),
        [{"id": page.order_by}],
    )


@LoginLogRouter.post(
    "/create",
    summary="创建登录日志",
    description="创建登录日志（由系统自动调用）",
    response_model=ResponseSchema[LoginLogDetailOutSchema],
)
async def create(
    *,
    data: LoginLogCreateSchema,
    auth: AuthSchema = Depends(get_current_user),
):
    return await LoginLogService.create_service(auth, data)


@LoginLogRouter.delete(
    "/delete",
    summary="删除登录日志",
    description="批量删除登录日志",
    response_model=ResponseSchema,
    dependencies=[Depends(AuthPermission("module_platform:login_log:delete"))],
)
async def delete(
    *,
    data: BatchDelete,
    auth: AuthSchema = Depends(get_current_user),
):
    await LoginLogService.delete_service(auth, data.ids)
    return ResponseSchema()
