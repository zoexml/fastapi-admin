/**
 * RoutePermissionValidator - 路由权限校验器
 *
 * 从 guards/beforeEach 中提取的独立权限校验模块，
 * 提供扁平菜单路径匹配、动态路由正则匹配、路径前缀检查等能力。
 *
 * @module RoutePermissionValidator
 * @author FastapiAdmin Team
 */

import type { AppRouteRecord } from "@/types/router";

export class RoutePermissionValidator {
  static hasPermission(targetPath: string, menuList: AppRouteRecord[]): boolean {
    if (targetPath === "/") {
      return true;
    }
    return this.matchRoute(targetPath, menuList);
  }

  static buildMenuPathSet(
    menuList: AppRouteRecord[],
    pathSet: Set<string> = new Set()
  ): Set<string> {
    if (!Array.isArray(menuList) || menuList.length === 0) {
      return pathSet;
    }

    for (const menuItem of menuList) {
      if (!menuItem.path) {
        continue;
      }

      const menuPath = menuItem.path.startsWith("/") ? menuItem.path : `/${menuItem.path}`;
      pathSet.add(menuPath);

      if (menuItem.children?.length) {
        this.buildMenuPathSet(menuItem.children, pathSet);
      }
    }

    return pathSet;
  }

  static checkPathPrefix(targetPath: string, pathSet: Set<string>): boolean {
    for (const menuPath of pathSet) {
      if (targetPath.startsWith(`${menuPath}/`)) {
        return true;
      }
    }
    return false;
  }

  static matchRoute(targetPath: string, routes: AppRouteRecord[]): boolean {
    if (!Array.isArray(routes) || routes.length === 0) {
      return false;
    }

    for (const route of routes) {
      if (!route.path) {
        continue;
      }

      const routePath = route.path.startsWith("/") ? route.path : `/${route.path}`;

      if (
        routePath === targetPath ||
        this.isDynamicRouteMatch(targetPath, routePath) ||
        targetPath.startsWith(`${routePath}/`)
      ) {
        return true;
      }

      if (route.children?.length && this.matchRoute(targetPath, route.children)) {
        return true;
      }
    }

    return false;
  }

  static isDynamicRouteMatch(targetPath: string, routePath: string): boolean {
    if (!routePath.includes(":")) {
      return false;
    }

    const pattern = routePath
      .replace(/[.*+?^${}()|[\]\\]/g, "\\$&")
      .replace(/:([^/]+)/g, "[^/]+")
      .replace(/\\\*/g, ".*");

    return new RegExp(`^${pattern}$`).test(targetPath);
  }

  static validatePath(
    targetPath: string,
    menuList: AppRouteRecord[],
    homePath: string = "/"
  ): { path: string; hasPermission: boolean } {
    const hasPermission = this.hasPermission(targetPath, menuList);

    if (hasPermission) {
      return { path: targetPath, hasPermission: true };
    }

    return { path: homePath, hasPermission: false };
  }
}
