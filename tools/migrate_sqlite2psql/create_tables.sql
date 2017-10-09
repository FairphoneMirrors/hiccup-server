--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.4
-- Dumped by pg_dump version 9.6.4

DROP TABLE IF EXISTS account_emailaddress           CASCADE;
DROP TABLE IF EXISTS account_emailconfirmation      CASCADE;
DROP TABLE IF EXISTS auth_group                     CASCADE;
DROP TABLE IF EXISTS auth_group_permissions         CASCADE;
DROP TABLE IF EXISTS auth_permission                CASCADE;
DROP TABLE IF EXISTS auth_user                      CASCADE;
DROP TABLE IF EXISTS auth_user_groups               CASCADE;
DROP TABLE IF EXISTS auth_user_user_permissions     CASCADE;
DROP TABLE IF EXISTS authtoken_token                CASCADE;
DROP TABLE IF EXISTS crashreport_stats_version      CASCADE;
DROP TABLE IF EXISTS crashreport_stats_versiondaily CASCADE;
DROP TABLE IF EXISTS crashreports_crashreport       CASCADE;
DROP TABLE IF EXISTS crashreports_device            CASCADE;
DROP TABLE IF EXISTS crashreports_heartbeat         CASCADE;
DROP TABLE IF EXISTS crashreports_logfile           CASCADE;
DROP TABLE IF EXISTS django_admin_log               CASCADE;
DROP TABLE IF EXISTS django_content_type            CASCADE;
DROP TABLE IF EXISTS django_migrations              CASCADE;
DROP TABLE IF EXISTS django_session                 CASCADE;
DROP TABLE IF EXISTS django_site                    CASCADE;
DROP TABLE IF EXISTS socialaccount_socialaccount    CASCADE;
DROP TABLE IF EXISTS socialaccount_socialapp        CASCADE;
DROP TABLE IF EXISTS socialaccount_socialapp_sites  CASCADE;
DROP TABLE IF EXISTS socialaccount_socialtoken      CASCADE;
DROP TABLE IF EXISTS taggit_tag                     CASCADE;
DROP TABLE IF EXISTS taggit_taggeditem              CASCADE;

--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.4
-- Dumped by pg_dump version 9.6.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: account_emailaddress; Type: TABLE; Schema: public; Owner: hiccupuser
--

CREATE TABLE account_emailaddress (
    id integer NOT NULL,
    verified integer NOT NULL,
    "primary" integer NOT NULL,
    user_id integer NOT NULL,
    email character varying(254) NOT NULL
);


ALTER TABLE account_emailaddress OWNER TO hiccupuser;

--
-- Name: account_emailaddress_id_seq; Type: SEQUENCE; Schema: public; Owner: hiccupuser
--

CREATE SEQUENCE account_emailaddress_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE account_emailaddress_id_seq OWNER TO hiccupuser;

--
-- Name: account_emailaddress_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hiccupuser
--

ALTER SEQUENCE account_emailaddress_id_seq OWNED BY account_emailaddress.id;


--
-- Name: account_emailconfirmation; Type: TABLE; Schema: public; Owner: hiccupuser
--

CREATE TABLE account_emailconfirmation (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    sent timestamp with time zone,
    key character varying(64) NOT NULL,
    email_address_id integer NOT NULL
);


ALTER TABLE account_emailconfirmation OWNER TO hiccupuser;

--
-- Name: account_emailconfirmation_id_seq; Type: SEQUENCE; Schema: public; Owner: hiccupuser
--

CREATE SEQUENCE account_emailconfirmation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE account_emailconfirmation_id_seq OWNER TO hiccupuser;

--
-- Name: account_emailconfirmation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hiccupuser
--

ALTER SEQUENCE account_emailconfirmation_id_seq OWNED BY account_emailconfirmation.id;


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: hiccupuser
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE auth_group OWNER TO hiccupuser;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: hiccupuser
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_group_id_seq OWNER TO hiccupuser;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hiccupuser
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: hiccupuser
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE auth_group_permissions OWNER TO hiccupuser;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: hiccupuser
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_group_permissions_id_seq OWNER TO hiccupuser;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hiccupuser
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: hiccupuser
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE auth_permission OWNER TO hiccupuser;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: hiccupuser
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_permission_id_seq OWNER TO hiccupuser;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hiccupuser
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: hiccupuser
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser integer NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff integer NOT NULL,
    is_active integer NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    username character varying(150) NOT NULL
);


ALTER TABLE auth_user OWNER TO hiccupuser;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: hiccupuser
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE auth_user_groups OWNER TO hiccupuser;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: hiccupuser
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_groups_id_seq OWNER TO hiccupuser;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hiccupuser
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: hiccupuser
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_id_seq OWNER TO hiccupuser;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hiccupuser
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: hiccupuser
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE auth_user_user_permissions OWNER TO hiccupuser;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: hiccupuser
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_user_permissions_id_seq OWNER TO hiccupuser;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hiccupuser
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- Name: authtoken_token; Type: TABLE; Schema: public; Owner: hiccupuser
--

CREATE TABLE authtoken_token (
    key character varying(40) NOT NULL,
    created timestamp with time zone NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE authtoken_token OWNER TO hiccupuser;

--
-- Name: crashreport_stats_version; Type: TABLE; Schema: public; Owner: hiccupuser
--

CREATE TABLE crashreport_stats_version (
    id integer NOT NULL,
    build_fingerprint character varying(200) NOT NULL,
    is_official_release integer NOT NULL,
    is_beta_release integer NOT NULL,
    first_seen_on date NOT NULL,
    released_on date NOT NULL,
    heartbeats integer NOT NULL,
    prob_crashes integer NOT NULL,
    smpl integer NOT NULL,
    other integer NOT NULL
);


ALTER TABLE crashreport_stats_version OWNER TO hiccupuser;

--
-- Name: crashreport_stats_version_id_seq; Type: SEQUENCE; Schema: public; Owner: hiccupuser
--

CREATE SEQUENCE crashreport_stats_version_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE crashreport_stats_version_id_seq OWNER TO hiccupuser;

--
-- Name: crashreport_stats_version_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hiccupuser
--

ALTER SEQUENCE crashreport_stats_version_id_seq OWNED BY crashreport_stats_version.id;


--
-- Name: crashreport_stats_versiondaily; Type: TABLE; Schema: public; Owner: hiccupuser
--

CREATE TABLE crashreport_stats_versiondaily (
    id integer NOT NULL,
    date date NOT NULL,
    heartbeats integer NOT NULL,
    prob_crashes integer NOT NULL,
    smpl integer NOT NULL,
    other integer NOT NULL,
    version_id integer NOT NULL
);


ALTER TABLE crashreport_stats_versiondaily OWNER TO hiccupuser;

--
-- Name: crashreport_stats_versiondaily_id_seq; Type: SEQUENCE; Schema: public; Owner: hiccupuser
--

CREATE SEQUENCE crashreport_stats_versiondaily_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE crashreport_stats_versiondaily_id_seq OWNER TO hiccupuser;

--
-- Name: crashreport_stats_versiondaily_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hiccupuser
--

ALTER SEQUENCE crashreport_stats_versiondaily_id_seq OWNED BY crashreport_stats_versiondaily.id;


--
-- Name: crashreports_crashreport; Type: TABLE; Schema: public; Owner: hiccupuser
--

CREATE TABLE crashreports_crashreport (
    id integer NOT NULL,
    is_fake_report integer NOT NULL,
    app_version integer NOT NULL,
    uptime character varying(200) NOT NULL,
    build_fingerprint character varying(200) NOT NULL,
    boot_reason character varying(200) NOT NULL,
    power_off_reason character varying(200) NOT NULL,
    date timestamp with time zone NOT NULL,
    device_local_id integer NOT NULL,
    next_logfile_key integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    device_id integer NOT NULL,
    power_on_reason character varying(200) NOT NULL,
    CONSTRAINT crashreports_crashreport_device_local_id_check CHECK ((device_local_id >= 0)),
    CONSTRAINT crashreports_crashreport_next_logfile_key_check CHECK ((next_logfile_key >= 0))
);


ALTER TABLE crashreports_crashreport OWNER TO hiccupuser;

--
-- Name: crashreports_crashreport_id_seq; Type: SEQUENCE; Schema: public; Owner: hiccupuser
--

CREATE SEQUENCE crashreports_crashreport_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE crashreports_crashreport_id_seq OWNER TO hiccupuser;

--
-- Name: crashreports_crashreport_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hiccupuser
--

ALTER SEQUENCE crashreports_crashreport_id_seq OWNED BY crashreports_crashreport.id;


--
-- Name: crashreports_device; Type: TABLE; Schema: public; Owner: hiccupuser
--

CREATE TABLE crashreports_device (
    id integer NOT NULL,
    imei character varying(32),
    board_date timestamp with time zone,
    chipset character varying(200),
    last_heartbeat timestamp with time zone,
    token character varying(200),
    next_per_crashreport_key integer NOT NULL,
    next_per_heartbeat_key integer NOT NULL,
    user_id integer NOT NULL,
    uuid character varying(64) NOT NULL,
    CONSTRAINT crashreports_device_next_per_crashreport_key_check CHECK ((next_per_crashreport_key >= 0)),
    CONSTRAINT crashreports_device_next_per_heartbeat_key_check CHECK ((next_per_heartbeat_key >= 0))
);


ALTER TABLE crashreports_device OWNER TO hiccupuser;

--
-- Name: crashreports_device_id_seq; Type: SEQUENCE; Schema: public; Owner: hiccupuser
--

CREATE SEQUENCE crashreports_device_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE crashreports_device_id_seq OWNER TO hiccupuser;

--
-- Name: crashreports_device_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hiccupuser
--

ALTER SEQUENCE crashreports_device_id_seq OWNED BY crashreports_device.id;


--
-- Name: crashreports_heartbeat; Type: TABLE; Schema: public; Owner: hiccupuser
--

CREATE TABLE crashreports_heartbeat (
    id integer NOT NULL,
    app_version integer NOT NULL,
    uptime character varying(200) NOT NULL,
    build_fingerprint character varying(200) NOT NULL,
    device_local_id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    device_id integer NOT NULL,
    date timestamp with time zone NOT NULL,
    CONSTRAINT crashreports_heartbeat_device_local_id_check CHECK ((device_local_id >= 0))
);


ALTER TABLE crashreports_heartbeat OWNER TO hiccupuser;

--
-- Name: crashreports_heartbeat_id_seq; Type: SEQUENCE; Schema: public; Owner: hiccupuser
--

CREATE SEQUENCE crashreports_heartbeat_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE crashreports_heartbeat_id_seq OWNER TO hiccupuser;

--
-- Name: crashreports_heartbeat_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hiccupuser
--

ALTER SEQUENCE crashreports_heartbeat_id_seq OWNED BY crashreports_heartbeat.id;


--
-- Name: crashreports_logfile; Type: TABLE; Schema: public; Owner: hiccupuser
--

CREATE TABLE crashreports_logfile (
    id integer NOT NULL,
    logfile_type text NOT NULL,
    logfile character varying(500) NOT NULL,
    crashreport_local_id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    crashreport_id integer NOT NULL,
    CONSTRAINT crashreports_logfile_crashreport_local_id_check CHECK ((crashreport_local_id >= 0))
);


ALTER TABLE crashreports_logfile OWNER TO hiccupuser;

--
-- Name: crashreports_logfile_id_seq; Type: SEQUENCE; Schema: public; Owner: hiccupuser
--

CREATE SEQUENCE crashreports_logfile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE crashreports_logfile_id_seq OWNER TO hiccupuser;

--
-- Name: crashreports_logfile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hiccupuser
--

ALTER SEQUENCE crashreports_logfile_id_seq OWNED BY crashreports_logfile.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: hiccupuser
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE django_admin_log OWNER TO hiccupuser;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: hiccupuser
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_admin_log_id_seq OWNER TO hiccupuser;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hiccupuser
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: hiccupuser
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE django_content_type OWNER TO hiccupuser;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: hiccupuser
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_content_type_id_seq OWNER TO hiccupuser;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hiccupuser
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: hiccupuser
--

CREATE TABLE django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE django_migrations OWNER TO hiccupuser;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: hiccupuser
--

CREATE SEQUENCE django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_migrations_id_seq OWNER TO hiccupuser;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hiccupuser
--

ALTER SEQUENCE django_migrations_id_seq OWNED BY django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: hiccupuser
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE django_session OWNER TO hiccupuser;

--
-- Name: django_site; Type: TABLE; Schema: public; Owner: hiccupuser
--

CREATE TABLE django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE django_site OWNER TO hiccupuser;

--
-- Name: django_site_id_seq; Type: SEQUENCE; Schema: public; Owner: hiccupuser
--

CREATE SEQUENCE django_site_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_site_id_seq OWNER TO hiccupuser;

--
-- Name: django_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hiccupuser
--

ALTER SEQUENCE django_site_id_seq OWNED BY django_site.id;


--
-- Name: socialaccount_socialaccount; Type: TABLE; Schema: public; Owner: hiccupuser
--

CREATE TABLE socialaccount_socialaccount (
    id integer NOT NULL,
    provider character varying(30) NOT NULL,
    uid character varying(191) NOT NULL,
    last_login timestamp with time zone NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    user_id integer NOT NULL,
    extra_data text NOT NULL
);


ALTER TABLE socialaccount_socialaccount OWNER TO hiccupuser;

--
-- Name: socialaccount_socialaccount_id_seq; Type: SEQUENCE; Schema: public; Owner: hiccupuser
--

CREATE SEQUENCE socialaccount_socialaccount_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE socialaccount_socialaccount_id_seq OWNER TO hiccupuser;

--
-- Name: socialaccount_socialaccount_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hiccupuser
--

ALTER SEQUENCE socialaccount_socialaccount_id_seq OWNED BY socialaccount_socialaccount.id;


--
-- Name: socialaccount_socialapp; Type: TABLE; Schema: public; Owner: hiccupuser
--

CREATE TABLE socialaccount_socialapp (
    id integer NOT NULL,
    provider character varying(30) NOT NULL,
    name character varying(40) NOT NULL,
    client_id character varying(191) NOT NULL,
    key character varying(191) NOT NULL,
    secret character varying(191) NOT NULL
);


ALTER TABLE socialaccount_socialapp OWNER TO hiccupuser;

--
-- Name: socialaccount_socialapp_id_seq; Type: SEQUENCE; Schema: public; Owner: hiccupuser
--

CREATE SEQUENCE socialaccount_socialapp_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE socialaccount_socialapp_id_seq OWNER TO hiccupuser;

--
-- Name: socialaccount_socialapp_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hiccupuser
--

ALTER SEQUENCE socialaccount_socialapp_id_seq OWNED BY socialaccount_socialapp.id;


--
-- Name: socialaccount_socialapp_sites; Type: TABLE; Schema: public; Owner: hiccupuser
--

CREATE TABLE socialaccount_socialapp_sites (
    id integer NOT NULL,
    socialapp_id integer NOT NULL,
    site_id integer NOT NULL
);


ALTER TABLE socialaccount_socialapp_sites OWNER TO hiccupuser;

--
-- Name: socialaccount_socialapp_sites_id_seq; Type: SEQUENCE; Schema: public; Owner: hiccupuser
--

CREATE SEQUENCE socialaccount_socialapp_sites_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE socialaccount_socialapp_sites_id_seq OWNER TO hiccupuser;

--
-- Name: socialaccount_socialapp_sites_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hiccupuser
--

ALTER SEQUENCE socialaccount_socialapp_sites_id_seq OWNED BY socialaccount_socialapp_sites.id;


--
-- Name: socialaccount_socialtoken; Type: TABLE; Schema: public; Owner: hiccupuser
--

CREATE TABLE socialaccount_socialtoken (
    id integer NOT NULL,
    token text NOT NULL,
    token_secret text NOT NULL,
    expires_at timestamp with time zone,
    account_id integer NOT NULL,
    app_id integer NOT NULL
);


ALTER TABLE socialaccount_socialtoken OWNER TO hiccupuser;

--
-- Name: socialaccount_socialtoken_id_seq; Type: SEQUENCE; Schema: public; Owner: hiccupuser
--

CREATE SEQUENCE socialaccount_socialtoken_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE socialaccount_socialtoken_id_seq OWNER TO hiccupuser;

--
-- Name: socialaccount_socialtoken_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hiccupuser
--

ALTER SEQUENCE socialaccount_socialtoken_id_seq OWNED BY socialaccount_socialtoken.id;


--
-- Name: taggit_tag; Type: TABLE; Schema: public; Owner: hiccupuser
--

CREATE TABLE taggit_tag (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    slug character varying(100) NOT NULL
);


ALTER TABLE taggit_tag OWNER TO hiccupuser;

--
-- Name: taggit_tag_id_seq; Type: SEQUENCE; Schema: public; Owner: hiccupuser
--

CREATE SEQUENCE taggit_tag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE taggit_tag_id_seq OWNER TO hiccupuser;

--
-- Name: taggit_tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hiccupuser
--

ALTER SEQUENCE taggit_tag_id_seq OWNED BY taggit_tag.id;


--
-- Name: taggit_taggeditem; Type: TABLE; Schema: public; Owner: hiccupuser
--

CREATE TABLE taggit_taggeditem (
    id integer NOT NULL,
    object_id integer NOT NULL,
    content_type_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE taggit_taggeditem OWNER TO hiccupuser;

--
-- Name: taggit_taggeditem_id_seq; Type: SEQUENCE; Schema: public; Owner: hiccupuser
--

CREATE SEQUENCE taggit_taggeditem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE taggit_taggeditem_id_seq OWNER TO hiccupuser;

--
-- Name: taggit_taggeditem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hiccupuser
--

ALTER SEQUENCE taggit_taggeditem_id_seq OWNED BY taggit_taggeditem.id;


--
-- Name: account_emailaddress id; Type: DEFAULT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY account_emailaddress ALTER COLUMN id SET DEFAULT nextval('account_emailaddress_id_seq'::regclass);


--
-- Name: account_emailconfirmation id; Type: DEFAULT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY account_emailconfirmation ALTER COLUMN id SET DEFAULT nextval('account_emailconfirmation_id_seq'::regclass);


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- Name: crashreport_stats_version id; Type: DEFAULT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY crashreport_stats_version ALTER COLUMN id SET DEFAULT nextval('crashreport_stats_version_id_seq'::regclass);


--
-- Name: crashreport_stats_versiondaily id; Type: DEFAULT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY crashreport_stats_versiondaily ALTER COLUMN id SET DEFAULT nextval('crashreport_stats_versiondaily_id_seq'::regclass);


--
-- Name: crashreports_crashreport id; Type: DEFAULT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY crashreports_crashreport ALTER COLUMN id SET DEFAULT nextval('crashreports_crashreport_id_seq'::regclass);


--
-- Name: crashreports_device id; Type: DEFAULT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY crashreports_device ALTER COLUMN id SET DEFAULT nextval('crashreports_device_id_seq'::regclass);


--
-- Name: crashreports_heartbeat id; Type: DEFAULT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY crashreports_heartbeat ALTER COLUMN id SET DEFAULT nextval('crashreports_heartbeat_id_seq'::regclass);


--
-- Name: crashreports_logfile id; Type: DEFAULT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY crashreports_logfile ALTER COLUMN id SET DEFAULT nextval('crashreports_logfile_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- Name: django_site id; Type: DEFAULT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY django_site ALTER COLUMN id SET DEFAULT nextval('django_site_id_seq'::regclass);


--
-- Name: socialaccount_socialaccount id; Type: DEFAULT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY socialaccount_socialaccount ALTER COLUMN id SET DEFAULT nextval('socialaccount_socialaccount_id_seq'::regclass);


--
-- Name: socialaccount_socialapp id; Type: DEFAULT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY socialaccount_socialapp ALTER COLUMN id SET DEFAULT nextval('socialaccount_socialapp_id_seq'::regclass);


--
-- Name: socialaccount_socialapp_sites id; Type: DEFAULT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY socialaccount_socialapp_sites ALTER COLUMN id SET DEFAULT nextval('socialaccount_socialapp_sites_id_seq'::regclass);


--
-- Name: socialaccount_socialtoken id; Type: DEFAULT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY socialaccount_socialtoken ALTER COLUMN id SET DEFAULT nextval('socialaccount_socialtoken_id_seq'::regclass);


--
-- Name: taggit_tag id; Type: DEFAULT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY taggit_tag ALTER COLUMN id SET DEFAULT nextval('taggit_tag_id_seq'::regclass);


--
-- Name: taggit_taggeditem id; Type: DEFAULT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY taggit_taggeditem ALTER COLUMN id SET DEFAULT nextval('taggit_taggeditem_id_seq'::regclass);


--
-- Name: account_emailaddress account_emailaddress_email_key; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY account_emailaddress
    ADD CONSTRAINT account_emailaddress_email_key UNIQUE (email);


--
-- Name: account_emailaddress account_emailaddress_pkey; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY account_emailaddress
    ADD CONSTRAINT account_emailaddress_pkey PRIMARY KEY (id);


--
-- Name: account_emailconfirmation account_emailconfirmation_key_key; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY account_emailconfirmation
    ADD CONSTRAINT account_emailconfirmation_key_key UNIQUE (key);


--
-- Name: account_emailconfirmation account_emailconfirmation_pkey; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY account_emailconfirmation
    ADD CONSTRAINT account_emailconfirmation_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: authtoken_token authtoken_token_pkey; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY authtoken_token
    ADD CONSTRAINT authtoken_token_pkey PRIMARY KEY (key);


--
-- Name: authtoken_token authtoken_token_user_id_key; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_key UNIQUE (user_id);


--
-- Name: crashreport_stats_version crashreport_stats_version_build_fingerprint_key; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY crashreport_stats_version
    ADD CONSTRAINT crashreport_stats_version_build_fingerprint_key UNIQUE (build_fingerprint);


--
-- Name: crashreport_stats_version crashreport_stats_version_pkey; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY crashreport_stats_version
    ADD CONSTRAINT crashreport_stats_version_pkey PRIMARY KEY (id);


--
-- Name: crashreport_stats_versiondaily crashreport_stats_versiondaily_pkey; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY crashreport_stats_versiondaily
    ADD CONSTRAINT crashreport_stats_versiondaily_pkey PRIMARY KEY (id);


--
-- Name: crashreports_crashreport crashreports_crashreport_pkey; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY crashreports_crashreport
    ADD CONSTRAINT crashreports_crashreport_pkey PRIMARY KEY (id);


--
-- Name: crashreports_device crashreports_device_pkey; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY crashreports_device
    ADD CONSTRAINT crashreports_device_pkey PRIMARY KEY (id);


--
-- Name: crashreports_device crashreports_device_user_id_key; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY crashreports_device
    ADD CONSTRAINT crashreports_device_user_id_key UNIQUE (user_id);


--
-- Name: crashreports_device crashreports_device_uuid_key; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY crashreports_device
    ADD CONSTRAINT crashreports_device_uuid_key UNIQUE (uuid);


--
-- Name: crashreports_heartbeat crashreports_heartbeat_pkey; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY crashreports_heartbeat
    ADD CONSTRAINT crashreports_heartbeat_pkey PRIMARY KEY (id);


--
-- Name: crashreports_logfile crashreports_logfile_pkey; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY crashreports_logfile
    ADD CONSTRAINT crashreports_logfile_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: django_site django_site_domain_a2e37b91_uniq; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_domain_a2e37b91_uniq UNIQUE (domain);


--
-- Name: django_site django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- Name: socialaccount_socialaccount socialaccount_socialaccount_pkey; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY socialaccount_socialaccount
    ADD CONSTRAINT socialaccount_socialaccount_pkey PRIMARY KEY (id);


--
-- Name: socialaccount_socialaccount socialaccount_socialaccount_provider_fc810c6e_uniq; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY socialaccount_socialaccount
    ADD CONSTRAINT socialaccount_socialaccount_provider_fc810c6e_uniq UNIQUE (provider, uid);


--
-- Name: socialaccount_socialapp socialaccount_socialapp_pkey; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY socialaccount_socialapp
    ADD CONSTRAINT socialaccount_socialapp_pkey PRIMARY KEY (id);


--
-- Name: socialaccount_socialapp_sites socialaccount_socialapp_sites_pkey; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY socialaccount_socialapp_sites
    ADD CONSTRAINT socialaccount_socialapp_sites_pkey PRIMARY KEY (id);


--
-- Name: socialaccount_socialapp_sites socialaccount_socialapp_sites_socialapp_id_71a9a768_uniq; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY socialaccount_socialapp_sites
    ADD CONSTRAINT socialaccount_socialapp_sites_socialapp_id_71a9a768_uniq UNIQUE (socialapp_id, site_id);


--
-- Name: socialaccount_socialtoken socialaccount_socialtoken_app_id_fca4e0ac_uniq; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_socialtoken_app_id_fca4e0ac_uniq UNIQUE (app_id, account_id);


--
-- Name: socialaccount_socialtoken socialaccount_socialtoken_pkey; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_socialtoken_pkey PRIMARY KEY (id);


--
-- Name: taggit_tag taggit_tag_name_key; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY taggit_tag
    ADD CONSTRAINT taggit_tag_name_key UNIQUE (name);


--
-- Name: taggit_tag taggit_tag_pkey; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY taggit_tag
    ADD CONSTRAINT taggit_tag_pkey PRIMARY KEY (id);


--
-- Name: taggit_tag taggit_tag_slug_key; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY taggit_tag
    ADD CONSTRAINT taggit_tag_slug_key UNIQUE (slug);


--
-- Name: taggit_taggeditem taggit_taggeditem_pkey; Type: CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY taggit_taggeditem
    ADD CONSTRAINT taggit_taggeditem_pkey PRIMARY KEY (id);


--
-- Name: account_emailaddress_e8701ad4; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX account_emailaddress_e8701ad4 ON account_emailaddress USING btree (user_id);


--
-- Name: account_emailaddress_email_03be32b2_like; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX account_emailaddress_email_03be32b2_like ON account_emailaddress USING btree (email varchar_pattern_ops);


--
-- Name: account_emailconfirmation_6f1edeac; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX account_emailconfirmation_6f1edeac ON account_emailconfirmation USING btree (email_address_id);


--
-- Name: account_emailconfirmation_key_f43612bd_like; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX account_emailconfirmation_key_f43612bd_like ON account_emailconfirmation USING btree (key varchar_pattern_ops);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX auth_group_name_a6ea08ec_like ON auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_0e939a4f; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX auth_group_permissions_0e939a4f ON auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_8373b171; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX auth_group_permissions_8373b171 ON auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_417f1b1c; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX auth_permission_417f1b1c ON auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_0e939a4f; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX auth_user_groups_0e939a4f ON auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_e8701ad4; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX auth_user_groups_e8701ad4 ON auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_8373b171; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX auth_user_user_permissions_8373b171 ON auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_e8701ad4; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX auth_user_user_permissions_e8701ad4 ON auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX auth_user_username_6821ab7c_like ON auth_user USING btree (username varchar_pattern_ops);


--
-- Name: authtoken_token_key_10f0b77e_like; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX authtoken_token_key_10f0b77e_like ON authtoken_token USING btree (key varchar_pattern_ops);


--
-- Name: crashreport_stats_version_build_fingerprint_dcd2fcdf_like; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX crashreport_stats_version_build_fingerprint_dcd2fcdf_like ON crashreport_stats_version USING btree (build_fingerprint varchar_pattern_ops);


--
-- Name: crashreport_stats_versiondaily_316e8552; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX crashreport_stats_versiondaily_316e8552 ON crashreport_stats_versiondaily USING btree (version_id);


--
-- Name: crashreports_crashreport_9379346c; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX crashreports_crashreport_9379346c ON crashreports_crashreport USING btree (device_id);


--
-- Name: crashreports_crashreport_boot_reason_54c0d5ec_like; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX crashreports_crashreport_boot_reason_54c0d5ec_like ON crashreports_crashreport USING btree (boot_reason varchar_pattern_ops);


--
-- Name: crashreports_crashreport_boot_reason_54c0d5ec_uniq; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX crashreports_crashreport_boot_reason_54c0d5ec_uniq ON crashreports_crashreport USING btree (boot_reason);


--
-- Name: crashreports_crashreport_build_fingerprint_f5dc21a3_like; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX crashreports_crashreport_build_fingerprint_f5dc21a3_like ON crashreports_crashreport USING btree (build_fingerprint varchar_pattern_ops);


--
-- Name: crashreports_crashreport_build_fingerprint_f5dc21a3_uniq; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX crashreports_crashreport_build_fingerprint_f5dc21a3_uniq ON crashreports_crashreport USING btree (build_fingerprint);


--
-- Name: crashreports_crashreport_date_e191f150_uniq; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX crashreports_crashreport_date_e191f150_uniq ON crashreports_crashreport USING btree (date);


--
-- Name: crashreports_crashreport_power_off_reason_22d2d6d6_like; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX crashreports_crashreport_power_off_reason_22d2d6d6_like ON crashreports_crashreport USING btree (power_off_reason varchar_pattern_ops);


--
-- Name: crashreports_crashreport_power_off_reason_22d2d6d6_uniq; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX crashreports_crashreport_power_off_reason_22d2d6d6_uniq ON crashreports_crashreport USING btree (power_off_reason);


--
-- Name: crashreports_crashreport_power_on_reason_0c0eafbb_like; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX crashreports_crashreport_power_on_reason_0c0eafbb_like ON crashreports_crashreport USING btree (power_on_reason varchar_pattern_ops);


--
-- Name: crashreports_crashreport_power_on_reason_0c0eafbb_uniq; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX crashreports_crashreport_power_on_reason_0c0eafbb_uniq ON crashreports_crashreport USING btree (power_on_reason);


--
-- Name: crashreports_device_uuid_9d635eb7_like; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX crashreports_device_uuid_9d635eb7_like ON crashreports_device USING btree (uuid varchar_pattern_ops);


--
-- Name: crashreports_heartbeat_9379346c; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX crashreports_heartbeat_9379346c ON crashreports_heartbeat USING btree (device_id);


--
-- Name: crashreports_logfile_b7d34b56; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX crashreports_logfile_b7d34b56 ON crashreports_logfile USING btree (crashreport_id);


--
-- Name: django_admin_log_417f1b1c; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX django_admin_log_417f1b1c ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_e8701ad4; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX django_admin_log_e8701ad4 ON django_admin_log USING btree (user_id);


--
-- Name: django_session_de54fa62; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX django_session_de54fa62 ON django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX django_session_session_key_c0390e0f_like ON django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: django_site_domain_a2e37b91_like; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX django_site_domain_a2e37b91_like ON django_site USING btree (domain varchar_pattern_ops);


--
-- Name: socialaccount_socialaccount_e8701ad4; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX socialaccount_socialaccount_e8701ad4 ON socialaccount_socialaccount USING btree (user_id);


--
-- Name: socialaccount_socialapp_sites_9365d6e7; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX socialaccount_socialapp_sites_9365d6e7 ON socialaccount_socialapp_sites USING btree (site_id);


--
-- Name: socialaccount_socialapp_sites_fe95b0a0; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX socialaccount_socialapp_sites_fe95b0a0 ON socialaccount_socialapp_sites USING btree (socialapp_id);


--
-- Name: socialaccount_socialtoken_8a089c2a; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX socialaccount_socialtoken_8a089c2a ON socialaccount_socialtoken USING btree (account_id);


--
-- Name: socialaccount_socialtoken_f382adfe; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX socialaccount_socialtoken_f382adfe ON socialaccount_socialtoken USING btree (app_id);


--
-- Name: taggit_tag_name_58eb2ed9_like; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX taggit_tag_name_58eb2ed9_like ON taggit_tag USING btree (name varchar_pattern_ops);


--
-- Name: taggit_tag_slug_6be58b2c_like; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX taggit_tag_slug_6be58b2c_like ON taggit_tag USING btree (slug varchar_pattern_ops);


--
-- Name: taggit_taggeditem_417f1b1c; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX taggit_taggeditem_417f1b1c ON taggit_taggeditem USING btree (content_type_id);


--
-- Name: taggit_taggeditem_76f094bc; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX taggit_taggeditem_76f094bc ON taggit_taggeditem USING btree (tag_id);


--
-- Name: taggit_taggeditem_af31437c; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX taggit_taggeditem_af31437c ON taggit_taggeditem USING btree (object_id);


--
-- Name: taggit_taggeditem_content_type_id_196cc965_idx; Type: INDEX; Schema: public; Owner: hiccupuser
--

CREATE INDEX taggit_taggeditem_content_type_id_196cc965_idx ON taggit_taggeditem USING btree (content_type_id, object_id);


--
-- Name: account_emailconfirmation account_em_email_address_id_5b7f8c58_fk_account_emailaddress_id; Type: FK CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY account_emailconfirmation
    ADD CONSTRAINT account_em_email_address_id_5b7f8c58_fk_account_emailaddress_id FOREIGN KEY (email_address_id) REFERENCES account_emailaddress(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: account_emailaddress account_emailaddress_user_id_2c513194_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY account_emailaddress
    ADD CONSTRAINT account_emailaddress_user_id_2c513194_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permiss_permission_id_84c5c92e_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permiss_permission_id_84c5c92e_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permiss_content_type_id_2f476e4b_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permiss_content_type_id_2f476e4b_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_per_permission_id_1fbb5f2c_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_per_permission_id_1fbb5f2c_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authtoken_token authtoken_token_user_id_35299eff_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_35299eff_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crashreports_logfile crashrep_crashreport_id_714d0a8d_fk_crashreports_crashreport_id; Type: FK CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY crashreports_logfile
    ADD CONSTRAINT crashrep_crashreport_id_714d0a8d_fk_crashreports_crashreport_id FOREIGN KEY (crashreport_id) REFERENCES crashreports_crashreport(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crashreport_stats_versiondaily crashreport_version_id_ddba23df_fk_crashreport_stats_version_id; Type: FK CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY crashreport_stats_versiondaily
    ADD CONSTRAINT crashreport_version_id_ddba23df_fk_crashreport_stats_version_id FOREIGN KEY (version_id) REFERENCES crashreport_stats_version(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crashreports_crashreport crashreports_crash_device_id_0c882278_fk_crashreports_device_id; Type: FK CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY crashreports_crashreport
    ADD CONSTRAINT crashreports_crash_device_id_0c882278_fk_crashreports_device_id FOREIGN KEY (device_id) REFERENCES crashreports_device(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crashreports_device crashreports_device_user_id_a9e0ce74_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY crashreports_device
    ADD CONSTRAINT crashreports_device_user_id_a9e0ce74_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: crashreports_heartbeat crashreports_heart_device_id_9cc9684c_fk_crashreports_device_id; Type: FK CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY crashreports_heartbeat
    ADD CONSTRAINT crashreports_heart_device_id_9cc9684c_fk_crashreports_device_id FOREIGN KEY (device_id) REFERENCES crashreports_device(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_content_type_id_c4bce8eb_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_content_type_id_c4bce8eb_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialtoken socialacc_account_id_951f210e_fk_socialaccount_socialaccount_id; Type: FK CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY socialaccount_socialtoken
    ADD CONSTRAINT socialacc_account_id_951f210e_fk_socialaccount_socialaccount_id FOREIGN KEY (account_id) REFERENCES socialaccount_socialaccount(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialapp_sites socialaccou_socialapp_id_97fb6e7d_fk_socialaccount_socialapp_id; Type: FK CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY socialaccount_socialapp_sites
    ADD CONSTRAINT socialaccou_socialapp_id_97fb6e7d_fk_socialaccount_socialapp_id FOREIGN KEY (socialapp_id) REFERENCES socialaccount_socialapp(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialtoken socialaccount_soc_app_id_636a42d7_fk_socialaccount_socialapp_id; Type: FK CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_soc_app_id_636a42d7_fk_socialaccount_socialapp_id FOREIGN KEY (app_id) REFERENCES socialaccount_socialapp(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialaccount socialaccount_socialaccount_user_id_8146e70c_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY socialaccount_socialaccount
    ADD CONSTRAINT socialaccount_socialaccount_user_id_8146e70c_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialapp_sites socialaccount_socialapp_site_site_id_2579dee5_fk_django_site_id; Type: FK CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY socialaccount_socialapp_sites
    ADD CONSTRAINT socialaccount_socialapp_site_site_id_2579dee5_fk_django_site_id FOREIGN KEY (site_id) REFERENCES django_site(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: taggit_taggeditem taggit_tagge_content_type_id_9957a03c_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY taggit_taggeditem
    ADD CONSTRAINT taggit_tagge_content_type_id_9957a03c_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: taggit_taggeditem taggit_taggeditem_tag_id_f4f5b767_fk_taggit_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: hiccupuser
--

ALTER TABLE ONLY taggit_taggeditem
    ADD CONSTRAINT taggit_taggeditem_tag_id_f4f5b767_fk_taggit_tag_id FOREIGN KEY (tag_id) REFERENCES taggit_tag(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--
