#!/usr/bin/env python3
"""Validate the generation policy manifest; this does not test the viewer runtime."""
import json
from pathlib import Path
root = Path(__file__).resolve().parents[1]
doc = json.loads((root/"config/nexverse-generations.json").read_text(encoding="utf-8"))
assert doc["product"] == "TrixieStorm Viewer"
assert doc["policy"] == "stadt-nexverse-only"
assert doc["allow_custom_grids"] is False
assert doc["allow_external_grid_logins"] is False
assert doc["allow_outbound_external_hypergrid_teleports"] is False
gens = doc["generations"]
assert [g["id"] for g in gens] == ["gen1","gen2"]
assert [g["hostname"] for g in gens] == ["hg.stadt-nexverse.de","beta.stadt-nexverse.de"]
assert [g["release_channel"] for g in gens] == ["stable","beta"]
assert [g["state"] for g in gens] == ["current","future-disabled"]
for gen in gens:
    assert gen["login_uri"] is None and gen["login_uri_verified"] is False, "Endpoints require verification"
print("Generation policy manifest validated (no C++ enforcement implemented).")
