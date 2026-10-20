# -*- coding: utf-8 -*-
"""Stripe Radar Custom Fraud Rules & Velocity Synthesizer for GenPark Agentic Commerce."""
import json
from typing import Dict, Any

class StripeRadarCustomRuleSynthesizer:
    """Automated Stripe Radar rule syntax compiler and merchant revenue protector."""

    @staticmethod
    def synthesize_stripe_radar_rules(attack_pattern: str, velocity_window_hours: int = 1, max_allowed_attempts: int = 3, risk_score_threshold: int = 75) -> Dict[str, Any]:
        """Synthesize official Stripe Radar predicate strings."""
        if attack_pattern == "CARD_TESTING_VELOCITY":
            rule_type = "BLOCK"
            predicate = f":count(charge:card:number, {velocity_window_hours}h) > {max_allowed_attempts}"
            reason = "Mitigate card-testing micro-authorization botnets."
        elif attack_pattern == "PROXY_TOR_IP":
            rule_type = "CHALLENGE_3DS"
            predicate = ":ip_is_anonymous_vpn: OR :ip_is_tor: OR :risk_score: > 65"
            reason = "Force biometric 3DS authentication on anonymized proxies."
        elif attack_pattern == "COUNTRY_MISMATCH_HIGH_TICKET":
            rule_type = "REVIEW"
            predicate = f":amount_in_usd: > 500 AND :card_country: != :ip_country: AND :risk_score: > {risk_score_threshold}"
            reason = "Queue cross-border high-ticket orders for human underwriting."
        else:
            rule_type = "BLOCK"
            predicate = ":is_disposable_email: AND :risk_score: > 70"
            reason = "Reject burner email addresses with elevated ML risk score."

        return {
            "attack_pattern": attack_pattern,
            "action": rule_type,
            "radar_rule_syntax": f"{rule_type.lower()} if {predicate}",
            "predicate_expression": predicate,
            "security_objective": reason,
            "deployment_instruction": "Paste expression into Stripe Dashboard -> Radar -> Rules -> Add Rule."
        }

    @staticmethod
    def audit_rule_false_positive_impact(monthly_gmv_usd: float, monthly_order_count: int, estimated_blocked_tx_rate_pct: float, chargeback_rate_reduction_bps: int) -> Dict[str, Any]:
        """Compare revenue blocked vs chargeback fees and dispute losses saved."""
        blocked_gmv = monthly_gmv_usd * (estimated_blocked_tx_rate_pct / 100.0)
        # Assume 80% of blocked transactions were false positives (legitimate buyers rejected)
        lost_good_gmv = blocked_gmv * 0.80
        # Chargeback savings (basis points * GMV)
        dispute_savings = monthly_gmv_usd * (chargeback_rate_reduction_bps / 10000.0)
        net_impact = dispute_savings - lost_good_gmv

        return {
            "monthly_gmv_usd": monthly_gmv_usd,
            "blocked_gmv_usd": round(blocked_gmv, 2),
            "estimated_false_positive_loss_usd": round(lost_good_gmv, 2),
            "chargeback_loss_reduction_usd": round(dispute_savings, 2),
            "net_revenue_impact_usd": round(net_impact, 2),
            "verdict": "OPTIMAL_HEALTH" if net_impact >= 0 else "TOO_RESTRICTIVE_SWITCH_TO_3DS",
            "tuning_advice": "Convert hard BLOCK rules to CHALLENGE (Request 3D Secure) to recover false positives without chargeback risk."
        }
