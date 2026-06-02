from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path
from fastapi.responses import JSONResponse

from app.api.v1.module_system.auth.schema import AuthSchema
from app.common.response import ResponseSchema, SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.base_schema import BatchDelete, BatchSetAvailable
from app.core.dependencies import AuthPermission
from app.core.logger import log
from app.core.router_class import OperationLogRoute

from .schema import (
    PackageCreateSchema,
    PackageMenuSetSchema,
    PackageOutSchema,
    PackageQueryParam,
    PackageUpdateSchema,
)
from .service import PackageService

PackageRouter = APIRouter(route_class=OperationLogRoute, prefix="/package", tags=["套餐管理"])


@PackageRouter.get(
    "/detail/{id}",
    summary="获取套餐详情",
    description="根据套餐ID获取套餐详情",
    response_model=ResponseSchema[PackageOutSchema],
)
async def get_obj_detail_controller(
    id: Annotated[int, Path(description="套餐ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_package:package:query"]))],
) -> JSONResponse:
    result_dict = await PackageService.detail_service(auth=auth, id=id)
    log.info(f"获取套餐详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取套餐详情成功")


@PackageRouter.get(
    "/list",
    summary="获取套餐列表",
    description="分页获取套餐列表",
    response_model=ResponseSchema[dict],
)
async def get_obj_list_controller(
    page: Annotated[PaginationQueryParam, Depends()],
    search: Annotated[PackageQueryParam, Depends()],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_package:package:query"]))],
) -> JSONResponse:
    result_dict = await PackageService.page_service(
        auth=auth,
        page_no=page.page_no,
        page_size=page.page_size,
        search=search,
        order_by=page.order_by,
    )
    return SuccessResponse(data=result_dict, msg="查询成功")


@PackageRouter.post(
    "/create",
    summary="创建套餐",
    description="创建新的租户套餐",
    response_model=ResponseSchema[PackageOutSchema],
)
async def create_obj_controller(
    data: Annotated[PackageCreateSchema, Body(description="套餐信息")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_package:package:create"]))],
) -> JSONResponse:
    result_dict = await PackageService.create_service(auth=auth, data=data)
    log.info(f"创建套餐成功 {result_dict.get('name')}")
    return SuccessResponse(data=result_dict, msg="创建成功")


@PackageRouter.put(
    "/update/{id}",
    summary="更新套餐",
    description="更新套餐信息",
    response_model=ResponseSchema[PackageOutSchema],
)
async def update_obj_controller(
    id: Annotated[int, Path(description="套餐ID")],
    data: Annotated[PackageUpdateSchema, Body(description="套餐信息")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_package:package:update"]))],
) -> JSONResponse:
    result_dict = await PackageService.update_service(auth=auth, id=id, data=data)
    log.info(f"更新套餐成功 {id}")
    return SuccessResponse(data=result_dict, msg="更新成功")


@PackageRouter.delete(
    "/delete",
    summary="删除套餐",
    description="批量删除套餐（已被租户使用的套餐无法删除）",
    response_model=ResponseSchema,
)
async def delete_obj_controller(
    data: Annotated[BatchDelete, Body(description="删除信息")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_package:package:delete"]))],
) -> JSONResponse:
    await PackageService.delete_service(auth=auth, ids=data.ids)
    log.info(f"删除套餐成功 {data.ids}")
    return SuccessResponse(msg="删除成功")


@PackageRouter.patch(
    "/status/batch",
    summary="批量修改状态",
    description="批量启用/禁用套餐",
    response_model=ResponseSchema,
)
async def set_available_controller(
    data: Annotated[BatchSetAvailable, Body(description="状态设置")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_package:package:update"]))],
) -> JSONResponse:
    for id in data.ids:
        await PackageService.update_service(auth=auth, id=id, data=PackageUpdateSchema(status=data.status))
    log.info(f"套餐状态设置成功 {data.ids}")
    return SuccessResponse(msg="状态设置成功")


@PackageRouter.get(
    "/menus/{package_id}",
    summary="获取套餐菜单",
    description="获取套餐包含的菜单ID列表",
    response_model=ResponseSchema[list[int]],
)
async def get_menus_controller(
    package_id: Annotated[int, Path(description="套餐ID")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_package:package:query"]))],
) -> JSONResponse:
    result = await PackageService.get_menus_service(auth=auth, package_id=package_id)
    return SuccessResponse(data=result, msg="获取成功")


@PackageRouter.post(
    "/menus/{package_id}/set",
    summary="设置套餐菜单",
    description="批量设置套餐包含的菜单（先清空再写入）",
    response_model=ResponseSchema,
)
async def set_menus_controller(
    package_id: Annotated[int, Path(description="套餐ID")],
    data: Annotated[PackageMenuSetSchema, Body(description="菜单列表")],
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_package:package:update"]))],
) -> JSONResponse:
    await PackageService.set_menus_service(auth=auth, package_id=package_id, data=data)
    log.info(f"套餐[{package_id}]菜单权限已设置, count={len(data.menu_ids)}")
    return SuccessResponse(msg="设置成功")
