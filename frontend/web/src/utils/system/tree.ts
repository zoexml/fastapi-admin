/**
 * tree.ts - 树形数据工具函数
 *
 * 提供通用的树结构构建与扁平化能力。
 *
 * ## 主要功能
 *
 * - buildTree: 将扁平数组构建树形结构（通过 id/parentId 关系）
 * - flattenTree: 将树形结构扁平化为扁平数组
 *
 * @module utils/system/tree
 * @author FastapiAdmin Team
 */

/**
 * 将扁平数组构建树形结构
 *
 * @param rows 扁平数据数组
 * @param idKey 唯一标识字段名
 * @param parentKey 父级标识字段名
 * @returns 树形结构数组
 *
 * @example
 * ```ts
 * const data = [
 *   { id: 1, parentId: 0, name: 'Root' },
 *   { id: 2, parentId: 1, name: 'Child' },
 * ]
 * buildTree(data, 'id', 'parentId')
 * // => [{ id: 1, children: [{ id: 2, children: [] }] }]
 * ```
 */
export function buildTree<T extends Record<string, any>>(
  rows: T[],
  idKey: string,
  parentKey: string
): T[] {
  const map = new Map<number | string, T>();
  const roots: T[] = [];

  rows.forEach((row) => {
    map.set(row[idKey], { ...row, children: [] });
  });

  map.forEach((row: T) => {
    const parent = map.get(row[parentKey]);
    if (parent) {
      (parent.children as T[]).push(row);
    } else {
      roots.push(row);
    }
  });

  return roots;
}

/**
 * 将树形结构扁平化为数组
 *
 * @param rows 树形结构数组
 * @returns 扁平化后的数组（保留原始 children 字段）
 *
 * @example
 * ```ts
 * const tree = [{ id: 1, children: [{ id: 2, children: [] }] }]
 * flattenTree(tree)
 * // => [{ id: 1, children: [...] }, { id: 2, children: [] }]
 * ```
 */
export function flattenTree<T extends Record<string, any>>(rows: T[]): T[] {
  return rows.flatMap((row) => [
    row,
    ...flattenTree(((row as any).children || []) as T[]),
  ]);
}
