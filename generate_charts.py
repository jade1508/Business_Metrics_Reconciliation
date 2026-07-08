import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Automatically fetch the excel file directly from your GitHub repository
github_raw_url = "https://raw.githubusercontent.com/jade1508/Business_Metrics_Reconciliation/main/Reconciliation_Output.xlsx"

try:
    df = pd.read_excel(github_raw_url)
    print("Successfully fetched data directly from GitHub!")
except Exception as e:
    print(f"Could not fetch from GitHub ({e}). Ensure the file exists and the repository is public.")
    # Place your local fallback dataframe initialization here if needed

# Convert Month to string format to ensure clean labels on X-axis
df['Month'] = df['Month'].astype(str)

# Set clean, modern plot aesthetics
sns.set_theme(style="whitegrid")
plt.rcParams['font.family'] = 'sans-serif'

# ------------------------------------------------------------------
# CHART 1: METRIC ROLLING TRENDS (LTV vs CAC with 3MA)
# ------------------------------------------------------------------
fig, ax1 = plt.subplots(figsize=(11, 5.5))

# --- Plot LTV Data on the Primary Y-Axis (Left) ---
color_ltv_main = '#2ca02c'  # Solid line Green
color_ltv_3ma = '#87d59c'   # Light Green for 3MA

ax1.set_xlabel('Timeline (Months)', fontsize=12, fontweight='bold', labelpad=10)
ax1.set_ylabel('LTV Metrics ($)', color=color_ltv_main, fontsize=12, fontweight='bold')

# LTV Avg - Solid Line
line1 = ax1.plot(df['Month'], df['LTV_avg'], color=color_ltv_main, marker='o', 
                 linewidth=2.5, linestyle='-', label='LTV Avg')

# LTV 3MA - Dashed Line (Only plots if the column exists in your Excel)
line1_3ma = []
if 'LTV_3MA' in df.columns:
    line1_3ma = ax1.plot(df['Month'], df['LTV_3MA'], color=color_ltv_3ma, 
                         linewidth=1.8, linestyle='--', label='LTV 3MA')

ax1.tick_params(axis='y', labelcolor=color_ltv_main)


# --- Plot CAC Data on the Secondary Y-Axis (Right) ---
ax2 = ax1.twinx()
color_cac_main = '#d62728'  # Solid line Red
color_cac_3ma = '#ff9999'   # Light Red/Pink for 3MA

ax2.set_ylabel('CAC Metrics ($)', color=color_cac_main, fontsize=12, fontweight='bold')

# CAC Avg - Solid Line (Changed from dashed to solid)
line2 = ax2.plot(df['Month'], df['CAC_avg'], color=color_cac_main, marker='s', 
                 linewidth=2.5, linestyle='-', label='CAC Avg')

# CAC 3MA - Dashed Line (Only plots if the column exists in your Excel)
line2_3ma = []
if 'CAC_3MA' in df.columns:
    line2_3ma = ax2.plot(df['Month'], df['CAC_3MA'], color=color_cac_3ma, 
                         linewidth=1.8, linestyle='--', label='CAC 3MA')

ax2.tick_params(axis='y', labelcolor=color_cac_main)


# --- Combine Legends ---
lines = line1 + line1_3ma + line2 + line2_3ma
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left', frameon=True)

plt.title('Unit Economics Trend: LTV vs CAC & 3-Month Moving Averages', fontsize=14, fontweight='bold', pad=15)
fig.tight_layout()
plt.savefig('ltv_cac_trends.png', dpi=300)
plt.close()

# ------------------------------------------------------------------
# CHART 3: RISK FLAG DISTRIBUTION (Donut Chart with Fixed Order & Colors)
# ------------------------------------------------------------------
all_risks = []
if 'Risk_Flags' in df.columns:
    for row in df['Risk_Flags'].dropna():
        # Handle rows containing comma-separated multiple risks
        all_risks.extend([risk.strip() for risk in str(row).split(',')])

if all_risks:
    # 1. Get original counts
    raw_counts = pd.Series(all_risks).value_counts()
    
    # 2. Reorder to force 'No Risk' to be the VERY FIRST element
    ordered_index = []
    if 'No Risk' in raw_counts.index:
        ordered_index.append('No Risk')
    
    # Append all other risks behind 'No Risk'
    for risk_label in raw_counts.index:
        if risk_label != 'No Risk':
            ordered_index.append(risk_label)
            
    # Reindex the series with the new forced order
    risk_counts = raw_counts.reindex(ordered_index)
    
    # 3. Define the explicit color map
    hex_colors = ['#87d59c', '#999999', '#ff9999', '#ffcc99', '#99ff99']
    color_mapping = {}
    
    # Assign #87d59c to 'No Risk'
    if 'No Risk' in risk_counts.index:
        color_mapping['No Risk'] = '#87d59c'
        remaining_colors = [c for c in hex_colors if c != '#87d59c']
    else:
        remaining_colors = hex_colors.copy()
        
    # Assign remaining colors to other risks
    color_idx = 0
    for risk_label in risk_counts.index:
        if risk_label != 'No Risk':
            if color_idx < len(remaining_colors):
                color_mapping[risk_label] = remaining_colors[color_idx]
                color_idx += 1
            else:
                color_mapping[risk_label] = '#d3d3d3'
                
    chart_colors = [color_mapping[label] for label in risk_counts.index]
    
    # 4. Plot the Chart
    plt.figure(figsize=(6, 5))
    
    # startangle=90 forces the first slice ('No Risk') to start exactly at 12 o'clock
    # counterclock=False makes it go clockwise
    plt.pie(risk_counts, labels=risk_counts.index, autopct='%1.1f%%', 
            startangle=90, counterclock=False, colors=chart_colors, 
            wedgeprops={'edgecolor': 'white', 'linewidth': 2})
    
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
