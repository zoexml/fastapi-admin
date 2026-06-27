<template>
  <FBadge :type="badgeType" :text="String(label)" />
</template>

<script setup lang="ts">
import { computed } from "vue";

defineOptions({ name: "FaStatusTag" });

interface Props {
  /** 显示文本 */
  label?: string | number;
  /**
   * 标签类型（与 EP ElTag 一致）。
   * 不传时为 EP 默认样式（无 type 属性）。
   */
  type?: "primary" | "success" | "warning" | "danger" | "error" | "info";
  /** 尺寸 */
  size?: "large" | "default" | "small";
  /** 主题效果：light（默认）/ dark / plain */
  effect?: "light" | "dark" | "plain";
  /** 是否圆角 */
  round?: boolean;
  /** 是否可关闭 */
  closable?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  label: "",
  type: undefined,
  size: "default",
  effect: "light",
  round: false,
  closable: false,
});

/**
 * ElTag type "danger" → FBadge type "error"
 * 其余类型直接透传，undefined 按 FBadge 默认 "primary" 处理。
 */
const badgeType = computed(() => {
  if (props.type === "danger") return "error" as const;
  return (props.type as "primary" | "success" | "warning" | "info" | "error") ?? "primary";
});
</script>
