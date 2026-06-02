from typing import Annotated

from fastapi import APIRouter, Depends, Path

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.response import ResponseSchema
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import BatchDelete
from app.core.dependencies import AuthPermission, get_current_user

from .schema import (
    OperationLogCreateSchema,
    OperationLogDetailOutSchema,
    OperationLogQueryParam,
)
from .service import OperationLogService

OperationLogRouter = APIRouter(prefix="/operationlog", tags=["操作日志"])


@OperationLogRouter.get(
    "/detail/{id}",
    summary="获取操作日志详情",
    description="根据ID获取操作日志详情",
    response_model=ResponseSchema[OperationLogDetailOutSchema],
    dependencies=[Depends(AuthPermission("module_system:operation_log:query"))],
)
async def detail(
    *,
    id: Annotated[int, Path(gt=0)],
    auth: AuthSchema = Depends(get_current_user),
):
    return await OperationLogService.detail_service(auth, id)


@OperationLogRouter.get(
    "/list",
    summary="获取操作日志列表",
    description="分页获取操作日志列表",
    response_model=ResponseSchema[dict],
    dependencies=[Depends(AuthPermission("module_system:operation_log:query"))],
)
async def list(
    *,
    page: Annotated[PaginationQueryParam, Depends()],
    search: OperationLogQueryParam,
    auth: AuthSchema = Depends(get_current_user),
):
    return await OperationLogService.page_service(
        auth,
        page.page,
        page.page_size,
        search.to_dict(),
        [{"id": page.order_by}],
    )


@OperationLogRouter.post(
    "/create",
    summary="创建操作日志",
    description="创建操作日志（由系统自动调用）",
    response_model=ResponseSchema[OperationLogDetailOutSchema],
)
async def create(
    *,
    data: OperationLogCreateSchema,
    auth: AuthSchema = Depends(get_current_user),
):
    return await OperationLogService.create_service(auth, data)


@OperationLogRouter.delete(
    "/delete",
    summary="删除操作日志",
    description="批量删除操作日志",
    response_model=ResponseSchema,
    dependencies=[Depends(AuthPermission("module_system:operation_log:delete"))],
)
async def delete(
    *,
    data: BatchDelete,
    auth: AuthSchema = Depends(get_current_user),
):
    await OperationLogService.delete_service(auth, data.ids)
    return ResponseSchema()
