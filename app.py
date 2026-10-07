import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Automated Insight Generation",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Automated Healthcare Insight Generation")
st.write(
    "Automatically detect trends, outliers, correlations and "
    "generate actionable insights from healthcare data."
)


# ============================================================
# 2. LOAD DATA
# ============================================================

DATA_PATH = "data/healthcare_data.csv"

try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    st.error(f"Dataset not found at: {DATA_PATH}")
    st.stop()


# ============================================================
# 3. DATA VALIDATION
# ============================================================

st.header("1. Data Validation")

required_columns = [
    "month",
    "district",
    "anc_coverage",
    "institutional_delivery",
    "immunization",
    "high_risk_cases"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error(f"Missing columns: {missing_columns}")
    st.stop()

# Convert month to datetime
df["month"] = pd.to_datetime(df["month"])

numeric_columns = [
    "anc_coverage",
    "institutional_delivery",
    "immunization",
    "high_risk_cases"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")


# ============================================================
# 4. DATA INFORMATION
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Rows", len(df))

with col2:
    st.metric("Districts", df["district"].nunique())

with col3:
    st.metric("Months", df["month"].nunique())


with st.expander("View Dataset"):
    st.dataframe(df, use_container_width=True)

with st.expander("Missing Values"):
    missing_values = df.isnull().sum().reset_index()
    missing_values.columns = ["Column", "Missing Values"]
    st.dataframe(missing_values, use_container_width=True)


# ============================================================
# 5. SIDEBAR FILTERS
# ============================================================

st.sidebar.header("⚙️ Analysis Settings")

district_options = ["All"] + sorted(df["district"].unique().tolist())

selected_district = st.sidebar.selectbox(
    "District",
    district_options
)

month_options = ["All"] + sorted(
    df["month"].dt.strftime("%Y-%m").unique().tolist()
)

selected_month = st.sidebar.selectbox(
    "Month",
    month_options
)

indicator_options = numeric_columns

selected_indicator = st.sidebar.selectbox(
    "Indicator",
    indicator_options
)


# ============================================================
# 6. CONFIGURABLE THRESHOLDS
# ============================================================

trend_threshold = st.sidebar.slider(
    "Trend Threshold (%)",
    min_value=1,
    max_value=50,
    value=10
)

correlation_threshold = st.sidebar.slider(
    "Correlation Threshold",
    min_value=0.50,
    max_value=1.00,
    value=0.70,
    step=0.05
)

outlier_multiplier = st.sidebar.slider(
    "IQR Multiplier",
    min_value=1.0,
    max_value=3.0,
    value=1.5,
    step=0.5
)


# ============================================================
# 7. FILTER DATA
# ============================================================

filtered_df = df.copy()

if selected_district != "All":
    filtered_df = filtered_df[
        filtered_df["district"] == selected_district
    ]

if selected_month != "All":
    filtered_df = filtered_df[
        filtered_df["month"].dt.strftime("%Y-%m") == selected_month
    ]


st.header("2. Filtered Data")

st.dataframe(
    filtered_df,
    use_container_width=True
)


# ============================================================
# 8. TREND DETECTION
# ============================================================

def detect_trends(data, threshold):
    insights = []

    sorted_data = data.sort_values(
        ["district", "month"]
    )

    for district in sorted_data["district"].unique():

        district_data = sorted_data[
            sorted_data["district"] == district
        ]

        for indicator in numeric_columns:

            values = district_data[
                ["month", indicator]
            ].dropna()

            if len(values) < 2:
                continue

            for i in range(1, len(values)):

                previous_value = values.iloc[i - 1][indicator]
                current_value = values.iloc[i][indicator]

                if previous_value == 0:
                    continue

                change_pct = (
                    (current_value - previous_value)
                    / previous_value
                ) * 100

                if abs(change_pct) >= threshold:

                    if change_pct < 0:
                        direction = "decreased"
                    else:
                        direction = "increased"

                    severity_ratio = abs(change_pct) / threshold

                    if severity_ratio >= 2:
                        severity = "High"
                    elif severity_ratio >= 1:
                        severity = "Medium"
                    else:
                        severity = "Low"

                    period = values.iloc[i]["month"].strftime("%Y-%m")

                    explanation = (
                        f"{district} {indicator.replace('_', ' ')} "
                        f"{direction} by {abs(change_pct):.1f}% "
                        f"from {previous_value:.1f} to "
                        f"{current_value:.1f} during {period}."
                    )

                    insights.append({
                        "insight_id": f"TR-{len(insights)+1:03d}",
                        "type": "trend",
                        "indicator": indicator,
                        "entity": district,
                        "period": period,
                        "metric": current_value,
                        "previous_metric": previous_value,
                        "change_pct": round(change_pct, 2),
                        "severity": severity,
                        "explanation": explanation
                    })

    return insights


trend_insights = detect_trends(df, trend_threshold)


# ============================================================
# 9. OUTLIER DETECTION
# ============================================================

def detect_outliers(data, multiplier):
    insights = []

    for indicator in numeric_columns:

        values = data[indicator].dropna()

        if len(values) < 4:
            continue

        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - multiplier * iqr
        upper_bound = q3 + multiplier * iqr

        outlier_rows = data[
            (data[indicator] < lower_bound)
            | (data[indicator] > upper_bound)
        ]

        for _, row in outlier_rows.iterrows():

            value = row[indicator]

            if value < lower_bound:
                explanation = (
                    f"{row['district']} {indicator.replace('_', ' ')} "
                    f"value of {value:.1f} is below the IQR lower "
                    f"bound of {lower_bound:.1f}."
                )
            else:
                explanation = (
                    f"{row['district']} {indicator.replace('_', ' ')} "
                    f"value of {value:.1f} is above the IQR upper "
                    f"bound of {upper_bound:.1f}."
                )

            insights.append({
                "insight_id": f"OUT-{len(insights)+1:03d}",
                "type": "outlier",
                "indicator": indicator,
                "entity": row["district"],
                "period": row["month"].strftime("%Y-%m"),
                "metric": value,
                "previous_metric": np.nan,
                "change_pct": np.nan,
                "severity": "High",
                "explanation": explanation
            })

    return insights


outlier_insights = detect_outliers(df, outlier_multiplier)


# ============================================================
# 10. CORRELATION DETECTION
# ============================================================

correlation_matrix = df[numeric_columns].corr()

correlation_insights = []

for i in range(len(numeric_columns)):

    for j in range(i + 1, len(numeric_columns)):

        indicator_a = numeric_columns[i]
        indicator_b = numeric_columns[j]

        correlation_value = correlation_matrix.loc[
            indicator_a,
            indicator_b
        ]

        if (
            not pd.isna(correlation_value)
            and abs(correlation_value) >= correlation_threshold
        ):

            direction = (
                "positive"
                if correlation_value > 0
                else "negative"
            )

            correlation_insights.append({
                "insight_id": f"COR-{len(correlation_insights)+1:03d}",
                "type": "correlation",
                "indicator": f"{indicator_a} vs {indicator_b}",
                "entity": "All Districts",
                "period": "All",
                "metric": round(correlation_value, 3),
                "previous_metric": np.nan,
                "change_pct": np.nan,
                "severity": "Medium",
                "explanation": (
                    f"{indicator_a.replace('_', ' ')} and "
                    f"{indicator_b.replace('_', ' ')} have a "
                    f"{direction} Pearson correlation of "
                    f"{correlation_value:.2f}."
                )
            })


# ============================================================
# 11. COMBINE ALL INSIGHTS
# ============================================================

all_insights = (
    trend_insights
    + outlier_insights
    + correlation_insights
)

insights_df = pd.DataFrame(all_insights)


# ============================================================
# 12. INSIGHTS DISPLAY
# ============================================================

st.header("3. Automated Insights")

if insights_df.empty:

    st.info(
        "No significant insights were detected using the "
        "current thresholds."
    )

else:

    st.dataframe(
        insights_df,
        use_container_width=True
    )


# ============================================================
# 13. SEVERITY SUMMARY
# ============================================================

st.header("4. Severity Summary")

if not insights_df.empty:

    severity_counts = (
        insights_df["severity"]
        .value_counts()
        .reindex(
            ["Low", "Medium", "High"],
            fill_value=0
        )
        .reset_index()
    )

    severity_counts.columns = [
        "Severity",
        "Count"
    ]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Low",
            int(
                severity_counts[
                    severity_counts["Severity"] == "Low"
                ]["Count"].iloc[0]
            )
        )

    with col2:
        st.metric(
            "Medium",
            int(
                severity_counts[
                    severity_counts["Severity"] == "Medium"
                ]["Count"].iloc[0]
            )
        )

    with col3:
        st.metric(
            "High",
            int(
                severity_counts[
                    severity_counts["Severity"] == "High"
                ]["Count"].iloc[0]
            )
        )

    fig_severity = px.bar(
        severity_counts,
        x="Severity",
        y="Count",
        title="Insights by Severity"
    )

    st.plotly_chart(
        fig_severity,
        use_container_width=True
    )


# ============================================================
# 14. CORRELATION HEATMAP
# ============================================================

st.header("5. Correlation Analysis")

fig_corr = px.imshow(
    correlation_matrix,
    text_auto=".2f",
    title="Healthcare Indicator Correlation Matrix",
    aspect="auto"
)

st.plotly_chart(
    fig_corr,
    use_container_width=True
)


# ============================================================
# 15. DISTRICT TREND CHART
# ============================================================

st.header("6. District Trend Analysis")

trend_chart_df = df.copy()

if selected_district != "All":
    trend_chart_df = trend_chart_df[
        trend_chart_df["district"] == selected_district
    ]

fig_trend = px.line(
    trend_chart_df,
    x="month",
    y=selected_indicator,
    color="district",
    markers=True,
    title=f"{selected_indicator.replace('_', ' ').title()} Over Time"
)

st.plotly_chart(
    fig_trend,
    use_container_width=True
)


# ============================================================
# 16. SAVE OUTPUT FILES
# ============================================================

os.makedirs("outputs", exist_ok=True)

if not insights_df.empty:
    insights_df.to_csv(
        "outputs/insights.csv",
        index=False
    )

correlation_matrix.to_csv(
    "outputs/correlation_matrix.csv"
)


# ============================================================
# 17. DOWNLOAD INSIGHTS
# ============================================================

if not insights_df.empty:

    csv_data = insights_df.to_csv(index=False)

    st.download_button(
        label="⬇️ Download Insights CSV",
        data=csv_data,
        file_name="insights.csv",
        mime="text/csv"
    )

st.success("Analysis completed successfully!")