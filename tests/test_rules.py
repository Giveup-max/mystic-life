# -*- coding: utf-8 -*-
"""mystic-life 回归测试。仅用标准库，CI 无需安装依赖。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, os.path.join(ROOT, "scripts", "vendor"))

import calculate as calc  # noqa: E402


def test_day_master():
    solar = calc.Solar.fromYmdHms(1986, 1, 24, 0, 30, 0)
    chart = calc.build_chart(solar, "male")
    assert chart["day_wx"] == "土", chart["day_wx"]
    assert chart["shengxiao"] == "牛", chart["shengxiao"]
    assert chart["day_gan"] == "戊", chart["day_gan"]


def test_multi_view_strong():
    solar = calc.Solar.fromYmdHms(1986, 1, 24, 0, 30, 0)
    chart = calc.build_chart(solar, "male")
    mv = calc.multi_view_use(chart)
    assert mv["strong"] is True
    assert "金" in mv["fuyi_favor"], mv["fuyi_favor"]
    assert "木" in mv["fuyi_favor"], mv["fuyi_favor"]
    assert "火" in mv["fuyi_avoid"], mv["fuyi_avoid"]
    assert "土" in mv["fuyi_avoid"], mv["fuyi_avoid"]


def test_profile_overrides():
    profile = {"observations": [
        {"item": "白色", "wx": "金", "kind": "体感", "times": 5, "verdict": "利"},
        {"item": "红色", "wx": "火", "kind": "体感", "times": 3, "verdict": "弊"},
        {"item": "绿色", "wx": "木", "kind": "体感", "times": 3, "verdict": "利"},
    ]}
    score, favor, avoid = calc.profile_conclusion(profile)
    assert "金" in favor, favor
    assert "木" in favor, favor
    assert "火" in avoid, avoid


def test_ming_gua():
    solar = calc.Solar.fromYmdHms(1986, 1, 24, 0, 30, 0)
    chart = calc.build_chart(solar, "male")
    mg = calc.ming_gua(chart, "male")
    assert mg["gua"] == "乾", mg
    assert mg["group"] == "西四命"


def test_eight_stars_keys():
    for a, b in calc.EIGHT_STARS:
        assert a in "12346789", a
        assert b in "12346789", b
        assert len(a) == 1 and len(b) == 1


def test_body_nature():
    solar = calc.Solar.fromYmdHms(1986, 1, 24, 0, 30, 0)
    chart = calc.build_chart(solar, "male")
    assert "寒湿" in calc.body_nature(chart)
    solar2 = calc.Solar.fromYmdHms(1990, 7, 15, 12, 0, 0)
    chart2 = calc.build_chart(solar2, None)
    assert "燥热" in calc.body_nature(chart2)

if __name__ == "__main__":
    test_day_master()
    test_multi_view_strong()
    test_profile_overrides()
    test_ming_gua()
    test_eight_stars_keys()
    test_body_nature()
    print("ALL TESTS PASSED")

