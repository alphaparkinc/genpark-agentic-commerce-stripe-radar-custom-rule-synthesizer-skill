# -*- coding: utf-8 -*-
"""MCP Server for Stripe Radar Custom Fraud Rules & Velocity Synthesizer Skill."""
import sys
import json
import logging
from typing import Dict, Any

from .core import StripeRadarCustomRuleSynthesizer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

TOOLS_SCHEMA = [
    {
        "name": "synthesize_stripe_radar_rules",
        "description": "Generate concrete Stripe Radar rule syntax strings targeting identified fraud attack vectors (e.g. BIN velocity, country mismatch, high-risk email domains).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "attack_pattern": {
                    "type": "string",
                    "enum": [
                        "CARD_TESTING_VELOCITY",
                        "PROXY_TOR_IP",
                        "COUNTRY_MISMATCH_HIGH_TICKET",
                        "DISPOSABLE_EMAIL_RUSH"
                    ]
                },
                "velocity_window_hours": {
                    "type": "integer"
                },
                "max_allowed_attempts": {
                    "type": "integer"
                },
                "risk_score_threshold": {
                    "type": "integer"
                }
            },
            "required": [
                "attack_pattern"
            ]
        }
    },
    {
        "name": "audit_rule_false_positive_impact",
        "description": "Simulate transaction block rate and estimated gross merchant revenue loss caused by overly aggressive fraud rules.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "monthly_gmv_usd": {
                    "type": "number"
                },
                "monthly_order_count": {
                    "type": "integer"
                },
                "estimated_blocked_tx_rate_pct": {
                    "type": "number"
                },
                "chargeback_rate_reduction_bps": {
                    "type": "integer"
                }
            },
            "required": [
                "monthly_gmv_usd",
                "monthly_order_count",
                "estimated_blocked_tx_rate_pct",
                "chargeback_rate_reduction_bps"
            ]
        }
    }
]

def handle_rpc(line: str) -> str:
    try:
        req = json.loads(line)
        method = req.get("method")
        msg_id = req.get("id")

        if method == "initialize":
            res = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-stripe-radar-custom-rule-synthesizer-skill", "version": "1.0.0"}
            }
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": res})

        elif method == "tools/list":
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS_SCHEMA}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            target_func = getattr(StripeRadarCustomRuleSynthesizer, tool_name, None)
            if not target_func:
                return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {tool_name}"}})

            result = target_func(**args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                }
            })

        else:
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {method}"}})

    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "id": req.get("id") if "req" in locals() else None, "error": {"code": -32000, "message": str(e)}})

def run_test():
    print("[TEST] Running internal RPC self-test for genpark-agentic-commerce-stripe-radar-custom-rule-synthesizer-skill...")
    init_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    init_res = json.loads(handle_rpc(init_req))
    assert init_res.get("result", {}).get("serverInfo", {}).get("name") == "genpark-agentic-commerce-stripe-radar-custom-rule-synthesizer-skill"

    list_req = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    list_res = json.loads(handle_rpc(list_req))
    assert len(list_res.get("result", {}).get("tools", [])) == 2
    print(f"[TEST] SUCCESS: {len(list_res['result']['tools'])} tools verified.")
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        if run_test():
            sys.exit(0)
        sys.exit(1)

    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
