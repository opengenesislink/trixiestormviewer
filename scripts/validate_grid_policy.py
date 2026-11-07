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
gen1, gen2 = gens
assert gen1["login_uri"] == "http://hg.stadt-nexverse.de:80/"
assert gen1["login_uri_verified"] is False, "Live Gen1 authentication is not verified"
assert gen1["credential_transport_tls"] is False
assert gen1["discovery_url"] == "http://hg.stadt-nexverse.de:80/ogl/v1/grid-info"
assert gen2["login_uri"] is None
assert gen2["login_uri_verified"] is False
assert gen2["state"] == "future-disabled"
assert gen2["credential_transport_tls"] is None
print("Generation manifest validated: G1 pinned, unverified HTTP; G2 disabled.")
