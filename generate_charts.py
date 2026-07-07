import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Automatically fetch the excel file directly from your GitHub repository
# Note: Ensure openpyxl is installed (pip install openpyxl) to read .xlsx files
github_raw_url = "https://raw.githubusercontent.com/jade1508/Business_Metrics_Reconciliation/main/business_metrics_raw.xlsx"

try:
    # Read the data (Adjust the sheet_name if your processed data is on a specific sheet)
    df = pd.read_excel(github_raw_url)
    print("Successfully fetched data directly from GitHub!")
except Exception as e:
    print(f"Could not fetch from GitHub ({e}). Using local fallback data instead.")
    # Local fallback mockup data if offline
    data = {
        'Month': ['Jan24', 'Feb24', 'Mar24', 'Apr24', 'May24', 'Jun24', 'Jul24', 'Aug24', 'Sep24', 'Oct24'],
        'CAC_avg': [220, 240, 310, 250, 230, 210, 240, 320, 215, 225],
        'LTV_avg': [1400, 1450, 1150, 1300, 1500, 1600, 1550, 1100, 1650, 1700],
        'Risk_Flags': ['No Risk', 'No Risk', 'Value Erosion Risk, Retention Risk', 'No Risk', 'No Risk', 'No Risk', 'No Risk', 'Value Erosion Risk, Retention Risk, Cost Inflation Risk', 'No Risk', 'No Risk']
    }
    df = pd.DataFrame(data)

# Set clean, modern plot aesthetics
sns.set_theme(style="whitegrid")
plt.rcParams['font.family'] = 'sans-serif'

# ------------------------------------------------------------------
# CHART 1: METRIC ROLLING TRENDS (LTV vs CAC)
# ------------------------------------------------------------------
fig, ax1 = plt.subplots(figsize=(10, 5))

# Plot LTV on the Primary Y-Axis (Left)
color_ltv = '#2ca02c'  # Growth/Value Green
ax1.set_xlabel('Timeline (Months)', fontsize=12, fontweight='bold', labelpad=10)
ax1.set_ylabel('LTV Average ($)', color=color_ltv, fontsize=12, fontweight='bold')
line1 = ax1.plot(df['Month'], df['LTV_avg'], color=color_ltv, marker='o', linewidth=2.5, label='LTV Avg')
ax1.tick_params(axis='y', labelcolor=color_ltv)

# Plot CAC on the Secondary Y-Axis (Right)
ax2 = ax1.twinx()
color_cac = '#d62728'  # Cost/Risk Red
ax2.set_ylabel('CAC Average ($)', color=color_cac, fontsize=12, fontweight='bold')
line2 = ax2.plot(df['Month'], df['CAC_avg'], color=color_cac, marker='s', linewidth=2.5, linestyle='--', label='CAC Avg')
ax2.tick_params(axis='y', labelcolor=color_cac)

# Combine legends from both axes
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left', frameon=True)

plt.title('Unit Economics Trend: LTV vs CAC Trajectory', fontsize=14, fontweight='bold', pad=15)
fig.tight_layout()
plt.savefig('ltv_cac_trends.png', dpi=300)
plt.close()

# ------------------------------------------------------------------
# CHART 3: RISK FLAG DISTRIBUTION (Donut Chart)
# ------------------------------------------------------------------
# Parse and flatten the comma-separated risk logs
all_risks = []
if 'Risk_Flags' in df.columns:
    for row in df['Risk_Flags'].dropna():
        if str(row).strip() != 'No Risk':
            all_risks.extend([risk.strip() for risk in str(row).split(',')])

if all_risks:
    risk_counts = pd.Series(all_risks).value_counts()
    
    plt.figure(figsize=(6, 5))
    # Soft, professional risk alert palette
    colors = ['#ff9999', '#66b3ff', '#ffcc99', '#99ff99']
    
    plt.pie(risk_counts, labels=risk_counts.index, autopct='%1.1f%%', 
            startangle=140, colors=colors, wedgeprops={'edgecolor': 'white', 'linewidth': 2})
    
    # Draw center circle to transform Pie chart into a clean Donut chart
    centre_circle = plt.Circle((0,0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    
    plt.title('Operational Risk Flag Distribution', fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig('risk_distribution_donut.png', dpi=300)
    plt.close()
    print("Process completed. Visualizations saved as 'ltv_cac_trends.png' and 'risk_distribution_donut.png'!")
else:
    print("No operational risks found in the dataset to generate Chart 3.")