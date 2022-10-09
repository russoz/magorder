# -*- coding: utf-8 -*-

# Copyright (c) 2022, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from .base import BaseMagnitudeOrder, BaseMagnitudeUnit


class StdSIMagnitudeUnit(BaseMagnitudeUnit):
    std_si_order = [
        {"prefix": "y", "power": -24},
        {"prefix": "z", "power": -21},
        {"prefix": "a", "power": -18},
        {"prefix": "f", "power": -15},
        {"prefix": "p", "power": -12},
        {"prefix": "n", "power": -9},
        {"prefix": "µ", "power": -6, "aliases": ["u"]},
        {"prefix": "m", "power": -3},
        {"prefix": "c", "power": -2},
        {"prefix": "d", "power": -1},
        {"prefix": "", "power": 0},
        {"prefix": "da", "power": 1},
        {"prefix": "h", "power": 2},
        {"prefix": "k", "power": 3},
        {"prefix": "M", "power": 6},
        {"prefix": "G", "power": 9},
        {"prefix": "T", "power": 12},
        {"prefix": "P", "power": 15},
        {"prefix": "E", "power": 18},
        {"prefix": "Z", "power": 21},
        {"prefix": "Y", "power": 24},
    ]

    def __init__(self, unit, lower=None, upper=None, base=10):
        orders = BaseMagnitudeOrder(self.std_si_order, lower=lower, upper=upper, base=base)
        super().__init__(unit, orders)
