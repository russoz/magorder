# -*- coding: utf-8 -*-

# Copyright (c) 2022, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later


from typing import Optional, Sequence, Set

from .types import MagOrderListSpec, MagOrderSpec, Number

class MagnitudeOrder:
    """This class represents one order of magnitude."""

    def __init__(self, prefix: str, power: int, aliases: Optional[Sequence[str]] = None) -> None:
        """Create an object.

        Args:
            prefix (str): primary prefix for this order of magnitude. Examples: "c" for centimeters or "k" for kilograms.
            power (int): integer power of the base (usually 10) for this order of magnitude. Examples: 3 for "k" (from 10 ** 3), and -3 for "m" (from 10 ** -3).
            aliases (Optional[Sequence[str]], optional): List of prefix aliases. Defaults to ``None``. Examples: some systems won't display "µg" correctly, so we might use "ug" as an alias.
        """
        self.prefix = prefix
        self.power = power
        if aliases is None:
            aliases = []
        self.aliases = aliases
        self._matching = set(aliases).union({prefix})

    @property
    def prefixes(self) -> Set[str]:
        """All prefixes recognized by this magnitude order.

        Returns:
            Set[str]: a set containing the primary prefix and its aliases.
        """
        return set(self._matching)

    def match(self, prefix: str) -> bool:
        """Test whether a string is a valid prefix for this magnitude order.

        Args:
            prefix (str): string to be tested.

        Returns:
            bool: ``True`` if it is a valid prefix, ``False`` otherwise.
        """
        return prefix in self.prefixes

    def match_all(self, loc: MagOrderSpec) -> bool:
        """Test whether the parameter is a valid prefix or if it matches the
        power of the base for this order of magnitude.

        Args:
            loc (MagOrderSpec): string to be tested.

        Returns:
            bool: ``True`` if it is a valid prefix or power, ``False`` otherwise.
        """
        return loc in self.prefixes or loc == self.power


class MagnitudeSystem:
    """System allowing conversion between different magnitudes."""

    class MagnitudeDoesNotExist(ValueError):
        """Exception for when a magnitude order passed as a parameter does not exist."""
        def __init__(self, text: MagOrderSpec) -> None:
            """Create the exception object.

            Args:
                text (MagOrderSpec): the invalid specification for the magnitude order.
            """
            super().__init__(f"Cannot find magnitude order with '{text}'")


    class PrefixConflict(ValueError):
        """Exception for when a magnitude order declares an alias that clashes with
        a prefix (or alias) of another order of magnitude.
        """
        def __init__(self, prefix: str, alias: Optional[str] = None) -> None:
            """Create the exception object.

            Args:
                prefix (str): prefix causing the conflict.
                alias (Optional[str]): the offending alias, when applicable.
            """
            if alias is None:
                msg = f"Magnitude order '{prefix}' conflicts with existing magnitude order"
            else:
                msg = f"Alias '{alias}' for magnitude order '{prefix}' conflicts with existing magnitude order"
            super().__init__(msg)


    def __init__(self, magnitudes_spec: MagOrderListSpec,
                 lower: Optional[MagOrderSpec] = None,
                 upper: Optional[MagOrderSpec] = None,
                 base: int = 10, default: str = ""):
        """Create an object.

        Args:
            magnitudes (MagOrderListSpec): list of dictionaries, each specifying one order of magnitude.
            lower (Optional[MagOrderSpec], optional): smaller order of magnitude allowed. Defaults to the smaller one in ``magnitudes``.
            upper (Optional[MagOrderSpec], optional): largest order of magnitude allowed. Defaults to the largest one in ``magnitudes``.
            base (int, optional): base number used to apply the magnitude order's powers. Defaults to 10.
            default_power (int, optional): default power of the base to be used when not specified in transformations. Defaults to 0.

        Raises:
            self.MagnitudeDoesNotExist: raised if any of the specified lower or upper bounds does not exist.
            self.PrefixConflict: raised if the magnitudes specs contains conflicts.
        """
        mags = [MagnitudeOrder(**kw) for kw in magnitudes_spec]

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
        self._prefix_mag_map = {}
        for m in mags:
            if m.prefix in self._prefix_mag_map:
                raise self.PrefixConflict(m.prefix)
            self._prefix_mag_map[m.prefix] = m
            for a in m.aliases:
                if a in self._prefix_mag_map and self._prefix_mag_map[a] != m:
                    raise self.PrefixConflict(m.prefix, a)
                self._prefix_mag_map[a] = m
        self.base = base
        self.default = default

    def magnitude_by_prefix(self, prefix: str) -> "MagnitudeOrder":
        """Return the MagnitudeOrder object matching a prefix.

        Args:
            prefix (str): magnitude order's prefix to be matched.

        Raises:
            self.MagnitudeDoesNotExist: raised if the prefix does not exist.

        Returns:
            MagnitudeOrder: the MagnitudeOrder object corresponding the specified prefix.
        """
        try:
            return self._prefix_mag_map[prefix]
        except KeyError:
            raise self.MagnitudeDoesNotExist(prefix)

    def convert(self, value: Number,
                from_order: Optional[str] = None,
                to_order: Optional[str] = None,
                decimals: Optional[int] = None) -> float:
        """Convert a value between two specified magnitude orders.

        Args:
            value (Number): number to be converted.
            from_order (Optional[str], optional): prefix for the targeted order of magnitude. Defaults to the prefix matching the ``default_order``.
            to_order (Optional[str], optional): prefix for the value's original order of magnitude. Defaults to the prefix matching the ``default_order``.
            decimals (Optional[int], optional): result is rounded to mitigate floating-point errors. Defaults to the greater of 6 and the absolute difference between the two magnitude's powers.

        Returns:
            float: the value converted to
        """
        to_order_power = self.magnitude_by_prefix(to_order if to_order else self.default).power
        from_order_power = self.magnitude_by_prefix(from_order if from_order else self.default).power
        if to_order_power == from_order_power:
            return value
        if decimals is None:
            decimals = max(6, abs(to_order_power - from_order_power))
        return round(value / (self.base ** (to_order_power - from_order_power)), decimals)

    def factor(self, prefix: str) -> Number:
        """Return the multiplication factor for a specific prefix.

        Args:
            prefix (str): magnitude prefix for which to calculate the multiplication factor (base to the prefix's power).

        Returns:
            Number: the multiplication factor for the prefix.
        """
        return self.base ** self.magnitude_by_prefix(prefix).power

    def to_prefix(self, power: int) -> Optional[str]:
        """Return the primary prefix for a specific power of base.

        Args:
            power (int): value of the power to be converted.

        Returns:
            Optional[str]: primary prefix for the specified power, or ``None`` if there's no magnitude for that value of power.
        """
        for m in self.magnitudes:
            if power == m.power:
                return m.prefix
        return None


class MagnitudeUnit:
    """Base class for magnitude-aware unit."""
    class UnknownUnit(ValueError):
        """Exception for when a unit passed as parameter is not known."""
        def __init__(self, unit: str) -> None:
            """Create the exception object.

            Args:
                unit (str): offending unit parameter.
            """
            super().__init__(f"Unknown unit '{unit}'")

    def __init__(self, base_unit: str, mag_sys: MagnitudeSystem):
        """Create the object.

        Args:
            base_unit (str): base unit for this system. Examples: "m", "g".
            mag_sys (MagnitudeSystem): magnitude system to be used with the base unit.
        """
        self.base_unit = base_unit
        self.mag_sys = mag_sys

    def transform(self, value: Number,
                  from_unit: Optional[str] = None,
                  to_unit: Optional[str] = None,
                  decimals: Optional[int] = None) -> float:
        """Transform a value from one prefixed unit to another.

        Args:
            value (Number): value to be transofrmed.
            from_unit (Optional[str], optional): prefixed unit to transform from. Defaults to the object's base_unit.
            to_unit (Optional[str], optional): prefixed unit to transform to. Defaults to the object's base_unit.
            decimals (Optional[int], optional): _description_. Defaults to None.

        Raises:
            self.UnknownUnit: raised if any of from_unit or to_unit is not recognized.

        Returns:
            float: value in the target unit.
        """
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

        return self.mag_sys.convert(value=value, to_order=to_unit, from_order=from_unit, decimals=decimals)

# code: language=python tabSize=4
