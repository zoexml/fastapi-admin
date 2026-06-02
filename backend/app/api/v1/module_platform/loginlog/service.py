from app.api.v1.module_system.auth.schema import AuthSchema
from app.api.v1.module_platform.loginlog.crud import LoginLogCRUD
from app.api.v1.module_platform.loginlog.schema import (
    LoginLogCreateSchema,
    LoginLogDetailOutSchema,
    LoginLogOutSchema,
)
from app.core.logger import log


class LoginLogService:
    @staticmethod
    async def create_service(auth: AuthSchema, data: LoginLogCreateSchema) -> LoginLogDetailOutSchema:
        crud = LoginLogCRUD(auth)
        obj = await crud.create(data.model_dump())
        return LoginLogDetailOutSchema.model_validate(obj)

    @staticmethod
    async def page_service(
        auth: AuthSchema,
        page: int,
        page_size: int,
        search: dict | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        crud = LoginLogCRUD(auth)
        
        # 构建过滤条件
        filters = {}
        if search:
            if search.get("status"):
                filters["status"] = search["status"]
            if search.get("username"):
                filters["username"] = search["username"]

        result = await crud.page(
            offset=(page - 1) * page_size,
            limit=page_size,
            order_by=order_by or [{"id": "desc"}],
            search=filters,
            out_schema=LoginLogOutSchema,
        )
        return result

    @staticmethod
    async def detail_service(auth: AuthSchema, id: int) -> LoginLogDetailOutSchema:
        crud = LoginLogCRUD(auth)
        obj = await crud.get(id=id)
        return LoginLogDetailOutSchema.model_validate(obj)

    @staticmethod
    async def delete_service(auth: AuthSchema, ids: list[int]) -> None:
        crud = LoginLogCRUD(auth)
        await crud.delete(ids)
        log.info(f"删除登录日志成功, ids={ids}")
