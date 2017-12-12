from django.conf import settings

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
    if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql_psycopg2':
        return psql_execute_device_update_history_query(cursor, params)
    else:
        return sqlite_execute_device_update_history_query(cursor, params)


def execute_device_report_history(cursor, params):
    if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql_psycopg2':
        return psql_execute_device_report_history(cursor, params)
    else:
        return sqlite_execute_device_report_history(cursor, params)

def sqlite_execute_device_update_history_query(cursor, params):
    query = '''
    SELECT
        min(crashreports_heartbeat.date) as update_date,
        build_fingerprint,
        ( select count(crashreports_crashreport.id) from crashreports_crashreport
          where  boot_reason in ("UNKNOWN", "keyboard power on")
          and    crashreports_device.id == crashreports_crashreport.device_id
          and    crashreports_crashreport.build_fingerprint == crashreports_heartbeat.build_fingerprint ) as prob_crashes,
        ( select count(crashreports_crashreport.id) from crashreports_crashreport
        where  boot_reason in ("RTC alarm")
        and    crashreports_device.id == crashreports_crashreport.device_id
        and    crashreports_crashreport.build_fingerprint == crashreports_heartbeat.build_fingerprint ) as smpl,
        ( select count(crashreports_crashreport.id) from crashreports_crashreport
        where  boot_reason not in ("UNKNOWN", "keyboard power on", "RTC alarm")
        and    crashreports_device.id == crashreports_crashreport.device_id
        and    crashreports_crashreport.build_fingerprint == crashreports_heartbeat.build_fingerprint ) as other,
        count(crashreports_heartbeat.id) as heartbeats
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


def psql_execute_device_update_history_query(cursor, params):
    query = '''
    SELECT
        min(crashreports_heartbeat.date) as update_date,
        build_fingerprint,
        max(crashreports_device.id),
        ( select count(crashreports_crashreport.id) from crashreports_crashreport
          where  boot_reason in ('UNKNOWN', 'keyboard power on')
          and    max(crashreports_device.id) = crashreports_crashreport.device_id
          and    crashreports_crashreport.build_fingerprint = crashreports_heartbeat.build_fingerprint ) as prob_crashes,
        ( select count(crashreports_crashreport.id) from crashreports_crashreport
        where  boot_reason in ('RTC alarm')
        and    max(crashreports_device.id) = crashreports_crashreport.device_id
        and    crashreports_crashreport.build_fingerprint = crashreports_heartbeat.build_fingerprint ) as smpl,
        ( select count(crashreports_crashreport.id) from crashreports_crashreport
        where  boot_reason not in ('UNKNOWN', 'keyboard power on', 'RTC alarm')
        and    max(crashreports_device.id) = crashreports_crashreport.device_id
        and    crashreports_crashreport.build_fingerprint = crashreports_heartbeat.build_fingerprint ) as other,
        count(crashreports_heartbeat.id) as heartbeats
    FROM
        crashreports_device
    JOIN
        crashreports_heartbeat
    ON
        crashreports_device.id = crashreports_heartbeat.device_id
    where
        crashreports_device.uuid=%s
        group by build_fingerprint;
    '''
    uuid = params.get('uuid', '18f530d7-e9c3-4dcf-adba-3dddcd7d3155')
    param_array = [uuid]
    cursor.execute(query, param_array)


def sqlite_execute_device_report_history(cursor, params):
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


def psql_execute_device_report_history(cursor, params):
    query = '''
    SELECT
      crashreports_heartbeat.date::date as date,
      count(crashreports_heartbeat.id) as heartbeats,
      count(crashreports_crashreport.id) filter (where crashreports_crashreport.boot_reason in ('RTC alarm')) as SMPL,
      count(crashreports_crashreport.id) filter (where crashreports_crashreport.boot_reason in ('UNKNOWN', 'keyboard power on')) as prob_crashes,
      count(crashreports_crashreport.id) filter (where crashreports_crashreport.boot_reason not in ('RTC alarm', 'UNKNOWN', 'keyboard power on')) as other
    from crashreports_device
    join crashreports_heartbeat on crashreports_device.id = crashreports_heartbeat.device_id
    left join crashreports_crashreport on crashreports_device.id = crashreports_crashreport.device_id and  crashreports_heartbeat.date::date = crashreports_crashreport.date::date
    where
      crashreports_device.uuid = %s group by crashreports_heartbeat.date, crashreports_device.id;
    '''
    uuid = params.get('uuid', '18f530d7-e9c3-4dcf-adba-3dddcd7d3155')
    param_array = [uuid]
    cursor.execute(query, param_array)
