"""Guard: the NHIF scheme was repealed and replaced by SHA/SHIF in October 2024. These stale pointers must not return to the source."""
import pathlib

STALE = ("nhif.or.ke", "NHIF-accredited", "NHIF accredited", "NHIF offices", "NHIF office")


def test_no_stale_nhif_pointers_in_source():
    root = pathlib.Path(__file__).resolve().parents[1] / "src"
    found = [(str(f.relative_to(root)), s) for f in root.rglob("*.py") for s in STALE if s in f.read_text(encoding="utf-8")]
    assert not found, f"stale NHIF-era pointers: {found}"
