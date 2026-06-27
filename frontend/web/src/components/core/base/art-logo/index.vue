<!-- 兼容 artpro-ui 调用约定的 logo 组件（薄壳，复用主项目 FaLogo） -->
<template>
  <FaLogo :size="size" />
</template>

<script setup lang="ts">
  import FaLogo from "@/components/base/fa-logo/index.vue"

  defineOptions({ name: "ArtLogo" })

  interface Props {
    /** logo 大小 */
    size?: number | string
  }

  withDefaults(defineProps<Props>(), {
    size: 46
  })
</script>
