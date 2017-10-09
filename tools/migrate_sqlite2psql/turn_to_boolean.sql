ALTER TABLE auth_user ALTER COLUMN is_superuser DROP DEFAULT;
ALTER TABLE auth_user ALTER is_superuser TYPE bool USING CASE WHEN is_superuser=0 THEN FALSE ELSE TRUE END;
ALTER TABLE auth_user ALTER COLUMN is_superuser SET DEFAULT FALSE;

ALTER TABLE auth_user ALTER COLUMN is_active DROP DEFAULT;
ALTER TABLE auth_user ALTER is_active TYPE bool USING CASE WHEN is_active=0 THEN FALSE ELSE TRUE END;
ALTER TABLE auth_user ALTER COLUMN is_active SET DEFAULT FALSE;

ALTER TABLE auth_user ALTER COLUMN is_staff DROP DEFAULT;
ALTER TABLE auth_user ALTER is_staff TYPE bool USING CASE WHEN is_staff=0 THEN FALSE ELSE TRUE END;
ALTER TABLE auth_user ALTER COLUMN is_staff SET DEFAULT FALSE;

ALTER TABLE account_emailaddress ALTER COLUMN "primary" DROP DEFAULT;
ALTER TABLE account_emailaddress ALTER "primary" TYPE bool USING CASE WHEN "primary"=0 THEN FALSE ELSE TRUE END;
ALTER TABLE account_emailaddress ALTER COLUMN "primary" SET DEFAULT FALSE;

ALTER TABLE account_emailaddress ALTER COLUMN verified DROP DEFAULT;
ALTER TABLE account_emailaddress ALTER verified TYPE bool USING CASE WHEN verified=0 THEN FALSE ELSE TRUE END;
ALTER TABLE account_emailaddress ALTER COLUMN verified SET DEFAULT FALSE;

ALTER TABLE crashreports_crashreport ALTER COLUMN is_fake_report DROP DEFAULT;
ALTER TABLE crashreports_crashreport ALTER is_fake_report TYPE bool USING CASE WHEN is_fake_report=0 THEN FALSE ELSE TRUE END;
ALTER TABLE crashreports_crashreport ALTER COLUMN is_fake_report SET DEFAULT FALSE;

ALTER TABLE crashreport_stats_version ALTER COLUMN is_official_release DROP DEFAULT;
ALTER TABLE crashreport_stats_version ALTER is_official_release TYPE bool USING CASE WHEN is_official_release=0 THEN FALSE ELSE TRUE END;
ALTER TABLE crashreport_stats_version ALTER COLUMN is_official_release SET DEFAULT FALSE;

ALTER TABLE crashreport_stats_version ALTER COLUMN is_beta_release DROP DEFAULT;
ALTER TABLE crashreport_stats_version ALTER is_beta_release TYPE bool USING CASE WHEN is_beta_release=0 THEN FALSE ELSE TRUE END;
ALTER TABLE crashreport_stats_version ALTER COLUMN is_beta_release SET DEFAULT FALSE;
