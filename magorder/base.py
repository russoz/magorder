# -*- coding: utf-8 -*-

# Copyright (c) 2022, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later


from typing import Optional, Sequence

from .types import MagOrderListSpec, MagOrderSpec, Number


class MagnitudeOrder:
    def __init__(self, prefix: str, power: int, aliases: Optional[Sequence[str]] = None) -> None:
        self.prefix = prefix
        self.power = power
        if aliases is None:
            aliases = []
        self.aliases = aliases
        self._matching = set(aliases).union({prefix})

    @property
    def symbols(self):
        return set(self._matching)

    def match(self, text: str) -> bool:
        return text in self._matching

    def match_all(self, text: MagOrderSpec) -> bool:
        return text in self._matching or text == self.power


class BaseMagnitudeOrder:
    """Base class for calculating orders of magnitude.
    """

    class MagnitudeDoesNotExist(ValueError):
        def __init__(self, text: MagOrderSpec) -> None:
            super().__init__(f"Cannot find magnitude order with '{text}'")


    class AliasConflict(ValueError):
        def __init__(self, alias: str, prefix: str) -> None:
            super().__init__(f"Alias '{alias}' for magnitude order '{prefix}' conflicts with existing magnitude order")


    def __init__(self, magnitudes: MagOrderListSpec,
                 lower: Optional[MagOrderSpec] = None,
                 upper: Optional[MagOrderSpec] = None,
                 base: int = 10, default_power: int = 0):
        mags = [MagnitudeOrder(**kw) for kw in magnitudes]

        lower_power = mags[0].power
        if lower is not None:
            lower_power = [m for m in mags if m.match_all(lower)]
            if not lower_power:
                raise self.MagnitudeDoesNotExist(lower)
            lower_power = lower_power[0].power

        upper_power = mags[-1].power
        if upper is not None:
            upper_power = [m for m in mags if m.match_all(upper)]
            if not upper_power:
                raise self.MagnitudeDoesNotExist(upper)
            upper_power = upper_power[0].power

        mags = [m for m in mags if lower_power <= m.power <= upper_power]

        self.magnitudes = mags
        self._mags_dict = {m.prefix: m for m in mags}
        for m in mags:
            for a in m.aliases:
                if a in self._mags_dict and self._mags_dict[a] != m:
                    raise self.AliasConflict(a, m.prefix)
                self._mags_dict[a] = m
        self.base = base
        self.default_power = default_power

    def magnitude_by_prefix(self, prefix: str) -> "MagnitudeOrder":
        try:
            return self._mags_dict[prefix]
        except KeyError:
            raise self.MagnitudeDoesNotExist(prefix)

    def convert(self, value: Number,
                to_order: Optional[str] = None,
                from_order: Optional[str] = None,
                decimals: Optional[int] = None) -> float:
        to_order_power = self.default_power if not to_order else self.magnitude_by_prefix(to_order).power
        from_order_power = self.default_power if not from_order else self.magnitude_by_prefix(from_order).power
        if decimals is None:
            decimals = max(6, abs(to_order_power - from_order_power))
        return round(value / (self.base ** (to_order_power - from_order_power)), decimals)

    def factor(self, prefix) -> Number:
        return self.base ** self.magnitude_by_prefix(prefix).power

    def to_prefix(self, power: int) -> Optional[str]:
        for m in self.magnitudes:
            if power == m.power:
                return m.prefix
        return None


class BaseMagnitudeUnit:
    class UnknownUnit(ValueError):
        def __init__(self, unit: str) -> None:
            super().__init__(f"Unknown unit '{unit}'")

    def __init__(self, base_unit: str, orders: BaseMagnitudeOrder):
        self.base_unit = base_unit
        self.orders = orders

    def transform(self, value: Number, from_unit: Optional[str] = None, to_unit: Optional[str] = None, decimals: Optional[int] = None):
        if from_unit is None:
            from_unit = self.base_unit
        if to_unit is None:
            to_unit = self.base_unit

        if not from_unit.endswith(self.base_unit):
            raise self.UnknownUnit(from_unit)
        from_unit = from_unit[0:-len(self.base_unit)]

        if not to_unit.endswith(self.base_unit):
            raise self.UnknownUnit(to_unit)
        to_unit = to_unit[0:-len(self.base_unit)]

        return self.orders.convert(value=value, to_order=to_unit, from_order=from_unit, decimals=decimals)

# code: language=python tabSize=4
