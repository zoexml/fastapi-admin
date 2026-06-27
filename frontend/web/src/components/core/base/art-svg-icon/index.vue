<!-- 兼容 artpro-ui 调用约定的 svg-icon 组件（薄壳，复用主项目 FaSvgIcon） -->
<template>
  <FaSvgIcon v-if="icon" :icon="localIcon" v-bind="$attrs" class="art-svg-icon inline" />
</template>

<script setup lang="ts">
  import FaSvgIcon from "@/components/base/fa-svg-icon/index.vue"

  defineOptions({ name: "ArtSvgIcon", inheritAttrs: false })

  interface Props {
    /** Iconify icon name */
    icon?: string
  }

  const props = defineProps<Props>()

  // 主项目 FaSvgIcon 已通过 useIconify() 注册 ri/svg-spinners/line-md 集合，
  // 离线图标前缀可直接传入；不识别的图标交由 iconify 默认行为（CDN 兜底）
  const localIcon = computed(() => props.icon || "")
</script>
