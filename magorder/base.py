# -*- coding: utf-8 -*-

# Copyright (c) 2022, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later


class BaseMagnitudeOrder:
    def __init__(self, magnitudes, lower=None, upper=None, base=10, default_order=0):
        if lower is not None:
            magnitudes = dict([(k, v) for k, v in magnitudes.items() if magnitudes[lower] <= v])
        if upper is not None:
            magnitudes = dict([(k, v) for k, v in magnitudes.items() if v <= magnitudes[upper]])
        self.magnitudes = magnitudes
        self.powers = sorted(self.magnitudes.keys())
        self.lower = self.powers[0]
        self.upper = self.powers[-1]
        self.base = base
        self.default_order = default_order

    def convert(self, value, to_order=None, from_order=None, decimals=None):
        try:
            to_order = self.default_order if not to_order else self.magnitudes[to_order]
            from_order = self.default_order if not from_order else self.magnitudes[from_order]
            if decimals is None:
                decimals = max(6, abs(to_order - from_order))
            return round(value / (self.base ** (to_order - from_order)), decimals)
        except KeyError:
            raise ValueError("to_order or from_order not recognzed: to={0} from={1}".format(to_order, from_order))

    def factor(self, order):
        return self.base ** self.magnitudes[order]

    def to_order(self, power):
        for order, p in self.magnitudes.items():
            if power == p:
                return order

        return None


class BaseMagnitudeUnit:
    def __init__(self, unit, orders):
        self.unit = unit
        self.orders = orders

    def transform(self, value, units=None, decimals=None):
        if units is None:
            return value

        units = units.strip()
        if ":" not in units:
            to_unit = ""
            from_unit = units
        else:
            from_unit, to_unit = units.split(":", 1)

        if to_unit.endswith(self.unit):
            to_unit = to_unit[0:-len(self.unit)]
        if from_unit.endswith(self.unit):
            from_unit = from_unit[0:-len(self.unit)]

        return self.orders.convert(value=value, to_order=to_unit, from_order=from_unit, decimals=decimals)
