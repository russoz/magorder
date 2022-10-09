# -*- coding: utf-8 -*-

# Copyright (c) 2022, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from .base import MagnitudeSystem, BaseMagnitudeUnit


class SIDataMagnitudeUnit(BaseMagnitudeUnit):
    si_order = [
        {"prefix": "", "power": 0},
        {"prefix": "k", "power": 1},
        {"prefix": "M", "power": 2},
        {"prefix": "G", "power": 3},
        {"prefix": "T", "power": 4},
        {"prefix": "P", "power": 5},
        {"prefix": "E", "power": 6},
        {"prefix": "Z", "power": 7},
        {"prefix": "Y", "power": 8},
    ]

    def __init__(self, unit, lower=None, upper=None):
        orders = MagnitudeSystem(self.si_order, lower=lower, upper=upper, base=1000)
        super().__init__(unit, orders)


class IECDataMagnitudeUnit(BaseMagnitudeUnit):
    iec_order = [
        {"prefix": "", "power": 0},
        {"prefix": "Ki", "power": 1},
        {"prefix": "Mi", "power": 2},
        {"prefix": "Gi", "power": 3},
        {"prefix": "Ti", "power": 4},
        {"prefix": "Pi", "power": 5},
        {"prefix": "Ei", "power": 6},
        {"prefix": "Zi", "power": 7},
        {"prefix": "Yi", "power": 8},
    ]

    def __init__(self, unit: str, lower=None, upper=None, legacy=False, case=True):
        def _no_case(order):
            existing = set(order.get("aliases", [])).union({order["prefix"]})
            aliases = {e.lower() for e in existing}
            new_order = dict(order)
            new_order["aliases"] = list(aliases)
            return new_order

        self.case = case
        orders = list(self.iec_order)
        if legacy:
            orders.extend([
                {"prefix": "K", "power": 1},
                {"prefix": "M", "power": 2},
                {"prefix": "G", "power": 3},
            ])
        if not case:
            orders = [_no_case(o) for o in orders]

        orders = MagnitudeSystem(orders, lower=lower, upper=upper, base=1024)
        super().__init__(unit, orders)

# code: language=python tabSize=4
