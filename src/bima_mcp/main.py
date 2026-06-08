#!/usr/bin/env python3
# bima-mcp — Kenya Insurance Intelligence MCP Server
# © 2026 Gabriel Mahia / AI Kung Fu LLC — MIT License
#
# Western parallel: Lemonade API, Root Insurance, Policygenius, ACRE Africa parametric methodology
# East Africa context: Insurance penetration ~2.3% GDP vs 8-11% in developed markets
# Source: Kenya IRA Annual Report 2024, World Bank FinSAT database
#
# TRUST INTEGRITY: All data is DEMO / synthetic unless explicitly marked otherwise.
# No real insurance products, premiums, or coverages are implied.
# Always consult a licensed IRA-registered insurance agent for actual products.
# =============================================================================

from __future__ import annotations
import json
import datetime
from typing import Annotated
from fastmcp import FastMCP

mcp = FastMCP(
    name="bima-mcp",
    instructions="""Kenya insurance intelligence MCP server.
    Provides tools for exploring insurance products, NHIF coverage, premium estimation,
    parametric crop risk, and microinsurance comparison for the East African market.
    
    IMPORTANT: All data is DEMO/synthetic for educational purposes.
    Not affiliated with any insurer or the Kenya IRA.
    Always consult a licensed insurance agent for actual products and pricing.
    """,
)

# ── DEMO DATASET: Kenya Insurance Products ─────────────────────────────────────
_PRODUCTS = [
    {
        "id": "NHIF-001", "type": "health", "provider": "NHIF (National Hospital Insurance Fund)",
        "name": "NHIF Individual Cover", "monthly_premium_kes": 500,
        "coverage": "Inpatient + Outpatient (select facilities)", "regulatory_body": "NHIF Board",
        "mpesa_paybill": "200222", "target": "Employed individuals (PAYE deduction)",
        "source": "DEMO — Synthetic. Reference: nhif.or.ke",
    },
    {
        "id": "NHIF-002", "type": "health", "provider": "NHIF",
        "name": "NHIF Voluntary Cover", "monthly_premium_kes": 500,
        "coverage": "Inpatient (Level 2–6 hospitals)", "regulatory_body": "NHIF Board",
        "mpesa_paybill": "200222", "target": "Self-employed, informal sector",
        "source": "DEMO — Synthetic. Reference: nhif.or.ke",
    },
    {
        "id": "MBELE-001", "type": "life", "provider": "Jubilee Life Insurance",
        "name": "Mbele Savings Plan", "monthly_premium_kes": 1000,
        "coverage": "Life cover + savings maturity benefit", "regulatory_body": "Kenya IRA",
        "mpesa_paybill": "220000", "target": "Working adults 18–60",
        "source": "DEMO — Synthetic. Reference: jubaileealife.com",
    },
    {
        "id": "PULA-001", "type": "crop", "provider": "Pula Advisors",
        "name": "Pula Smallholder Crop Insurance", "monthly_premium_kes": 0,
        "coverage": "Area-based yield index — pays if county yield < trigger",
        "regulatory_body": "Kenya IRA", "mpesa_paybill": "N/A",
        "target": "Smallholder farmers (KALRO partnership)", "min_acreage": 0.1,
        "source": "DEMO — Synthetic. Reference: pula-advisors.com",
    },
    {
        "id": "ACRE-001", "type": "crop", "provider": "ACRE Africa",
        "name": "ACRE Maize Cover", "monthly_premium_kes": 0,
        "coverage": "Satellite NDVI + rainfall index trigger, pays via M-PESA",
        "regulatory_body": "Kenya IRA", "mpesa_paybill": "N/A",
        "target": "Maize smallholders, bundled with input loans",
        "source": "DEMO — Synthetic. Reference: acreafrica.com",
    },
    {
        "id": "TURACO-001", "type": "health", "provider": "Turaco",
        "name": "Turaco Afya Cover", "monthly_premium_kes": 200,
        "coverage": "Inpatient hospitalization up to KES 100,000",
        "regulatory_body": "Kenya IRA", "mpesa_paybill": "4018228",
        "target": "Informal workers, gig economy", "min_age": 18, "max_age": 65,
        "source": "DEMO — Synthetic. Reference: turaco.io",
    },
    {
        "id": "BIMA-001", "type": "device", "provider": "Airtel x Jubilee",
        "name": "Bima ya Simu (Device Insurance)", "monthly_premium_kes": 100,
        "coverage": "Smartphone theft/damage up to device value", "regulatory_body": "Kenya IRA",
        "mpesa_paybill": "N/A", "target": "Mobile phone owners",
        "source": "DEMO — Synthetic. Based on bundled airtime insurance models",
    },
]

# ── DEMO: NDMA Drought History by County ──────────────────────────────────────
_NDMA_DROUGHT = {
    "Turkana": {"drought_frequency_pct": 85, "phase": "Crisis", "last_drought": "2023"},
    "Marsabit": {"drought_frequency_pct": 75, "phase": "Emergency", "last_drought": "2022"},
    "Mandera": {"drought_frequency_pct": 80, "phase": "Crisis", "last_drought": "2023"},
    "Wajir": {"drought_frequency_pct": 78, "phase": "Crisis", "last_drought": "2023"},
    "Garissa": {"drought_frequency_pct": 72, "phase": "Alert", "last_drought": "2022"},
    "Isiolo": {"drought_frequency_pct": 65, "phase": "Alert", "last_drought": "2022"},
    "Kajiado": {"drought_frequency_pct": 45, "phase": "Stressed", "last_drought": "2021"},
    "Machakos": {"drought_frequency_pct": 40, "phase": "Stressed", "last_drought": "2021"},
    "Kitui": {"drought_frequency_pct": 55, "phase": "Alert", "last_drought": "2022"},
    "Makueni": {"drought_frequency_pct": 50, "phase": "Stressed", "last_drought": "2021"},
    "Nairobi": {"drought_frequency_pct": 10, "phase": "Minimal", "last_drought": "2009"},
    "Kiambu": {"drought_frequency_pct": 15, "phase": "Minimal", "last_drought": "2011"},
    "Nakuru": {"drought_frequency_pct": 25, "phase": "Stressed", "last_drought": "2019"},
    "Kisumu": {"drought_frequency_pct": 20, "phase": "Minimal", "last_drought": "2016"},
    "Mombasa": {"drought_frequency_pct": 18, "phase": "Minimal", "last_drought": "2017"},
    "Uasin Gishu": {"drought_frequency_pct": 20, "phase": "Minimal", "last_drought": "2016"},
    "Trans Nzoia": {"drought_frequency_pct": 15, "phase": "Minimal", "last_drought": "2014"},
    "Nyandarua": {"drought_frequency_pct": 12, "phase": "Minimal", "last_drought": "2012"},
    "Nyeri": {"drought_frequency_pct": 18, "phase": "Minimal", "last_drought": "2015"},
    "Kakamega": {"drought_frequency_pct": 12, "phase": "Minimal", "last_drought": "2013"},
}

_CROP_RISK_MULTIPLIERS = {
    "maize": 1.0, "beans": 0.9, "potatoes": 0.8, "wheat": 0.85, "sorghum": 0.7,
    "millet": 0.65, "cassava": 0.6, "tea": 0.5, "coffee": 0.55, "cotton": 0.95,
}

def _audit(tool: str, params: dict, result: str):
    ts = datetime.datetime.utcnow().isoformat()
    entry = {"ts": ts, "tool": tool, "params": params, "result": result, "source": "bima-mcp"}
    return entry


@mcp.tool(
    description=(
        "List Kenya insurance product categories and representative products. "
        "Returns DEMO synthetic data for educational/research purposes. "
        "Not real insurance products or binding quotes."
    ),
    annotations={"readOnlyHint": True},
)
def kenya_insurance_products(
    product_type: Annotated[str, "Filter by type: health, life, crop, device, or 'all'"] = "all",
) -> dict:
    _audit("kenya_insurance_products", {"product_type": product_type}, "OK")
    products = _PRODUCTS if product_type == "all" else [
        p for p in _PRODUCTS if p.get("type") == product_type.lower()
    ]
    return {
        "status": "OK",
        "products": products,
        "count": len(products),
        "note": "DEMO — Synthetic data for educational purposes. Verify at ira.go.ke before advising clients.",
        "regulatory_body": "Insurance Regulatory Authority (IRA) Kenya — ira.go.ke",
        "source": "bima-mcp synthetic dataset, 2026. Reference: IRA Annual Report 2024, NHIF, ACRE Africa.",
    }


@mcp.tool(
    description=(
        "Query NHIF (National Hospital Insurance Fund) coverage details by hospital tier and procedure. "
        "NHIF is Kenya's state health insurer, analogous to Medicare in the US or NHS in the UK. "
        "DEMO data — verify at nhif.or.ke."
    ),
    annotations={"readOnlyHint": True},
)
def nhif_coverage_query(
    tier: Annotated[str, "Hospital tier: level_2, level_3, level_4, level_5, level_6"] = "level_4",
    procedure_type: Annotated[str, "Procedure type: inpatient, outpatient, maternity, renal, cancer, mental_health"] = "inpatient",
) -> dict:
    _audit("nhif_coverage_query", {"tier": tier, "procedure_type": procedure_type}, "OK")
    
    NHIF_BENEFITS = {
        "level_2": {"inpatient": 1800, "outpatient": 0, "maternity": 2500, "renal": 0, "cancer": 0},
        "level_3": {"inpatient": 2500, "outpatient": 0, "maternity": 5000, "renal": 2500, "cancer": 0},
        "level_4": {"inpatient": 8000, "outpatient": 0, "maternity": 8000, "renal": 7000, "cancer": 0},
        "level_5": {"inpatient": 20000, "outpatient": 0, "maternity": 20000, "renal": 15000, "cancer": 20000},
        "level_6": {"inpatient": 100000, "outpatient": 0, "maternity": 100000, "renal": 50000, "cancer": 100000},
    }
    
    tier_data = NHIF_BENEFITS.get(tier.lower(), NHIF_BENEFITS["level_4"])
    benefit = tier_data.get(procedure_type.lower(), 0)
    
    return {
        "status": "OK",
        "tier": tier,
        "procedure_type": procedure_type,
        "nhif_benefit_kes_per_day": benefit if benefit > 0 else "Not covered at this tier",
        "coverage_notes": {
            "outpatient": "NHIF outpatient only available at accredited facilities with Super Cover (SHIF 2024)",
            "renal": "Dialysis covered from Level 3 upward",
            "mental_health": "Limited coverage — SHA 2024 expanding this",
            "cancer": "Available at Level 5 and 6 (KNH, Aga Khan, Nairobi Hospital)",
        },
        "monthly_premium": {"employed": "KES 500 (PAYE deduction)", "self_employed": "KES 500 voluntary"},
        "gap_analysis": {
            "typical_inpatient_cost_kes": 15000 if tier == "level_4" else 50000,
            "nhif_covers": f"KES {benefit:,}" if benefit > 0 else "Not covered",
            "out_of_pocket_risk": f"KES {max(0, 15000 - benefit):,}+ at {tier}",
        },
        "note": "DEMO — Synthetic data. Verify at nhif.or.ke. SHA (Social Health Authority) restructuring underway 2024.",
        "source": "bima-mcp synthetic dataset. Reference: NHIF Benefits Schedule 2023.",
    }


@mcp.tool(
    description=(
        "Estimate monthly insurance premium for a Kenya individual. "
        "Covers health, life, crop, and device insurance types. "
        "Western parallel: Online insurance quote engines (Policygenius, Lemonade). "
        "DEMO estimation — not a binding quote."
    ),
    annotations={"readOnlyHint": True},
)
def premium_estimate(
    insurance_type: Annotated[str, "Type: health, life, crop, device"],
    age: Annotated[int, "Age in years (18–65)"],
    monthly_income_kes: Annotated[int, "Monthly income in KES"],
    county: Annotated[str, "Kenya county of residence"] = "Nairobi",
    acreage: Annotated[float, "Farm acreage (crop insurance only)"] = 0.0,
    crop: Annotated[str, "Crop type (crop insurance only)"] = "maize",
) -> dict:
    _audit("premium_estimate", {
        "insurance_type": insurance_type, "age": age,
        "monthly_income_kes": monthly_income_kes
    }, "OK")
    
    base_rates = {
        "health": 0.03,   # 3% of income, min KES 300
        "life": 0.01,     # 1% of income — term life
        "crop": 0.08,     # 8% of season input cost (ACRE Africa benchmark)
        "device": 0.025,  # 2.5% of device value per month
    }
    
    est = 0
    notes = []
    
    if insurance_type == "health":
        est = max(300, int(monthly_income_kes * base_rates["health"]))
        est = min(est, 5000)  # cap at KES 5,000 for basic health
        notes = [
            "NHIF minimum: KES 500/month covers inpatient only",
            f"For income KES {monthly_income_kes:,}, private supplement ~KES {est:,}/month",
            "Top-up cover from providers like Jubilee, AAR adds KES 1,000–5,000",
        ]
    elif insurance_type == "life":
        age_factor = 1.0 + max(0, (age - 35) * 0.03)
        est = max(500, int(monthly_income_kes * base_rates["life"] * age_factor))
        notes = [
            f"Term life for age {age}: age loading factor {age_factor:.2f}x",
            f"KES {monthly_income_kes * 12 * 5:,} sum assured (5× annual income rule)",
            "ICEA Lion, Jubilee Life, Britam Life offer KES 500–3,000/month term plans",
        ]
    elif insurance_type == "crop":
        drought_data = _NDMA_DROUGHT.get(county, {"drought_frequency_pct": 30})
        drought_pct = drought_data["drought_frequency_pct"]
        crop_mult = _CROP_RISK_MULTIPLIERS.get(crop.lower(), 1.0)
        input_cost_kes = acreage * 8000  # ~KES 8,000/acre input cost
        est = int(input_cost_kes * base_rates["crop"] * (drought_pct / 50) * crop_mult)
        notes = [
            f"County drought frequency: {drought_pct}% ({county})",
            f"Crop risk multiplier ({crop}): {crop_mult}x",
            f"Estimated input cost: KES {input_cost_kes:,} for {acreage} acres",
            f"ACRE Africa: pays via M-PESA when NDVI index drops below trigger",
        ]
    else:  # device
        device_value = max(5000, monthly_income_kes * 2)
        est = int(device_value * base_rates["device"])
        notes = [
            f"Estimated device value: KES {device_value:,} (2× monthly income proxy)",
            "Bundled insurance via Airtel/Safaricom: KES 100–500/month",
        ]
    
    return {
        "status": "OK",
        "insurance_type": insurance_type,
        "estimated_monthly_premium_kes": est,
        "annual_premium_kes": est * 12,
        "affordability_ratio": f"{est / monthly_income_kes * 100:.1f}% of income",
        "notes": notes,
        "note": "DEMO — Rough estimation for educational purposes only. Not a binding quote. Consult an IRA-licensed broker.",
        "source": "bima-mcp synthetic dataset. Reference: IRA 2024, ACRE Africa, World Bank Insurance Primer.",
    }


@mcp.tool(
    description=(
        "Calculate parametric crop insurance risk for a Kenya smallholder farmer. "
        "Based on ACRE Africa methodology: NDVI satellite index + NDMA drought history. "
        "Western parallel: Root Insurance telematic scoring, Skywatch EasyCrop satellite insurance. "
        "DEMO data — actual payouts require enrollment with a licensed insurer."
    ),
    annotations={"readOnlyHint": True},
)
def parametric_crop_risk(
    county: Annotated[str, "Kenya county name (e.g., Nakuru, Turkana, Machakos)"],
    crop: Annotated[str, "Crop type: maize, beans, potatoes, wheat, sorghum, millet, cassava, tea, coffee"],
    acreage: Annotated[float, "Farm size in acres"],
    season: Annotated[str, "Farming season: long_rains (Mar-May) or short_rains (Oct-Dec)"] = "long_rains",
) -> dict:
    _audit("parametric_crop_risk", {"county": county, "crop": crop, "acreage": acreage}, "OK")
    
    drought = _NDMA_DROUGHT.get(county, {"drought_frequency_pct": 30, "phase": "Minimal", "last_drought": "2020"})
    crop_mult = _CROP_RISK_MULTIPLIERS.get(crop.lower(), 1.0)
    drought_pct = drought["drought_frequency_pct"]
    
    # Risk score: 0–100
    risk_score = min(100, int(drought_pct * crop_mult))
    
    # Premium as % of input cost
    input_cost = acreage * 8000  # KES 8,000/acre inputs (seeds, fertilizer, labor)
    season_premium_kes = int(input_cost * 0.08 * (drought_pct / 100))
    
    risk_category = (
        "VERY HIGH" if risk_score > 65 else
        "HIGH" if risk_score > 45 else
        "MEDIUM" if risk_score > 25 else "LOW"
    )
    
    # Expected payout probability and value
    payout_trigger = drought_pct > 40
    expected_payout_kes = int(input_cost * 0.9 * (drought_pct / 100)) if payout_trigger else 0
    
    return {
        "status": "OK",
        "county": county,
        "crop": crop,
        "acreage": acreage,
        "season": season,
        "risk_score": risk_score,
        "risk_category": risk_category,
        "drought_frequency_pct": drought_pct,
        "current_ndma_phase": drought["phase"],
        "last_major_drought": drought["last_drought"],
        "economics": {
            "estimated_input_cost_kes": input_cost,
            "recommended_premium_kes": season_premium_kes,
            "premium_as_pct_of_inputs": f"{season_premium_kes / input_cost * 100:.1f}%",
            "payout_if_drought_triggers": f"KES {expected_payout_kes:,}",
            "trigger_threshold": "County NDVI below 0.3 for >3 consecutive weeks OR <60% normal rainfall",
        },
        "payment_flow": {
            "enrollment": "Via ACRE Africa app or Pula bundled with input loan",
            "premium_payment": "M-PESA at start of planting season",
            "payout_mechanism": "Automatic M-PESA transfer within 14 days of trigger confirmation",
            "trigger_verification": "Satellite (Copernicus NDVI) + NDMA field assessment",
        },
        "note": "DEMO — Synthetic risk model for educational purposes. Real parametric insurance requires enrollment with ACRE Africa or Pula Advisors. NDMA data: ndma.go.ke.",
        "source": "bima-mcp synthetic dataset. Reference: ACRE Africa Methodology Paper 2023, NDMA County Reports.",
    }


@mcp.tool(
    description=(
        "Compare available microinsurance options for low-income Kenyans. "
        "Western parallel: Insurtech comparison platforms (Policygenius, The Zebra, NerdWallet Insurance). "
        "East Africa context: 67% of Kenyans cannot afford conventional insurance premiums. "
        "DEMO data — verify products at ira.go.ke."
    ),
    annotations={"readOnlyHint": True},
)
def compare_microinsurance(
    target_group: Annotated[str, "Target group: informal_worker, farmer, student, elderly, refugee"] = "informal_worker",
    max_monthly_budget_kes: Annotated[int, "Maximum monthly premium budget in KES"] = 500,
) -> dict:
    _audit("compare_microinsurance", {"target_group": target_group, "budget": max_monthly_budget_kes}, "OK")
    
    affordable = [p for p in _PRODUCTS if p.get("monthly_premium_kes", 0) <= max_monthly_budget_kes]
    
    TARGET_GUIDANCE = {
        "informal_worker": {
            "priority": "Health (hospitalization) + device protection",
            "risks": "Medical bills, phone theft/damage",
            "best_fit": ["NHIF-002", "TURACO-001", "BIMA-001"],
        },
        "farmer": {
            "priority": "Crop insurance + health",
            "risks": "Drought, crop failure, illness during planting",
            "best_fit": ["ACRE-001", "PULA-001", "NHIF-002"],
        },
        "student": {
            "priority": "Device + small life cover",
            "risks": "Phone loss, accidental death/disability",
            "best_fit": ["BIMA-001", "MBELE-001"],
        },
        "elderly": {
            "priority": "Health (inpatient) + last expense cover",
            "risks": "High hospitalization costs, funeral expenses",
            "best_fit": ["NHIF-002", "MBELE-001"],
        },
        "refugee": {
            "priority": "Health — limited options",
            "risks": "Medical access, UNHCR may provide some coverage",
            "best_fit": ["NHIF-002"],
        },
    }
    
    guidance = TARGET_GUIDANCE.get(target_group, TARGET_GUIDANCE["informal_worker"])
    
    return {
        "status": "OK",
        "target_group": target_group,
        "max_budget_kes": max_monthly_budget_kes,
        "affordable_products": [p for p in affordable if p["id"] in guidance["best_fit"]],
        "priority_risks": guidance["risks"],
        "coverage_priority": guidance["priority"],
        "gap_analysis": {
            "west_comparison": "In the US/UK, basic health + life cover costs $50–150/month. In Kenya, NHIF covers less at KES 500/month — ~$4.",
            "what_kenbright_would_say": "The protection gap in Kenya is structural, not cultural. Technology can close it.",
            "biggest_gap": "Disability/income protection insurance — virtually absent in Kenya microinsurance market",
        },
        "how_to_enroll": {
            "NHIF": "Walk into any Huduma Centre or go to nhif.or.ke",
            "Turaco": "Download Turaco app or enroll via employer",
            "ACRE Africa": "Enroll at planting time through agrivet shops or KALRO extension officers",
            "Payment": "All accept M-PESA payments",
        },
        "note": "DEMO — Synthetic comparison for educational purposes. Verify all products at ira.go.ke.",
        "source": "bima-mcp synthetic dataset. Reference: IRA Kenya, Turaco, ACRE Africa public disclosures.",
    }


@mcp.tool(
    description=(
        "Calculate parameters for a community group (chama) pooled insurance arrangement. "
        "Western parallel: Fraternal benefit societies, mutual insurance companies, credit unions with insurance. "
        "Kenya parallel: Chama savings groups can formalize as Micro Insurance Groups under IRA. "
        "DEMO educational tool — not a licensed insurance product."
    ),
    annotations={"readOnlyHint": True},
)
def community_pool_calculator(
    group_size: Annotated[int, "Number of chama members (5–200)"],
    monthly_contribution_kes: Annotated[int, "Monthly contribution per member in KES"],
    coverage_goal: Annotated[str, "Coverage goal: hospitalization, funeral, crop_loss, education"] = "hospitalization",
) -> dict:
    _audit("community_pool_calculator", {
        "group_size": group_size, "monthly_contribution_kes": monthly_contribution_kes,
        "coverage_goal": coverage_goal
    }, "OK")
    
    monthly_pool = group_size * monthly_contribution_kes
    annual_pool = monthly_pool * 12
    reserve_ratio = 0.3  # 30% reserve (standard for mutual insurance)
    claims_pool = annual_pool * (1 - reserve_ratio)
    
    BENEFIT_STRUCTURES = {
        "hospitalization": {
            "max_per_claim_kes": min(50000, claims_pool // max(1, group_size // 5)),
            "waiting_period_days": 30,
            "max_claims_per_year": 2,
            "exclusions": "Pre-existing conditions in year 1, self-inflicted",
        },
        "funeral": {
            "max_per_claim_kes": min(80000, claims_pool // max(1, group_size // 10)),
            "waiting_period_days": 60,
            "max_claims_per_year": 1,
            "exclusions": "Suicide",
        },
        "crop_loss": {
            "max_per_claim_kes": min(30000, claims_pool // max(1, group_size // 3)),
            "waiting_period_days": 14,
            "max_claims_per_year": 2,
            "exclusions": "Self-caused damage, non-agricultural losses",
        },
        "education": {
            "max_per_claim_kes": min(40000, claims_pool // max(1, group_size // 4)),
            "waiting_period_days": 0,
            "max_claims_per_year": 1,
            "exclusions": "Non-registered institutions",
        },
    }
    
    structure = BENEFIT_STRUCTURES.get(coverage_goal, BENEFIT_STRUCTURES["hospitalization"])
    
    return {
        "status": "OK",
        "group_size": group_size,
        "monthly_contribution_kes": monthly_contribution_kes,
        "coverage_goal": coverage_goal,
        "pool_economics": {
            "monthly_pool_kes": monthly_pool,
            "annual_pool_kes": annual_pool,
            "reserve_fund_kes": int(annual_pool * reserve_ratio),
            "available_for_claims_kes": int(claims_pool),
        },
        "suggested_benefit_structure": structure,
        "sustainability_check": {
            "viable": group_size >= 10 and monthly_pool >= 5000,
            "note": "IRA recommends minimum 10 members and KES 5,000/month pool for sustainability",
            "actuarial_warning": "Group must track claims history and adjust contributions annually",
        },
        "formalization_path": {
            "step_1": "Register as a chama at Ministry of Public Service, Gender, Senior Citizens Affairs",
            "step_2": "Open a group M-PESA Paybill or business account",
            "step_3": "Draft a constitution with claims committee and dispute resolution",
            "step_4": "After 2 years of history, apply for IRA Micro Insurance License",
            "ira_contact": "ira.go.ke / +254 20 499 0000",
        },
        "western_parallel": "Fraternal benefit societies in the US (e.g., Mutual of Omaha origins) started as community pooling arrangements in the 1800s.",
        "note": "DEMO — Educational tool. Not a licensed insurance product. Consult IRA for formal registration.",
        "source": "bima-mcp synthetic dataset. Reference: IRA Micro Insurance Framework 2022.",
    }


def main():
    mcp.run()


if __name__ == "__main__":
    main()
