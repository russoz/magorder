# -*- coding: utf-8 -*-

# Copyright (c) 2022, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from magorder.base import MagnitudeSystem
from magorder.stdsi import StdSIMagnitudeUnit


def test_base_magnitude_order_factor():
    ord = StdSIMagnitudeUnit("m").orders
    assert ord.factor("k") == 1000
    assert ord.factor("m") == 0.001
    assert ord.factor("µ") == 0.000_001

def test_base_magnitude_order_to_prefix():
    ord = StdSIMagnitudeUnit("m").orders
    assert ord.to_prefix(3) == "k"
    assert ord.to_prefix(-6) == "µ"

def test_base_magnitude_order_alias_conflict():
    ord = [
        {"prefix": "µ", "power": -6, "aliases": ["u"]},
        {"prefix": "m", "power": -3},
        {"prefix": "", "power": 0, "aliases": ["m"]},
    ]
    with pytest.raises(ValueError):
        b = MagnitudeSystem(ord)

def test_base_magnitude_order_duplicate_conflict():
    ord = [
        {"prefix": "µ", "power": -6, "aliases": ["u"]},
        {"prefix": "m", "power": -3},
        {"prefix": "m", "power": 6},
        {"prefix": "", "power": 0, "aliases": ["m"]},
    ]
    with pytest.raises(ValueError):
        b = MagnitudeSystem(ord)

def test_base_magnitude_order_invalid_limits():
    ord = [
        {"prefix": "µ", "power": -6, "aliases": ["u"]},
        {"prefix": "m", "power": -3},
        {"prefix": "", "power": 0},
    ]
    with pytest.raises(ValueError):
        b = MagnitudeSystem(ord, lower="y")
    with pytest.raises(ValueError):
        b = MagnitudeSystem(ord, upper="Y")

# code: language=python tabSize=4
