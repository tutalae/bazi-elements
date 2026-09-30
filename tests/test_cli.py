import json

import pytest

from bazi_elements.cli import main


def test_cli_text(capsys):
    main(["2000-01-01", "12:00"])
    out = capsys.readouterr().out
    assert "Day Master: Yang Earth" in out
    assert "Six Clash 六冲: 子午" in out


def test_cli_thai(capsys):
    main(["2000-01-01", "12:00", "--lang", "th", "--gender", "female"])
    out = capsys.readouterr().out
    assert "ธาตุประจำตัว: ดินหยาง" in out
    assert "วัยจร" in out


def test_cli_json(capsys):
    main(["2000-01-01", "12:00", "--json", "--tz", "Asia/Bangkok", "--longitude", "100.5"])
    data = json.loads(capsys.readouterr().out)
    assert data["day_master"] == "Yang Earth"
    assert data["chart_time"] == "2000-01-01 11:38"  # 11:42 mean solar time, -3.3 min equation of time
    assert data["strength"]["verdict"] in ("Strong", "Weak")


@pytest.mark.parametrize("args", [
    ["01/01/2000"],
    ["2000-01-01", "12:00", "--longitude", "100"],
    ["2000-01-01", "12:00", "--tz", "Not/AZone"],
])
def test_cli_errors(args):
    with pytest.raises(SystemExit):
        main(args)
