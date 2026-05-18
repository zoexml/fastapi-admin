<template>
  <div class="dashboard-container">
    <FaGithubCorner class="github-corner" />
    <!-- 卡片组件演示区 ← workplace -->
    <ElRow :gutter="20">
      <ElCol :xs="24" class="mb-5">
        <!-- 问候 + 外链 -->
        <ElCard shadow="hover">
          <div class="flex flex-wrap items-center gap-y-3">
            <div class="flex min-w-0 flex-1 items-center">
              <div class="size-20 shrink-0 rounded-full bg-g-100 flex items-center justify-center">
                <ElAvatar
                  v-if="userStore.basicInfo.avatar"
                  size="large"
                  :src="userStore.basicInfo.avatar"
                  class="workplace-hero__avatar"
                />
                <ElIcon v-else :size="40" class="text-g-600"><UserFilled /></ElIcon>
              </div>
              <div>
                <div class="workplace-hero__greeting">
                  {{ timefix }}{{ currentUser.name }}，{{ welcome }}
                </div>
                <ElText class="workplace-hero__meta">
                  <p class="text-sm text-g-600">
                    {{ currentUser.username }} · {{ currentUser.dept_name }} ·
                    {{ currentUser.description }}
                  </p>
                </ElText>
              </div>
            </div>
            <div class="hidden shrink-0 sm:block">
              <div class="flex items-center space-x-6">
                <div class="flex flex-col items-center">
                  <div class="flex items-center text-sm font-bold text-[#4080ff]">
                    <ElIcon class="mr-0.5"><Document /></ElIcon>
                    文档
                  </div>
                  <div class="mt-3 whitespace-nowrap">
                    <ElLink
                      href="https://blog.csdn.net/weixin_46768253/article/details/149569141"
                      target="_blank"
                    >
                      <FaSvgIcon :icon="resolveIconForFaSvgIcon('csdn')" class="text-lg" />
                    </ElLink>
                  </div>
                </div>
                <div class="flex flex-col items-center">
                  <div class="flex items-center text-sm font-bold text-[#ff9a2e]">
                    <ElIcon class="mr-0.5"><Folder /></ElIcon>
                    仓库
                  </div>
                  <div class="mt-3 whitespace-nowrap">
                    <ElLink href="https://gitee.com/fastapiadmin/FastapiAdmin" target="_blank">
                      <FaSvgIcon
                        :icon="resolveIconForFaSvgIcon('gitee')"
                        class="text-lg text-[#F76560]"
                      />
                    </ElLink>
                    <ElDivider direction="vertical" />
                    <ElLink href="https://github.com/fastapiadmin/FastapiAdmin" target="_blank">
                      <FaSvgIcon
                        :icon="resolveIconForFaSvgIcon('github')"
                        class="text-lg text-[#4080FF]"
                      />
                    </ElLink>
                    <ElDivider direction="vertical" />
                    <ElLink href="https://gitcode.com/qq_36002987/FastapiAdmin" target="_blank">
                      <FaSvgIcon
                        :icon="resolveIconForFaSvgIcon('gitcode')"
                        class="text-lg text-[#FF9A2E]"
                      />
                    </ElLink>
                  </div>
                </div>
              </div>
            </div>
            <div class="w-full sm:hidden">
              <div class="flex justify-end space-x-4 overflow-x-auto">
                <ElLink href="https://gitee.com/fastapiadmin/FastapiAdmin" target="_blank">
                  <FaSvgIcon :icon="resolveIconForFaSvgIcon('gitee')" class="text-lg text-[#F76560]" />
                </ElLink>
                <ElDivider direction="vertical" />
                <ElLink href="https://github.com/fastapiadmin/FastapiAdmin" target="_blank">
                  <FaSvgIcon :icon="resolveIconForFaSvgIcon('github')" class="text-lg text-[#4080FF]" />
                </ElLink>
                <ElDivider direction="vertical" />
                <ElLink href="https://gitcode.com/qq_36002987/FastapiAdmin" target="_blank">
                  <FaSvgIcon
                    :icon="resolveIconForFaSvgIcon('gitcode')"
                    class="text-lg text-[#FF9A2E]"
                  />
                </ElLink>
              </div>
            </div>
          </div>
        </ElCard>
      </ElCol>
      <ElCol :xs="24" :sm="12" :md="12" class="mb-5">
        <FaBasicBanner
          title="数据中心运行状态"
          subtitle="系统访问量同比增长 23%，所有服务运行稳定，数据监控正常。"
        />
      </ElCol>
      <ElCol :xs="24" :sm="12" :md="12" class="mb-5">
        <FaBasicBanner
          title="欢迎使用 Fastapi Admin"
          subtitle="基于 Vue 3 + TypeScript + Element Plus 构建的现代化管理系统。"
          titleColor="#333"
          subtitleColor="#666"
          boxStyle="bg-[#D4F1F7]!"
          :buttonConfig="{
            show: true,
            text: '开始探索',
            color: 'var(--fa-success)',
            textColor: '#fff',
            radius: '6px',
          }"
          @buttonClick="handleBannerDemoClick"
        />
      </ElCol>
      <ElCol :xs="24" class="mb-5">
        <!-- CardList 概览统计（含在线用户/UV/PV/访问量等） -->
        <CardList />
      </ElCol>
      <ElCol :xs="24" :sm="12" :md="12" class="mb-5">
        <AboutProject />
      </ElCol>
      <ElCol :xs="24" :sm="12" :md="12" class="mb-5">
        <ElCard shadow="hover" class="flex flex-col h-full">
          <template #header>
            <div class="workplace-bookmarks-card__header">
              <div>
                <span class="workplace-panel-title workplace-bookmarks-card__title-line">
                  <ElIcon class="workplace-bookmarks-card__star" :size="18"><Star /></ElIcon>
                  我的收藏
                  <p class="workplace-section-sub workplace-section-sub--inline">
                    最多 {{ QUICK_LINK_MAX }} 个 · 标签栏星标添加 · 仅本机
                  </p>
                  <ElTag
                    v-if="quickLinks.length > 0"
                    type="info"
                    size="small"
                    effect="plain"
                    round
                    class="workplace-bookmarks-card__count"
                  >
                    {{ quickLinks.length }}/{{ QUICK_LINK_MAX }}
                  </ElTag>
                </span>
              </div>
              <div class="workplace-bookmarks-card__header-actions">
                <ElTooltip content="在顶部标签栏左侧星标上点击，可加入或取消收藏" placement="top">
                  <ElIcon class="workplace-module-bookmarks__help" :size="15">
                    <QuestionFilled />
                  </ElIcon>
                </ElTooltip>
                <ElButton size="small" type="danger" plain @click="clearBookmarks()">
                  <ElIcon><Delete /></ElIcon>
                  {{ t("common.clear") }}
                </ElButton>
              </div>
            </div>
          </template>
          <ElRow v-if="quickLinks.length > 0" :gutter="12">
            <ElCol
              v-for="(item, index) in quickLinks"
              :key="item.id || `${item.href}-${index}`"
              :xs="24"
              :sm="12"
              :md="8"
              :lg="8"
              :xl="8"
              class="mb-3"
            >
              <ElTooltip
                placement="top"
                :show-after="400"
                :content="item.title"
              >
                <div
                  class="workplace-quick-row workplace-quick-row--compact workplace-quick-row--chip"
                  role="button"
                  tabindex="0"
                  @click="handleQuickLinkClick(item)"
                  @keydown.enter.prevent="handleQuickLinkClick(item)"
                  @keydown.space.prevent="handleQuickLinkClick(item)"
                >
                  <span
                    class="workplace-quick-row__accent"
                    :style="{ backgroundColor: getQuickLinkColor(getQuickLinkStableIndex(item)) }"
                  />
                  <div
                    class="workplace-quick-row__icon"
                    :style="{ color: getQuickLinkColor(getQuickLinkStableIndex(item)) }"
                  >
                    <FaMenuRouteIcon :icon="item.icon || 'menu'" />
                  </div>
                  <div class="workplace-quick-row__text">
                    <span class="workplace-quick-row__title">{{ item.title }}</span>
                  </div>
                  <div class="workplace-quick-row__actions">
                    <button
                      type="button"
                      class="workplace-quick-row__remove"
                      :disabled="!item.id && !item.href"
                      :title="item.id || item.href ? '移除收藏' : '无法移除（缺少路径）'"
                      :aria-label="`移除收藏 ${item.title}`"
                      @click.stop="handleDeleteLink(item)"
                    >
                      <ElIcon><Close /></ElIcon>
                    </button>
                  </div>
                </div>
              </ElTooltip>
            </ElCol>
          </ElRow>
          <ElEmpty v-else :image-size="100">
            <template #description>
              <p class="workplace-quick-empty__title">暂无收藏</p>
              <p class="workplace-quick-empty__hint">
                在顶部
                <strong>标签栏</strong>
                左侧星标点击添加
              </p>
            </template>
          </ElEmpty>
        </ElCard>
      </ElCol>
      <ElCol :xs="24" :sm="12" :md="12" class="mb-5">
        <ElCard shadow="hover" class="workplace-surface workplace-ops-card flex flex-col h-full">
          <template #header>
            <div class="workplace-section-card__head">
              <div>
                <span class="workplace-panel-title">日程日历</span>
                <p class="workplace-section-sub workplace-section-sub--inline">
                  点击日期添加或编辑（本地演示）
                </p>
              </div>
            </div>
          </template>
          <div class="workplace-ops-card__body">
            <FaCalendar />
          </div>
        </ElCard>
      </ElCol>
      <ElCol :xs="24" :sm="12" :md="12" class="mb-5">
        <ElCard shadow="hover" class="h-full flex flex-col">
          <template #header>
            <div class="flex items-center justify-between">
              <span class="font-medium">最新动态</span>
              <ElLink
                type="primary"
                underline="never"
                href="https://gitee.com/fastapiadmin/FastapiAdmin/releases"
                target="_blank"
              >
                完整记录
                <ElIcon class="link-icon"><TopRight /></ElIcon>
              </ElLink>
            </div>
          </template>
          <ElScrollbar class="h-full">
            <ElTimeline class="p-2">
              <ElTimelineItem
                v-for="(item, index) in vesionList"
                :key="index"
                :timestamp="item.date"
                placement="top"
                :color="index === 0 ? '#67C23A' : '#909399'"
                :hollow="index !== 0"
              >
                <div class="version-item" :class="{ 'latest-item': index === 0 }">
                  <div class="flex items-center justify-between">
                    <ElText tag="strong">{{ item.title }}</ElText>
                    <ElTag v-if="item.tag" :type="index === 0 ? 'success' : 'info'" size="small">
                      {{ item.tag }}
                    </ElTag>
                  </div>
                  <ElText class="version-content">{{ item.content }}</ElText>
                  <div v-if="item.link">
                    <ElLink
                      :type="index === 0 ? 'primary' : 'info'"
                      :href="item.link"
                      target="_blank"
                      underline="never"
                    >
                      详情
                      <ElIcon class="link-icon"><TopRight /></ElIcon>
                    </ElLink>
                  </div>
                </div>
              </ElTimelineItem>
            </ElTimeline>
          </ElScrollbar>
        </ElCard>
      </ElCol>
      <ElCol
        v-for="card in statsCards"
        :key="`t-${card.id}`"
        :xs="24"
        :sm="12"
        :md="6"
        class="mb-5"
      >
        <FaStatsCard
          :icon="card.icon"
          :iconStyle="card.iconStyle"
          :title="card.title"
          :description="card.description"
          :showArrow="card.showArrow"
        />
      </ElCol>
      <ElCol
        v-for="card in statsCards"
        :key="`n-${card.id}`"
        :xs="24"
        :sm="12"
        :md="6"
        class="mb-5"
      >
        <FaStatsCard
          :icon="card.icon"
          :iconStyle="card.iconStyle"
          :title="card.title"
          :description="card.description"
          :count="card.count"
          :decimals="0"
          :showArrow="card.showArrow"
          separator=","
        />
      </ElCol>
      <ElCol
        v-for="card in statsCards"
        :key="`c-${card.id}`"
        :xs="24"
        :sm="12"
        :md="6"
        class="mb-5"
      >
        <FaStatsCard
          :icon="card.icon"
          :iconStyle="card.customIconStyle"
          :boxStyle="card.boxStyle"
          :title="card.title"
          :description="card.description"
          :textColor="card.textColor"
          :showArrow="card.showArrow"
        />
      </ElCol>
      <ElCol
        v-for="card in progressCards"
        :key="`p-${card.id}`"
        :xs="24"
        :sm="12"
        :md="6"
        class="mb-5"
      >
        <FaProgressCard :percentage="card.percentage" :title="card.title" :color="card.color" />
      </ElCol>
      <ElCol
        v-for="card in progressCards"
        :key="`pi-${card.id}`"
        :xs="24"
        :sm="12"
        :md="6"
        class="mb-5"
      >
        <FaProgressCard
          :percentage="card.percentage"
          :title="card.title"
          :color="card.color"
          :icon="card.icon"
          :iconStyle="card.iconStyle"
        />
      </ElCol>
      <ElCol :xs="24" :sm="12" :md="6" class="mb-5">
        <FaLineChartCard
          :isMiniChart="true"
          :value="2545"
          label="新用户"
          date="过去7天"
          :percentage="1.2"
          :height="9.5"
          :chartData="[120, 132, 101, 134, 90, 230, 210]"
        />
      </ElCol>
      <ElCol :xs="24" :sm="12" :md="6" class="mb-5">
        <FaBarChartCard
          :isMiniChart="true"
          :value="15480"
          label="浏览量"
          date="过去14天"
          :percentage="-4.15"
          :height="9.5"
          barWidth="45%"
          :chartData="[120, 100, 150, 140, 90, 120, 130]"
        />
      </ElCol>
      <ElCol :xs="24" :sm="12" :md="6" class="mb-5">
        <FaLineChartCard
          :isMiniChart="true"
          :value="2545"
          label="粉丝数"
          date="过去30天"
          :percentage="1.2"
          :height="9.5"
          :showAreaColor="true"
          :chartData="[150, 180, 160, 200, 180, 220, 240]"
        />
      </ElCol>
      <ElCol :xs="24" :sm="12" :md="6" class="mb-5">
        <FaDonutChartCard
          :value="36358"
          title="粉丝量"
          :percentage="18"
          percentageLabel="较去年"
          :data="[50, 40]"
          :height="9.5"
          currentValue="2022"
          previousValue="2021"
          :radius="['50%', '70%']"
        />
      </ElCol>
      <ElCol :xs="24" :sm="12" :md="6" class="mb-5">
        <FaLineChartCard
          :value="2545"
          label="新用户"
          :percentage="1.2"
          :height="11"
          :chartData="[120, 132, 101, 134, 90, 230, 210]"
        />
      </ElCol>
      <ElCol :xs="24" :sm="12" :md="6" class="mb-5">
        <FaBarChartCard
          :value="15480"
          label="浏览量"
          :percentage="-4.15"
          :height="11"
          :chartData="[120, 100, 150, 140, 90, 120, 130, 110]"
        />
      </ElCol>
      <ElCol :xs="24" :sm="12" :md="6" class="mb-5">
        <FaLineChartCard
          :value="2545"
          label="粉丝数"
          :percentage="1.2"
          :height="11"
          :showAreaColor="true"
          :chartData="[150, 180, 160, 200, 180, 220, 240]"
        />
      </ElCol>
      <ElCol :xs="24" :sm="12" :md="6" class="mb-5">
        <FaDonutChartCard
          :value="36358"
          title="粉丝量"
          :percentage="-18"
          percentageLabel="较2021年"
          :data="[70, 30]"
          :height="11"
          currentValue="12月"
          previousValue="11月"
        />
      </ElCol>
      <ElCol :xs="24" :sm="12" :lg="8" class="mb-5">
        <FaDataListCard :list="dataList" title="待办事项" subtitle="今日待处理任务" />
      </ElCol>
      <ElCol :xs="24" :sm="12" :lg="8" class="mb-5">
        <FaDataListCard
          :maxCount="4"
          :list="dataList"
          title="最近活动"
          subtitle="近期活动列表"
          :showMoreButton="true"
          @more="handleMore"
        />
      </ElCol>
      <ElCol :xs="24" :sm="12" :lg="8" class="mb-5">
        <FaTimelineListCard :list="timelineData" title="最近交易" subtitle="2024年12月20日" />
      </ElCol>
      <ElCol v-for="card in imageCards" :key="card.id" :xs="24" :sm="12" :md="6" class="mb-5">
        <FaImageCard
          :imageUrl="card.imageUrl"
          :title="card.title"
          :category="card.category"
          :readTime="card.readTime"
          :views="card.views"
          :comments="card.comments"
          :date="card.date"
          @click="handleImageCardClick(card)"
        />
      </ElCol>
      <ElCol :xs="24" :sm="12" :md="12" :lg="6" class="mb-5">
        <FaCardBanner
          title="系统运行正常"
          description="所有核心服务运行稳定，响应时间在正常范围内。"
        />
      </ElCol>
      <ElCol :xs="24" :sm="12" :md="12" :lg="6" class="mb-5">
        <FaCardBanner
          :image="bannerIcon2"
          title="重要消息通知"
          description="您有 3 条待处理的重要消息，请及时查看。"
          :button="{
            show: true,
            text: '查看详情',
            color: 'var(--fa-warning)',
            textColor: '#fff',
          }"
        />
      </ElCol>
      <ElCol :xs="24" :sm="12" :md="12" :lg="6" class="mb-5">
        <FaCardBanner
          :image="bannerIcon3"
          title="数据分析报告"
          description="本周业务数据分析报告已完成，请查看关键指标。"
          :button="{
            show: true,
            text: '下载报告',
            color: 'var(--fa-error)',
            textColor: '#fff',
          }"
        />
      </ElCol>
      <ElCol :xs="24" :sm="12" :md="12" :lg="6" class="mb-5">
        <FaCardBanner
          :image="bannerIcon4"
          title="版本更新提醒"
          description="Art Design Pro v2.1.0 已发布，包含性能优化和新功能。"
          :button="{
            show: true,
            text: '立即更新',
            color: 'var(--theme-color)',
            textColor: '#fff',
          }"
          :cancelButton="{ show: true, text: '稍后提醒', color: '#eee', textColor: '#333' }"
          @click="handleBannerDemoConfirm"
          @cancel="handleBannerDemoCancel"
        />
      </ElCol>
    </ElRow>
  </div>
</template>

<script setup lang="ts">
defineOptions({ name: "Home", inheritAttrs: false });

import { useUserStore } from "@stores";
import CardList from "../workplace/modules/card-list.vue";
import AboutProject from "../workplace/modules/about-project.vue";
import {
  greetings,
  resolveIconForFaSvgIcon,
  quickStartManager,
  QUICK_LINK_MAX,
  type QuickLink,
} from "@utils";
import { ref, onMounted, onUnmounted } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import {
  Delete,
  UserFilled,
  Close,
  Star,
  QuestionFilled,
  Document,
  Folder,
  TopRight,
} from "@element-plus/icons-vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { dayjs } from "element-plus";
import bannerIcon2 from "@imgs/3d/icon2.webp";
import bannerIcon3 from "@imgs/3d/icon3.webp";
import bannerIcon4 from "@imgs/3d/icon4.webp";
import cover1 from "@imgs/cover/img1.webp";
import cover2 from "@imgs/cover/img2.webp";
import cover3 from "@imgs/cover/img3.webp";
import cover4 from "@imgs/cover/img4.webp";
import FaCardBanner from "@/components/banners/fa-card-banner/index.vue";
import FaDonutChartCard from "@/components/cards/fa-donut-chart-card/index.vue";
import FaImageCard from "@/components/cards/fa-image-card/index.vue";
import FaDataListCard from "@/components/cards/fa-data-list-card/index.vue";
import FaLineChartCard from "@/components/cards/fa-line-chart-card/index.vue";
import FaStatsCard from "@/components/cards/fa-stats-card/index.vue";
import FaProgressCard from "@/components/cards/fa-progress-card/index.vue";
import FaBarChartCard from "@/components/cards/fa-bar-chart-card/index.vue";
import FaTimelineListCard from "@/components/cards/fa-timeline-list-card/index.vue";
import FaBasicBanner from "@/components/banners/fa-basic-banner/index.vue";

const timefix = greetings();
const userStore = useUserStore();
const { t } = useI18n();
const router = useRouter();
const welcome = "祝你开心每一天！";

interface VersionItem {
  id: string;
  title: string;
  date: string;
  content: string;
  link: string;
  tag?: string;
}
const vesionList = ref<VersionItem[]>([
  {
    id: "1",
    title: "v3.2.1",
    date: dayjs().format("YYYY-MM-DD HH:mm:ss"),
    content: "优化性能，修复若干小bug。",
    link: "https://gitee.com/fastapiadmin/FastapiAdmin/releases",
    tag: "更新",
  },
  {
    id: "2",
    title: "v3.2.0",
    date: dayjs().subtract(1, "day").format("YYYY-MM-DD HH:mm:ss"),
    content: "新增用户行为分析功能。",
    link: "https://gitee.com/fastapiadmin/FastapiAdmin/releases",
    tag: "新功能",
  },
  {
    id: "3",
    title: "v3.1.0",
    date: dayjs().subtract(3, "day").format("YYYY-MM-DD HH:mm:ss"),
    content: "优化权限管理系统。",
    link: "https://gitee.com/fastapiadmin/FastapiAdmin/releases",
    tag: "优化",
  },
]);

const currentUser = {
  avatar:
    userStore.basicInfo.avatar ||
    "https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png",
  name: userStore.basicInfo.name || "吴彦祖",
  username: userStore.basicInfo.username || "账号信息",
  description: userStore.basicInfo.description || "用户说明",
  dept_name: userStore.basicInfo.dept_name || "软件专业部",
  last_login: userStore.basicInfo.last_login || "2023-01-01 00:00:00",
};

const quickLinks = ref<QuickLink[]>(quickStartManager.getQuickLinks());
const handleQuickLinkClick = (item: QuickLink) => {
  if (item.href) {
    router.push(item.href).catch(() => {
      ElMessage.warning(`路由 ${item.href} 不存在，请检查配置`);
    });
  } else {
    ElMessage.info(`${item.title} 功能待开发`);
  }
};
const QUICK_LINK_PALETTE = ["#4080ff", "#23c343", "#ff9a2e", "#f76560", "#a9aeb8", "#00b42a"];
const getQuickLinkColor = (index: number) => QUICK_LINK_PALETTE[index % QUICK_LINK_PALETTE.length];
const getQuickLinkStableIndex = (item: QuickLink): number => {
  const i = quickLinks.value.findIndex((l) =>
    l.id != null && l.id !== "" ? l.id === item.id : l.href === item.href
  );
  return i >= 0 ? i : 0;
};
const handleDeleteLink = async (item: QuickLink) => {
  try {
    await ElMessageBox.confirm(`确定要取消收藏"${item.title}"吗？`, "取消收藏确认", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });
    if (item.id) quickStartManager.removeQuickLink(item.id);
    else if (item.href) quickStartManager.removeQuickLinkByHref(item.href);
    else {
      ElMessage.warning("无法移除：缺少标识");
      return;
    }
    ElMessage.success(`已取消收藏：${item.title}`);
  } catch {
    /* 用户取消 */
  }
};
const clearBookmarks = async () => {
  try {
    await ElMessageBox.confirm("确定要清空收藏吗？", "清空收藏确认", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });
    quickStartManager.clearQuickLinks();
    ElMessage.success("已清空收藏");
  } catch {
    /* 用户取消 */
  }
};
const updateQuickLinks = (links: QuickLink[]) => {
  quickLinks.value = links;
};

// === 横幅组件演示 ===
function handleBannerDemoClick() {
  console.log("banner clicked");
}
function handleBannerDemoConfirm() {
  console.log("confirm clicked");
}
function handleBannerDemoCancel() {
  console.log("cancel clicked");
}
// === 卡片演示数据 ← workplace ===
const statsCards = [
  {
    id: 1,
    title: "销售产品",
    count: 1235,
    description: "鞋子、牛仔裤、派对服装、手表",
    icon: "ri:bar-chart-box-line",
    boxStyle: "bg-theme/10!",
    customIconStyle: "text-theme! text-3xl!",
    iconStyle: "bg-info",
    textColor: "var(--theme-color)",
    showArrow: false,
  },
  {
    id: 2,
    title: "活跃用户",
    count: 5000,
    description: "日活跃用户超过5,000+",
    icon: "ri:account-box-2-line",
    boxStyle: "bg-warning/10!",
    customIconStyle: "text-warning! text-3xl!",
    iconStyle: "bg-warning",
    textColor: "var(--fa-warning)",
    showArrow: false,
  },
  {
    id: 3,
    title: "总收入",
    count: 35000,
    description: "月收入超过¥350,000+",
    icon: "ri:money-cny-box-line",
    boxStyle: "bg-secondary/10!",
    customIconStyle: "text-secondary! text-3xl!",
    iconStyle: "bg-secondary",
    textColor: "var(--fa-secondary)",
    showArrow: false,
  },
  {
    id: 4,
    title: "客户评价",
    count: 4800,
    description: "平均评分4.8/5",
    icon: "ri:message-3-line",
    boxStyle: "bg-error/10!",
    customIconStyle: "text-error! text-3xl!",
    iconStyle: "bg-error",
    textColor: "var(--fa-error)",
    showArrow: false,
  },
];
const progressCards = [
  {
    id: 1,
    title: "完成进度",
    percentage: 75,
    color: "var(--fa-success)",
    icon: "ri:arrow-up-circle-line",
    iconStyle: "bg-success/12 text-success",
  },
  {
    id: 2,
    title: "项目进度",
    percentage: 65,
    color: "var(--theme-color)",
    icon: "ri:twitch-line",
    iconStyle: "bg-theme/12 text-theme",
  },
  {
    id: 3,
    title: "学习进度",
    percentage: 45,
    color: "var(--fa-error)",
    icon: "ri:game-line",
    iconStyle: "bg-error/12! text-error",
  },
  {
    id: 4,
    title: "任务进度",
    percentage: 90,
    color: "var(--fa-secondary)",
    icon: "ri:flag-2-line",
    iconStyle: "bg-secondary/12 text-secondary",
  },
];
const imageCards = [
  {
    id: 1,
    imageUrl: cover1,
    title: "AI技术在医疗领域的创新应用与发展前景",
    category: "社交",
    readTime: "2分钟",
    views: 9125,
    comments: 3,
    date: "12月19日 周一",
  },
  {
    id: 2,
    imageUrl: cover2,
    title: "大数据分析助力企业决策的实践案例",
    category: "技术",
    readTime: "3分钟",
    views: 7234,
    comments: 5,
    date: "12月20日 周二",
  },
  {
    id: 3,
    imageUrl: cover3,
    title: "区块链技术在供应链管理中的应用",
    category: "科技",
    readTime: "4分钟",
    views: 5678,
    comments: 8,
    date: "12月21日 周三",
  },
  {
    id: 4,
    imageUrl: cover4,
    title: "云计算技术发展趋势与未来展望",
    category: "云技术",
    readTime: "5分钟",
    views: 4321,
    comments: 6,
    date: "12月22日 周四",
  },
];
const dataList = [
  {
    title: "新加坡之行",
    status: "进行中",
    time: "5分钟",
    class: "bg-theme/12 text-theme",
    icon: "ri:camera-4-line",
  },
  {
    title: "归档数据",
    status: "进行中",
    time: "10分钟",
    class: "bg-secondary/12 text-secondary",
    icon: "ri:bar-chart-box-line",
  },
  {
    title: "客户会议",
    status: "待处理",
    time: "15分钟",
    class: "bg-warning/12 text-warning",
    icon: "ri:user-3-line",
  },
  {
    title: "筛选任务团队",
    status: "进行中",
    time: "20分钟",
    class: "bg-error/12 text-error",
    icon: "ri:account-circle-line",
  },
  {
    title: "发送信封给小王",
    status: "已完成",
    time: "20分钟",
    class: "bg-success/12 text-success",
    icon: "ri:message-3-line",
  },
];
const timelineData = [
  {
    time: "上午 09:30",
    status: "rgb(73, 190, 255)",
    content: "收到 John Doe 支付的 385.90 美元",
  },
  { time: "上午 10:00", status: "rgb(54, 158, 255)", content: "新销售记录", code: "ML-3467" },
  { time: "上午 12:00", status: "rgb(103, 232, 207)", content: "向 Michael 支付了 64.95 美元" },
  { time: "下午 14:30", status: "rgb(255, 193, 7)", content: "系统维护通知", code: "MT-2023" },
  {
    time: "下午 15:45",
    status: "rgb(255, 105, 105)",
    content: "紧急订单取消提醒",
    code: "OR-9876",
  },
  { time: "下午 17:00", status: "rgb(103, 232, 207)", content: "完成每日销售报表" },
];

function handleMore() {
  ElMessage.info("查看更多");
}
function handleImageCardClick(card: (typeof imageCards)[0]) {
  console.log("点击卡片:", card);
}
onMounted(() => {
  quickStartManager.addListener(updateQuickLinks);
});
onUnmounted(() => {
  quickStartManager.removeListener(updateQuickLinks);
});
</script>

<style scoped lang="scss">
:deep(.el-card) {
  --el-card-border-radius: calc(var(--custom-radius) + 2px);

  border: 1px solid var(--fa-card-border);
}

.dashboard-container {
  position: relative;
  display: flex;
  flex-direction: column;

  > * {
    margin-bottom: 16px;
  }

  > :last-child {
    margin-bottom: 0;
  }

  &::after {
    display: block;
    flex-shrink: 0;
    height: 16px;
    content: "";
  }
}

.github-corner {
  position: absolute;
  top: 0;
  right: 0;
  z-index: 1;
  border: 0;
}

.version-item {
  padding: 10px 12px;
  background: var(--el-fill-color-lighter);
  border-radius: 8px;
  transition: all 0.2s;

  &.latest-item {
    background: var(--el-color-primary-light-9);
    border: 1px solid var(--el-color-primary-light-5);
  }

  &:hover {
    transform: translateX(5px);
  }

  .version-content {
    display: block;
    margin-top: 6px;
    margin-bottom: 8px;
    font-size: 13px;
    line-height: 1.4;
    color: var(--el-text-color-secondary);
  }
}

.workplace-section-sub {
  margin: 4px 0 0;
  font-size: 12px;
  font-weight: normal;
  line-height: 1.45;
  color: var(--el-text-color-secondary);
}

.workplace-section-sub--inline {
  margin: 2px 0 0;
}

.workplace-surface {
  overflow: hidden;
  border: 1px solid var(--el-border-color-lighter);
  border-radius: 12px;

  :deep(.el-card__header) {
    border-bottom-color: var(--el-border-color-extra-light);
  }
}

.workplace-ops-card__body--calendar {
  max-height: min(300px, 36vh);
  overflow: auto;
}

.workplace-panel-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  letter-spacing: 0.02em;
}

.workplace-hero__avatar {
  border: 2px solid var(--el-bg-color);
}

.workplace-hero__greeting {
  margin-bottom: 6px;
  font-size: 20px;
  font-weight: 700;
  line-height: 1.3;
  color: var(--el-text-color-primary);
}

.workplace-hero__meta {
  font-size: 13px;
  line-height: 1.5;
  color: var(--el-text-color-secondary);
}

.workplace-bookmarks-card__header {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 12px;
  align-items: flex-start;
  justify-content: space-between;
}

.workplace-bookmarks-card__title-line {
  display: inline-flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.workplace-bookmarks-card__star {
  flex-shrink: 0;
  color: var(--el-color-warning);
}

.workplace-bookmarks-card__count {
  height: 22px;
  font-variant-numeric: tabular-nums;
}

.workplace-bookmarks-card__header-actions {
  display: flex;
  flex-shrink: 0;
  gap: 8px;
  align-items: center;
}

.workplace-module-bookmarks__help {
  flex-shrink: 0;
  color: var(--el-text-color-secondary);
  cursor: help;
}

.workplace-quick-row--compact {
  min-height: 44px;
  padding: 6px 8px 6px 4px;
}

.workplace-quick-row {
  position: relative;
  display: flex;
  gap: 10px;
  align-items: center;
  min-height: 56px;
  padding: 8px 10px 8px 6px;
  cursor: pointer;
  outline: none;
  background: var(--el-fill-color-blank);
  border: 1px solid var(--el-border-color-lighter);
  border-radius: var(--el-border-radius-base);
  transition:
    border-color 0.2s,
    box-shadow 0.2s,
    background 0.2s;

  &:hover {
    background: var(--el-bg-color);
    border-color: var(--el-color-primary-light-5);
    box-shadow: var(--el-box-shadow-light);
  }

  &:focus-visible {
    border-color: var(--el-color-primary);
    box-shadow: 0 0 0 2px var(--el-color-primary-light-7);
  }
}

.workplace-quick-row__accent {
  flex-shrink: 0;
  align-self: stretch;
  width: 3px;
  min-height: 36px;
  border-radius: 2px;
}

.workplace-quick-row__icon {
  display: flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  font-size: 22px;
  line-height: 1;
  background: var(--el-color-primary-light-9);
  border-radius: 10px;
}

.workplace-quick-row__text {
  flex: 1;
  min-width: 0;
}

.workplace-quick-row__title {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 13px;
  font-weight: 600;
  line-height: 1.35;
  color: var(--el-text-color-primary);
  white-space: nowrap;
}

.workplace-quick-row__actions {
  display: flex;
  flex-shrink: 0;
  gap: 2px;
  align-items: center;
}

.workplace-quick-row__remove {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  padding: 0;
  color: var(--el-text-color-secondary);
  cursor: pointer;
  background: transparent;
  border: 1px solid transparent;
  border-radius: 8px;
  transition:
    color 0.2s,
    background 0.2s,
    border-color 0.2s,
    opacity 0.2s;

  .workplace-quick-row--chip & {
    width: 26px;
    height: 26px;
  }

  &:disabled {
    cursor: not-allowed;
    opacity: 0.35;
  }

  &:hover:not(:disabled) {
    color: var(--el-color-danger);
    background: var(--el-color-danger-light-9);
    border-color: var(--el-color-danger-light-7);
  }
}

.workplace-quick-empty__title {
  margin: 0 0 8px;
  font-size: 14px;
  color: var(--el-text-color-regular);
}

.workplace-quick-empty__hint {
  margin: 0;
  font-size: 13px;
  line-height: 1.55;
  color: var(--el-text-color-secondary);
}

.workplace-section-card__head {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: flex-start;
  justify-content: space-between;
  width: 100%;
}
</style>
