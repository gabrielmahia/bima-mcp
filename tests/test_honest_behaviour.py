from bima_mcp import main as server

_fn = lambda name: (getattr(server, name).fn if hasattr(getattr(server, name), "fn") else getattr(server, name))


def test_unknown_county_and_crop_are_flagged_as_defaults_not_presented_as_data():
    r = _fn("parametric_crop_risk")("Atlantis", "moonberries", 2.0, "long_rains")
    assert r["county_in_table"] is False and r["crop_in_table"] is False
    assert _fn("parametric_crop_risk")("Turkana", "maize", 2.0, "long_rains")["county_in_table"] is True


def test_the_nhif_coverage_tool_says_its_figures_are_outdated_and_flags_a_defaulted_tier():
    r = _fn("nhif_coverage_query")("level_99", "inpatient")
    assert r["tier_applied"] == "level_4" and "replaced by SHA" in r["deprecated"]
