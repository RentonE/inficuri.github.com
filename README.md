# inficuri.github.com

个人工作区仓库，当前核心用途：**用女娲（huashu-nuwa）技能做人物思维蒸馏**——输入一个名字，自动完成「调研 → 提炼 → 验证」，把真实人物的思维框架蒸馏成可加载的 Agent 技能。

## 目录结构

| 路径 | 用途 |
|---|---|
| `.claude/skills/` | **当前生效的技能**（Claude Code 自动加载）：`wang-xiaobo-perspective`、`huashu-nuwa`（指向技能本体的软链接） |
| `.agents/skills/huashu-nuwa/` | 女娲技能本体 + 15 个官方示例人物（[技能介绍](.agents/skills/huashu-nuwa/README.md)） |
| `projects/` | **活跃项目区**：本地仓库整合进来后放这里，约定见 [projects/README.md](projects/README.md) |
| `archive/` | **归档区**：不再活跃但保留历史的内容，规则与索引见 [archive/README.md](archive/README.md) |
| `scripts/` | 仓库维护脚本（`archive.sh` 一键归档） |
| `skills-lock.json` | 技能安装锁定信息 |

## 已蒸馏人物（16）

### 本仓库自己蒸馏的

| 人物 | 位置 | 保真度 |
|---|---|---|
| 王小波（作家，1952–1997） | `.claude/skills/wang-xiaobo-perspective/` | 未评分 |

### 女娲自带示例（`.agents/skills/huashu-nuwa/examples/`）

| 领域 | 人物 | 保真度 |
|---|---|---|
| AI / 科技 | Andrej Karpathy | 97/100 |
| AI / 科技 | Ilya Sutskever | 94/100 |
| AI / 科技 | Elon Musk（马斯克） | 89/100 |
| 科技创业 | 张一鸣 | 93/100 |
| 产品 / 创业 | Steve Jobs（乔布斯） | 97/100 |
| 产品 / 创业 | Paul Graham | 97/100 |
| 投资 / 思想 | Charlie Munger（芒格） | 96/100 |
| 投资 / 思想 | Naval Ravikant | 97/100 |
| 投资 / 思想 | Nassim Taleb（塔勒布） | 97/100 |
| 科学 | Richard Feynman（费曼） | 96/100 |
| 内容创作 | MrBeast | 97/100 |
| 内容创作 | 张雪峰 | 97/100 |
| 内容创作 | x-mastery-mentor（多人复合导师）* | 96/100 |
| 加密 | 孙宇晨 | 91/100 |
| 政治 | Donald Trump（特朗普） | 95/100 |

\* 非单一人物：Nicolas Cole、Dickie Bush、Sahil Bloom、Justin Welsh 等多位 X/Twitter 运营高手的复合蒸馏。

## 怎么用

- **调用人物视角**：对 agent 说「用王小波的视角看看这个问题」「切换到芒格模式」
- **蒸馏新人物**：对 agent 说「用女娲蒸馏〈某人〉」，产出会生成在 `.claude/skills/<名字>-perspective/`
- **归档旧内容**：`scripts/archive.sh <路径> "<原因>"`（自动 `git mv` 并登记索引）

## 仓库维护规则（速记）

1. 活跃项目进 `projects/`，废弃内容进 `archive/`，技能进 `.claude/skills/` / `.agents/skills/`——**根目录不放散文件**
2. 归档必登记：每次归档在 [archive/README.md](archive/README.md) 索引表留一行（脚本会自动做）
3. 本地仓库整合进来时，按 [projects/README.md](projects/README.md) 的导入约定执行（清理构建产物、写来源 README、大文件走 LFS）
4. 归档区只进不改；要复活先移出

---

*历史注记：本仓库最初是 2013 年的 Jekyll 博客（uberobert.com 主题），该内容已完整保存在 `archive/legacy-jekyll-blog/`。*
