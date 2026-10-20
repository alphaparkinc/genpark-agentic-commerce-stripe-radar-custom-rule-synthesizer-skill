# Stripe Radar Custom Fraud Rules & Velocity Synthesizer Skill

[![GenPark Official](https://img.shields.io/badge/GenPark-Official%20Skill-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-blue)](https://www.linkedin.com/company/92955550)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-green)](https://modelcontextprotocol.io/)
[![Zero Dependency](https://img.shields.io/badge/Dependencies-Zero%20Stdlib-brightgreen)](https://python.org)

Automated merchant chargeback root-cause analysis, dynamic Stripe Radar / Adyen RevenueProtect risk rules synthesis, and false positive reducer. Built for GenPark (https://www.genpark.ai).

## 🌐 Official Channels
- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## 🛠️ MCP Tools Exposed
- `synthesize_stripe_radar_rules`: Generate concrete Stripe Radar rule syntax strings targeting identified fraud attack vectors (e.g. BIN velocity, country mismatch, high-risk email domains).
- `audit_rule_false_positive_impact`: Simulate transaction block rate and estimated gross merchant revenue loss caused by overly aggressive fraud rules.

## 🚀 Installation & Usage
Run directly with pure Python standard library:
```bash
python -m genpark_agentic_commerce_stripe_radar_custom_rule_synthesizer_skill.server --test
```
