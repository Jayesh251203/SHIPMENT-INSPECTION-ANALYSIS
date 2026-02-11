import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import site

# Ensure user site packages are included (fix for environment issues)
site.main()

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.float_format', '{:.2f}'.format)

DATA_PATH = r'c:\Users\Jayesh\Desktop\development\Fischer Jordan\FJ Assignment - FJ Assignment - Sheet1.csv'

def classify_charge(charge_type):
    """
    Classifies charge types into Categories:
    A: Core Freight Charges (Base Rate, Freight)
    B: Structural Surcharges (Fuel, DAS, Weight/Dims, Residential, COD, Signature)
    C: Conditional Charges (Weekend, Special, Future Day Pickup anomalies)
    D: Non-Comparable/Exclusions (Tax, Duty, Adjustments, Admin Fees)
    """
    ct = str(charge_type).lower()
    
    # Category D: Exclusions (Taxes, Duties, Adjustments, etc.)
    if any(x in ct for x in ['gst', 'hst', 'pst', 'vat', 'tax', 'duty', 'customs', 'adjustment', 'admin', 'disbursement', 'broker']):
        # Exceptions: 'fuel surcharge adjustment' is usually B, 'address correction' is B/C.
        # But 'billing adjustment' is D. 
        # 'Delivery Area Surcharge - Extended Adjustment' -> B (it's a correction to a B charge)
        # Let's refine:
        if 'fuel surcharge adjustment' in ct: return 'B'
        if 'delivery area surcharge' in ct and 'adjustment' in ct: return 'B'
        if 'signature required adjustment' in ct: return 'B'
        return 'D'
    
    # Category A: Core Freight
    if ct in ['base rate', 'freight']:
        return 'A'
    
    # Category B: Structural Surcharges
    # Fuel, DAS, Residential, Weight/Dim, Signature, COD, Declared Value
    if any(x in ct for x in ['fuel', 'delivery area', 'extended area', 'remote', 'residential', 
                             'oversize', 'overweight', 'large package', 'handling', 'weight', 'ahs',
                             'signature', 'cod', 'declared value', 'address correction']):
        return 'B'
    
    # Category C: Conditional Charges
    # Weekend, Holiday, Special Handling, Call Tag
    if any(x in ct for x in ['weekend', 'saturday', 'sunday', 'call tag', 'call ahead', 'special handling']):
        return 'C'
        
    # Default fallback:
    # If it's "Future Day Pickup" variants not caught above (e.g. generic ones)
    if 'future day pickup' in ct:
        # If it wasn't caught by Fuel/DAS/etc above, it's likely a specific service fee
        return 'C'
        
    # Unclassified -> Assign to C or D? 
    # "Early Surcharge", "Late Arrival" -> D (Penalty/Service)
    return 'D'

def run_analysis():
    print("="*50)
    print("STARTING SHIPMENT INSPECTION ANALYSIS")
    print("="*50)

    # --- STAGE 1: DATA LOADING & PROFILING ---
    print("\n[STAGE 1] Loading Data...")
    try:
        df = pd.read_csv(DATA_PATH)
        print(f"Loaded {len(df)} rows.")
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # Column Mapping
    # Tracking Number -> Shipment ID
    if 'Tracking Number' in df.columns:
        df['Shipment ID'] = df['Tracking Number'].astype(str)
    else:
        print("CRITICAL: 'Tracking Number' column not found!")
        print(f"Columns: {df.columns.tolist()}")
        return

    # Basic Cleaning
    df['Charge'] = pd.to_numeric(df['Charge'], errors='coerce').fillna(0)
    
    # --- STAGE 2: CLASSIFICATION ---
    print("\n[STAGE 2] Classifying Charge Types...")
    df['Category'] = df['Charge Type'].apply(classify_charge)
    
    # Validation of Classification
    print("\nCharge Classification Summary (Count of Rows):")
    print(df['Category'].value_counts())
    
    # Check unclassified (should be none ideally, or check 'D')
    cat_d_examples = df[df['Category'] == 'D']['Charge Type'].unique()[:10]
    print(f"\nSample Category D (Excluded) Charges:\n{cat_d_examples}")

    # --- STAGE 3: DEFINING NORMALIZED COST ---
    # Normalized Cost = A + B (Core + Structural)
    # Conditional (C) is excluded for apples-to-apples comparison
    # Non-Comparable (D) is excluded
    
    # Create mapped columns for aggregation
    df['Cost_Raw'] = df['Charge']
    df['Cost_Normalized'] = df.apply(lambda x: x['Charge'] if x['Category'] in ['A', 'B'] else 0, axis=1)
    df['Cost_A'] = df.apply(lambda x: x['Charge'] if x['Category'] == 'A' else 0, axis=1)
    df['Cost_B'] = df.apply(lambda x: x['Charge'] if x['Category'] == 'B' else 0, axis=1)
    df['Cost_C'] = df.apply(lambda x: x['Charge'] if x['Category'] == 'C' else 0, axis=1)
    df['Cost_D'] = df.apply(lambda x: x['Charge'] if x['Category'] == 'D' else 0, axis=1)

    # --- STAGE 4: SHIPMENT AGGREGATION ---
    print("\n[STAGE 4] Aggregating by Shipment...")
    
    # Group by Shipment ID
    # Use 'Carrier Name' and 'Zones' (Take first/mode per shipment)
    agg_funcs = {
        'Carrier Name': 'first',
        'Zones': 'first',
        'Cost_Raw': 'sum',
        'Cost_Normalized': 'sum',
        'Cost_A': 'sum',
        'Cost_B': 'sum',
        'Cost_C': 'sum',
        'Cost_D': 'sum'
    }
    
    shipments = df.groupby('Shipment ID').agg(agg_funcs).reset_index()
    shipments['Surcharge_Ratio'] = shipments['Cost_B'] / shipments['Cost_A'].replace(0, np.nan)
    
    print(f"Total Shipments: {len(shipments)}")
    print(f"Total Reference Spend (Raw): {shipments['Cost_Raw'].sum():,.2f}")
    print(f"Total Normalized Spend: {shipments['Cost_Normalized'].sum():,.2f}")

    # --- STAGE 5: CARRIER LEVEL COMPARISON ---
    print("\n[STAGE 5] Carrier Comparison...")
    
    carrier_stats = shipments.groupby('Carrier Name').agg(
        Shipment_Count=('Shipment ID', 'count'),
        Avg_Raw_Cost=('Cost_Raw', 'mean'),
        Avg_Norm_Cost=('Cost_Normalized', 'mean'),
        Median_Norm_Cost=('Cost_Normalized', 'median'),
        Std_Norm_Cost=('Cost_Normalized', 'std'),
        P90_Norm_Cost=('Cost_Normalized', lambda x: x.quantile(0.90)),
        Total_Spend=('Cost_Raw', 'sum')
    ).sort_values('Total_Spend', ascending=False)
    
    carrier_stats['%_Difference'] = ((carrier_stats['Avg_Norm_Cost'] - carrier_stats['Avg_Raw_Cost']) / carrier_stats['Avg_Raw_Cost']) * 100
    
    print("\nCarrier Level Statistics:")
    print(carrier_stats)

    # --- STAGE 6: IMPACT OF NORMALIZATION ---
    print("\n[STAGE 6] Impact Analysis...")
    # Explanation: Negative % Difference means excluded costs (Taxes, Conditional) were removed.
    # Positive % is impossible unless we had negative adjustments in D that were removed (increasing cost).
    
    for carrier in carrier_stats.index:
        raw = carrier_stats.loc[carrier, 'Avg_Raw_Cost']
        norm = carrier_stats.loc[carrier, 'Avg_Norm_Cost']
        print(f"{carrier}: Raw {raw:.2f} -> Norm {norm:.2f} ({carrier_stats.loc[carrier, '%_Difference']:.1f}%)")

    # --- STAGE 7: WORST 10% ANALYSIS ---
    print("\n[STAGE 7] Worst 10% Analysis...")
    
    # Calculate strict top 10% by count
    top_10_count = int(len(shipments) * 0.1)
    if top_10_count < 1: top_10_count = 1
    
    worst_shipments = shipments.nlargest(top_10_count, 'Cost_Normalized').copy()
    
    print(f"Top 10% Count: {len(worst_shipments)} shipments (out of {len(shipments)})")
    
    worst_spend = worst_shipments['Cost_Normalized'].sum()
    total_norm_spend = shipments['Cost_Normalized'].sum()
    print(f"Spend Contribution of Worst 10%: {worst_spend:,.2f} ({worst_spend/total_norm_spend*100:.1f}% of Total Normalized Spend)")
    
    # Distribution of Worst 10% by Carrier
    print("\nHigh-Cost Shipments by Carrier:")
    print(worst_shipments['Carrier Name'].value_counts(normalize=True) * 100)

    # --- STAGE 10: STORYTELLING SUMMARY ---
    print("\n" + "="*50)
    print("EXECUTIVE SUMMARY")
    print("="*50)
    
    print("1. DATA OVERVIEW")
    print(f"- Processed {len(shipments)} shipments.")
    print(f"- Total Invoiced Amount: {shipments['Cost_Raw'].sum():,.2f}")
    print(f"- Normalized Evaluated Amount: {shipments['Cost_Normalized'].sum():,.2f}")
    
    print("\n2. CARRIER PERFORMANCE (NORMALIZED)")
    cheapest = carrier_stats['Avg_Norm_Cost'].idxmin()
    most_expensive = carrier_stats['Avg_Norm_Cost'].idxmax()
    print(f"- Most Cost-Effective Carrier: {cheapest} ({carrier_stats.loc[cheapest, 'Avg_Norm_Cost']:.2f}/shp)")
    print(f"- Most Expensive Carrier: {most_expensive} ({carrier_stats.loc[most_expensive, 'Avg_Norm_Cost']:.2f}/shp)")
    
    print("\n3. DISTORTION ANALYSIS")
    print("Normalization removed non-comparable charges (Taxes, Duties, One-off Penalties).")
    for car in carrier_stats.index:
        diff = carrier_stats.loc[car, '%_Difference']
        print(f"- {car}: {'Reduced' if diff < 0 else 'Increased'} cost basis by {abs(diff):.1f}%")
        
    print("\n4. RISK ANALYSIS (WORST 10%)")
    worst_share = (worst_spend / total_norm_spend) * 100
    print(f"- The most expensive 10% of shipments contribute {worst_share:.1f}% of total spend.")
    if worst_share > 30:
        print("  -> ALERT: Heavy tail risk detected. Significant spend concentration in outliers.")
    else:
        print("  -> Spend is relatively well-distributed.")

    # Save outputs
    carrier_stats.to_csv('carrier_stats.csv')
    worst_shipments.to_csv('worst_shipments_10pct.csv', index=False)
    shipments.to_csv('shipment_level_data.csv', index=False)
    print("\nSaved carrier_stats.csv, worst_shipments_10pct.csv, shipment_level_data.csv")

if __name__ == "__main__":
    run_analysis()
