# SHIPMENT-INSPECTION-ANALYSIS
Fischer Jordan Assignment

# Carrier Cost Normalization & Impact Analysis

## Overview
This project analyzes shipment-level invoice data, classifies charge types, normalizes costs by removing non-comparable charges, and evaluates carrier performance with risk insights.

---

# Execution Stages & Results

## [STAGE 1] Loading Data
- Loaded **214 rows** of invoice-level data.

---

## [STAGE 2] Charge Classification

### Charge Classification Summary

| Category | Count |
|----------|-------|
| B        | 118   |
| D        | 75    |
| C        | 19    |
| A        | 2     |

### Sample Category D (Excluded Charges)

Additional Tax
Adjustment
Admin. Fees
Additional Vat Charge
Agri Processing Fee
Alternate Broker
Australia GST
Billing Adjustment for w/e 01/07/2023
Billing Adjustment for w/e 01/14/2023
Billing Adjustment for w/e 01/21/2023


---

## [STAGE 4] Shipment Aggregation

- **Total Shipments:** 106  
- **Total Reference Spend (Raw):** 183.00  
- **Total Normalized Spend:** 88.50  

---

## [STAGE 5] Carrier Comparison

### Carrier Level Statistics

| Carrier | Shipments | Avg Raw | Avg Norm | Median Norm | Std Norm | P90 Norm | Total Spend | % Diff |
|----------|-----------|---------|----------|-------------|----------|----------|-------------|--------|
| Delhivery | 13 | 3.13 | 2.50 | 0.00 | 4.76 | 11.00 | 40.75 | -20.25% |
| Ekart Logistics | 13 | 2.21 | 0.88 | 0.00 | 3.19 | 0.00 | 28.75 | -60.00% |
| DHL | 11 | 2.25 | 1.09 | 0.00 | 3.62 | 0.00 | 24.75 | -51.52% |
| DTDC | 14 | 1.66 | 0.68 | 0.00 | 2.54 | 0.00 | 23.25 | -59.14% |
| Blue Dart | 11 | 1.66 | 0.00 | 0.00 | 0.00 | 0.00 | 18.25 | -100.00% |
| FedEx | 12 | 1.40 | 1.40 | 0.00 | 3.27 | 6.98 | 16.75 | 0.00% |
| Ecom Express | 11 | 1.39 | 0.00 | 0.00 | 0.00 | 0.00 | 15.25 | -100.00% |
| Gati | 12 | 1.27 | 0.52 | 0.00 | 1.80 | 0.00 | 15.25 | -59.02% |
| Safe Express | 9 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | NaN |

---

## [STAGE 6] Impact Analysis

Delhivery: Raw 3.13 -> Norm 2.50 (-20.2%)
Ekart Logistics: Raw 2.21 -> Norm 0.88 (-60.0%)
DHL: Raw 2.25 -> Norm 1.09 (-51.5%)
DTDC: Raw 1.66 -> Norm 0.68 (-59.1%)
Blue Dart: Raw 1.66 -> Norm 0.00 (-100.0%)
FedEx: Raw 1.40 -> Norm 1.40 (0.0%)
Ecom Express: Raw 1.39 -> Norm 0.00 (-100.0%)
Gati: Raw 1.27 -> Norm 0.52 (-59.0%)
Safe Express: Raw 0.00 -> Norm 0.00 (NaN)


---

## [STAGE 7] Worst 10% Risk Analysis

- **Top 10% Shipments:** 10 (out of 106)
- **Spend Contribution:** 88.50  
- **Contribution to Total Normalized Spend:** 100%

### High-Cost Shipment Distribution

| Carrier | Proportion (%) |
|----------|----------------|
| Delhivery | 30% |
| FedEx | 20% |
| DHL | 10% |
| Ekart Logistics | 10% |
| DTDC | 10% |
| Gati | 10% |
| Safe Express | 10% |

---

# Executive Summary

## 1️⃣ Data Overview
- Processed **106 shipments**
- Total Invoiced Amount: **183.00**
- Normalized Evaluated Amount: **88.50**

---

## 2️⃣ Carrier Performance (Normalized)

- **Most Cost-Effective Carrier:** Blue Dart (0.00/shipment)
- **Most Expensive Carrier:** Delhivery (2.50/shipment)

---

## 3️⃣ Distortion Analysis

Normalization removed non-comparable charges such as:
- Taxes  
- Duties  
- One-off Penalties  

### Cost Basis Reduction:

- Delhivery: -20.2%
- Ekart Logistics: -60.0%
- DHL: -51.5%
- DTDC: -59.1%
- Blue Dart: -100.0%
- FedEx: 0.0%
- Ecom Express: -100.0%
- Gati: -59.0%

---

## 4️⃣ Risk Insight (Heavy Tail Alert)

The **top 10% most expensive shipments contribute 100% of total normalized spend.**

> ⚠️ Significant spend concentration in high-cost outliers.  
> Indicates heavy tail risk and pricing volatility across carriers.

---

# 📁 Output Files Generated

- `carrier_stats.csv`
- `worst_shipments_10pct.csv`
- `shipment_level_data.csv`

---
