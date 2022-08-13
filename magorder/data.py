# -*- coding: utf-8 -*-

# Copyright (c) 2022, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from .base import BaseMagnitudeOrder, BaseMagnitudeUnit


class SIDataMagnitudeUnit(BaseMagnitudeUnit):
    si_order = {
        "": 0,
        "k": 1,
        "M": 2,
        "G": 3,
        "T": 4,
        "P": 5,
        "E": 6,
        "Z": 7,
        "Y": 8,
    }

    def __init__(self, unit, lower=None, upper=None):
        orders = BaseMagnitudeOrder(self.si_order, lower=lower, upper=upper, base=1000)
        super().__init__(unit, orders)


class IECDataMagnitudeUnit(BaseMagnitudeUnit):
    iec_order = {
        "": 0,
        "Ki": 1,
        "Mi": 2,
        "Gi": 3,
        "Ti": 4,
        "Pi": 5,
        "Ei": 6,
        "Zi": 7,
        "Yi": 8,
    }

    def __init__(self, unit, lower=None, upper=None, legacy=False, case=True):
        self.case = case
        orders = dict(self.iec_order)
        if legacy:
            orders.update({"K": 1, "M": 2, "G": 3})
        if not case:
            orders = dict((k.lower(), v) for k, v in orders.items())
        orders = BaseMagnitudeOrder(orders, lower=lower, upper=upper, base=1024)
        super().__init__(unit, orders)

    def transform(self, value, units=None):
        if not self.case and units is not None:
            units = units.lower()
        return super().transform(value, units)
