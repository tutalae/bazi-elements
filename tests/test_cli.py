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
    ["2000-13-45"],
    ["yesterday"],
    ["2000-01-01", "12:00", "--longitude", "100"],
    ["2000-01-01", "12:00", "--tz", "Not/AZone"],
])
def test_cli_errors(args):
    with pytest.raises(SystemExit):
        main(args)


def test_cli_city_and_explain(capsys):
    main(["1990-05-12", "14:30", "--city", "Bangkok", "--explain"])
    out = capsys.readouterr().out
    assert "Solar time used: 1990-05-12 14:15" in out
    assert "What your chart says" in out


def test_cli_unknown_city():
    with pytest.raises(SystemExit):
        main(["1990-05-12", "--city", "Atlantis"])


def test_guided_mode(monkeypatch, capsys):
    answers = iter(["not a date", "12/05/2533", "", "?", "เชียงใหม่", "f"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))
    main(["--lang", "th"])
    out = capsys.readouterr().out
    assert "แปลง พ.ศ. 2533 เป็น ค.ศ. 1990" in out
    assert "Chiang Mai" in out          # printed by the city list after "?"
    assert "ดวงของคุณบอกอะไร" in out    # guided mode always explains
    assert "เสายามจึงเป็นเพียงการคาดเดา" in out
