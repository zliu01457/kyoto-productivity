import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

excel_file = "R-JIP2017_180424-2.xlsx"  
# Define the analysis years in advance for 1992–2012 decomposition
# and panel data construction.
years_range = list(range(1992, 2013))  
n = 20                                

# Growth Accounting:
# This growth accounting is intended as an exploratory exercise.
# It decomposes Kyoto Prefecture's GDP growth over 1972-2012 into the contributions of capital, labor, and TFP. 
# The results are compared with Tokyo perfecture and Japan 
# The objective is to develop an initial understanding of the sources of productivity growth and identify economic patterns for later research questions. 
# To conduct the growth accoutning excercise, I need the follwing variables from the R-JIP excel sheet
# Y: Real output (Real Value Added, RV) in 1972, 1992, and 2012 for kyoto perfecture and tokyo perfecture 
# K: Net capital stock (KT) in 1972, 1992, and 2012 for kyoto perfecture and tokyo perfecture
# L: Labor input (Man-hours, MH) in 1972, 1992, and 2012 for kyoto perfecture and tokyo perfecture
# g_Y = (Y_end / Y_start)**(1/n) - 1
# g_K = (K_end / K_start)**(1/n) - 1
# g_L = (L_end / L_start)**(1/n) - 1
# TFP 
# g_A = g_Y - alpha*g_K - (1-alpha)*g_L
# Note: The analysis covers 1972–2012 because prefecture-level data for Okinawa are unavailable for 1970 and 1971. 
# Starting in 1972 ensures a consistent sample across prefectures and over time.
# ===========================================================================
# Extract macroeconomic variables for growth accounting，construct data frame
df_real_value_added = pd.read_excel(excel_file, sheet_name="Real value added (RV)", header=2)
df_capital_stock = pd.read_excel(excel_file, sheet_name="Net capital stock (KT)", header=2)
df_man_hours = pd.read_excel(excel_file, sheet_name="Man-hours (MH)", header=2)
df_nominal_value_added = pd.read_excel(excel_file, sheet_name="Nominal value added (NV)", header=2)
df_labor_cost = pd.read_excel(excel_file, sheet_name="Labor costs (WL)", header=2)

def growth_accounting_exercise(region_name):
    
    real_value_total = df_real_value_added[(df_real_value_added.iloc[:, 1] == region_name) & (df_real_value_added.iloc[:, 2] == "T")]
    capital_stock_total = df_capital_stock[(df_capital_stock.iloc[:, 1] == region_name) & (df_capital_stock.iloc[:, 2] == "T")]
    man_hours_total = df_man_hours[(df_man_hours.iloc[:, 1] == region_name) & (df_man_hours.iloc[:, 2] == "T")]
    nominal_value_total = df_nominal_value_added[(df_nominal_value_added.iloc[:, 1] == region_name) & (df_nominal_value_added.iloc[:, 2] == "T")]
    labor_cost_total = df_labor_cost[(df_labor_cost.iloc[:, 1] == region_name) & (df_labor_cost.iloc[:, 2] == "T")]
    
    return real_value_total, capital_stock_total, man_hours_total, nominal_value_total, labor_cost_total

# Kyoto
kyoto_data = growth_accounting_exercise("Kyoto")
tokyo_data = growth_accounting_exercise("Tokyo")

kyoto_real_value, kyoto_capital_stock, kyoto_man_hours, kyoto_nominal_value, kyoto_labor_cost = kyoto_data
kyoto_output_1972 = kyoto_real_value[1972].iloc[0]
kyoto_output_1992 = kyoto_real_value[1992].iloc[0]
kyoto_output_2012 = kyoto_real_value[2012].iloc[0]

kyoto_capital_1972 = kyoto_capital_stock[1972].iloc[0]
kyoto_capital_1992 = kyoto_capital_stock[1992].iloc[0]
kyoto_capital_2012 = kyoto_capital_stock[2012].iloc[0]

kyoto_labor_1972 = kyoto_man_hours[1972].iloc[0]
kyoto_labor_1992 = kyoto_man_hours[1992].iloc[0]
kyoto_labor_2012 = kyoto_man_hours[2012].iloc[0]

# Tokyo
# Tokyo serves as a frontier benchmark for evaluating Kyoto's productivity growth.
# Comparing Kyoto with the national average alone is insufficient, as the
# aggregate may be pulled down by lower-productivity regions.
tokyo_real_value, tokyo_capital_stock, tokyo_man_hours, tokyo_nominal_value, tokyo_labor_cost = tokyo_data

tokyo_output_1972 = tokyo_real_value[1972].iloc[0]
tokyo_output_1992 = tokyo_real_value[1992].iloc[0]
tokyo_output_2012 = tokyo_real_value[2012].iloc[0]

tokyo_capital_1972 = tokyo_capital_stock[1972].iloc[0]
tokyo_capital_1992 = tokyo_capital_stock[1992].iloc[0]
tokyo_capital_2012 = tokyo_capital_stock[2012].iloc[0]

tokyo_labor_1972 = tokyo_man_hours[1972].iloc[0]
tokyo_labor_1992 = tokyo_man_hours[1992].iloc[0]
tokyo_labor_2012 = tokyo_man_hours[2012].iloc[0]
    
years_span_first = 1992 - 1972   # 20 years
years_span_second = 2012 - 1992  # 20 years

# We take logs in growth accounting to turn the production function into an additive relationship. 
# This allows us to separate output growth into the contributions of capital, labor, and TFP. 
# CAGR measures the average annual compound growth rate. 
# When annual growth rates are small, it is very close to the log growth rate. 
# Therefore, we use CAGR in our growth accounting exercise
# Period 1: 1972 - 1992
kyoto_growth_output_72_92 = ((kyoto_output_1992 / kyoto_output_1972) ** (1 / years_span_first) - 1) * 100
kyoto_growth_capital_72_92 = ((kyoto_capital_1992 / kyoto_capital_1972) ** (1 / years_span_first) - 1) * 100
kyoto_growth_labor_72_92 = ((kyoto_labor_1992 / kyoto_labor_1972) ** (1 / years_span_first) - 1) * 100

# Period 2: 1992 - 2012
kyoto_growth_output_92_12 = ((kyoto_output_2012 / kyoto_output_1992) ** (1 / years_span_second) - 1) * 100
kyoto_growth_capital_92_12 = ((kyoto_capital_2012 / kyoto_capital_1992) ** (1 / years_span_second) - 1) * 100
kyoto_growth_labor_92_12 = ((kyoto_labor_2012 / kyoto_labor_1992) ** (1 / years_span_second) - 1) * 100

#Tokyo

# Period 1: 1972 - 1992
tokyo_growth_output_72_92 = ((tokyo_output_1992 / tokyo_output_1972) ** (1 / years_span_first) - 1) * 100
tokyo_growth_capital_72_92 = ((tokyo_capital_1992 / tokyo_capital_1972) ** (1 / years_span_first) - 1) * 100
tokyo_growth_labor_72_92 = ((tokyo_labor_1992 / tokyo_labor_1972) ** (1 / years_span_first) - 1) * 100

# Period 2: 1992 - 2012
tokyo_growth_output_92_12 = ((tokyo_output_2012 / tokyo_output_1992) ** (1 / years_span_second) - 1) * 100
tokyo_growth_capital_92_12 = ((tokyo_capital_2012 / tokyo_capital_1992) ** (1 / years_span_second) - 1) * 100
tokyo_growth_labor_92_12 = ((tokyo_labor_2012 / tokyo_labor_1992) ** (1 / years_span_second) - 1) * 100

# Labor share: 1-alpha = WL / NV  using 2010's labor cost and nominal value added 
# Capital share alpha = 1 - (1-alpha)
# WL: Labor costs 
# NV: Nominal value added
# We use the 2010 factor shares throughout 1972–2012 to keep the weights constant when calculating the contributions of capital and labor to output growth.
#Kyoto
kyoto_labor_cost_2010 = kyoto_labor_cost[2010].iloc[0]
kyoto_nominal_value_2010 = kyoto_nominal_value[2010].iloc[0]
kyoto_labor_share = kyoto_labor_cost_2010 / kyoto_nominal_value_2010
kyoto_capital_share = 1.0 - kyoto_labor_share
# --- Period 1: 1972 - 1992 Growth Accounting ---
kyoto_capital_contribution_72_92 = kyoto_capital_share * kyoto_growth_capital_72_92
kyoto_labor_contribution_72_92 = kyoto_labor_share * kyoto_growth_labor_72_92
kyoto_tfp_growth_72_92 = kyoto_growth_output_72_92 - kyoto_capital_contribution_72_92 - kyoto_labor_contribution_72_92

# --- Period 2: 1992 - 2012 Growth Accounting ---
kyoto_capital_contribution_92_12 = kyoto_capital_share * kyoto_growth_capital_92_12
kyoto_labor_contribution_92_12 = kyoto_labor_share * kyoto_growth_labor_92_12
kyoto_tfp_growth_92_12 = kyoto_growth_output_92_12 - kyoto_capital_contribution_92_12 - kyoto_labor_contribution_92_12

#Tokyo
tokyo_labor_cost_2010 = tokyo_labor_cost[2010].iloc[0]
tokyo_nominal_value_2010 = tokyo_nominal_value[2010].iloc[0]
tokyo_labor_share = tokyo_labor_cost_2010 / tokyo_nominal_value_2010
tokyo_capital_share = 1.0 - tokyo_labor_share

# --- Period 1: 1972 - 1992 Growth Accounting ---
tokyo_capital_contribution_72_92 = tokyo_capital_share * tokyo_growth_capital_72_92
tokyo_labor_contribution_72_92 = tokyo_labor_share * tokyo_growth_labor_72_92
tokyo_tfp_growth_72_92 = tokyo_growth_output_72_92 - tokyo_capital_contribution_72_92 - tokyo_labor_contribution_72_92

# --- Period 2: 1992 - 2012 Growth Accounting ---
tokyo_capital_contribution_92_12 = tokyo_capital_share * tokyo_growth_capital_92_12
tokyo_labor_contribution_92_12 = tokyo_labor_share * tokyo_growth_labor_92_12
tokyo_tfp_growth_92_12 = tokyo_growth_output_92_12 - tokyo_capital_contribution_92_12 - tokyo_labor_contribution_92_12  

# ===========================================================================
# Japan National Growth Accounting
# ===========================================================================

# National aggregates: sum across all prefectures except Kyoto
japan_real_value = df_real_value_added[(df_real_value_added.iloc[:, 2] == "T") & (df_real_value_added.iloc[:, 1] != "Kyoto")].sum(numeric_only=True)
japan_capital_stock = df_capital_stock[(df_capital_stock.iloc[:, 2] == "T") & (df_capital_stock.iloc[:, 1] != "Kyoto")].sum(numeric_only=True)
japan_man_hours = df_man_hours[(df_man_hours.iloc[:, 2] == "T") & (df_man_hours.iloc[:, 1] != "Kyoto")].sum(numeric_only=True)
japan_nominal_value = df_nominal_value_added[(df_nominal_value_added.iloc[:, 2] == "T") & (df_nominal_value_added.iloc[:, 1] != "Kyoto")].sum(numeric_only=True)
japan_labor_cost = df_labor_cost[(df_labor_cost.iloc[:, 2] == "T") & (df_labor_cost.iloc[:, 1] != "Kyoto")].sum(numeric_only=True)

# Japan National output
japan_output_1972 = japan_real_value[1972]
japan_output_1992 = japan_real_value[1992]
japan_output_2012 = japan_real_value[2012]

# Japan National capital stock
japan_capital_1972 = japan_capital_stock[1972]
japan_capital_1992 = japan_capital_stock[1992]
japan_capital_2012 = japan_capital_stock[2012]

# Japan National labor
japan_labor_1972 = japan_man_hours[1972]
japan_labor_1992 = japan_man_hours[1992]
japan_labor_2012 = japan_man_hours[2012]

# Period 1: 1972 - 1992
japan_growth_output_72_92 = ((japan_output_1992 / japan_output_1972) ** (1 / years_span_first) - 1) * 100
japan_growth_capital_72_92 = ((japan_capital_1992 / japan_capital_1972) ** (1 / years_span_first) - 1) * 100
japan_growth_labor_72_92 = ((japan_labor_1992 / japan_labor_1972) ** (1 / years_span_first) - 1) * 100

# Period 2: 1992 - 2012
japan_growth_output_92_12 = ((japan_output_2012 / japan_output_1992) ** (1 / years_span_second) - 1) * 100
japan_growth_capital_92_12 = ((japan_capital_2012 / japan_capital_1992) ** (1 / years_span_second) - 1) * 100
japan_growth_labor_92_12 = ((japan_labor_2012 / japan_labor_1992) ** (1 / years_span_second) - 1) * 100

# Japan National factor shares: 2010 labor costs and nominal value added
japan_labor_cost_2010 = japan_labor_cost[2010]
japan_nominal_value_2010 = japan_nominal_value[2010]
japan_labor_share = japan_labor_cost_2010 / japan_nominal_value_2010
japan_capital_share = 1.0 - japan_labor_share

# --- Period 1: 1972 - 1992 Growth Accounting ---
japan_capital_contribution_72_92 = japan_capital_share * japan_growth_capital_72_92
japan_labor_contribution_72_92 = japan_labor_share * japan_growth_labor_72_92
japan_tfp_growth_72_92 = japan_growth_output_72_92 - japan_capital_contribution_72_92 - japan_labor_contribution_72_92

# --- Period 2: 1992 - 2012 Growth Accounting ---
japan_capital_contribution_92_12 = japan_capital_share * japan_growth_capital_92_12
japan_labor_contribution_92_12 = japan_labor_share * japan_growth_labor_92_12
japan_tfp_growth_92_12 = japan_growth_output_92_12 - japan_capital_contribution_92_12 - japan_labor_contribution_92_12

#later change it to excel or latex
results_summary = pd.DataFrame({
    "Kyoto (72-92)": [kyoto_growth_output_72_92, kyoto_capital_share, kyoto_capital_contribution_72_92, kyoto_labor_share, kyoto_labor_contribution_72_92, kyoto_tfp_growth_72_92],
    "Kyoto (92-12)": [kyoto_growth_output_92_12, kyoto_capital_share, kyoto_capital_contribution_92_12, kyoto_labor_share, kyoto_labor_contribution_92_12, kyoto_tfp_growth_92_12],
    "Tokyo (72-92)": [tokyo_growth_output_72_92, tokyo_capital_share, tokyo_capital_contribution_72_92, tokyo_labor_share, tokyo_labor_contribution_72_92, tokyo_tfp_growth_72_92],
    "Tokyo (92-12)": [tokyo_growth_output_92_12, tokyo_capital_share, tokyo_capital_contribution_92_12, tokyo_labor_share, tokyo_labor_contribution_92_12, tokyo_tfp_growth_92_12],
    "Japan National (72-92)": [japan_growth_output_72_92, japan_capital_share, japan_capital_contribution_72_92, japan_labor_share, japan_labor_contribution_72_92, japan_tfp_growth_72_92],
    "Japan National (92-12)": [japan_growth_output_92_12, japan_capital_share, japan_capital_contribution_92_12, japan_labor_share, japan_labor_contribution_92_12, japan_tfp_growth_92_12]
}, index=["Real GDP Growth", "Capital Share", "Capital Contribution", "Labor Share", "Labor Contribution", "TFP Growth"])

# 记得改 打印整洁的汇总表，或者直接用 .to_excel("growth_accounting_results.xlsx") 保存
print(results_summary.round(2))
