from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.module_system.auth.schema import AuthSchema
from app.api.v1.module_system.operationlog.crud import OperationLogCRUD
from app.api.v1.module_system.operationlog.schema import (
    OperationLogCreateSchema,
    OperationLogDetailOutSchema,
    OperationLogOutSchema,
)
from app.core.logger import log


class OperationLogService:
    @staticmethod
    async def create_service(auth: AuthSchema, data: OperationLogCreateSchema) -> OperationLogDetailOutSchema:
        crud = OperationLogCRUD(auth)
        obj = await crud.create(data.model_dump())
        return OperationLogDetailOutSchema.model_validate(obj)

    @staticmethod
    async def page_service(
        auth: AuthSchema,
        page: int,
        page_size: int,
        search: dict | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        crud = OperationLogCRUD(auth)
        
        # 构建过滤条件
        filters = {}
        if search:
            if search.get("request_path"):
                filters["request_path"] = search["request_path"]
            if search.get("request_method"):
                filters["request_method"] = search["request_method"]
            if search.get("username"):
                filters["username"] = search["username"]

        result = await crud.page(
            offset=(page - 1) * page_size,
            limit=page_size,
            order_by=order_by or [{"id": "desc"}],
            search=filters,
            out_schema=OperationLogOutSchema,
        )
        return result

    @staticmethod
    async def detail_service(auth: AuthSchema, id: int) -> OperationLogDetailOutSchema:
        crud = OperationLogCRUD(auth)
        obj = await crud.get(id=id)
        return OperationLogDetailOutSchema.model_validate(obj)

    @staticmethod
    async def delete_service(auth: AuthSchema, ids: list[int]) -> None:
        crud = OperationLogCRUD(auth)
        await crud.delete(ids)
        log.info(f"删除操作日志成功, ids={ids}")
