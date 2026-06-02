from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_crud import CRUDBase

from .model import PackageModel


class PackageCRUD(CRUDBase):
    """套餐模块 CRUD"""

    def __init__(self, auth: AuthSchema):
        super().__init__(PackageModel, auth)
