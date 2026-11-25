# mystic-life 仓库说明

这是一个 Codex Skill 仓库，根目录即 skill（SKILL.md 在根）。

- 核心逻辑与全部规则表在 `scripts/calculate.py`，改规则只改文件顶部的常量表。
- 内置 `lunar-python`（MIT）于 `scripts/vendor/lunar_python/`，请勿删除其 LICENSE。
- 测试：用任意 Python 3 运行 `python scripts/calculate.py --birth 1990-05-20 --mode all`；Windows 下先设 `$env:PYTHONIOENCODING='utf-8'`。
- 提交前请勿包含 `data/profile.json`（个人档案，已在 .gitignore 排除）。
