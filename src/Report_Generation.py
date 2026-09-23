# AUTOMATIC PDF REPORT GENERATION

import pandas as pd
import matplotlib.pyplot as plt

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

# 1. LOAD DATA

mf_data = pd.read_csv(
    "../data/combined_mutual_fund_data.csv"
)

direct_equity = pd.read_csv(
    "../data/direct_equity/direct_equity_monthly_data.csv"
)

print("Data loaded successfully")

# 2. BASIC CALCULATIONS

yearly_aum = (
    mf_data.groupby("Year")["AUM"]
    .mean()
)

yearly_inflow = (
    mf_data.groupby("Year")["Net_Inflow"]
    .mean()
)

yearly_equity = (
    direct_equity.groupby("Year")
    ["Total_Equity_Settlement_Value"]
    .mean()
)

top_schemes = (
    mf_data.groupby("Scheme_Name")["AUM"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

positive_inflow = (
    mf_data["Net_Inflow"] > 0
).sum()

negative_inflow = (
    mf_data["Net_Inflow"] < 0
).sum()

# 3. CREATE CHART 1 - AUM
yearly_aum.plot(
    kind="line",
    marker="o"
)
plt.title("Year-wise Average AUM")
plt.xlabel("Year")
plt.ylabel("Average AUM")
plt.grid()
plt.savefig(
    "aum_chart.png",
    bbox_inches="tight"
)
plt.close()

# 4. CREATE CHART 2 - NET INFLOW

yearly_inflow.plot(
    kind="line",
    marker="o"
)
plt.title("Year-wise Average Net Inflow")
plt.xlabel("Year")
plt.ylabel("Average Net Inflow")
plt.grid()
plt.savefig(
    "net_inflow_chart.png",
    bbox_inches="tight"
)
plt.close()

# 5. CREATE CHART 3 - DIRECT EQUITY

yearly_equity.plot(
    kind="line",
    marker="o"
)

plt.title(
    "Year-wise Average Direct Equity Settlement Value"
)
plt.xlabel("Year")
plt.ylabel("Average Settlement Value")
plt.grid()
plt.savefig(
    "direct_equity_chart.png",
    bbox_inches="tight"
)
plt.close()

# 6. CREATE CHART 4 - BSE VS NSE

bse_nse = direct_equity[
    ["BSE_Equity_Value", "NSE_Equity_Value"]
].mean()

bse_nse.plot(
    kind="bar"
)
plt.title("Average BSE vs NSE Equity Value")
plt.xlabel("Exchange")
plt.ylabel("Average Equity Value")
plt.xticks(rotation=0)
plt.savefig(
    "bse_nse_chart.png",
    bbox_inches="tight"
)
plt.close()

# 7. CREATE CHART 5 - MF VS EQUITY

mf_yearly = (
    mf_data.groupby("Year")["AUM"]
    .mean()
)
equity_yearly = (
    direct_equity.groupby("Year")
    ["Total_Equity_Settlement_Value"]
    .mean()
)
comparison = pd.DataFrame({
    "Mutual_Fund_AUM": mf_yearly,
    "Direct_Equity_Value": equity_yearly
})
comparison = comparison.loc[
    [2024, 2025, 2026]
]
comparison["MF_Index"] = (
    comparison["Mutual_Fund_AUM"]
    / comparison["Mutual_Fund_AUM"].iloc[0]
) * 100

comparison["Equity_Index"] = (
    comparison["Direct_Equity_Value"]
    / comparison["Direct_Equity_Value"].iloc[0]
) * 100

comparison[
    ["MF_Index", "Equity_Index"]
].plot(
    kind="line",
    marker="o"
)

plt.title(
    "Mutual Fund vs Direct Equity Trend"
)

plt.xlabel("Year")
plt.ylabel("Index (2024 = 100)")

plt.xticks(
    [2024, 2025, 2026]
)

plt.grid()

plt.savefig(
    "comparison_chart.png",
    bbox_inches="tight"
)
plt.close()

# 8. CREATE CHART 6 - TOP SCHEMES

top_schemes.plot(
    kind="barh"
)

plt.title(
    "Top 10 Mutual Fund Schemes by Average AUM"
)

plt.xlabel("Average AUM")
plt.ylabel("Scheme")
plt.savefig(
    "top_schemes_chart.png",
    bbox_inches="tight"
)
plt.close()


# 9. CREATE CHART 7 - POSITIVE VS NEGATIVE

inflow_data = [
    positive_inflow,
    negative_inflow
]

plt.bar(
    ["Positive", "Negative"],
    inflow_data
)

plt.title(
    "Positive vs Negative Net Inflow"
)
plt.xlabel("Net Inflow")
plt.ylabel("Number of Records")
plt.savefig(
    "positive_negative_chart.png",
    bbox_inches="tight"
)
plt.close()

# 10. CREATE PDF

pdf = SimpleDocTemplate(
    "Mutual_Fund_Direct_Equity_Report.pdf",
    pagesize=A4
)
styles = getSampleStyleSheet()
report = []

# TITLE
report.append(
    Paragraph(
        "Mutual Fund Vs Direct Equity Investment Trend Analysis",
        styles["Title"]
    )
)
report.append(
    Spacer(1, 20)
)

# BUSINESS INSIGHTS

report.append(
    Paragraph(
        "Business Insights",
        styles["Heading1"]
    )
)
report.append(
    Spacer(1, 10)
)
report.append(
    Paragraph(
        f"1. Highest average Mutual Fund AUM was recorded in "
        f"{yearly_aum.idxmax()}.",
        styles["BodyText"]
    )
)

report.append(
    Paragraph(
        f"2. Highest average Mutual Fund Net Inflow was recorded in "
        f"{yearly_inflow.idxmax()}.",
        styles["BodyText"]
    )
)

report.append(
    Paragraph(
        f"3. Highest average Direct Equity Settlement Value was "
        f"recorded in {yearly_equity.idxmax()}.",
        styles["BodyText"]
    )
)

report.append(
    Paragraph(
        f"4. Top Mutual Fund Scheme by average AUM was "
        f"{top_schemes.index[0]}.",
        styles["BodyText"]
    )
)

report.append(
    Paragraph(
        f"5. Positive Net Inflow Records: {positive_inflow}.",
        styles["BodyText"]
    )
)

report.append(
    Paragraph(
        f"6. Negative Net Inflow Records: {negative_inflow}.",
        styles["BodyText"]
    )
)

report.append(
    Spacer(1, 20)
)

# ADD CHARTS TO PDF
charts = [
    (
        "Year-wise Average AUM",
        "aum_chart.png"
    ),
    (
        "Year-wise Average Net Inflow",
        "net_inflow_chart.png"
    ),
    (
        "Direct Equity Trend",
        "direct_equity_chart.png"
    ),
    (
        "BSE vs NSE Equity Value",
        "bse_nse_chart.png"
    ),
    (
        "Mutual Fund vs Direct Equity Trend",
        "comparison_chart.png"
    ),
    (
        "Top 10 Mutual Fund Schemes",
        "top_schemes_chart.png"
    ),
    (
        "Positive vs Negative Net Inflow",
        "positive_negative_chart.png"
    )
]
for title, chart in charts:

    report.append(
        Paragraph(
            title,
            styles["Heading2"]
        )
    )

    report.append(
        Image(
            chart,
            width=450,
            height=280
        )
    )

    report.append(
        Spacer(1, 15)
    )

# CONCLUSION

report.append(
    Paragraph(
        "Conclusion",
        styles["Heading1"]
    )
)

report.append(
    Paragraph(
        "The analysis compares Mutual Fund and Direct Equity "
        "investment trends using historical financial data. "
        "Mutual Fund analysis focuses on AUM, Net Inflow and "
        "scheme-level AUM, while Direct Equity analysis focuses "
        "on settlement value and BSE-NSE comparison. The analysis "
        "helps identify investment trends and provides useful "
        "business insights from the available data.",
        styles["BodyText"]
    )
)

# GENERATE PDF

pdf.build(report)

print(
    "PDF Report Generated Successfully!"
)