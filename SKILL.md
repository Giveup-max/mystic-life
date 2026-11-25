---
name: mystic-life
description: 基于生辰八字、五行、生肖与老黄历的娱乐性命理生活决策，输出幸运色、水晶、食物、方位、手机品牌建议、手机号数字能量吉凶、当日宜忌与择日，并支持用个人体感档案校准结论。仅作娱乐，不构成科学、医疗、投资或法律建议。
metadata:
  short-description: 命理生活决策测算
---

# 命理生活决策（mystic-life）

根据用户生日（可含时辰、性别）用内置的 `lunar-python` 推算八字、五行、日主、生肖、纳音，并映射到日常选择。核心特点是**多视角喜用神 + 个人体感档案校准**，让结论随使用者的真实反馈逐渐贴近本人。**仅供娱乐，结论不具科学依据。**

## 何时使用

用户想基于生日做命理类测算或生活选择时使用，例如：换手机选什么品牌、幸运色/穿衣颜色、增能招财水晶、适合的食物、居住/朝向、手机号吉凶、某天适不适合做某事。纯科学问题、医疗/投资/法律/重大人生决策不要用本 skill，应建议用户谨慎并咨询专业人士。

## 快速开始

1. 收集输入：公历生日 `YYYY-MM-DD`；出生时间 `HH:MM`（尽量准确，缺省 12:00）；性别 `male`/`female`（算八宅命卦用，可省略）；按需手机号、要决策的日期。
2. 运行 `scripts/calculate.py`（已内置 `lunar_python`，无需安装依赖，任意 Python 3 均可）。
3. 整理输出并回复用户，结尾附“仅供娱乐参考”。

```powershell
$env:PYTHONIOENCODING='utf-8'
python '<skill>/scripts/calculate.py' --birth 1990-05-20 --time 12:30 --gender male --mode all
```

- 若 `python`/`py` 不可用，用 `load_workspace_dependencies` 获取 Codex bundled Python 路径后替换 `python`。
- `--mode`：`chart`（命盘+三视角）、`life`（生活选择）、`day`（当日决策）、`all`（默认）。
- `--number 13812345678` 附加手机号数字能量；`--date 2026-12-03` 用于 `day` 指定日期。

## 三视角喜用神

`chart` 模式会输出三种独立判断，结论可能冲突（这是正常的，不同流派本身就不一致）：
- **扶抑**：按日主强弱定喜忌（身强喜克泄耗，身弱喜生扶）。
- **调候**：按月令寒暖燥湿定喜忌。
- **日主特性**：按日主天干的传统喜忌。

冲突处不要替用户拍板，应说明“这里流派不一致”，并优先参考用户体感档案。

## 个人档案校准（最重要）

算法只是起点，**用户的身体反馈才是最终标准**。用 `record` 记录观察、`profile-show` 查看结论；档案结论会自动覆盖算法建议。

```powershell
python '<skill>/scripts/calculate.py' --mode record --item 白色 --wx 金 --kind 体感 --times 5 --verdict 利
python '<skill>/scripts/calculate.py' --mode record --item 红色 --wx 火 --kind 体感 --times 3 --verdict 弊
python '<skill>/scripts/calculate.py' --mode profile-show
python '<skill>/scripts/calculate.py' --birth ... --mode life   # 自动读取默认档案
```

- `--kind` 区分**偏好**与**体感**：偏好权重低，体感权重高；多次稳定出现的体感最可信。
- 采集要点（写进询问话术）：记**身体指标**（睡眠、精力、情绪、烦躁感、做事顺利度）而非“喜不喜欢”；多观察几次、做对照；回溯自然状态下的关联。
- 档案默认存 `data/profile.json`，可用 `--profile <路径>` 指定。五行粒度按 `木火土金水`，同一五行内有分歧时（如红色弊、橙色利）以具体条目为准。

## 参考与扩展

规则来源、流派说明、映射表、如何修改规则，见 `references/rules.md`；安装与发布见 `README.md`。
