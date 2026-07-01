/**
 * 插件统一导出
 * 集中管理第三方库的封装和配置
 */

export * from './echarts'

import type { App } from 'vue'
import { initGlobDirectives } from '@/directives'
import { initI18n } from '@/locales'
import { initRouter } from '@/router'
import { initStore } from '@stores'
import { initErrorHandle } from '@utils'
import { initCodeMirror } from './codemirror'
import { initElementPlus } from './element-plus'
import { initElIcons } from './icons'
import { initIconify } from './iconify'
import { initTerminal } from './terminal'

/**
 * 插件注册入口 —— 调用顺序依赖说明：
 *
 * 1. initElIcons    图标注册（纯组件，无依赖，最先执行）
 * 2. initStore      Pinia 状态管理（路由守卫、指令、组件均依赖 store，须在 router 之前）
 * 3. initRouter     Vue Router（守卫中用到已初始化的 store）
 * 4. initGlobDirectives  全局指令（v-auth、v-highlight 等，依赖 router 的 meta 权限）
 * 5. initErrorHandle     全局错误处理（window.onerror、unhandledrejection）
 * 6. initTerminal        终端/控制台相关
 * 7. initI18n            国际化（依赖 Element Plus 部分类型，但 Element Plus 尚未注册，先注册语言包）
 * 8. initCodeMirror      CodeMirror 编辑器（独立注册，无依赖）
 * 9. initElementPlus     最后注册 Element Plus，避免组件扫描过早触发（样式和组件完整注册）
 */
export async function initPlugins(app: App<Element>): Promise<void> {
  initElIcons(app)
  initIconify()
  initStore(app)
  await initRouter(app)
  initGlobDirectives(app)
  initErrorHandle(app)
  initTerminal(app)
  initI18n(app)
  initCodeMirror(app)
  initElementPlus(app)
}
