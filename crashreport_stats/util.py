from django.db import migrations, models
import django.db.models.deletion

from django.db import connection
from datetime import date, timedelta

from . import models as myModels

from django.db import transaction

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

@transaction.atomic
def fill_version_data():
    myModels.Version.objects.all().delete()
    query = '''
        SELECT fingerprint as build_fingerprint,
        ( select count(id) from crashreports_crashreport where boot_reason in ("RTC alarm")  and crashreports_crashreport.build_fingerprint = fingerprint) as SMPL,
        ( select count(id) from crashreports_crashreport where boot_reason in ("UNKNOWN", "keyboard power on")  and crashreports_crashreport.build_fingerprint = fingerprint) as prob_crashes,
        ( select count(id) from crashreports_crashreport where boot_reason not in ("RTC alarm", "UNKNOWN", "keyboard power on")  and crashreports_crashreport.build_fingerprint = fingerprint) as other,
        ( select count(id) from crashreports_heartbeat where  crashreports_heartbeat.build_fingerprint = fingerprint) as heartbeats,
        ( select min(crashreports_heartbeat.created_at) from crashreports_heartbeat where  crashreports_heartbeat.build_fingerprint = fingerprint) as first_seen
        from  (select distinct(build_fingerprint) as fingerprint
        from crashreports_heartbeat) group by fingerprint order by heartbeats;'''
    cursor = connection.cursor()
    cursor.execute(query,[])
    desc = cursor.description
    for row in cursor.fetchall():
        i = dict(zip([col[0] for col in desc], row))
        version = myModels.Version(
            build_fingerprint = i['build_fingerprint'],
            first_seen_on = i['first_seen'].split()[0],
            released_on = i['first_seen'].split()[0],
            heartbeats= i['heartbeats'],
            prob_crashes = i['prob_crashes'],
            smpl = i['SMPL'],
            other = i['other']
        )
        version.save()

@transaction.atomic
def fill_version_daily_data():
    myModels.VersionDaily.objects.all().delete()
    query = '''
        SELECT build_fingerprint, count(id) as heartbeats,
        strftime("%%Y-%%m-%%d",crashreports_heartbeat.date) as date,
        ( select count(id) from crashreports_crashreport where boot_reason in ("RTC alarm")  and crashreports_crashreport.build_fingerprint = crashreports_heartbeat.build_fingerprint and  crashreports_crashreport.date >= %s and  crashreports_crashreport.date < %s) as SMPL,
        ( select count(id) from crashreports_crashreport where boot_reason in ("UNKNOWN", "keyboard power on")  and crashreports_crashreport.build_fingerprint =  crashreports_heartbeat.build_fingerprint and crashreports_crashreport.date >= %s and  crashreports_crashreport.date < %s) as prob_crashes,
        ( select count(id) from crashreports_crashreport where boot_reason not in ("RTC alarm", "UNKNOWN", "keyboard power on")  and crashreports_crashreport.build_fingerprint =  crashreports_heartbeat.build_fingerprint and crashreports_crashreport.date >= %s and  crashreports_crashreport.date < %s) as other
         from crashreports_heartbeat where  crashreports_heartbeat.date >= %s and  crashreports_heartbeat.date < %s
         group by build_fingerprint'''
    start = date(2016, 8, 1)
    end   = date.today() + timedelta(days=5)
    delta = end - start
    for d in range(delta.days + 1):
        day = start + timedelta(days=d)
        print("Getting Stats for " + str(day))
        cursor = connection.cursor()
        cursor.execute(query,[str(day), str(day+timedelta(days=1))]*4)
        desc = cursor.description
        for row in cursor.fetchall():
            i = dict(zip([col[0] for col in desc], row))
            try:
                version_daily = myModels.VersionDaily(
                    version = myModels.Version.objects.get(build_fingerprint=i['build_fingerprint']),
                    heartbeats= i['heartbeats'],
                    date=day,
                    prob_crashes = i['prob_crashes'],
                    smpl = i['SMPL'],
                    other = i['other']
                )
            except:
                print("Skipping entry for {} {}".format(i['build_fingerprint'],day))
            version_daily.save()
