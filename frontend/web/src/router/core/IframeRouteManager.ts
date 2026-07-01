/**
 * IframeRouteManager - iframe 路由注册表
 *
 * 管理所有 iframe 类型路由的注册、查询、持久化。
 * 与动态路由、守卫共用，确保 iframe 页面正确加载。
 *
 * @module IframeRouteManager
 * @author FastapiAdmin Team
 */

import type { AppRouteRecord } from "@/types/router";

export class IframeRouteManager {
  private static instance: IframeRouteManager;
  private iframeRoutes: AppRouteRecord[] = [];

  private constructor() {}

  static getInstance(): IframeRouteManager {
    if (!IframeRouteManager.instance) {
      IframeRouteManager.instance = new IframeRouteManager();
    }
    return IframeRouteManager.instance;
  }

  add(route: AppRouteRecord): void {
    if (!this.iframeRoutes.find((r) => r.path === route.path)) {
      this.iframeRoutes.push(route);
    }
  }

  getAll(): AppRouteRecord[] {
    return this.iframeRoutes;
  }

  findByPath(path: string): AppRouteRecord | undefined {
    return this.iframeRoutes.find((route) => route.path === path);
  }

  clear(): void {
    this.iframeRoutes = [];
  }

  save(): void {
    if (this.iframeRoutes.length > 0) {
      sessionStorage.setItem("iframeRoutes", JSON.stringify(this.iframeRoutes));
    }
  }

  load(): void {
    try {
      const data = sessionStorage.getItem("iframeRoutes");
      if (data) {
        this.iframeRoutes = JSON.parse(data);
      }
    } catch (error) {
      console.error("[IframeRouteManager] 加载 iframe 路由失败:", error);
      this.iframeRoutes = [];
    }
  }
}
