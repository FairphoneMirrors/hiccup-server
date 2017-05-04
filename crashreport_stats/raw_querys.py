class FormatDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"

def fill_in_build_fingerprints(query, build_fingerprints):
    all_fingerprints_query = 'select distinct build_fingerprint from crashreports_crashreport'
    if len(build_fingerprints) > 0 :
        return query.format(
                FormatDict(fingerprint_placeholers=
                    ','.join(["%s"] * len(build_fingerprints))))
    else:
        return query.format(FormatDict(fingerprint_placeholers = all_fingerprints_query))

def execute_device_update_history_query(cursor, params):
    query = '''
    SELECT 
        min(crashreports_heartbeat.date) as update_date,
        build_fingerprint
    FROM 
        crashreports_device
    JOIN 
        crashreports_heartbeat 
    ON 
        crashreports_device.id == crashreports_heartbeat.device_id 
    where 
        crashreports_device.uuid=%s
        group by build_fingerprint;
    '''
    uuid = params.get('uuid', '18f530d7-e9c3-4dcf-adba-3dddcd7d3155')
    param_array = [uuid]
    cursor.execute(query, param_array)


def execute_device_report_history(cursor, params):
    query = '''
    SELECT
      strftime("%%Y-%%m-%%d",crashreports_heartbeat.date) as date, 
      count(crashreports_heartbeat.id) as heartbeats,
      (
        select count(id) from crashreports_crashreport 
        where 
          boot_reason in ("RTC alarm")  
          and strftime("%%Y-%%m-%%d",crashreports_crashreport.date) == strftime("%%Y-%%m-%%d",crashreports_heartbeat.date)
          and crashreports_device.id == crashreports_crashreport.device_id
      ) as smpl,
      (
        select count(id) from crashreports_crashreport 
        where 
          boot_reason in ("UNKNOWN", "keyboard power on") 
          and strftime("%%Y-%%m-%%d",crashreports_crashreport.date) == strftime("%%Y-%%m-%%d",crashreports_heartbeat.date)
          and crashreports_device.id == crashreports_crashreport.device_id
        ) as prob_crashes,
        (
        select count(id) from crashreports_crashreport 
        where 
          boot_reason not in ("RTC alarm", "UNKNOWN", "keyboard power on") 
          and strftime("%%Y-%%m-%%d",crashreports_crashreport.date) == strftime("%%Y-%%m-%%d",crashreports_heartbeat.date)
          and crashreports_device.id == crashreports_crashreport.device_id
        ) as other
    from crashreports_device 
    join 
      crashreports_heartbeat on crashreports_device.id == crashreports_heartbeat.device_id 
    where  
      crashreports_device.uuid = %s
    group by date;
    '''
    uuid = params.get('uuid', '18f530d7-e9c3-4dcf-adba-3dddcd7d3155')
    param_array = [uuid]
    cursor.execute(query, param_array)
