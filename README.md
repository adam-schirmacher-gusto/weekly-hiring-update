# weekly-hiring-update
Utilities to make it easier to present the team with weekly hiring updates.

# Instructions

1. Go to https://gusto.greenhouse.io/plans/192676/candidates?job_status=open&hiring_plan_id%5B%5D=192676
2. Export
3. Download from email
4. Open xls file downloaded, save as CSV
5. `python process_csv.py > /dev/null && cat out.csv`
6. Copy/paste value the output to the "raw" tab of `present.ods`
7. Use the "Present" tab to present
