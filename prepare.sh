#!/bin/bash

#Step 1
python generate_dirty_data.py

#Step 2
input="ms_data_dirty.csv"   
output="ms_data.csv"
grep -v '^#' "$input" |         
sed '/^$/d' |                        
sed 's/,,*/,/g' > "$output"  

#Step 3
ins="insurance.lst"
echo "insurance_type" > "$ins"
echo -e "Basic\nPremium\nPlatinum" >> "$ins"

#Step 4
total_visits=$(tail -n +2 "$output" | wc -l)
echo "Total visits: $total_visits"
head "$output"