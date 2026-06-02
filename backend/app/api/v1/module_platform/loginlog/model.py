from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class LoginLogModel(ModelMixin, UserMixin):
    """
    登录日志模型
    """

    __tablename__: str = "platform_login_log"
    __table_args__: dict[str, str] = {"comment": "登录日志表"}

    status: Mapped[int] = mapped_column(Integer, default=1, comment="登录状态(1成功 2失败)")
    login_location: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="登录位置")
    login_ip: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="登录IP地址")
    request_os: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="操作系统")
    request_browser: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="浏览器")
    msg: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="提示消息")
