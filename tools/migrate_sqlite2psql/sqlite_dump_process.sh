#!/bin/bash

sed -e 's/INTEGER PRIMARY KEY AUTOINCREMENT/SERIAL PRIMARY KEY/' | \
sed -e 's/PRAGMA foreign_keys=OFF;//' | \
sed -e 's/unsigned big int/BIGINT/g' | \
sed -e 's/UNSIGNED BIG INT/BIGINT/g' | \
sed -e 's/BIG INT/BIGINT/g' | \
sed -e 's/UNSIGNED INT(10)/BIGINT/' |\
sed -e 's/BOOLEAN/SMALLINT/g' | \
sed -e 's/boolean/SMALLINT/g' | \
sed -e 's/UNSIGNED BIG INT/INTEGER/g' |\
sed -e 's/INT(3)/INT2/g' |\
sed -e 's/DATETIME/TIMESTAMP/g' |\
sed -e 's/DATETIME/TIMESTAMP/g' |\
grep -v "CREATE" | \
grep -v "BEGIN T" | \
grep -v "COMMIT" |\
grep -v "sqlite" 
