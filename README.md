# 🛡️ bima-mcp — Kenya Insurance Intelligence MCP Server
<!-- mcp-name: io.github.gabrielmahia/bima-mcp -->

[![bima-mcp Glama score](https://glama.ai/mcp/servers/gabrielmahia/bima-mcp/badges/score.svg)](https://glama.ai/mcp/servers/gabrielmahia/bima-mcp)
[![smithery badge](https://smithery.ai/badge/@gabrielmahia/bima-mcp)](https://smithery.ai/server/@gabrielmahia/bima-mcp)


---
**Compatible with `claude-sonnet-5`** (released 2026-06-30) — Anthropic's most agentic
Sonnet yet. Runs multi-step tool chains end-to-end without stopping short.
Install: `pip install bima-mcp` · Use with any MCP client.

---


Insurance products exist — NHIF, parametric crop cover, microinsurance — but comparing them or checking eligibility requires navigating separate portals with no shared interface.

Exposes Kenya insurance data, NHIF coverage analysis, parametric crop risk scoring,
and microinsurance comparison through the Model Context Protocol.

## Why Insurance Infrastructure Matters

In mature economies, insurance is invisible infrastructure — it enables risk-taking by
capping downside. A farmer plants a new crop because crop insurance limits loss.
A parent starts a business because health insurance protects the family.
Without this floor, the rational choice is perpetual caution.

Kenya's insurance penetration: **2.3% of GDP** vs 8–11% in developed markets.
The gap is not cultural — it is the cost of distribution, claims verification,
and actuarial data. All three can be compressed by technology.

## Tools

| Tool | What it does |
|------|-------------|
| `kenya_insurance_products` | List IRA-registered products by type (health, life, crop, device) |
| `nhif_coverage_query` | Query NHIF benefits by hospital tier and procedure type |
| `premium_estimate` | Estimate monthly premiums for any coverage type + income bracket |
| `parametric_crop_risk` | NDMA-based crop insurance risk for smallholder farmers |
| `compare_microinsurance` | Compare affordable products by target group and budget |
| `community_pool_calculator` | Size a chama pooled insurance arrangement |

## Quick Start

```bash
pip install bima-mcp       # coming soon to PyPI
bima-mcp                   # starts the MCP server on stdio
```

## Claude Desktop Integration

```json
{
  "mcpServers": {
    "bima-mcp": {
      "command": "bima-mcp"
    }
  }
}
```

## Use Cases

- **Farmers**: "What crop insurance do I need for my 2-acre maize farm in Nakuru?"
- **Informal workers**: "What NHIF tier 4 inpatient coverage do I get for KES 500/month?"
- **Chama treasurers**: "How do I set up pooled hospitalization cover for 25 members?"
- **Researchers**: "Compare parametric crop insurance risk across Kenya counties"

## Research Basis

- ACRE Africa Parametric Crop Insurance Methodology (2023)
- Kenya IRA Annual Report 2024
- World Bank Insurance Primer for Low-Income Markets (2023)
- NDMA County Drought Monitoring Reports

## ⚠️ Disclaimers

> DEMO data — not real insurance products or binding quotes.
> Not affiliated with NHIF, IRA, or any insurance provider.
> Always consult a licensed IRA-registered insurance agent for actual products.
> Kenya IRA: ira.go.ke

---
*© 2026 Gabriel Mahia / AI Kung Fu LLC · MIT License*

## Part of the East Africa Coordination Stack

This MCP server is one of 32 tools in the Kenya coordination infrastructure.
It connects to [`africa-coord-bus`](https://github.com/gabrielmahia/africa-coord-bus) — the coordination
event bus that routes signals between domains automatically.

When this server detects a threshold condition, the bus notifies:
- `bima-mcp` — parametric insurance evaluation
- `kilimo-mcp` — agricultural advisory
- `afya-mcp` — health surveillance activation
- `county-mcp` — county office alert

```python
pip install africa-coord-bus
```

All servers: [pypi.org/user/gmahia](https://pypi.org/user/gmahia/)

## IP & Collaboration

MIT licensed. Feedback via GitHub Issues only — pull requests are not accepted. Demo data is labeled DEMO and is not suitable for operational decisions. Full policy: [docs/architecture/IP_POLICY.md](docs/architecture/IP_POLICY.md). Security reports: see [SECURITY.md](SECURITY.md).
