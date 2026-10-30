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
# The results are compared with Tokyo perfecture. 
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

#later change it to excel or latex
results_summary = pd.DataFrame({
    "Kyoto (72-92)": [kyoto_growth_output_72_92, kyoto_capital_share, kyoto_capital_contribution_72_92, kyoto_labor_share, kyoto_labor_contribution_72_92, kyoto_tfp_growth_72_92],
    "Kyoto (92-12)": [kyoto_growth_output_92_12, kyoto_capital_share, kyoto_capital_contribution_92_12, kyoto_labor_share, kyoto_labor_contribution_92_12, kyoto_tfp_growth_92_12],
    "Tokyo (72-92)": [tokyo_growth_output_72_92, tokyo_capital_share, tokyo_capital_contribution_72_92, tokyo_labor_share, tokyo_labor_contribution_72_92, tokyo_tfp_growth_72_92],
    "Tokyo (92-12)": [tokyo_growth_output_92_12, tokyo_capital_share, tokyo_capital_contribution_92_12, tokyo_labor_share, tokyo_labor_contribution_92_12, tokyo_tfp_growth_92_12]
}, index=["Real GDP Growth", "Capital Share", "Capital Contribution", "Labor Share", "Labor Contribution", "TFP Growth"])

# 记得改 打印整洁的汇总表，或者直接用 .to_excel("growth_accounting_results.xlsx") 保存
print(results_summary.round(2))
#=====================================================================================================================
# Kyoto shift-share decomposition
#=======================================================================================================================
# Growth accounting shows that TFP is the main source of productivity growth
# but it does not tell us where that growth occurs
# To answer why Kyoto maintained productivity growth despite a declining workforce
# Objective: first need to identify the sources of labor productivity growth 
# To conduct the decomposition, I need to construct follwoing variables: labor productivity, Initial industry labor share, Initial industry labor productivity, Change in industry labor productivity,Change in industry labor share. 
# In R-JIP, "T" marks the Total row; excluded so it is not counted as a 24th industry
real_value_added_industries = df_real_value_added[(df_real_value_added.iloc[:, 1] == "Kyoto") & (df_real_value_added.iloc[:, 2] != "T")]
assert len(real_value_added_industries) == 23
man_hours_industries = df_man_hours[(df_man_hours.iloc[:, 1] == "Kyoto") & (df_man_hours.iloc[:, 2] != "T")]
assert len(man_hours_industries) == 23

real_value_1992, real_value_2012 = kyoto_output_1992, kyoto_output_2012
man_hours_1992, man_hours_2012 = kyoto_labor_1992, kyoto_labor_2012

assert np.isclose(real_value_1992, real_value_added_industries[1992].sum())
assert np.isclose(real_value_2012, real_value_added_industries[2012].sum())
assert np.isclose(man_hours_1992, man_hours_industries[1992].sum())
assert np.isclose(man_hours_2012, man_hours_industries[2012].sum())

# Labor input is man-hours, productivity = real value added per man-hour
Big_X_1992 = real_value_1992 / man_hours_1992
Big_X_2012 = real_value_2012 / man_hours_2012
change_in_X = Big_X_2012 - Big_X_1992 

# Calculates each industry's initial labor share as its proportion of total labor input at the beginning of the period
# serves as the weight for the within-industry effect
# computing change in share
# used to calculate the across-effect and interaction effect
s_i_1992 = pd.Series(man_hours_industries[1992].values, index=man_hours_industries.iloc[:, 3].str.strip()) / man_hours_1992  
s_i_2012 = pd.Series(man_hours_industries[2012].values, index=man_hours_industries.iloc[:, 3].str.strip()) / man_hours_2012   
assert np.isclose(s_i_1992.sum(), 1) and np.isclose(s_i_2012.sum(), 1)
change_in_si = s_i_2012 - s_i_1992 
# Ensure industry ordering and alignment between value added and man-hours
assert (real_value_added_industries.iloc[:, 3].str.strip().values == man_hours_industries.iloc[:, 3].str.strip().values).all()

# Calculate the initial productivity level of each industry 
# serves as the weight for changes in industry labor shares when calculating the across-industry effect
# computing Change in industry labor productivity
# used to calculate the within-industry effect and interaction effect
xi_1992 = pd.Series(real_value_added_industries[1992].values / man_hours_industries[1992].values, index=real_value_added_industries.iloc[:, 3].str.strip())
xi_2012 = pd.Series(real_value_added_industries[2012].values / man_hours_industries[2012].values, index=real_value_added_industries.iloc[:, 3].str.strip())
change_in_xi = xi_2012 - xi_1992

# I calculate the within-industry, across-industry, and interaction effects.
# To connect productivity growth to economic performance, I convert each effect into an AAGR contribution.
within_effect = s_i_1992 * change_in_xi 
across_effect = xi_1992 * change_in_si 
interaction_effect = change_in_si * change_in_xi 

total_within = within_effect.sum()
total_across = across_effect.sum() 
total_interaction = interaction_effect.sum() 
# The three effects must sum to the change in labor productivity.
assert np.isclose(total_within + total_across + total_interaction, change_in_X)

aagr_change_in_worker = (100 / (man_hours_1992 * n)) * (man_hours_2012 - man_hours_1992)
scaling_factor = 100 / (Big_X_1992 * n) 
aagr_within = total_within * scaling_factor 
aagr_across = total_across * scaling_factor 
aagr_interaction = total_interaction * scaling_factor 
# Y = labor term + productivity term x (N1/N0); see Appendix for mathematical derivation
computed_aagr_Y = aagr_change_in_worker + (aagr_within + aagr_across + aagr_interaction) * (man_hours_2012 / man_hours_1992)
# Verify that the AAGR calculate from the shift-share decomposition
# matches the AAGR calculated directly using the standard definition.
aagr_Y_direct = 100 * (real_value_2012 - real_value_1992) / (real_value_1992 * n) 
assert np.isclose(computed_aagr_Y, aagr_Y_direct)


# Apply the same decomposition to Japan as a whole to compare Kyoto's
# productivity growth pattern with the national pattern.
real_value_added_japan_industries = df_real_value_added[(df_real_value_added.iloc[:, 1] == "Total") & (df_real_value_added.iloc[:, 2] != "T")]
assert len(real_value_added_japan_industries) == 23
man_hours_japan_industries = df_man_hours[(df_man_hours.iloc[:, 1] == "Total") & (df_man_hours.iloc[:, 2] != "T")]
assert len(man_hours_japan_industries) == 23
# Ensure industry ordering and alignment between national value added and man-hours
assert (real_value_added_japan_industries.iloc[:, 3].str.strip().values == man_hours_japan_industries.iloc[:, 3].str.strip().values).all()
japan_industry_names = real_value_added_japan_industries.iloc[:, 3].str.strip().values

man_hours_1992_japan_industries = man_hours_japan_industries[1992].values
man_hours_2012_japan_industries = man_hours_japan_industries[2012].values 
real_value_1992_japan_industries = real_value_added_japan_industries[1992].values 
real_value_2012_japan_industries = real_value_added_japan_industries[2012].values

# Extract national aggregate (Total) real value added and man-hours for Japan
real_value_added_japan_total = df_real_value_added[(df_real_value_added.iloc[:, 1] == "Total") & (df_real_value_added.iloc[:, 2] == "T")]
man_hours_japan_total = df_man_hours[(df_man_hours.iloc[:, 1] == "Total") & (df_man_hours.iloc[:, 2] == "T")]
# Ensure one national aggregate entry
assert len(real_value_added_japan_total) == 1 and len(man_hours_japan_total) == 1  

real_value_1992_japan, real_value_2012_japan = real_value_added_japan_total[1992].iloc[0], real_value_added_japan_total[2012].iloc[0]
man_hours_1992_japan, man_hours_2012_japan = man_hours_japan_total[1992].iloc[0], man_hours_japan_total[2012].iloc[0]
# Ensure that the national aggregate totals exactly match the sum of the 23 sub-industries
assert np.isclose(real_value_1992_japan, real_value_1992_japan_industries.sum()) and np.isclose(real_value_2012_japan, real_value_2012_japan_industries.sum()) 
assert np.isclose(man_hours_1992_japan, man_hours_1992_japan_industries.sum()) and np.isclose(man_hours_2012_japan, man_hours_2012_japan_industries.sum())

# producivity 
Big_X_1992_jap = real_value_1992_japan / man_hours_1992_japan  
Big_X_2012_jap = real_value_2012_japan / man_hours_2012_japan 
# share of emploment 
s_i_1992_japan = pd.Series(man_hours_1992_japan_industries, index=japan_industry_names) / man_hours_1992_japan
s_i_2012_japan = pd.Series(man_hours_2012_japan_industries, index=japan_industry_names) / man_hours_2012_japan
change_in_si_japan = s_i_2012_japan - s_i_1992_japan

# industry producivity 
xi_1992_japan = pd.Series(real_value_1992_japan_industries / man_hours_1992_japan_industries, index=japan_industry_names)
xi_2012_japan = pd.Series(real_value_2012_japan_industries / man_hours_2012_japan_industries, index=japan_industry_names)
change_in_xi_japan = xi_2012_japan - xi_1992_japan
# Verify aggregation consistency: weighted sum of industry productivities must equal macro aggregate productivity
assert np.isclose((s_i_1992_japan * xi_1992_japan).sum(), Big_X_1992_jap) 
assert np.isclose((s_i_2012_japan * xi_2012_japan).sum(), Big_X_2012_jap)

# Japan decomposition and converting to aagr
within_effect_jap = s_i_1992_japan * change_in_xi_japan
across_effect_jap = xi_1992_japan * change_in_si_japan
interaction_effect_jap = change_in_si_japan * change_in_xi_japan

total_within_jap = within_effect_jap.sum() 
total_across_jap = across_effect_jap.sum() 
total_interaction_jap = interaction_effect_jap.sum() 


change_in_X_jap = Big_X_2012_jap - Big_X_1992_jap 
#check, Verify that the sum of the three shift-share components equals total productivity change 
assert np.isclose(total_within_jap + total_across_jap + total_interaction_jap, change_in_X_jap) 

aagr_change_in_worker_jap = (100 / (man_hours_1992_japan * n)) * (man_hours_2012_japan - man_hours_1992_japan)
scaling_factor_jap = 100 / (Big_X_1992_jap * n) 
aagr_within_jap = total_within_jap * scaling_factor_jap 
aagr_across_jap = total_across_jap * scaling_factor_jap
aagr_interaction_jap = total_interaction_jap * scaling_factor_jap
computed_aagr_Y_jap = aagr_change_in_worker_jap + (aagr_within_jap + aagr_across_jap + aagr_interaction_jap) * (man_hours_2012_japan / man_hours_1992_japan)
aagr_Y_direct_japan = 100 * (real_value_2012_japan - real_value_1992_japan) / (real_value_1992_japan * n)   # compute aagr y using aagr definition
# check, the two answer should be the same 
assert np.isclose(computed_aagr_Y_jap, aagr_Y_direct_japan) 

# 6. Result come back and fix it later 
for name, w, a, i, lab, gdp in [
    ("Kyoto", aagr_within, aagr_across, aagr_interaction, aagr_change_in_worker, aagr_Y_direct),
    ("Japan", aagr_within_jap, aagr_across_jap, aagr_interaction_jap, aagr_change_in_worker_jap, aagr_Y_direct_japan),
]:
    print(f"{name}: within {w:.2f}  across {a:.2f}  interaction {i:.2f} | labor productivity {w+a+i:.2f}  labor {lab:.2f}  GDP {gdp:.2f}")

# I want to know Industry share of within effect, to see which industry contribute the most 
industry_share_of_within_percent = (within_effect / total_within) * 100
df_kyoto_within_shares = pd.DataFrame({
    "Share_of_Total_Within_Percent": industry_share_of_within_percent
}).sort_values(by="Share_of_Total_Within_Percent", ascending=False)
assert np.isclose(df_kyoto_within_shares["Share_of_Total_Within_Percent"].sum(), 100.0)
print("\nTop 5 Industries by Share of Within Effect:")
print(df_kyoto_within_shares.head(5).round(2))
#====================================================================================================
# PANEL DATA CONSTRUCTION (INDUSTRY-YEAR)
#====================================================================================================
# The decomposition shows that productivity growth came from within industries.
# Electrical machinery contributed the most. But the decomposition does not explain what generated these gains.
# Prior studies suggest automation as a poential driver.  
# If automation drove these gains, industries that automated more should have experienced faster TFP growth.
# The R-JIP database has no direct measure of automation. I therefore use capital deepening as a proxy. 
# Testing this requires variation across industries and over time. I therefore construct an industry-year panel for Kyoto.
exact_industry_mapping = {
    "Food and beverages": "Food and beverages",
    "Textile mill products": "Textile mill products",
    "Pulp and paper": "Pulp and paper",
    "Chemicals": "Chemicals",
    "Petroleum and coal products": "Petroleum and coal products",
    "Ceramics, stone and clay": "Ceramics, stone and clay",
    "Basic metal": "Basic metal",
    "Processed metals": "Processed metals",
    "General machinery": "General machinery",
    "Electrical machinery": "Electrical machinery",
    "Transport equipment": "Transport equipment",
    "Precision instruments": "Precision instruments",
    "Other manufacturing": "Other manufacturing"
}

# Real Value Added used to construct TFP and output growth
# Net Capital Stock used to construct TFP and capital deepening.
# Man-hours used to measures labor input and is used to construct TFP. 
# Nominal Value Added provides the denominator for calculating the labor share,alhpa
# Labor Costs is the numerator for calculating the labor share, alpha.
# Number of Employed Persons is used to calculate capital per worker K/N, which serves as a proxy for automation
# Quality of Capital serves as an alternative proxy for automation in the regression analysis.
sheets_to_process = {
    "Real value added (RV)": "Y_Real_Value_Added",
    "Net capital stock (KT)": "K_Net_Capital",
    "Man-hours (MH)": "L_Man_Hours",
    "Nominal value added (NV)": "NV_Nominal_Value_Added",
    "Labor costs (WL)": "WL_Labor_Costs",
    "Number of employed persons (N)": "E_Employed_Persons",
    "Quality of capital (QK)": "QK_Capital_Quality"
}

kyoto_panel_melted_dataframes = []

for excel_sheet_name, target_variable_name in sheets_to_process.items():
    # Reuse previously loaded sheets and read the remaining sheets directly.
    if excel_sheet_name == "Real value added (RV)":
        df_sheet_raw = df_real_value_added
    elif excel_sheet_name == "Net capital stock (KT)":
        df_sheet_raw = df_capital_stock
    elif excel_sheet_name == "Man-hours (MH)":
        df_sheet_raw = df_man_hours
    elif excel_sheet_name == "Nominal value added (NV)":
        df_sheet_raw = df_nominal_value_added
    elif excel_sheet_name == "Labor costs (WL)":
        df_sheet_raw = df_labor_cost
    else:
        df_sheet_raw = pd.read_excel(excel_file, sheet_name=excel_sheet_name, header=2)
    
    df_kyoto_filtered = df_sheet_raw[
        (df_sheet_raw.iloc[:, 1] == "Kyoto") & (df_sheet_raw.iloc[:, 2] != "T")
    ].copy()
    
    # Standardize industry names and retain only the 13 target manufacturing industries.
    df_kyoto_filtered["Raw_Industry_Name"] = df_kyoto_filtered.iloc[:, 3].astype(str).str.strip()
    df_kyoto_filtered["Industry"] = df_kyoto_filtered["Raw_Industry_Name"].map(exact_industry_mapping)
    df_kyoto_filtered = df_kyoto_filtered.dropna(subset=["Industry"])
    
     # Verify that every required year is available
    missing_years = [yr for yr in years_range if yr not in df_kyoto_filtered.columns]
    assert not missing_years, f"Sheet '{excel_sheet_name}' is missing expected year columns: {missing_years}"
    
    # industry-year panel
    df_industry_year_long = df_kyoto_filtered[["Industry"] + years_range].melt(
        id_vars=["Industry"], value_vars=years_range, var_name="Year", value_name=target_variable_name
    )
    df_industry_year_long["Year"] = df_industry_year_long["Year"].astype(int)
    
    assert not df_industry_year_long.duplicated(subset=["Industry", "Year"]).any(), \
        f"Duplicate Industry-Year pairs detected in sheet '{excel_sheet_name}'!"
  # Index by industry and year       
    df_industry_year_long = df_industry_year_long.set_index(["Industry", "Year"])
    kyoto_panel_melted_dataframes.append(df_industry_year_long)

kyoto_manufacturing_panel = pd.concat(kyoto_panel_melted_dataframes, axis=1).reset_index()
kyoto_manufacturing_panel = kyoto_manufacturing_panel.sort_values(by=["Industry", "Year"]).reset_index(drop=True)

# Final sanity check 
# total number of observations matches the expected number of industries multiplied by the number of years.
# Verify that all 13 target manufacturing industries are represented in the panel
# Ensure that each industry-year pair appears only once in the panel
# Verify that all seven variables contain no missing values across the panel
assert len(kyoto_manufacturing_panel) == len(exact_industry_mapping) * len(years_range), \
    "Panel row count mismatch! Check industry filtering or year span."
assert kyoto_manufacturing_panel["Industry"].nunique() == 13
assert not kyoto_manufacturing_panel.duplicated(
    subset=["Industry", "Year"]
).any()
assert not kyoto_manufacturing_panel[
    list(sheets_to_process.values())
].isna().any().any()
