import type { App } from "vue";
import { createRouter, createWebHashHistory } from "vue-router";
import { ROOT_LAYOUT_ROUTE_NAME, staticRoutes } from "./routes/staticRoutes";
import { setupAfterEachGuard } from "./guards/afterEach";
import "@utils/ui";

/**
 * 路由入口：`staticRoutes` 首屏注册；业务路由由 `beforeEach` 内 `RouteRegistry` 动态挂载。
 * `initRouter` 注册前置/后置守卫并 `app.use(router)`。
 *
 * 选择 Hash 模式（createWebHashHistory）而非 History 模式的原因：
 * - 纯静态部署场景下无需服务端 URL 回落配置（NGINX try_files 等）
 * - 兼容 Electron 等非 HTTP 协议环境
 * - 开发环境 HMR 不受影响
 */
export const router = createRouter({
  history: createWebHashHistory(),
  routes: staticRoutes,
  scrollBehavior: () => ({ left: 0, top: 0 }),
});

export async function initRouter(app: App<Element>): Promise<void> {
  const { setupBeforeEachGuard } = await import("./guards/beforeEach");
  setupBeforeEachGuard(router);
  setupAfterEachGuard(router);
  app.use(router);
}

/** 应用首页入口；原 `/home` 路径已移除，由工作台承接首页内容 */
export const HOME_PAGE_PATH = "/dashboard/workplace";

export { ROOT_LAYOUT_ROUTE_NAME };

/** 动态路由注册与菜单转换（一般从 `@/router` 按需导入） */
export {
  RouteRegistry,
  ComponentLoader,
  RouteTransformer,
  RouteValidator,
  RoutePermissionValidator,
  IframeRouteManager,
} from "./core";
export type { ValidationResult } from "./core";
export { MenuProcessor, builtinFrontendRoutes } from "./core/MenuProcessor";

/** 路由别名枚举 */
export { RoutesAlias } from "./routesAlias";
