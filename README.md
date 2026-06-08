# 🛡️ bima-mcp — Kenya Insurance Intelligence MCP Server

**First insurance intelligence MCP server for East Africa.**

Exposes Kenya insurance data, NHIF coverage analysis, parametric crop risk scoring, and microinsurance comparison through the Model Context Protocol.

## Western Parallel

In the US and UK, insurance APIs and comparison tools (Policygenius, Lemonade API, Root Insurance, The Zebra) have lowered the barrier to insurance access and literacy. bima-mcp brings that intelligence layer to the East African market.

**The gap:** Kenya insurance penetration is ~2.3% of GDP vs 8–11% in developed markets (IRA Annual Report 2024). The barrier is access, literacy, and distribution — not demand.

## Tools

| Tool | What it does |
|------|-------------|
| `kenya_insurance_products` | List IRA-registered products by type (health, life, crop, device) |
| `nhif_coverage_query` | Query NHIF benefits by hospital tier and procedure type |
| `premium_estimate` | Estimate monthly premiums for any coverage type |
| `parametric_crop_risk` | Calculate NDMA-based crop insurance risk for smallholder farmers |
| `compare_microinsurance` | Compare affordable products by target group and budget |
| `community_pool_calculator` | Size a chama (savings group) pooled insurance arrangement |

## Quick Start

```bash
pip install bima-mcp
bima-mcp  # starts the MCP server on stdio
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
- **Chama treasurers**: "How do I set up pooled hospitalization cover for 25 members at KES 300 each?"
- **Researchers**: "Compare parametric crop insurance risk across Kenya counties"

## Research Basis

- ACRE Africa Parametric Crop Insurance Methodology (2023)
- Kenya IRA Annual Report 2024
- World Bank Insurance Primer for Low-Income Markets
- NDMA County Drought Monitoring Reports
- Pula Advisors Smallholder Insurance Framework

## ⚠️ Important Disclaimers

> DEMO data only — not real insurance products or binding quotes.  
> Not affiliated with NHIF, IRA, ACRE Africa, Pula Advisors, or Turaco.  
> Always consult a licensed IRA-registered insurance agent for actual products.  
> Kenya IRA: ira.go.ke · +254 20 499 0000

---
*© 2026 Gabriel Mahia / AI Kung Fu LLC · MIT License*  
*Inspired by the insight of Kenbright Insurance CEO on structural support systems for East Africa*
