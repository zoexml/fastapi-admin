/**
 * useDict - 字典数据获取 Hook
 *
 * 提供轻量级字典数据获取能力，带内存缓存，避免重复请求。
 * 与 dict.store.ts 配合使用，按需加载指定类型的字典数据。
 *
 * ## 使用示例
 *
 * ```typescript
 * const { dict, loading } = useDict('sys_user_sex', 'sys_normal_disable')
 *
 * // 模板中使用
 * <el-option
 *   v-for="item in dict.sys_user_sex"
 *   :key="item.dict_value"
 *   :label="item.dict_label"
 *   :value="item.dict_value"
 * />
 * ```
 *
 * @module useDict
 * @author FastapiAdmin Team
 */

import { reactive, ref, onMounted } from "vue";
import DictAPI, { type DictDataTable } from "@/api/module_system/dict";

const cache = new Map<string, DictDataTable[]>();

export function useDict(...types: string[]) {
  const dict = reactive<Record<string, DictDataTable[]>>({});
  const loading = ref(false);

  onMounted(async () => {
    loading.value = true;
    try {
      await Promise.all(
        types.map(async (type) => {
          if (!cache.has(type)) {
            const response = await DictAPI.getInitDict(type);
            cache.set(type, (response.data.data as DictDataTable[]) || []);
          }
          dict[type] = cache.get(type) || [];
        })
      );
    } finally {
      loading.value = false;
    }
  });

  return { dict, loading };
}

/**
 * 清除字典内存缓存（用于系统配置变更后刷新）
 */
export function clearDictCache() {
  cache.clear();
}
