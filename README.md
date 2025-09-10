# College Scorecard API - Music Schools Analysis

This project fetches data from the U.S. Department of Education's College Scorecard API to analyze key metrics for top music conservatories from 2012-2022.

## 🎼 Featured Music Schools

- **Berklee College of Music**
- **The Juilliard School** 
- **New England Conservatory**
- **Manhattan School of Music**
- **Curtis Institute of Music**

## 📊 **[View Interactive Report →](./index.html)**

### **Comprehensive Analysis with 19 Tableau Dashboards**

**[→ Music Conservatories Analysis: A Comprehensive Study (2012-2022)](./index.html)**

This interactive report includes:

- **📈 Student Outcomes:** Acceptance, retention, and graduation rate analysis
- **💰 Financial Analysis:** Tuition trends and net price comparisons across institutions
- **🏫 Individual School Profiles:** Dedicated dashboards for each conservatory
- **📊 Enrollment Patterns:** Multi-year trends and institutional insights
- **📝 Academic Analysis:** Professional report format with methodology and conclusions

![Dashboard Preview](https://public.tableau.com/static/images/To/TotalEnrollmentDash/TotalEnrollmentDash/1.png)

## 🔧 How It Works

The `scorecard_api.py` script:

1. **Fetches Data**: Connects to the College Scorecard API using your API key
2. **Processes Metrics**: Collects enrollment, admission rates, retention, graduation rates, and cost data
3. **Exports Results**: Creates both long and wide format CSV files for analysis

### Key Metrics Tracked
- Total Enrollment
- Admission Rate
- Retention Rate (Full-time, 4-year)
- Graduation Rate (150% normal time)
- Tuition & Fees
- Average Net Price

## 🚀 Quick Start

1. **Get API Key**: Register at [api.data.gov](https://api.data.gov/signup) 
2. **Set Environment**: Create `.env` file with `SCORECARD_API_KEY=your_key_here`
3. **Install Dependencies**: `pip install requests pandas python-dotenv`
4. **Run Script**: `python scorecard_api.py`

## 📁 Output Files

- `music_school_long_YYYY_YYYY_YYYYMMDD.csv` - Long format (one row per school per year)
- `music_school_wide_YYYY_YYYY_YYYYMMDD.csv` - Wide format (pivot table structure)

## 🎯 Use Cases

- **Comparative Analysis**: Compare music schools across multiple dimensions
- **Trend Analysis**: Track changes in enrollment and performance over time
- **Cost Analysis**: Understand tuition trends and net prices
- **Academic Performance**: Analyze retention and graduation rates

---

*Data Source: [College Scorecard](https://collegescorecard.ed.gov/) - U.S. Department of Education*
