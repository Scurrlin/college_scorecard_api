# The Cost of Virtuosity

This report uses data from the U.S. Department of Education's College Scorecard API to analyze key metrics for top music conservatories from 2012-2022.

## 🎼 Featured Schools

- **Berklee College of Music**
- **The Juilliard School** 
- **New England Conservatory**
- **Manhattan School of Music**
- **Curtis Institute of Music**

## 📊 **[View Report →](https://scurrlin.github.io/cost_of_virtuosity/)**

![Dashboard Preview](https://public.tableau.com/static/images/Ac/AcceptanceDash/AcceptanceDash/1.png)

## Key Metrics Tracked
- Total Enrollment
- Admission Rate
- Retention Rate (Full-time, 4-year)
- Graduation Rate (150% normal time)
- Tuition & Fees
- Average Net Price

## Quick Start

1. **Get API Key**: Register at [api.data.gov](https://api.data.gov/signup) 
2. **Set Environment Variable**: Create `.env` file with `SCORECARD_API_KEY=your_key_here`
3. **Install Dependencies**: `pip3 install requests pandas python-dotenv`
4. **Run Script**: `python3 api_to_csv.py` or `python3 api_to_sql.py`

---

*Data Source: [College Scorecard](https://collegescorecard.ed.gov/) - U.S. Department of Education*