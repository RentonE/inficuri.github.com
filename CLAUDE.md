# 仓库工作约定

## 任务归档（必须遵守）

本仓库的所有任务完成后，必须按 `tasks/README.md` 中的规范分类建档：

1. 按任务类型选择分类目录：`tasks/research/`（调研查询）、`tasks/feature/`（功能开发）、`tasks/fix/`（问题修复）、`tasks/docs/`（文档维护）、`tasks/chore/`（日常维护）
2. 新建档案文件，命名为 `YYYY-MM-DD-任务简称.md`，内容包含：任务描述、分类、日期、分支、结论/产出、参考来源
3. 在 `tasks/README.md` 的任务索引表中追加一行
4. 将档案与任务产出一并提交推送

## 仓库 Skill

- `player-comparison`（`.claude/skills/player-comparison/`）：球员/球队表现对比调研工作流。所有球员对比、球员评价、球员数据查询类任务必须走此 skill（五维评估框架 + 数据交叉验证 + 归档规范）。

## 仓库结构

- `inficuri.github.com/`：Jekyll 博客站点源码（含 `_site/` 构建产物）
- `tasks/`：任务分类档案
