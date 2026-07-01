/**
 * RoutesAlias - 路由别名枚举
 *
 * 存放系统级公共路由路径，用类型化常量替代魔法字符串，
 * 提高代码可维护性并支持类型提示。
 *
 * @module RoutesAlias
 * @author FastapiAdmin Team
 */

export enum RoutesAlias {
  /** 主框架布局容器 */
  Layout = '/index/index',
  /** 登录页 */
  Login = '/auth/login',
  /** 首页/工作台 */
  Home = '/dashboard/workplace',
  /** 数据分析页 */
  Analysis = '/dashboard/analysis',
  /** 数据大屏 */
  Screen = '/dashboard/screen',
}
