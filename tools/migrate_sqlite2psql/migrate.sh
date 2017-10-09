#!/bin/bash

_db_conninfo=$1

_sqlite_db_path=$2

_db_cmdstr="psql --dbname=${_db_conninfo}"


( 
 echo "BEGIN;";
 cat create_tables.sql;
 echo "SET CONSTRAINTS ALL DEFERRED;";  
 sqlite $2 .dump | bash sqlite_dump_process.sh;
 echo "COMMIT"; 
) | $_db_cmdstr

(
 cat turn_to_boolean.sql;
 cat reset_sequences.sql;
) | $_db_cmdstr
