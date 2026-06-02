"""
系统级模块 - module_system

租户内部管理功能，受租户隔离限制：
- 认证授权 (auth)
- 用户管理 (user)
- 角色管理 (role)
- 部门管理 (dept)
- 菜单管理 (menu)
- 岗位管理 (position)
- 字典管理 (dict)
- 公告管理 (notice)
- 参数管理 (params)
- 操作日志 (operationlog)
"""
from fastapi import APIRouter

system_router = APIRouter(prefix="/system", tags=["系统管理"])
_routers_included = False


def _include_routers():
    """延迟导入路由以避免循环导入"""
    global _routers_included
    if _routers_included:
        return
    
    from app.api.v1.module_system.auth.controller import AuthRouter
    from app.api.v1.module_system.dept.controller import DeptRouter
    from app.api.v1.module_system.dict.controller import DictRouter
    from app.api.v1.module_system.menu.controller import MenuRouter
    from app.api.v1.module_system.notice.controller import NoticeRouter
    from app.api.v1.module_system.operationlog.controller import OperationLogRouter
    from app.api.v1.module_system.params.controller import ParamsRouter
    from app.api.v1.module_system.position.controller import PositionRouter
    from app.api.v1.module_system.role.controller import RoleRouter
    from app.api.v1.module_system.user.controller import UserRouter

    system_router.include_router(AuthRouter)
    system_router.include_router(DeptRouter)
    system_router.include_router(DictRouter)
    system_router.include_router(OperationLogRouter)
    system_router.include_router(MenuRouter)
    system_router.include_router(NoticeRouter)
    system_router.include_router(ParamsRouter)
    system_router.include_router(PositionRouter)
    system_router.include_router(RoleRouter)
    system_router.include_router(UserRouter)
    _routers_included = True


# 提供一个属性访问器，在首次访问时才加载路由
class _SystemRouter(APIRouter):
    def __getattr__(self, name):
        _include_routers()
        return getattr(system_router, name)


# 使用包装类延迟路由加载
system_router = _SystemRouter(prefix="/system", tags=["系统管理"])

# 保持向后兼容性，直接暴露 include_router 方法
system_router.include_router = lambda router: _include_routers() or system_router.include_router(router)
