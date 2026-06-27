<script setup lang="ts">
/**
 * dict-tag - 字典标签展示组件
 *
 * 根据字典值在选项列表中查找匹配的项，并以标签形式展示。
 * 支持通过 list_class 设置标签颜色类型。
 * 通常配合 useDict hook 使用。
 */
import { computed } from "vue";
import { ElTag } from "element-plus";
import type { DictDataTable } from "@/api/module_system/dict";

const props = defineProps<{
  /** 字典选项列表 */
  options: DictDataTable[];
  /** 要展示的字典值 */
  value?: string | number;
}>();

const item = computed(() =>
  props.options.find((option) => String(option.dict_value) === String(props.value))
);

/** 将 list_class 映射为 ElTag 的 type 属性 */
const tagType = computed(() => {
  const listClass = item.value?.list_class ?? "";
  const validTypes = ["success", "info", "warning", "danger"] as const;
  return validTypes.includes(listClass as (typeof validTypes)[number])
    ? (listClass as (typeof validTypes)[number])
    : undefined;
});
</script>

<template>
  <ElTag v-if="item" :type="tagType" size="small">
    {{ item.dict_label }}
  </ElTag>
  <span v-else>{{ value }}</span>
</template>
