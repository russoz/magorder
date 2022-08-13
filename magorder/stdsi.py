# -*- coding: utf-8 -*-

# Copyright (c) 2022, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from .base import BaseMagnitudeOrder, BaseMagnitudeUnit


class StdSIMagnitudeUnit(BaseMagnitudeUnit):
    std_si_order = {
        "y": -24,
        "z": -21,
        "a": -18,
        "f": -15,
        "p": -12,
        "n": -9,
        "µ": -6,
        "u": -6,
        "m": -3,
        "c": -2,
        "d": -1,
        "": 0,
        "da": 1,
        "h": 2,
        "k": 3,
        "M": 6,
        "G": 9,
        "T": 12,
        "P": 15,
        "E": 18,
        "Z": 21,
        "Y": 24,
    }

    def __init__(self, unit, lower=None, upper=None, base=10):
        self.unit = unit
        orders = BaseMagnitudeOrder(self.std_si_order, lower=lower, upper=upper, base=base)
        super().__init__(unit, orders)
