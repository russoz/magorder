magorder
========

This library streamlines the conversion of different multipliers, like transforming nm (nanometers) to meters, or kilobytes to gigabytes.

It is meant to take the load off the developer of larger applications.

## Installation

Install it as usual:

    pip install magorder

## Dependencies

This library has no runtime dependencies.

## Usage

To use the library in some other code:

```python
from magorder.stdsi import StdSIMagnitudeUnit

mag = StdSIMagnitudeUnit("m")
assert mag.transform(0.1, "km") == 100
assert mag.transform(100_000_000, "µm") == 100
assert mag.transform(100_000_000_000_000_000_000_000_000.0, "ym") == 100
assert mag.transform(0.0000000000000000000001, "Ym", 3) == 100
```

Or to transform data units:

```python
from magorder.data import SIDataMagnitudeUnit, IECDataMagnitudeUnit

mags = SIDataMagnitudeUnit("b")
assert mags.transform(1, "kb") == 1000
assert mags.transform(1, "Gb:kb") == 1_000_000

mags = IECDataMagnitudeUnit("b")
assert mags.transform(1, "Kib") == 1024
assert mags.transform(4096, "Mib:Gib") == 4
```

See the module tests for more examples.

## License

Check the file [LICENSE](LICENSE).

## Contributions

Feel free to contribute to this code at:

[https://github.com/russoz/magorder](https://github.com/russoz/magorder)
