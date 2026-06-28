<template>
  <div class="fa-page-segmented" :class="{ 'fa-page-segmented--with-top-margin': withTopMargin }">
    <ElSegmented
      v-model="model"
      :disabled="disabled"
      :options="options"
      :size="size"
      @change="handleChange"
    />
  </div>
</template>

<script setup lang="ts">
defineOptions({ name: "FaPageSegmented", inheritAttrs: false });

type PageSegmentedValue = string | number;

export type PageSegmentedOption =
  | PageSegmentedValue
  | {
      label: string | number;
      value: PageSegmentedValue;
      disabled?: boolean;
    };

withDefaults(
  defineProps<{
    options: PageSegmentedOption[];
    size?: "large" | "default" | "small";
    disabled?: boolean;
    withTopMargin?: boolean;
  }>(),
  {
    size: "default",
    disabled: false,
    withTopMargin: false,
  }
);

const model = defineModel<PageSegmentedValue>({ required: true });
const emit = defineEmits<{
  change: [value: PageSegmentedValue];
}>();

const handleChange = (value: PageSegmentedValue) => {
  emit("change", value);
};
</script>

<style scoped lang="scss">
.fa-page-segmented {
  display: flex;
  width: 100%;
  max-width: 100%;
  padding: 4px;
  background: var(--default-box-color);
  border: 1px solid var(--fa-card-border);
  border-radius: 8px;
  margin-bottom: 12px;

  &--with-top-margin {
    margin-top: 12px;
  }

  :deep(.el-segmented) {
    --el-segmented-item-selected-bg-color: var(--el-color-primary);
    --el-segmented-item-selected-color: #fff;
    --el-border-radius-base: 6px;

    width: fit-content;
    max-width: 100%;
    height: 32px;
    padding: 0;
    background: transparent;
  }

  :deep(.el-segmented__item) {
    min-width: 116px;
    height: 32px;
    padding: 0 14px;
    font-size: 13px;
    color: var(--fa-gray-800);
  }

  :deep(.el-segmented__item-selected) {
    box-shadow: 0 4px 12px color-mix(in srgb, var(--el-color-primary) 24%, transparent);
  }
}
</style>
