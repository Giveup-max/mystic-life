# mystic-life

基于生辰八字、五行、生肖与老黄历的**娱乐性**命理生活决策 Skill。输出幸运色、增能水晶、幸运食物、有利方位、手机品牌建议、手机号数字能量吉凶、当日宜忌与择日，并支持用**个人体感档案**校准结论。

> 仅作娱乐，不构成科学、医疗、投资或法律建议。

## 功能

- 八字命盘：四柱、纳音、日主五行、五行统计、身强弱。
- 三视角喜用神：扶抑（身强弱）、调候（月令）、日主特性，冲突处如实呈现。
- 生活选择：幸运色 / 食物 / 水晶 / 方位 / 八宅命卦 / 手机品牌（五行归类）。
- 手机号数字能量：八星吉凶逐段解读。
- 当日决策与择日：宜忌、冲煞、吉神方位、值星、黄黑道、星宿吉凶。
- 个人档案：`record` 记录体感 → 自动区分偏好/体感并加权 → 覆盖算法结论。

## 安装

安装到 `$CODEX_HOME/skills/`（默认 `~/.codex/skills/`）。

方式一：在 Codex 里直接说

```
用 skill-installer 安装 <owner>/<repo> 的 skills/mystic-life
```

方式二：命令行 skill-installer（本仓库根目录即 skill）

```bash
python "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo <owner>/<repo> --path . --name mystic-life
```

方式三：手动

```bash
git clone https://github.com/<owner>/<repo>.git
cp -r <repo> "$CODEX_HOME/skills/mystic-life"
```

已内置 `lunar-python`（MIT），无需 pip 安装，任意 Python 3 均可运行。

## 使用

```bash
python scripts/calculate.py --birth 1990-05-20 --time 12:30 --gender male --mode all
python scripts/calculate.py --birth 1990-05-20 --mode day --date 2026-12-03
python scripts/calculate.py --birth 1990-05-20 --mode all --number 13812345678
```

建立个人档案：

```bash
python scripts/calculate.py --mode record --item 白色 --wx 金 --kind 体感 --times 5 --verdict 利
python scripts/calculate.py --mode record --item 红色 --wx 火 --kind 体感 --times 3 --verdict 弊
python scripts/calculate.py --mode profile-show
```

Windows PowerShell 下先设 `$env:PYTHONIOENCODING='utf-8'`。

## 目录

- `SKILL.md` — Skill 入口说明
- `scripts/calculate.py` — 核心脚本（含全部规则表）
- `scripts/vendor/lunar_python/` — 内置推算库
- `references/rules.md` — 规则来源与扩展方法
- `data/profile.example.json` — 个人档案示例

## 许可

本 skill 代码采用 MIT 许可。内置的 `lunar-python` 由 6tail 开发，MIT 许可，详见 `scripts/vendor/lunar_python/LICENSE`。
