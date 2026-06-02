from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_crud import CRUDBase

from .model import LoginLogModel


class LoginLogCRUD(CRUDBase[LoginLogModel, None, None]):
    """登录日志 CRUD"""

    def __init__(self, auth: AuthSchema):
        super().__init__(LoginLogModel, auth)
