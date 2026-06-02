import sqlalchemy as sa
from sqlalchemy import func, select

from app.api.v1.module_platform.tenant.model import TenantModel
from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException
from app.core.logger import log

from .crud import PackageCRUD
from .model import PackageMenuModel, PackageModel
from .schema import (
    PackageCreateSchema,
    PackageMenuSetSchema,
    PackageOutSchema,
    PackageQueryParam,
    PackageUpdateSchema,
)


class PackageService:
    """套餐模块服务层"""

    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        obj = await PackageCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="套餐不存在")
        return PackageOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: PackageQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        return await PackageCRUD(auth).page_crud(
            offset=(page_no - 1) * page_size,
            limit=page_size,
            order_by=order_by or [{"sort": "asc"}, {"id": "asc"}],
            search=search.__dict__ if search else {},
            out_schema=PackageOutSchema,
        )

    @classmethod
    async def create_service(cls, auth: AuthSchema, data: PackageCreateSchema) -> dict:
        if await PackageCRUD(auth).get(name=data.name):
            raise CustomException(msg="创建失败，套餐名称已存在")
        if await PackageCRUD(auth).get(code=data.code):
            raise CustomException(msg="创建失败，套餐编码已存在")

        obj = await PackageCRUD(auth).create_crud(data=data)
        if not obj:
            raise CustomException(msg="创建套餐失败")
        result = PackageOutSchema.model_validate(obj).model_dump()
        log.info(f"创建套餐成功: {result.get('name')}")
        return result

    @classmethod
    async def update_service(
        cls, auth: AuthSchema, id: int, data: PackageUpdateSchema
    ) -> dict:
        obj = await PackageCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="套餐不存在")

        if data.name is not None:
            exist = await PackageCRUD(auth).get(name=data.name)
            if exist and exist.id != id:
                raise CustomException(msg="更新失败，名称重复")
        if data.code is not None:
            exist = await PackageCRUD(auth).get(code=data.code)
            if exist and exist.id != id:
                raise CustomException(msg="更新失败，编码重复")

        updated = await PackageCRUD(auth).update_crud(id=id, data=data)
        if not updated:
            raise CustomException(msg="更新失败")
        return PackageOutSchema.model_validate(updated).model_dump()

    @classmethod
    async def delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        if not ids:
            raise CustomException(msg="删除失败，删除对象不能为空")

        for pid in ids:
            stmt = select(func.count()).select_from(TenantModel).where(TenantModel.package_id == pid)
            result = await auth.db.execute(stmt)
            count = result.scalar()
            if count and count > 0:
                raise CustomException(msg=f"套餐 ID={pid} 已被 {count} 个租户使用，无法删除")

        await PackageCRUD(auth).delete_crud(ids=ids)

    @classmethod
    async def get_menus_service(cls, auth: AuthSchema, package_id: int) -> list[int]:
        """获取套餐菜单权限（返回 menu_id 列表）"""
        stmt = select(PackageMenuModel.menu_id).where(PackageMenuModel.package_id == package_id)
        result = await auth.db.execute(stmt)
        return [row[0] for row in result.all()]

    @classmethod
    async def set_menus_service(
        cls, auth: AuthSchema, package_id: int, data: PackageMenuSetSchema
    ) -> None:
        """批量设置套餐菜单权限（先清空再写入）"""
        await auth.db.execute(sa.delete(PackageMenuModel).where(PackageMenuModel.package_id == package_id))
        for menu_id in data.menu_ids:
            auth.db.add(PackageMenuModel(package_id=package_id, menu_id=menu_id))
        await auth.db.flush()
        log.info(f"套餐[{package_id}]菜单权限已设置, count={len(data.menu_ids)}")

    @staticmethod
    async def get_package_menu_ids(auth: AuthSchema, package_id: int) -> list[int]:
        """获取套餐包含的菜单ID列表"""
        stmt = select(PackageMenuModel.menu_id).where(PackageMenuModel.package_id == package_id)
        result = await auth.db.execute(stmt)
        return [row[0] for row in result.all()]

    @staticmethod
    async def get_tenant_available_menu_ids(auth: AuthSchema, tenant_id: int) -> list[int]:
        """获取租户的完整可用菜单ID列表（套餐菜单 + 自定义授权菜单）"""
        from app.api.v1.module_platform.tenant.model import TenantMenuModel, TenantModel

        stmt = select(TenantModel).where(TenantModel.id == tenant_id).limit(1)
        result = await auth.db.execute(stmt)
        tenant = result.scalar_one_or_none()
        if not tenant:
            return []

        all_menu_ids: set[int] = set()

        if tenant.package_id:
            pkg_stmt = select(PackageModel.status).where(PackageModel.id == tenant.package_id).limit(1)
            pkg_result = await auth.db.execute(pkg_stmt)
            pkg_status = pkg_result.scalar_one_or_none()
            if pkg_status == "0":
                stmt = select(PackageMenuModel.menu_id).where(PackageMenuModel.package_id == tenant.package_id)
                result = await auth.db.execute(stmt)
                for row in result.all():
                    all_menu_ids.add(row[0])

        stmt = select(TenantMenuModel.menu_id).where(TenantMenuModel.tenant_id == tenant_id)
        result = await auth.db.execute(stmt)
        for row in result.all():
            all_menu_ids.add(row[0])

        return list(all_menu_ids)
