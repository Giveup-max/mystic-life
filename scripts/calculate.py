#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mystic-life 命理生活决策。仅供娱乐参考，不构成科学、医疗、投资或法律建议。"""
import argparse
import datetime
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))

from lunar_python import Solar  # noqa: E402

GAN_WX = {"甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
          "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"}
ZHI_WX = {"子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土", "巳": "火",
          "午": "火", "未": "土", "申": "金", "酉": "金", "戌": "土", "亥": "水"}
WX_SHENG = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
WX_KE = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}
WX_ORDER = ["木", "火", "土", "金", "水"]

WX_COLOR = {"金": ["白色", "金色", "银色", "米白"], "木": ["绿色", "青色"], "水": ["黑色", "蓝色", "藏青"],
            "火": ["红色", "紫色", "橙色", "酒红"], "土": ["黄色", "棕色", "卡其", "米色"]}
WX_TASTE = {"木": "酸味", "火": "苦味", "土": "甘味（甜）", "金": "辛味", "水": "咸味"}
WX_FOOD = {
    "金": ["百合", "银耳", "白萝卜", "梨", "豆腐", "山药", "杏仁"],
    "木": ["绿叶蔬菜", "西兰花", "芹菜", "绿豆", "菠菜", "莴笋"],
    "水": ["黑豆", "黑米", "黑木耳", "海带", "蓝莓", "桑葚"],
    "火": ["红枣", "番茄", "红豆", "枸杞", "山楂", "胡萝卜"],
    "土": ["南瓜", "小米", "玉米", "土豆", "黄豆", "山药", "红薯"],
}
WX_CRYSTAL = {
    "金": ["白水晶", "白幽灵", "金发晶", "银发晶", "黄铁矿"],
    "木": ["绿幽灵", "东陵玉", "孔雀石", "橄榄石", "翡翠"],
    "水": ["黑曜石", "茶晶", "黑发晶", "蓝玉髓", "海蓝宝", "月光石"],
    "火": ["红玛瑙", "石榴石", "红纹石", "紫水晶", "红发晶"],
    "土": ["黄水晶", "钛晶", "金发晶", "茶晶", "虎眼石", "黄玉"],
}
WX_DIR = {"木": "东方", "火": "南方", "土": "中央/本地", "金": "西方", "水": "北方"}

BRAND_WX = {
    "苹果 Apple": "金", "三星 Samsung": "水", "华为 HUAWEI": "火",
    "小米 Xiaomi": "土", "OPPO": "木", "vivo": "水", "荣耀 Honor": "水",
    "一加 OnePlus": "火", "realme 真我": "土", "魅族 MEIZU": "水",
    "摩托罗拉 Motorola": "水", "索尼 Sony": "水", "谷歌 Pixel": "火",
    "努比亚 nubia": "火", "iQOO": "土",
}

EIGHT_STARS = {
    ("1", "3"): ("天医", "吉", "正财、感情、健康"), ("6", "8"): ("天医", "吉", "正财、感情、健康"),
    ("4", "9"): ("天医", "吉", "正财、感情、健康"), ("2", "7"): ("天医", "吉", "正财、感情、健康"),
    ("1", "4"): ("生气", "吉", "贵人、人缘、乐观"), ("6", "7"): ("生气", "吉", "贵人、人缘、乐观"),
    ("3", "9"): ("生气", "吉", "贵人、人缘、乐观"), ("2", "8"): ("生气", "吉", "贵人、人缘、乐观"),
    ("1", "9"): ("延年", "吉", "领导力、事业、长寿"), ("8", "7"): ("延年", "吉", "领导力、事业、长寿"),
    ("3", "4"): ("延年", "吉", "领导力、事业、长寿"), ("2", "6"): ("延年", "吉", "领导力、事业、长寿"),
    ("1", "1"): ("伏位", "中", "稳定、等待、积蓄"), ("2", "2"): ("伏位", "中", "稳定、等待、积蓄"),
    ("8", "8"): ("伏位", "中", "稳定、等待、积蓄"), ("9", "9"): ("伏位", "中", "稳定、等待、积蓄"),
    ("6", "6"): ("伏位", "中", "稳定、等待、积蓄"), ("7", "7"): ("伏位", "中", "稳定、等待、积蓄"),
    ("3", "3"): ("伏位", "中", "稳定、等待、积蓄"), ("4", "4"): ("伏位", "中", "稳定、等待、积蓄"),
    ("1", "2"): ("绝命", "凶", "冒险、破财、冲动"), ("6", "9"): ("绝命", "凶", "冒险、破财、冲动"),
    ("4", "8"): ("绝命", "凶", "冒险、破财、冲动"), ("3", "7"): ("绝命", "凶", "冒险、破财、冲动"),
    ("1", "8"): ("五鬼", "凶", "思维活跃、多变动"), ("7", "9"): ("五鬼", "凶", "思维活跃、多变动"),
    ("3", "6"): ("五鬼", "凶", "思维活跃、多变动"), ("2", "4"): ("五鬼", "凶", "思维活跃、多变动"),
    ("1", "6"): ("六煞", "凶", "桃花、情绪波动"), ("7", "4"): ("六煞", "凶", "桃花、情绪波动"),
    ("3", "8"): ("六煞", "凶", "桃花、情绪波动"), ("2", "9"): ("六煞", "凶", "桃花、情绪波动"),
    ("1", "7"): ("祸害", "凶", "口舌、是非"), ("8", "9"): ("祸害", "凶", "口舌、是非"),
    ("4", "6"): ("祸害", "凶", "口舌、是非"), ("2", "3"): ("祸害", "凶", "口舌、是非"),
}

ITEM_WX_HINTS = {
    "金": ["白", "金", "银", "米白", "透明", "玻璃", "金属", "镜"],
    "木": ["绿", "青", "木", "竹", "翠"],
    "水": ["黑", "蓝", "藏青", "深灰", "海"],
    "火": ["红", "紫", "橙", "玫", "酒红"],
    "土": ["黄", "棕", "卡其", "米色", "大地", "玳瑁", "茶"],
}

DEFAULT_PROFILE = os.path.join(HERE, "..", "data", "profile.json")


def build_chart(solar, gender):
    lunar = solar.getLunar()
    bazi = lunar.getEightChar()
    pillars = [
        ("年", bazi.getYearGan(), bazi.getYearZhi(), bazi.getYearNaYin()),
        ("月", bazi.getMonthGan(), bazi.getMonthZhi(), bazi.getMonthNaYin()),
        ("日", bazi.getDayGan(), bazi.getDayZhi(), bazi.getDayNaYin()),
        ("时", bazi.getTimeGan(), bazi.getTimeZhi(), bazi.getTimeNaYin()),
    ]
    counts = {k: 0 for k in WX_ORDER}
    for _, gan, zhi, _ in pillars:
        counts[GAN_WX[gan]] += 1
        counts[ZHI_WX[zhi]] += 1
    day_gan = bazi.getDayGan()
    day_wx = GAN_WX[day_gan]
    weakest = sorted(WX_ORDER, key=lambda x: (counts[x], WX_ORDER.index(x)))[0]
    return {
        "lunar": lunar, "bazi": bazi, "pillars": pillars, "counts": counts,
        "day_gan": day_gan, "day_wx": day_wx, "weakest": weakest,
        "shengxiao": lunar.getYearShengXiao(), "month_zhi": bazi.getMonthZhi(),
    }


def ming_gua(chart, gender):
    if gender not in ("male", "female"):
        return None
    year = chart["lunar"].getYear()
    tail = year % 100
    n = (100 - tail) % 9 if gender == "male" else (tail - 4) % 9
    if n == 0:
        n = 9
    if n == 5:
        n = 2 if gender == "male" else 8
    table = {1: ("坎", "水", "东四命"), 2: ("坤", "土", "西四命"), 3: ("震", "木", "东四命"),
             4: ("巽", "木", "东四命"), 6: ("乾", "金", "西四命"), 7: ("兑", "金", "西四命"),
             8: ("艮", "土", "西四命"), 9: ("离", "火", "东四命")}
    gua, wx, group = table[n]
    good_dirs = ["东", "南", "北", "东南"] if group == "东四命" else ["西", "西南", "西北", "东北"]
    return {"num": n, "gua": gua, "wx": wx, "group": group, "good_dirs": good_dirs}


def multi_view_use(chart):
    """三视角喜用神：扶抑 / 调候 / 日主特性。"""
    c = chart
    day_wx = c["day_wx"]
    body_strength = c["counts"][day_wx]
    strong = body_strength >= 3
    ke_day = [k for k, v in WX_KE.items() if v == day_wx]  # 克日主
    sheng_day = [k for k, v in WX_SHENG.items() if v == day_wx]  # 生日主
    xie_day = [v for k, v in WX_SHENG.items() if k == day_wx]  # 日主所生（泄）
    hao_day = [v for k, v in WX_KE.items() if k == day_wx]  # 日主所克（耗）
    if strong:
        fuyi_favor = ke_day + xie_day + hao_day
        fuyi_avoid = [day_wx] + sheng_day
    else:
        fuyi_favor = [day_wx] + sheng_day
        fuyi_avoid = ke_day + xie_day + hao_day
    # 调候：月支季节
    mz = c["month_zhi"]
    season = {"寅": "春", "卯": "春", "辰": "春", "巳": "夏", "午": "夏", "未": "夏",
              "申": "秋", "酉": "秋", "戌": "秋", "亥": "冬", "子": "冬", "丑": "冬"}[mz]
    tiaohou = {"春": ["木", "火"], "夏": ["水", "金"], "秋": ["火", "水"], "冬": ["火", "木"]}[season]
    rizhu = {"木": ["水", "火"], "火": ["木", "金"], "土": ["木", "火", "金"],
             "金": ["土", "水"], "水": ["金", "木"]}[day_wx]
    return {
        "strong": strong, "fuyi_favor": fuyi_favor, "fuyi_avoid": fuyi_avoid,
        "season": season, "tiaohou_favor": tiaohou,
        "rizhu_favor": rizhu,
    }


def load_profile(path):
    if not path or not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def infer_wx(item):
    for wx, hints in ITEM_WX_HINTS.items():
        for h in hints:
            if h in item:
                return wx
    return None


def record_observation(args):
    profile = load_profile(args.profile) or {"observations": []}
    wx = args.wx or infer_wx(args.item or "")
    if wx not in WX_ORDER:
        wx = None
    obs = {
        "item": args.item, "wx": wx, "kind": args.kind,
        "times": int(args.times or 1), "context": args.context or "",
        "indicators": args.indicators or "", "verdict": args.verdict,
    }
    profile["observations"].append(obs)
    os.makedirs(os.path.dirname(args.profile), exist_ok=True)
    with open(args.profile, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)
    print(f"已记录：{obs['item']}（{wx or '未识别五行'}，{obs['kind']}，{obs['verdict']}）")
    _print_profile_summary(profile)


def profile_conclusion(profile):
    score = {k: 0.0 for k in WX_ORDER}
    for obs in profile.get("observations", []):
        wx = obs.get("wx")
        if wx not in WX_ORDER:
            continue
        w = 2.0 if obs.get("kind") == "体感" else 1.0
        t = min(int(obs.get("times", 1)), 5)
        w *= 1 + 0.2 * (t - 1)
        v = obs.get("verdict")
        if v == "利":
            score[wx] += w
        elif v == "弊":
            score[wx] -= w
    favor = [k for k in WX_ORDER if score[k] > 0]
    avoid = [k for k in WX_ORDER if score[k] < 0]
    favor.sort(key=lambda x: -score[x])
    avoid.sort(key=lambda x: score[x])
    return score, favor, avoid


def _print_profile_summary(profile):
    score, favor, avoid = profile_conclusion(profile)
    print(f"  当前档案：{len(profile.get('observations', []))} 条观察")
    print(f"  有利五行：{'、'.join(favor) if favor else '（暂无）'}")
    print(f"  不利五行：{'、'.join(avoid) if avoid else '（暂无）'}")
    return favor, avoid


def print_chart(chart, profile=None):
    c = chart
    print("== 八字命盘 ==")
    for label, gan, zhi, nayin in c["pillars"]:
        print(f"  {label}柱：{gan}{zhi}（{GAN_WX[gan]}/{ZHI_WX[zhi]}） 纳音：{nayin}")
    print(f"  日主：{c['day_gan']}（{c['day_wx']}）  生肖：{c['shengxiao']}")
    print(f"  五行统计：{'  '.join(f'{k}{v}' for k, v in c['counts'].items())}")
    mv = multi_view_use(c)
    print(f"  身强弱：{'身强' if mv['strong'] else '身弱'}（日主五行出现 {c['counts'][c['day_wx']]} 次）")
    print(f"  扶抑视角：喜 {'、'.join(mv['fuyi_favor'])}，忌 {'、'.join(mv['fuyi_avoid'])}")
    print(f"  调候视角（{mv['season']}季）：喜 {'、'.join(mv['tiaohou_favor'])}")
    print(f"  日主特性视角（{c['day_wx']}）：喜 {'、'.join(mv['rizhu_favor'])}")
    if profile:
        favor, avoid = _print_profile_summary(profile)
        if favor or avoid:
            print("  → 以上若与你个人档案冲突，以档案为准（档案由体感累积而来）。")


def print_life(chart, gender, number=None, profile=None, use=None):
    c = chart
    if use is None:
        mv = multi_view_use(c)
        use = c["weakest"]
    favor = avoid = None
    if profile:
        _, favor, avoid = profile_conclusion(profile)
    if favor:
        use = favor[0]
    print("== 生活选择建议 ==")
    if favor:
        print(f"  [个人档案校准] 有利：{'、'.join(favor)}；不利：{'、'.join(avoid) if avoid else '—'}")
    else:
        print(f"  [未建立档案，按算法推演] 主用五行：{use}")
    print(f"  幸运色：{'、'.join(WX_COLOR[use])}")
    if favor and len(favor) > 1:
        extra = sum((WX_COLOR[x] for x in favor[1:]), [])
        print(f"  辅助色：{'、'.join(extra)}")
    print(f"  幸运食物（{WX_TASTE[use]}）：{'、'.join(WX_FOOD[use])}")
    print(f"  增能/招财水晶：{'、'.join(WX_CRYSTAL[use])}")
    print(f"  有利方位：{WX_DIR[use]}")
    mg = ming_gua(c, gender)
    if mg:
        print(f"  命卦：{mg['gua']}（{mg['wx']}，{mg['group']}）")
        print(f"  吉方位：{'、'.join(mg['good_dirs'])}")
    good = [b for b, w in BRAND_WX.items() if w == use]
    print(f"  手机品牌（主用五行 {use}）：{'、'.join(good) if good else '（自定义规则中暂无）'}")
    if avoid:
        print(f"  建议避开的五行：{'、'.join(avoid)}（颜色/品牌中对应项少选）")
    if number:
        print()
        print_phone(number)


def print_phone(number):
    digits = "".join(ch for ch in number if ch.isdigit())
    print("== 手机号数字能量 ==")
    print(f"  号码：{number}")
    if len(digits) < 2:
        print("  号码过短，无法分析。")
        return
    seen = {}
    for i in range(len(digits) - 1):
        a, b = digits[i], digits[i + 1]
        if a in "05" or b in "05":
            continue
        hit = EIGHT_STARS.get((a, b)) or EIGHT_STARS.get((b, a))
        if hit:
            seen.setdefault(hit[0], {"吉凶": hit[1], "含义": hit[2], "次数": 0})
            seen[hit[0]]["次数"] += 1
    if not seen:
        print("  未识别出明显组合（号码中 0/5 较多）。")
        return
    for name, info in sorted(seen.items(), key=lambda kv: -kv[1]["次数"]):
        print(f"  {name}（{info['吉凶']}）x{info['次数']}：{info['含义']}")


def print_day(chart, date_str):
    c = chart
    y, m, d = (int(x) for x in date_str.split("-"))
    lunar = Solar.fromYmdHms(y, m, d, 12, 0, 0).getLunar()
    def s(v):
        return "、".join(v) if isinstance(v, list) else str(v)
    print("== 当日决策参考 ==")
    print(f"  日期：{date_str}")
    print(f"  干支：{lunar.getDayInGanZhi()}  纳音：{lunar.getDayNaYin()}")
    print(f"  冲煞：{s(lunar.getDayChongDesc())}")
    print(f"  宜：{s(lunar.getDayYi())}")
    print(f"  忌：{s(lunar.getDayJi())}")
    print(f"  吉神：{s(lunar.getDayJiShen())}")
    print(f"  喜神方位：{s(lunar.getDayPositionXiDesc())}")
    print(f"  财神方位：{s(lunar.getDayPositionCaiDesc())}")
    print(f"  福神方位：{s(lunar.getDayPositionFuDesc())}")
    print(f"  阳贵神方位：{s(lunar.getDayPositionYangGuiDesc())}")
    try:
        print(f"  值星：{s(lunar.getZhiXing())}")
    except Exception:
        pass
    try:
        print(f"  天神：{s(lunar.getDayTianShen())}（{s(lunar.getDayTianShenType())}，{s(lunar.getDayTianShenLuck())}）")
    except Exception:
        pass
    try:
        print(f"  星宿：{s(lunar.getXiu())}（{s(lunar.getXiuLuck())}）")
        print(f"  星宿吉凶：{s(lunar.getXiuSong())}")
    except Exception:
        pass
    print(f"  你的日主：{c['day_gan']}（{c['day_wx']}）")
    print("  建议：优先安排「宜」中的事项，重要行动面向喜神/财神方位；避开冲煞对应的生肖协作。")


def main():
    ap = argparse.ArgumentParser(description="mystic-life 命理生活决策")
    ap.add_argument("--birth", help="公历生日 YYYY-MM-DD（mode=chart/life/day/all 必填）")
    ap.add_argument("--time", default="12:00", help="出生时间 HH:MM（默认 12:00）")
    ap.add_argument("--gender", choices=["male", "female"], default=None, help="性别，用于命卦")
    ap.add_argument("--mode", choices=["chart", "life", "day", "all", "record", "profile-show"], default="all")
    ap.add_argument("--date", default=None, help="当日决策日期 YYYY-MM-DD（默认今天）")
    ap.add_argument("--number", default=None, help="手机号，数字能量分析")
    ap.add_argument("--profile", default=DEFAULT_PROFILE, help="个人校准档案 JSON 路径")
    ap.add_argument("--item", help="[record] 颜色/物品，如 白色、橙色")
    ap.add_argument("--wx", help="[record] 五行，可省略自动推断")
    ap.add_argument("--kind", choices=["偏好", "体感"], default="体感", help="[record] 偏好或体感")
    ap.add_argument("--times", type=int, default=1, help="[record] 观察次数")
    ap.add_argument("--context", default="", help="[record] 情境")
    ap.add_argument("--indicators", default="", help="[record] 身体指标，如 睡眠,精力")
    ap.add_argument("--verdict", choices=["利", "弊", "中性"], default="利", help="[record] 结论")
    args = ap.parse_args()

    if args.mode == "record":
        record_observation(args)
        return
    if args.mode == "profile-show":
        profile = load_profile(args.profile)
        if not profile:
            print("尚无档案。用 --mode record 记录第一条观察。")
            return
        _print_profile_summary(profile)
        for obs in profile.get("observations", []):
            print(f"  - {obs.get('item')}（{obs.get('wx') or '未识别'}，{obs.get('kind')}x{obs.get('times')}，{obs.get('verdict')}）")
        return

    if not args.birth:
        ap.error("--birth 必填（chart/life/day/all 模式）")

    y, m, d = (int(x) for x in args.birth.split("-"))
    hh, mm = (int(x) for x in args.time.split(":"))
    solar = Solar.fromYmdHms(y, m, d, hh, mm, 0)
    chart = build_chart(solar, args.gender)
    profile = load_profile(args.profile)

    if args.mode in ("chart", "all"):
        print_chart(chart, profile)
    if args.mode in ("life", "all"):
        print()
        print_life(chart, args.gender, args.number, profile)
    if args.mode == "day":
        date_str = args.date or datetime.date.today().isoformat()
        print_day(chart, date_str)
    if args.number and args.mode not in ("life", "all"):
        print()
        print_phone(args.number)


if __name__ == "__main__":
    main()

