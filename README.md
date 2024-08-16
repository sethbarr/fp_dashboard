# Budget Impact Analysis of DMPA-SC Introduction in South Africa Over 4 Years

This models the budget impact of introducing DMPA-SC in South Africa over 4 years and tracks the cost and efficiency gain for users transitioning from DMPA-IM and NET-EN to the longer acting self injectable DMPSA-SC. The product costs are hypothetical and are solely for exploratory purposes. The [model](https://github.com/sethbarr/fp_dashboard/blob/main/dashboard.py) using [helper functions](https://github.com/sethbarr/fp_dashboard/blob/main/dashboard_helpers.py) is hosted on OnRender and can be accessed [here](https://fp-dashboard.onrender.com/).

The following elements can be manipulated to explore possible outcomes:
1. The initial number of users of DMPA-IM and NET-EN at baseline (Default values are 1,701,061; 552,108; and 0 respectively).
2. The cost per visit.
3. The number of visits per year for each intervention.
4. A first visit multiplier for DMPA-SC which increases the cost of the first visit (default 2x).
5. The annualized cost of the product for DMPA-IM (4/year), NET-EN (6/year), and DMPA-SC (4/year) (Default values are ZAR63.40, ZAR143.52, and ZAR116 respectively).
6. The market share conversion rates from DMPA-IM and NET-EN to DMPA-SC for each year (Default values are Year 1: 10%, Year 2:15%, Year 3: 20%, Year 4: 25% for DMPA-IM to DMPA-SC; Year 1: 25%, Year 2: 35%, Year 3: 50%, Year 4: 65% for NET-EN to DMPA-SC).
7. Optionally, the user can specify the population size in each year to override the conversions.
8. Optionally, the user can specify the color of each cost element in the plot.

The model will produce a stacked bar plot showing the cost of healthcare facility visits, product costs, and the total cost for each year over the 4 year period and the efficiency gain for switching to DMPA-SC each year. The app will also produce a data table (downloadable as a `.csv` file) showing the number of users of each intervention, the cost of healthcare facility visits, product costs, and the total cost for each year over the 4 year period and the efficiency gain for switching to DMPA-SC each year.

The model is based on the following assumptions:
1. Family planning product costs are hypothetical and are solely for exploratory purposes.
2. Family planning product users are able to change from DMPA-IM and NET-EN to DMPA-SC but not _vice versa_.
3. The market rate conversion from DMPA-IM and NET-EN to DMPA-SC is specified as a percent, but the model does not produce fractional people. All floating point numbers are converted to integers.
4. The market conversion rate is applied to the total number of users of DMPA-IM and NET-EN in the baseline year, not necessarily the year before.
   1. The model that does automatically apply the market conversion to the number of users in the previous year is probably more generalizable, and is available in an earlier form (without some features as [`dashboard_dynamic.py`](https://github.com/sethbarr/fp_dashboard/blob/main/dashboard_dynamic.py)).


### We have examined the following scenarios. * Note NET-EN population increases slightly by year based on numbers provided.

| Scenario | DMPA-IM Starting Population | NET-EN Starting Population | DMPA-IM -> DMPA-SC Conversion Rates | NET-EN -> DMPA-SC Conversion Rates | Scenario Description |
|----------|-----------------------------|----------------------------|-------------------------------------|------------------------------------| ---------------------|
| 1        | 1,701,061                   | 0                    | 15.8417599%, 35%, 50%, 65%         | N/A                 | Rapid adoption of DMPA-IM users without considering NET-EN users    |
| 2        | 1,701,061                   | 552,108*                    | 10%, 15%, 20%, 25%         | 10%, 15%, 20%, 25%                 | Slower but consistent adoption of DMPA-IM users and NET-EN users    |
| 3        | 1,701,061                   | 552,108*                    | 10%, 15%, 20%, 25%         | 25%, 35%, 50%, 65%                 | Slower adoption of DMPA-IM users and fast adoption of NET-EN users    |
