CREATE OR REPLACE FUNCTION "reset_sequence" (tablename text, columnname text)                                                       
RETURNS "pg_catalog"."void" AS                                                                                                                
$body$
DECLARE
BEGIN
EXECUTE format('SELECT setval(pg_get_serial_sequence(''%1$I'', %2$L),
        (SELECT COALESCE(MAX(%2$I)+1,1) FROM %1$I), false)',tablename,columnname);
END;
$body$  LANGUAGE 'plpgsql';

SELECT format('%s_%s_seq',table_name,column_name), reset_sequence(table_name,column_name)                                           
FROM information_schema.columns WHERE column_default like 'nextval%';
