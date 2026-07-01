/**
 * 表单工具集：响应式布局 + 字段验证
 *
 * 重新导出 standalone 文件，保持向后兼容。
 */

export {
  calculateResponsiveSpan,
  createResponsiveSpanCalculator,
  type ResponsiveBreakpoint,
} from "./responsive";

export {
  PasswordStrength,
  trimSpaces,
  validatePhone,
  validateTelPhone,
  validateAccount,
  validatePassword,
  validateStrongPassword,
  getPasswordStrength,
  validateIPv4Address,
  validateEmail,
  validateURL,
  validateChineseIDCard,
  validateBankCard,
} from "./validator";
