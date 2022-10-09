magorder
========
[![codecov](https://codecov.io/gh/russoz/magorder/branch/main/graph/badge.svg?token=URMPURMN8S)](https://codecov.io/gh/russoz/magorder)

This library streamlines the conversion between different orders of magnitude, like transforming nm (nanometers) to meters, or kilobytes to gigabytes.

It is meant to provide a drop-in mechanism that is simple and consistent to manipulate such conversions.

## Installation

Install it as usual:

    pip install magorder

## Dependencies

This library has no runtime dependencies.

## Usage

To use the library:

```python
# import the MagnitudeUnit class that meets your requirements
from magorder.stdsi import StdSIMagnitudeUnit

# create a magorder object, associated with an unit
mag = StdSIMagnitudeUnit("m")

# transform can convert from a different order of magnitude to the base unit
assert mag.transform(0.1, "km") == 100
assert mag.transform(100_000_000, "µm") == 100
assert mag.transform(100_000_000_000_000_000_000_000_000.0, "ym") == 100
assert mag.transform(0.0000000000000000000001, "Ym", decimals=3) == 100
```

Or to transform data units:

```python
from magorder.data import SIDataMagnitudeUnit, IECDataMagnitudeUnit

mags = SIDataMagnitudeUnit("b")
assert mags.transform(1, "kb") == 1000
assert mags.transform(1, from_unit="Gb", to_unit="kb") == 1_000_000

mags = IECDataMagnitudeUnit("b")
assert mags.transform(1, "Kib") == 1024
assert mags.transform(4096, from_unit="Mib", to_unit="Gib") == 4
```

See the module tests for more examples.

## License

Check the file [LICENSE](LICENSE).

## Contributions

Feel free to contribute to this code at:

[https://github.com/russoz/magorder](https://github.com/russoz/magorder)
