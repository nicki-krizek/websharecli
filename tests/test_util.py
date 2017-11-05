from websharecli.util import bytes2human


def test_bytes2human():
    assert bytes2human(900) == '900B'
    assert bytes2human(1023) == '1.0K'
    assert bytes2human(5930) == '5.8K'
    assert bytes2human(492304219) == '469M'
    assert bytes2human(1644360134) == '1.5G'
    assert bytes2human(29644360134) == ' 28G'
