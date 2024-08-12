# Budget Impact Analysis of DMPA-SC Introduction in South Africa Over 4 Years

This models the budget impact of introducing DMPA-SC in South Africa over 4 years and tracks the cost and efficiency gain for users transitioning from DMPA-IM and NET-EN to the longer acting self injectable DMPSA-SC. The product costs are hypothetical and are solely for exploratory purposes. The [model](https://github.com/sethbarr/fp_dashboard/blob/main/dashboard.py) is hosted on OnRender and can be accessed [here](https://fp-dashboard.onrender.com/).

The following elements can be manipulated to explore possible outcomes:
1. The initial number of users of DMPA-IM, NET-EN, and DMPA-SC at baseline (Default values are 1,701,061; 552,108; and 0 respectively).
2. The annualized cost of healthcare facility visits for a woman using DMPA-IM, NET-EN, and DMPA-SC (Default values are ZAR1,316, ZAR1,974, and ZAR658 respectively).
3. The annualized cost of the product for DMPA-IM, NET-EN, and DMPA-SC (Default values are ZAR63, ZAR144, and ZAR116 respectively).
4. The conversion rate of users from DMPA-IM and NET-EN to DMPA-SC for each year (Default values are Year 1: 15.8417599%, Year 2: 35%, Year 3: 50%, Year 4: 65% for DMPA-IM to DMPA-SC; Year 1: 25%, Year 2: 35%, Year 3: 50%, Year 4: 65% for NET-EN to DMPA-SC).
5. Optionally, the user can specify the population size in each year to override the conversions.
6. Optionally, the user can specify the color of each cost element in the plot.

The model will produce a stacked bar plot showing the cost of healthcare facility visits, product costs, and the total cost for each year over the 4 year period and the efficiency gain for switching to DMPA-SC each year. The app will also produce a data table (downloadable as a `.csv` file) showing the number of users of each intervention, the cost of healthcare facility visits, product costs, and the total cost for each year over the 4 year period and the efficiency gain for switching to DMPA-SC each year.

The model is based on the following assumptions:
1. Family planning product costs are hypothetical and are solely for exploratory purposes.
2. Family planning product users are able to change from DMPA-IM and NET-EN to DMPA-SC but not _vice versa_.
3. The percent of users converting from DMPA-IM and NET-EN to DMPA-SC is specified as a percent, but the model does not produce fractional people. All floating point numbers are converted to integers.
4. The percent conversion rate is applied to the total number of users of DMPA-IM and NET-EN in the baseline year, not necessarily the year before.
   1. The model that does automatically apply the conversion rate to the number of users in the previous year is probably more generalizable, and is available in an earlier form (without some features as [`dashboard_dynamic.py`](https://github.com/sethbarr/fp_dashboard/blob/main/dashboard_dynamic.py)).