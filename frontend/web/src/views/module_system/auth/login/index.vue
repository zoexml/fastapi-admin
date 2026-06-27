<template>
  <div class="login-page-panel flex h-screen w-full flex-col overflow-hidden">
    <FaAuthTopBar />

    <div class="login-auth-split min-h-0 flex-1" :class="`login-auth-split--${panelAlign}`">
      <div v-if="panelAlign !== 'center'" class="login-auth-split__col--illustration">
        <FaLoginLeftView />
      </div>

      <div
        class="login-auth-split__col--form relative flex min-h-0 flex-1 flex-col"
        :class="panelAlign === 'center' ? 'bg-transparent' : 'bg-(--el-bg-color-page)'"
      >
        <div
          class="login-page-panel__scroll min-h-0 flex-1 overflow-y-auto"
          :class="{ 'login-page-panel__scroll--centered': panelAlign === 'center' }"
        >
          <div class="login-panel-align-row flex min-h-full items-center justify-center px-8 py-16">
            <div class="auth-right-wrap">
              <div class="form">
                <h3 class="title">{{ panelTitle }}</h3>
                <p class="sub-title">{{ panelSubTitle }}</p>

                <FaLoginAccountForm
                  v-if="authPanel === 'login' && loginFlowMode === 'account'"
                  ref="accountFormRef"
                  v-model:login-form="loginForm"
                  v-model="isPassing"
                  v-model:is-click-pass="isClickPass"
                  :rules="rules"
                  :captcha-state="captchaState"
                  :code-loading="codeLoading"
                  :demo-account-key="demoAccountKey"
                  :accounts="accounts"
                  :form-key="formKey"
                  :is-dark="isDark"
                  :drag-verify-text-color="dragVerifyTextColor"
                  :loading="loading"
                  @submit="handleSubmit"
                  @setup-account="setupAccount"
                  @get-captcha="getCaptcha"
                  @open-mobile="openMobileLogin"
                  @open-qr="openQrLogin"
                  @forget="setAuthPanel('forget')"
                  @register="setAuthPanel('register')"
                  @oauth="handleOAuthLogin"
                />

                <FaLoginMobilePanel
                  v-else-if="authPanel === 'login' && loginFlowMode === 'mobile'"
                  ref="mobilePanelRef"
                  @back="backToAccountLogin"
                  @register="setAuthPanel('register')"
                />

                <FaLoginQrPanel
                  v-else-if="authPanel === 'login' && loginFlowMode === 'qr'"
                  @back="backToAccountLogin"
                  @register="setAuthPanel('register')"
                />

                <FaLoginRegisterPanel
                  v-else-if="authPanel === 'register'"
                  ref="registerPanelRef"
                  v-model:register-form="registerForm"
                  v-model:register-agreement-read="registerAgreementRead"
                  :register-rules="registerRules"
                  :form-key="formKey"
                  :register-loading="registerLoading"
                  :user-agreement-href="userAgreementHref"
                  show-email
                  @submit="submitRegister"
                  @to-login="setAuthPanel('login')"
                />

                <FaLoginForgetPanel
                  v-else
                  ref="forgetPanelRef"
                  v-model:forget-form="forgetForm"
                  :forget-rules="forgetRules"
                  :form-key="formKey"
                  :forget-loading="forgetLoading"
                  @submit="submitForget"
                  @to-login="setAuthPanel('login')"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia";
import { ElMessage, ElNotification, type FormRules } from "element-plus";
import { useI18n } from "vue-i18n";
import type { LocationQuery, RouteLocationRaw } from "vue-router";
import AuthAPI, {
  type CaptchaInfo,
  type LoginFormData,
  type OAuthProvider,
} from "@/api/module_system/auth";
import { UserAPI, type ForgetPasswordForm, type RegisterForm } from "@/api/module_system/user";
import { useAppStore, useConfigStore, useSettingsStore, useUserStore } from "@/store";
import { Auth, HttpError, startOAuthLogin } from "@utils";
import FaAuthTopBar from "@/components/views/fa-login/widgets/FaAuthTopBar.vue";
import FaLoginLeftView from "@/components/views/fa-login/backdrops/FaLoginLeftView.vue";
import FaLoginAccountForm from "@/components/views/fa-login/forms/FaLoginAccountForm.vue";
import FaLoginMobilePanel from "@/components/views/fa-login/panels/FaLoginMobilePanel.vue";
import FaLoginQrPanel from "@/components/views/fa-login/panels/FaLoginQrPanel.vue";
import FaLoginForgetPanel from "@/components/views/fa-login/panels/FaLoginForgetPanel.vue";
import FaLoginRegisterPanel from "@/components/views/fa-login/panels/FaLoginRegisterPanel.vue";
import { useLoginPanelAlign } from "@/components/views/fa-login/composables/useLoginPanelAlign";
import type { Account, AccountKey } from "./types";

defineOptions({ name: "Login" });

type AuthPanel = "login" | "register" | "forget";
type LoginFlowMode = "account" | "mobile" | "qr";

const appStore = useAppStore();
const configStore = useConfigStore();
const settingStore = useSettingsStore();
const userStore = useUserStore();
const router = useRouter();
const route = useRoute();
const { t, locale } = useI18n();
const { isDark } = storeToRefs(settingStore);
const { panelAlign } = useLoginPanelAlign();

const authPanel = ref<AuthPanel>("login");
const loginFlowMode = ref<LoginFlowMode>("account");
const formKey = ref(0);
const demoAccountKey = ref<AccountKey>("super");
const isPassing = ref(false);
const isClickPass = ref(false);
const loading = ref(false);
const registerLoading = ref(false);
const forgetLoading = ref(false);
const codeLoading = ref(false);
const registerAgreementRead = ref(false);

const accountFormRef = ref<InstanceType<typeof FaLoginAccountForm> | null>(null);
const mobilePanelRef = ref<InstanceType<typeof FaLoginMobilePanel> | null>(null);
const registerPanelRef = ref<InstanceType<typeof FaLoginRegisterPanel> | null>(null);
const forgetPanelRef = ref<InstanceType<typeof FaLoginForgetPanel> | null>(null);

const loginForm = reactive<LoginFormData>({
  username: "",
  password: "",
  captcha: "",
  captcha_key: "",
  remember: true,
  login_type: "PC端",
});

const registerForm = reactive<RegisterForm & { email: string }>({
  username: "",
  password: "",
  confirmPassword: "",
  email: "",
});

const forgetForm = reactive<ForgetPasswordForm>({
  username: "",
  new_password: "",
  confirmPassword: "",
});

const captchaState = reactive<CaptchaInfo>({
  enable: false,
  key: "",
  img_base: "",
});

const panelTitle = computed(() => {
  if (authPanel.value === "register") return t("login.reg");
  if (authPanel.value === "forget") return t("login.resetPassword");
  if (authPanel.value === "login" && loginFlowMode.value === "mobile") {
    return t("login.mobileLogin");
  }
  if (authPanel.value === "login" && loginFlowMode.value === "qr") {
    return t("login.qrLoginTitle");
  }
  return t("login.title");
});

const panelSubTitle = computed(() => {
  if (authPanel.value === "register") return t("register.subTitle");
  if (authPanel.value === "forget") return t("forgetPassword.subTitle");
  if (authPanel.value === "login" && loginFlowMode.value === "mobile") {
    return t("login.mobileLoginSubTitle");
  }
  if (authPanel.value === "login" && loginFlowMode.value === "qr") {
    return t("login.qrLoginSubTitle");
  }
  return t("login.subTitle");
});

const userAgreementHref = computed(() => configStore.configData?.clause?.config_value || "#");

const dragVerifyTextColor = computed(() =>
  isDark.value ? "rgba(255, 255, 255, 0.45)" : "var(--fa-gray-700)"
);

const rules = computed<FormRules>(() => {
  const base: FormRules = {
    username: [{ required: true, trigger: "blur", message: t("login.message.username.required") }],
    password: [
      { required: true, trigger: "blur", message: t("login.message.password.required") },
      { min: 6, message: t("login.message.password.min"), trigger: "blur" },
    ],
  };

  if (captchaState.enable) {
    base.captcha = [
      { required: true, trigger: "blur", message: t("login.message.captchaCode.required") },
    ];
  }

  return base;
});

const validateRegisterPassword = (_rule: unknown, value: string, callback: (e?: Error) => void) => {
  if (!value) {
    callback(new Error(t("login.message.password.required")));
    return;
  }
  if (registerForm.confirmPassword) {
    registerPanelRef.value?.validateField?.("confirmPassword");
  }
  callback();
};

const validateRegisterConfirm = (_rule: unknown, value: string, callback: (e?: Error) => void) => {
  if (!value) {
    callback(new Error(t("login.message.password.required")));
    return;
  }
  if (value !== registerForm.password) {
    callback(new Error(t("login.message.password.inconformity")));
    return;
  }
  callback();
};

const registerRules = computed<FormRules<RegisterForm & { email: string }>>(() => ({
  username: [{ required: true, message: t("login.message.username.required"), trigger: "blur" }],
  password: [
    { required: true, validator: validateRegisterPassword, trigger: "blur" },
    { min: 6, message: t("login.message.password.min"), trigger: "blur" },
  ],
  confirmPassword: [
    { required: true, message: t("login.message.password.required"), trigger: "blur" },
    { min: 6, message: t("login.message.password.min"), trigger: "blur" },
    { validator: validateRegisterConfirm, trigger: "blur" },
  ],
  email: [
    { required: true, message: t("login.message.email.required"), trigger: "blur" },
    { type: "email", message: t("login.message.email.invalid"), trigger: "blur" },
  ],
}));

const validateForgetConfirm = (_rule: unknown, value: string, callback: (e?: Error) => void) => {
  if (!value) {
    callback(new Error(t("login.message.password.required")));
    return;
  }
  if (value !== forgetForm.new_password) {
    callback(new Error(t("login.message.password.inconformity")));
    return;
  }
  callback();
};

const forgetRules = computed<FormRules<ForgetPasswordForm>>(() => ({
  username: [{ required: true, message: t("login.message.username.required"), trigger: "blur" }],
  new_password: [
    { required: true, message: t("login.message.password.required"), trigger: "blur" },
    { min: 6, message: t("login.message.password.min"), trigger: "blur" },
  ],
  confirmPassword: [
    { required: true, message: t("login.message.password.required"), trigger: "blur" },
    { min: 6, message: t("login.message.password.min"), trigger: "blur" },
    { validator: validateForgetConfirm, trigger: "blur" },
  ],
}));

const accounts = computed<Account[]>(() => [
  {
    key: "super",
    label: t("login.roles.super"),
    username: "super",
    password: "123456",
    roles: ["R_SUPER"],
  },
  {
    key: "admin",
    label: t("login.roles.admin"),
    username: "admin",
    password: "123456",
    roles: ["R_ADMIN"],
  },
  {
    key: "user",
    label: t("login.roles.user"),
    username: "user",
    password: "123456",
    roles: ["R_USER"],
  },
]);

const setAuthPanel = (panel: AuthPanel) => {
  authPanel.value = panel;
  if (panel !== "login") {
    loginFlowMode.value = "account";
  }

  nextTick(() => {
    accountFormRef.value?.clearValidate?.();
    registerPanelRef.value?.clearValidate?.();
    forgetPanelRef.value?.clearValidate?.();
  });
};

const openMobileLogin = () => {
  loginFlowMode.value = "mobile";
};

const openQrLogin = () => {
  loginFlowMode.value = "qr";
};

const backToAccountLogin = () => {
  loginFlowMode.value = "account";
  nextTick(() => {
    getCaptcha();
    loginForm.captcha = "";
    accountFormRef.value?.resetDragVerify?.();
    mobilePanelRef.value?.resetMobileLoginUi?.();
    isPassing.value = false;
    isClickPass.value = false;
  });
};

const handleOAuthLogin = (provider: OAuthProvider) => {
  startOAuthLogin(provider);
};

const setupAccount = (key: AccountKey) => {
  const selected = accounts.value.find((account) => account.key === key);
  demoAccountKey.value = key;
  loginForm.username = selected?.username ?? "";
  loginForm.password = selected?.password ?? "";
};

const getCaptcha = async () => {
  try {
    codeLoading.value = true;
    const response = await AuthAPI.getCaptcha();
    const data = response.data.data;
    loginForm.captcha_key = data.key;
    captchaState.img_base = data.img_base;
    captchaState.enable = data.enable;
  } catch {
    captchaState.enable = false;
    loginForm.captcha = "";
    loginForm.captcha_key = "";
  } finally {
    codeLoading.value = false;
  }
};

const resolveRedirectTarget = (query: LocationQuery): RouteLocationRaw => {
  const defaultPath = "/";
  const rawRedirect = (query.redirect as string) || defaultPath;
  try {
    const resolved = router.resolve(rawRedirect);
    return {
      path: resolved.path,
      query: resolved.query,
    };
  } catch {
    return { path: defaultPath };
  }
};

const tryConsumeOAuthCallback = async () => {
  const q = route.query;
  const oauthError = q.oauth_error as string | undefined;
  const access = q.access_token as string | undefined;
  const refresh = q.refresh_token as string | undefined;

  if (!oauthError && !(access && refresh)) return;

  const rest: Record<string, unknown> = { ...q };
  delete rest.oauth_error;
  delete rest.access_token;
  delete rest.refresh_token;
  delete rest.token_type;

  if (oauthError) {
    ElMessage.error(decodeURIComponent(oauthError));
    await router.replace({ path: route.path, query: rest as LocationQuery });
    return;
  }

  if (access && refresh) {
    try {
      Auth.setTokens(access, refresh, true);
      userStore.setToken(access, refresh);
      userStore.setLoginStatus(true);
      ElNotification({
        title: t("login.oauthNoticeTitle"),
        message: t("login.oauthLoginSuccess"),
        type: "success",
      });
      await router.replace(resolveRedirectTarget(rest as LocationQuery));
    } catch (error) {
      console.error("[Login] OAuth callback:", error);
      ElMessage.error(t("login.oauthLoginFailed"));
      await router.replace({ path: route.path, query: rest as LocationQuery });
    }
  }
};

const handleSubmit = async () => {
  if (!accountFormRef.value) return;

  try {
    const valid = await accountFormRef.value.validate?.();
    if (!valid) return;

    if (!isPassing.value) {
      isClickPass.value = true;
      return;
    }

    loading.value = true;
    await userStore.login(loginForm);
    await router.replace(resolveRedirectTarget(route.query));

    if (settingStore.showGuide) {
      appStore.showGuide(true);
    }
  } catch (error) {
    await getCaptcha();
    if (!(error instanceof HttpError)) {
      console.error("[Login] Unexpected error:", error);
      ElNotification({
        title: "提示",
        message: error instanceof Error ? error.message : String(error),
        type: "error",
      });
    }
  } finally {
    loading.value = false;
    accountFormRef.value?.resetDragVerify?.();
  }
};

const submitRegister = async () => {
  if (!registerAgreementRead.value) {
    ElMessage.warning(t("login.message.agree.required"));
    return;
  }
  if (!registerPanelRef.value) return;

  try {
    await registerPanelRef.value.validate?.();
    registerLoading.value = true;
    await AuthAPI.tenantRegister({
      username: registerForm.username,
      password: registerForm.password,
      email: registerForm.email,
    });
    loginForm.username = registerForm.username;
    loginForm.password = registerForm.password;
    registerForm.username = "";
    registerForm.password = "";
    registerForm.confirmPassword = "";
    registerForm.email = "";
    registerAgreementRead.value = false;
    setAuthPanel("login");
  } catch (error) {
    console.error("[Login] register:", error);
  } finally {
    registerLoading.value = false;
  }
};

const submitForget = async () => {
  if (!forgetPanelRef.value) return;

  try {
    await forgetPanelRef.value.validate?.();
    forgetLoading.value = true;
    await UserAPI.forgetPassword(forgetForm);
    loginForm.username = forgetForm.username;
    loginForm.password = forgetForm.new_password;
    forgetForm.username = "";
    forgetForm.new_password = "";
    forgetForm.confirmPassword = "";
    setAuthPanel("login");
  } catch (error) {
    console.error("[Login] forget password:", error);
  } finally {
    forgetLoading.value = false;
  }
};

watch(locale, () => {
  formKey.value++;
});

watch(authPanel, (panel) => {
  if (panel !== "login") return;
  if (loginFlowMode.value !== "account") return;
  getCaptcha();
  loginForm.captcha = "";
  accountFormRef.value?.resetDragVerify?.();
  isPassing.value = false;
  isClickPass.value = false;
});

watch(
  () => route.fullPath,
  () => {
    if (authPanel.value !== "login" || loginFlowMode.value !== "account") return;
    getCaptcha();
    loginForm.captcha = "";
  }
);

onMounted(async () => {
  setupAccount("super");
  await configStore.getConfig(true).catch(() => undefined);
  await tryConsumeOAuthCallback();
  if (userStore.isLogin) {
    await router.replace(resolveRedirectTarget(route.query));
    return;
  }
  getCaptcha();
});

onActivated(() => {
  if (authPanel.value !== "login" || loginFlowMode.value !== "account") return;
  getCaptcha();
  loginForm.captcha = "";
});
</script>

<style scoped lang="scss">
@use "@/components/views/fa-login/fa-login";
</style>
