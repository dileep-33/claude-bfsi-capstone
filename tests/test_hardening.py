"""Hardening tests: PCI masking, KYC block, geo signals, routing log, caching."""
import json
from pathlib import Path

import pytest

from bfsi.mcp import registry
from bfsi.compliance.pipeline import run_compliance
from bfsi.chatbot import sanitize
from bfsi.model_router import route
from bfsi.skills_loader import build_cached_system, load_skills


def test_pan_is_masked_in_audit_args():
    masked = registry._mask({"card_number": "4111111111111111", "account_id": "AC5001"})
    assert masked["card_number"] == "****1111"
    assert masked["account_id"] == "AC5001"


def test_unknown_customer_blocked_at_kyc():
    d = run_compliance("C9999", "Nobody", 100.0, "IN")
    assert d["decision"] == "BLOCK"
    assert d["failed_stage"] == "KYC"


def test_geo_mismatch_signal_via_mcp():
    r = registry.call("customer-info", "verify_ip_location",
                      customer_id="C5001", ip_country="RU")
    assert r["geo_mismatch"] is True


def test_unknown_mcp_tool_rejected():
    with pytest.raises(KeyError):
        registry.call("banking-api", "delete_everything")


def test_sanitize_strips_control_chars_and_truncates():
    assert "\x00" not in sanitize("hello\x00world")
    assert len(sanitize("a" * 5000)) <= 2000


def test_model_router_logs_rationale():
    model = route("decide", "TEST-ROUTE")
    last = json.loads(Path("audit_log/model_routing.jsonl").read_text().splitlines()[-1])
    assert last["request_id"] == "TEST-ROUTE"
    assert last["rationale"] and last["model"] == model


def test_skills_library_is_cached():
    assert len(load_skills()) == 6
    assert build_cached_system()[0]["cache_control"]["type"] == "ephemeral"
