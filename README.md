# Automated Insight Generation – AI/ML

An AI/ML-based healthcare analytics application that automatically analyzes healthcare data and generates meaningful insights related to trends, outliers, correlations, and threshold breaches.

The project provides an interactive Streamlit dashboard where users can explore healthcare indicators, apply filters, visualize trends, analyze correlations, and view automatically generated insights.

---

## 📌 Project Overview

Healthcare datasets often contain a large amount of information that can be difficult to analyze manually.

The **Automated Insight Generation Engine** is designed to automatically process healthcare data and identify important patterns in the dataset.

The system performs:

- Data loading and validation
- Trend detection
- Outlier detection
- Correlation analysis
- Threshold breach detection
- Automatic insight generation
- Severity classification
- Interactive data visualization

The generated insights help users quickly understand important changes and relationships in healthcare data.

---

## 🎯 Objectives

The main objectives of this project are:

1. Load and validate healthcare data from a CSV file.
2. Analyze healthcare indicators across districts and months.
3. Automatically detect significant trends.
4. Identify unusual or extreme values using outlier detection.
5. Find relationships between healthcare indicators using correlation analysis.
6. Generate human-readable insights dynamically from the data.
7. Classify generated insights based on their severity.
8. Provide an interactive dashboard for data exploration.
9. Export generated insights and correlation results as CSV files.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data processing and analysis |
| NumPy | Numerical operations |
| SciPy | Statistical analysis |
| Streamlit | Interactive web dashboard |
| Plotly | Interactive charts and visualizations |
| Git & GitHub | Version control and project hosting |

---

## 📊 Dataset

The project uses healthcare data containing indicators such as:

- Month
- District
- ANC Coverage
- Institutional Delivery
- Immunization
- High Risk Cases

### Example Dataset

| Month | District | ANC Coverage | Institutional Delivery | Immunization | High Risk Cases |
|---|---|---:|---:|---:|---:|
| 2026-07 | Ahmedabad | 85 | 91 | 93 | 10 |
| 2026-08 | Ahmedabad | 69 | 90 | 92 | 13 |
| 2026-07 | Surat | 81 | 87 | 91 | 13 |
| 2026-08 | Surat | 83 | 89 | 92 | 12 |
| 2026-07 | Vadodara | 90 | 93 | 96 | 7 |
| 2026-08 | Vadodara | 91 | 94 | 97 | 6 |
| 2026-07 | Rajkot | 79 | 85 | 89 | 15 |
| 2026-08 | Rajkot | 80 | 86 | 90 | 14 |
| 2026-07 | Mehsana | 84 | 89 | 92 | 11 |
| 2026-08 | Mehsana | 42 | 88 | 91 | 28 |
| 2026-07 | Bhavnagar | 77 | 82 | 87 | 17 |
| 2026-08 | Bhavnagar | 79 | 84 | 89 | 15 |

---

# 🔍 Key Features

## 1. Data Loading and Validation

The application loads healthcare data from a CSV file and performs basic validation before analysis.

It checks the availability and validity of required columns and prepares the dataset for further processing.

---

## 2. Trend Detection

The system compares indicator values across different time periods to identify significant increases or decreases.

The percentage change is calculated using:

```text
Percentage Change =
(Current Value - Previous Value) / Previous Value × 100

A configurable threshold is used to determine whether a change is significant.

For example:

Previous ANC Coverage = 85
Current ANC Coverage = 69

Percentage Change = -18.82%

The system can automatically generate an insight describing this change.

3. Outlier Detection

The project uses the Interquartile Range (IQR) method to detect unusual values.

The IQR is calculated as:

IQR = Q3 - Q1

Lower and upper boundaries are calculated using:

Lower Bound = Q1 - 1.5 × IQR

Upper Bound = Q3 + 1.5 × IQR

Values outside these boundaries are identified as potential outliers.

4. Correlation Analysis

The application calculates the Pearson correlation coefficient between numerical healthcare indicators.

Correlation values range from:

-1 to +1

A configurable correlation threshold can be used to identify strong relationships.

For example:

|Correlation| ≥ 0.70

can be considered a strong correlation.

The application also provides a correlation heatmap for visual analysis.

5. Threshold Breach Detection

The system can identify values that cross defined thresholds.

This helps highlight indicators that require additional attention.

Thresholds can be configured through the application.

6. Dynamic Insight Generation

Insights are generated dynamically from the analyzed data instead of being manually hardcoded.

Examples of generated insights include:

ANC Coverage decreased significantly in Ahmedabad.

An unusual ANC Coverage value was detected in Mehsana.

A strong correlation was detected between selected healthcare indicators.
7. Insight Severity

Generated insights are categorized according to their severity.

The project uses:

Low
Medium
High

Severity is determined based on the magnitude of the detected change or condition.

📈 Dashboard

The project provides an interactive Streamlit dashboard.

The dashboard allows users to:

Select districts
Select months
Select healthcare indicators
Configure trend thresholds
Configure correlation thresholds
View generated insights
View severity distribution
View trend charts
View correlation heatmaps
📁 Project Structure
Automated-Insight-Generation_AIML/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   └── healthcare_data.csv
│
├── outputs/
│   ├── insights.csv
│   └── correlation_matrix.csv
│
├── screenshots/
│   ├── dashboard.png
│   ├── trends.png
│   └── correlation.png
│
└── venv/

venv/ is a local Python virtual environment and should not be uploaded to GitHub.

📤 Generated Outputs

The application generates the following output files:

insights.csv

Contains automatically generated insights and information such as:

Insight ID
Insight type
Indicator
Entity/District
Period
Current value
Previous value
Percentage change
Severity
Explanation
correlation_matrix.csv

Contains the calculated Pearson correlation matrix between numerical healthcare indicators.

⚙️ Installation
1. Clone the Repository
git clone https://github.com/Princi310/Automated-Insight-Generation_AIML.git
2. Navigate to the Project
cd Automated-Insight-Generation_AIML
3. Create a Virtual Environment
python -m venv venv
4. Activate the Virtual Environment
Windows PowerShell
.\venv\Scripts\Activate.ps1

If PowerShell execution policy prevents activation, the application can also be run directly using the Python executable inside the virtual environment.

5. Install Dependencies
pip install -r requirements.txt
▶️ Running the Application

Run the following command:

streamlit run app.py

The Streamlit application will start and can be opened in a web browser.

📦 Requirements

The project dependencies are listed in requirements.txt.

pandas
numpy
scipy
streamlit
plotly
🔄 Application Workflow
Healthcare CSV Dataset
        ↓
Data Loading
        ↓
Data Validation
        ↓
Data Filtering
        ↓
 ┌───────────────┬───────────────┬────────────────┐
 ↓               ↓               ↓
Trend          Outlier       Correlation
Detection      Detection       Analysis
 ↓               ↓               ↓
 └───────────────┴───────────────┘
                 ↓
        Insight Generation
                 ↓
        Severity Classification
                 ↓
        Streamlit Dashboard
                 ↓
          CSV Output Files
💡 Example Insights

The system can identify situations such as:

Trend
ANC Coverage in Ahmedabad decreased significantly between the observed periods.
Outlier
An unusually low ANC Coverage value was detected for Mehsana.
Correlation
A strong relationship was detected between selected healthcare indicators.
Threshold Breach
The selected healthcare indicator crossed the configured threshold.
📸 Screenshots

Screenshots of the application dashboard, trend analysis, and correlation analysis are included in the screenshots/ folder.

⚠️ Limitations
The sample dataset contains a limited number of observations.
Correlation results may not be statistically reliable with a small dataset.
Generated insights depend on the quality and completeness of the input data.
Thresholds may need to be adjusted according to the specific healthcare use case.
The application is intended for analytical support and should not replace expert healthcare decision-making.
🚀 Future Enhancements

Possible future improvements include:

Real-time healthcare data integration
More advanced anomaly detection
Machine learning-based prediction
Natural Language Generation for richer insights
Automated report generation
Database integration
Role-based access
Deployment on cloud platforms
Larger real-world healthcare datasets
👩‍💻 Author

Princi310

GitHub:

https://github.com/Princi310
