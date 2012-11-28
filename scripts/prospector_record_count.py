deployment_duration_yrs = 1.5
days_per_year = 365
hours_per_day = 24
min_per_hour = 60
seconds_per_min = 60

# total fifteenMin records on Card
table1_minutes_per_record = 15
records_per_hour = min_per_hour / table1_minutes_per_record
records_per_year = (records_per_hour * hours_per_day) * days_per_year
print "Total number of fifteen minute records for the", deployment_duration_yrs, "year deployment is: ", records_per_year * deployment_duration_yrs

# total oneMin records on Card
table2_minutes_per_record = 1
records_per_hour = min_per_hour / table2_minutes_per_record
records_per_year = (records_per_hour * hours_per_day) * days_per_year
print "Total number of one minute records for the", deployment_duration_yrs, "year deployment is: ", records_per_year * deployment_duration_yrs

# total threeSec records on Card
table3_seconds_per_record = 3
records_per_hour = (seconds_per_min * min_per_hour) / table3_seconds_per_record
records_per_year = (records_per_hour * hours_per_day) * days_per_year
print "Total number of three second records for the", deployment_duration_yrs, "year deployment is: ", records_per_year * deployment_duration_yrs

# total threeSec records on CPU
table3_seconds_per_record = 3
records_per_hour = (seconds_per_min * min_per_hour) / table3_seconds_per_record
print "Total number of three second records for one hour is: ", records_per_hour