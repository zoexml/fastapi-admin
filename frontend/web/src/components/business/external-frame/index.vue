<script setup lang="ts">
/**
 * external-frame - 外部页面 iframe 嵌入组件
 *
 * 用于在系统内部嵌入第三方外部页面，如文档、监控面板等。
 */

defineProps<{
  /** 外部页面 URL */
  url: string;
}>();
</script>

<template>
  <div class="box-border w-full h-full">
    <iframe
      :src="url"
      frameborder="0"
      class="w-full h-full min-h-[calc(100vh-120px)] border-none"
    ></iframe>
  </div>
</template>
