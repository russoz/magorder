# -*- coding: utf-8 -*-

# Copyright (c) 2022, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from magorder.stdsi import StdSIMagnitudeUnit


def test_mag_unit_invalid_units():
    mag = StdSIMagnitudeUnit("m")
    with pytest.raises(ValueError):
        mag.transform(23, from_unit="xxm")
    with pytest.raises(ValueError):
        mag.transform(23, to_unit="xxm")
