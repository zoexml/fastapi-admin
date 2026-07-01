/**
 * 站点配置工具（兼容 artpro-ui 中 `getSiteConfig` 调用约定）。
 *
 * - 实际配置项由后端 `/api/v1/system/param/info` 返回（`useConfigStore` 拉取），
 *   后端键如 `demo_enable` / `ip_white_list` 等，未包含 `site.login.title` 这种「文案的键」。
 * - 因此对 `site.*` 这种纯展示类文案提供默认 fallback（同步 `i18n`），便于登录页等场景直接调用。
 * - 真实键（如 `name`）走 `useConfigStore().configData`，与 `useSiteConfig` 共享。
 */
import AppConfig from "@/config";
import { useConfigStore } from "@stores";
import { useI18n } from "vue-i18n";

type SiteConfigMap = Record<string, string>;

/** 默认站点配置；后端没有对应 key 时使用此处兜底 */
const DEFAULT_SITE_CONFIG: SiteConfigMap = {
  "site.name": AppConfig.systemInfo.name,
  "site.description": "商业化中后台管理系统",
  "site.login.title": "login.title",
  "site.login.description": "login.subTitle",
  "site.login-left-title": "login.leftView.title",
  "site.login-left-sub-title": "login.leftView.subTitle",
  "site.watermark.content": "",
  "site.watermark.mode": "username",
  "site.watermark.show-time": "false",
};

let remoteCache: SiteConfigMap = {};

/**
 * 将后端 `configData` 映射为 `site.*` 风格键，便于兼容 artpro-ui 调用约定。
 *
 * - 后端 `name.config_value` -> `site.name`
 * - 其他字段按需补充；缺失则不写入缓存，由 `getSiteConfig` 走 fallback
 */
function mapRemoteConfig(): SiteConfigMap {
  // 通过 Pinia 拿；为兼容 SSR / 单元测试，在 store 未挂载时静默返回空
  let raw: Record<string, { config_value?: string }>;
  try {
    raw = useConfigStore().configData || {};
  } catch {
    raw = {};
  }
  const mapped: SiteConfigMap = {};
  const nameValue = raw.name?.config_value;
  if (nameValue) mapped["site.name"] = nameValue;
  const descValue = raw.description?.config_value;
  if (descValue) mapped["site.description"] = descValue;
  return mapped;
}

/**
 * 读取站点配置值（按 key，未命中时返回 fallback）
 *
 * @param key 形如 `site.login.title` 的点分键
 * @param fallback 默认值；i18n key（`login.title`）会被自动翻译
 */
export function getSiteConfig(key: string, fallback = ""): string {
  const fromRemote = remoteCache[key];
  if (fromRemote) return fromRemote;
  const fromDefault = DEFAULT_SITE_CONFIG[key];
  if (fromDefault !== undefined) {
    // i18n key 形式：默认表里存的是 i18n key（无空格、无中文）则尝试 $t 翻译
    if (isI18nKey(fromDefault)) {
      try {
        const { t } = useI18n();
        return t(fromDefault) || fallback;
      } catch {
        return fallback || fromDefault;
      }
    }
    return fromDefault;
  }
  return fallback;
}

/** 是否是 i18n key（首尾非空白，不含中文/标点，长度 < 80） */
function isI18nKey(value: string): boolean {
  if (!value) return false;
  if (/[\u4e00-\u9fa5\s，。；：、]/.test(value)) return false;
  return value.length < 80 && /^[a-zA-Z0-9._-]+$/.test(value);
}

/**
 * 加载后端配置并写入缓存（一般在 `onMounted` 中调用一次）。
 *
 * - 调用 `useConfigStore().getConfig(true)` 强制拉取
 * - 成功后将后端配置按 `mapRemoteConfig` 写入 `remoteCache`
 * - 若 useConfigStore 未挂载（极端环境），安全跳过
 */
export async function loadSiteConfig(): Promise<void> {
  try {
    const store = useConfigStore();
    await store.getConfig(true);
    remoteCache = { ...mapRemoteConfig() };
    // 同步回写到 AppConfig.systemInfo.name，便于顶部/页脚复用
    const remoteName = remoteCache["site.name"];
    if (remoteName) AppConfig.systemInfo.name = remoteName;
  } catch {
    // 静默失败，使用默认配置
  }
}
