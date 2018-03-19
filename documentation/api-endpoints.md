# Hiccup API


<a name="overview"></a>
## Overview



<a name="paths"></a>
## Paths

<a name="devices_create"></a>
### POST /hiccup/api/v1/devices/

#### Body parameter
*Name* : data  
*Flags* : optional


|Name|Description|Schema|
|---|---|---|
|**board_date**  <br>*optional*|**Example** : `"string"`|string|
|**chipset**  <br>*optional*|**Example** : `"string"`|string|
|**imei**  <br>*optional*|**Example** : `"string"`|string|
|**last_heartbeat**  <br>*optional*|**Example** : `"string"`|string|
|**next_per_crashreport_key**  <br>*optional*|**Example** : `"string"`|string|
|**next_per_heartbeat_key**  <br>*optional*|**Example** : `"string"`|string|
|**token**  <br>*optional*|**Example** : `"string"`|string|
|**user**  <br>*required*|**Example** : `"string"`|string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**201**|No Content|


#### Consumes

* `application/json`


#### Tags

* devices


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/
```


##### Request body
```
json :
{
  "board_date" : "string",
  "next_per_heartbeat_key" : "string",
  "next_per_crashreport_key" : "string",
  "token" : "string",
  "user" : "string",
  "imei" : "string",
  "chipset" : "string",
  "last_heartbeat" : "string"
}
```


<a name="register_create"></a>
### POST /hiccup/api/v1/devices/register/

#### Responses

|HTTP Code|Schema|
|---|---|
|**201**|No Content|


#### Tags

* register


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/register/
```


<a name="crashreports_read"></a>
### GET /hiccup/api/v1/devices/{device__uuid}/crashreports/{device_local_id}/

#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**device__uuid**  <br>*required*|string|
|**Path**|**device_local_id**  <br>*required*|string|
|**Query**|**limit**  <br>*optional*|string|
|**Query**|**offset**  <br>*optional*|string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**200**|No Content|


#### Tags

* crashreports


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/crashreports/string/
```


##### Request query
```
json :
{
  "limit" : "string",
  "offset" : "string"
}
```


<a name="crashreports_update"></a>
### PUT /hiccup/api/v1/devices/{device__uuid}/crashreports/{device_local_id}/

#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**device__uuid**  <br>*required*|string|
|**Path**|**device_local_id**  <br>*required*|string|


#### Body parameter
*Name* : data  
*Flags* : optional


|Name|Description|Schema|
|---|---|---|
|**app_version**  <br>*required*|**Example** : `"string"`|string|
|**boot_reason**  <br>*required*|**Example** : `"string"`|string|
|**build_fingerprint**  <br>*required*|**Example** : `"string"`|string|
|**date**  <br>*required*|**Example** : `"string"`|string|
|**device_local_id**  <br>*optional*|**Example** : `"string"`|string|
|**is_fake_report**  <br>*optional*|**Example** : `"string"`|string|
|**next_logfile_key**  <br>*optional*|**Example** : `"string"`|string|
|**power_off_reason**  <br>*required*|**Example** : `"string"`|string|
|**power_on_reason**  <br>*required*|**Example** : `"string"`|string|
|**radio_version**  <br>*optional*|**Example** : `"string"`|string|
|**uptime**  <br>*required*|**Example** : `"string"`|string|
|**uuid**  <br>*required*|**Example** : `"string"`|string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**200**|No Content|


#### Consumes

* `application/json`


#### Tags

* crashreports


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/crashreports/string/
```


##### Request body
```
json :
{
  "uptime" : "string",
  "is_fake_report" : "string",
  "uuid" : "string",
  "boot_reason" : "string",
  "power_on_reason" : "string",
  "build_fingerprint" : "string",
  "power_off_reason" : "string",
  "radio_version" : "string",
  "next_logfile_key" : "string",
  "date" : "string",
  "app_version" : "string",
  "device_local_id" : "string"
}
```


<a name="crashreports_destroy"></a>
### DELETE /hiccup/api/v1/devices/{device__uuid}/crashreports/{device_local_id}/

#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**device__uuid**  <br>*required*|string|
|**Path**|**device_local_id**  <br>*required*|string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**204**|No Content|


#### Tags

* crashreports


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/crashreports/string/
```


<a name="crashreports_partial_update"></a>
### PATCH /hiccup/api/v1/devices/{device__uuid}/crashreports/{device_local_id}/

#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**device__uuid**  <br>*required*|string|
|**Path**|**device_local_id**  <br>*required*|string|


#### Body parameter
*Name* : data  
*Flags* : optional


|Name|Description|Schema|
|---|---|---|
|**app_version**  <br>*optional*|**Example** : `"string"`|string|
|**boot_reason**  <br>*optional*|**Example** : `"string"`|string|
|**build_fingerprint**  <br>*optional*|**Example** : `"string"`|string|
|**date**  <br>*optional*|**Example** : `"string"`|string|
|**device_local_id**  <br>*optional*|**Example** : `"string"`|string|
|**is_fake_report**  <br>*optional*|**Example** : `"string"`|string|
|**next_logfile_key**  <br>*optional*|**Example** : `"string"`|string|
|**power_off_reason**  <br>*optional*|**Example** : `"string"`|string|
|**power_on_reason**  <br>*optional*|**Example** : `"string"`|string|
|**radio_version**  <br>*optional*|**Example** : `"string"`|string|
|**uptime**  <br>*optional*|**Example** : `"string"`|string|
|**uuid**  <br>*optional*|**Example** : `"string"`|string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**200**|No Content|


#### Consumes

* `application/json`


#### Tags

* crashreports


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/crashreports/string/
```


##### Request body
```
json :
{
  "uptime" : "string",
  "is_fake_report" : "string",
  "uuid" : "string",
  "boot_reason" : "string",
  "power_on_reason" : "string",
  "build_fingerprint" : "string",
  "power_off_reason" : "string",
  "radio_version" : "string",
  "next_logfile_key" : "string",
  "date" : "string",
  "app_version" : "string",
  "device_local_id" : "string"
}
```


<a name="devices_read"></a>
### GET /hiccup/api/v1/devices/{uuid}/

#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**uuid**  <br>*required*|string|
|**Query**|**limit**  <br>*optional*|string|
|**Query**|**offset**  <br>*optional*|string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**200**|No Content|


#### Tags

* devices


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/
```


##### Request query
```
json :
{
  "limit" : "string",
  "offset" : "string"
}
```


<a name="devices_update"></a>
### PUT /hiccup/api/v1/devices/{uuid}/

#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**uuid**  <br>*required*|string|


#### Body parameter
*Name* : data  
*Flags* : optional


|Name|Description|Schema|
|---|---|---|
|**board_date**  <br>*optional*|**Example** : `"string"`|string|
|**chipset**  <br>*optional*|**Example** : `"string"`|string|
|**imei**  <br>*optional*|**Example** : `"string"`|string|
|**last_heartbeat**  <br>*optional*|**Example** : `"string"`|string|
|**next_per_crashreport_key**  <br>*optional*|**Example** : `"string"`|string|
|**next_per_heartbeat_key**  <br>*optional*|**Example** : `"string"`|string|
|**token**  <br>*optional*|**Example** : `"string"`|string|
|**user**  <br>*required*|**Example** : `"string"`|string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**200**|No Content|


#### Consumes

* `application/json`


#### Tags

* devices


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/
```


##### Request body
```
json :
{
  "board_date" : "string",
  "next_per_heartbeat_key" : "string",
  "next_per_crashreport_key" : "string",
  "token" : "string",
  "user" : "string",
  "imei" : "string",
  "chipset" : "string",
  "last_heartbeat" : "string"
}
```


<a name="devices_destroy"></a>
### DELETE /hiccup/api/v1/devices/{uuid}/

#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**uuid**  <br>*required*|string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**204**|No Content|


#### Tags

* devices


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/
```


<a name="devices_partial_update"></a>
### PATCH /hiccup/api/v1/devices/{uuid}/

#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**uuid**  <br>*required*|string|


#### Body parameter
*Name* : data  
*Flags* : optional


|Name|Description|Schema|
|---|---|---|
|**board_date**  <br>*optional*|**Example** : `"string"`|string|
|**chipset**  <br>*optional*|**Example** : `"string"`|string|
|**imei**  <br>*optional*|**Example** : `"string"`|string|
|**last_heartbeat**  <br>*optional*|**Example** : `"string"`|string|
|**next_per_crashreport_key**  <br>*optional*|**Example** : `"string"`|string|
|**next_per_heartbeat_key**  <br>*optional*|**Example** : `"string"`|string|
|**token**  <br>*optional*|**Example** : `"string"`|string|
|**user**  <br>*optional*|**Example** : `"string"`|string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**200**|No Content|


#### Consumes

* `application/json`


#### Tags

* devices


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/
```


##### Request body
```
json :
{
  "board_date" : "string",
  "next_per_heartbeat_key" : "string",
  "next_per_crashreport_key" : "string",
  "token" : "string",
  "user" : "string",
  "imei" : "string",
  "chipset" : "string",
  "last_heartbeat" : "string"
}
```


<a name="crashreports_create"></a>
### POST /hiccup/api/v1/devices/{uuid}/crashreports/

#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**uuid**  <br>*required*|string|


#### Body parameter
*Name* : data  
*Flags* : optional


|Name|Description|Schema|
|---|---|---|
|**app_version**  <br>*required*|**Example** : `"string"`|string|
|**boot_reason**  <br>*required*|**Example** : `"string"`|string|
|**build_fingerprint**  <br>*required*|**Example** : `"string"`|string|
|**date**  <br>*required*|**Example** : `"string"`|string|
|**device_local_id**  <br>*optional*|**Example** : `"string"`|string|
|**is_fake_report**  <br>*optional*|**Example** : `"string"`|string|
|**next_logfile_key**  <br>*optional*|**Example** : `"string"`|string|
|**power_off_reason**  <br>*required*|**Example** : `"string"`|string|
|**power_on_reason**  <br>*required*|**Example** : `"string"`|string|
|**radio_version**  <br>*optional*|**Example** : `"string"`|string|
|**uptime**  <br>*required*|**Example** : `"string"`|string|
|**uuid**  <br>*required*|**Example** : `"string"`|string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**201**|No Content|


#### Consumes

* `application/json`


#### Tags

* crashreports


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/crashreports/
```


##### Request body
```
json :
{
  "uptime" : "string",
  "is_fake_report" : "string",
  "uuid" : "string",
  "boot_reason" : "string",
  "power_on_reason" : "string",
  "build_fingerprint" : "string",
  "power_off_reason" : "string",
  "radio_version" : "string",
  "next_logfile_key" : "string",
  "date" : "string",
  "app_version" : "string",
  "device_local_id" : "string"
}
```


<a name="logfile_put_create"></a>
### POST /hiccup/api/v1/devices/{uuid}/crashreports/{device_local_id}/logfile_put/{filename}/

#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**device_local_id**  <br>*required*|string|
|**Path**|**filename**  <br>*required*|string|
|**Path**|**uuid**  <br>*required*|string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**201**|No Content|


#### Tags

* logfile_put


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/crashreports/string/logfile_put/string/
```


<a name="heartbeats_create"></a>
### POST /hiccup/api/v1/devices/{uuid}/heartbeats/

#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**uuid**  <br>*required*|string|


#### Body parameter
*Name* : data  
*Flags* : optional


|Name|Description|Schema|
|---|---|---|
|**app_version**  <br>*required*|**Example** : `"string"`|string|
|**build_fingerprint**  <br>*required*|**Example** : `"string"`|string|
|**date**  <br>*required*|**Example** : `"string"`|string|
|**device_local_id**  <br>*optional*|**Example** : `"string"`|string|
|**radio_version**  <br>*optional*|**Example** : `"string"`|string|
|**uptime**  <br>*required*|**Example** : `"string"`|string|
|**uuid**  <br>*required*|**Example** : `"string"`|string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**201**|No Content|


#### Consumes

* `application/json`


#### Tags

* heartbeats


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/heartbeats/
```


##### Request body
```
json :
{
  "uptime" : "string",
  "uuid" : "string",
  "build_fingerprint" : "string",
  "radio_version" : "string",
  "date" : "string",
  "app_version" : "string",
  "device_local_id" : "string"
}
```


<a name="heartbeats_read"></a>
### GET /hiccup/api/v1/devices/{uuid}/heartbeats/{device_local_id}/

#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**device_local_id**  <br>*required*|string|
|**Path**|**uuid**  <br>*required*|string|
|**Query**|**limit**  <br>*optional*|string|
|**Query**|**offset**  <br>*optional*|string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**200**|No Content|


#### Tags

* heartbeats


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/heartbeats/string/
```


##### Request query
```
json :
{
  "limit" : "string",
  "offset" : "string"
}
```


<a name="heartbeats_update"></a>
### PUT /hiccup/api/v1/devices/{uuid}/heartbeats/{device_local_id}/

#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**device_local_id**  <br>*required*|string|
|**Path**|**uuid**  <br>*required*|string|


#### Body parameter
*Name* : data  
*Flags* : optional


|Name|Description|Schema|
|---|---|---|
|**app_version**  <br>*required*|**Example** : `"string"`|string|
|**build_fingerprint**  <br>*required*|**Example** : `"string"`|string|
|**date**  <br>*required*|**Example** : `"string"`|string|
|**device_local_id**  <br>*optional*|**Example** : `"string"`|string|
|**radio_version**  <br>*optional*|**Example** : `"string"`|string|
|**uptime**  <br>*required*|**Example** : `"string"`|string|
|**uuid**  <br>*required*|**Example** : `"string"`|string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**200**|No Content|


#### Consumes

* `application/json`


#### Tags

* heartbeats


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/heartbeats/string/
```


##### Request body
```
json :
{
  "uptime" : "string",
  "uuid" : "string",
  "build_fingerprint" : "string",
  "radio_version" : "string",
  "date" : "string",
  "app_version" : "string",
  "device_local_id" : "string"
}
```


<a name="heartbeats_destroy"></a>
### DELETE /hiccup/api/v1/devices/{uuid}/heartbeats/{device_local_id}/

#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**device_local_id**  <br>*required*|string|
|**Path**|**uuid**  <br>*required*|string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**204**|No Content|


#### Tags

* heartbeats


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/heartbeats/string/
```


<a name="heartbeats_partial_update"></a>
### PATCH /hiccup/api/v1/devices/{uuid}/heartbeats/{device_local_id}/

#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**device_local_id**  <br>*required*|string|
|**Path**|**uuid**  <br>*required*|string|


#### Body parameter
*Name* : data  
*Flags* : optional


|Name|Description|Schema|
|---|---|---|
|**app_version**  <br>*optional*|**Example** : `"string"`|string|
|**build_fingerprint**  <br>*optional*|**Example** : `"string"`|string|
|**date**  <br>*optional*|**Example** : `"string"`|string|
|**device_local_id**  <br>*optional*|**Example** : `"string"`|string|
|**radio_version**  <br>*optional*|**Example** : `"string"`|string|
|**uptime**  <br>*optional*|**Example** : `"string"`|string|
|**uuid**  <br>*optional*|**Example** : `"string"`|string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**200**|No Content|


#### Consumes

* `application/json`


#### Tags

* heartbeats


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/heartbeats/string/
```


##### Request body
```
json :
{
  "uptime" : "string",
  "uuid" : "string",
  "build_fingerprint" : "string",
  "radio_version" : "string",
  "date" : "string",
  "app_version" : "string",
  "device_local_id" : "string"
}
```


<a name="logfiles_read"></a>
### GET /hiccup/api/v1/logfiles/{pk}/

#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**pk**  <br>*required*|string|
|**Query**|**limit**  <br>*optional*|string|
|**Query**|**offset**  <br>*optional*|string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**200**|No Content|


#### Tags

* logfiles


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/logfiles/string/
```


##### Request query
```
json :
{
  "limit" : "string",
  "offset" : "string"
}
```


<a name="logfiles_update"></a>
### PUT /hiccup/api/v1/logfiles/{pk}/

#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**pk**  <br>*required*|string|


#### Body parameter
*Name* : data  
*Flags* : optional


|Name|Description|Schema|
|---|---|---|
|**crashreport**  <br>*required*|**Example** : `"string"`|string|
|**crashreport_local_id**  <br>*optional*|**Example** : `"string"`|string|
|**logfile**  <br>*required*|**Example** : `"string"`|string|
|**logfile_type**  <br>*optional*|**Example** : `"string"`|string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**200**|No Content|


#### Consumes

* `application/json`


#### Tags

* logfiles


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/logfiles/string/
```


##### Request body
```
json :
{
  "logfile" : "string",
  "crashreport" : "string",
  "crashreport_local_id" : "string",
  "logfile_type" : "string"
}
```


<a name="logfiles_destroy"></a>
### DELETE /hiccup/api/v1/logfiles/{pk}/

#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**pk**  <br>*required*|string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**204**|No Content|


#### Tags

* logfiles


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/logfiles/string/
```


<a name="logfiles_partial_update"></a>
### PATCH /hiccup/api/v1/logfiles/{pk}/

#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**pk**  <br>*required*|string|


#### Body parameter
*Name* : data  
*Flags* : optional


|Name|Description|Schema|
|---|---|---|
|**crashreport**  <br>*optional*|**Example** : `"string"`|string|
|**crashreport_local_id**  <br>*optional*|**Example** : `"string"`|string|
|**logfile**  <br>*optional*|**Example** : `"string"`|string|
|**logfile_type**  <br>*optional*|**Example** : `"string"`|string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**200**|No Content|


#### Consumes

* `application/json`


#### Tags

* logfiles


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/logfiles/string/
```


##### Request body
```
json :
{
  "logfile" : "string",
  "crashreport" : "string",
  "crashreport_local_id" : "string",
  "logfile_type" : "string"
}
```


<a name="docs_read"></a>
### GET /hiccup/docs/

#### Responses

|HTTP Code|Schema|
|---|---|
|**200**|No Content|


#### Tags

* docs


#### Example HTTP request

##### Request path
```
/hiccup/docs/
```


<a name="device_overview_read"></a>
### GET /hiccup_stats/api/v1/device_overview/{uuid}/

#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**uuid**  <br>*required*|string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**200**|No Content|


#### Tags

* device_overview


#### Example HTTP request

##### Request path
```
/hiccup_stats/api/v1/device_overview/string/
```


<a name="device_report_history_read"></a>
### GET /hiccup_stats/api/v1/device_report_history/{uuid}/

#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**uuid**  <br>*required*|string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**200**|No Content|


#### Tags

* device_report_history


#### Example HTTP request

##### Request path
```
/hiccup_stats/api/v1/device_report_history/string/
```


<a name="device_update_history_read"></a>
### GET /hiccup_stats/api/v1/device_update_history/{uuid}/

#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**uuid**  <br>*required*|string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**200**|No Content|


#### Tags

* device_update_history


#### Example HTTP request

##### Request path
```
/hiccup_stats/api/v1/device_update_history/string/
```


<a name="logfile_download_read"></a>
### GET /hiccup_stats/api/v1/logfile_download/{id}/

#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**id**  <br>*required*|string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**200**|No Content|


#### Tags

* logfile_download


#### Example HTTP request

##### Request path
```
/hiccup_stats/api/v1/logfile_download/string/
```


<a name="status_read"></a>
### GET /hiccup_stats/api/v1/status/

#### Responses

|HTTP Code|Schema|
|---|---|
|**200**|No Content|


#### Tags

* status


#### Example HTTP request

##### Request path
```
/hiccup_stats/api/v1/status/
```


<a name="version_daily_read"></a>
### GET /hiccup_stats/api/v1/version_daily/

#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Query**|**date**  <br>*optional*|string|
|**Query**|**date_end**  <br>*optional*|string|
|**Query**|**date_start**  <br>*optional*|string|
|**Query**|**heartbeats**  <br>*optional*|string|
|**Query**|**limit**  <br>*optional*|string|
|**Query**|**offset**  <br>*optional*|string|
|**Query**|**other**  <br>*optional*|string|
|**Query**|**prob_crashes**  <br>*optional*|string|
|**Query**|**smpl**  <br>*optional*|string|
|**Query**|**version**  <br>*optional*|string|
|**Query**|**version__build_fingerprint**  <br>*optional*|string|
|**Query**|**version__is_beta_release**  <br>*optional*|string|
|**Query**|**version__is_official_release**  <br>*optional*|string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**200**|No Content|


#### Tags

* version_daily


#### Example HTTP request

##### Request path
```
/hiccup_stats/api/v1/version_daily/
```


##### Request query
```
json :
{
  "date" : "string",
  "date_end" : "string",
  "date_start" : "string",
  "heartbeats" : "string",
  "limit" : "string",
  "offset" : "string",
  "other" : "string",
  "prob_crashes" : "string",
  "smpl" : "string",
  "version" : "string",
  "version__build_fingerprint" : "string",
  "version__is_beta_release" : "string",
  "version__is_official_release" : "string"
}
```


<a name="versions_read"></a>
### GET /hiccup_stats/api/v1/versions/

#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Query**|**build_fingerprint**  <br>*optional*|string|
|**Query**|**first_seen_after**  <br>*optional*|string|
|**Query**|**first_seen_before**  <br>*optional*|string|
|**Query**|**first_seen_on**  <br>*optional*|string|
|**Query**|**heartbeats**  <br>*optional*|string|
|**Query**|**is_beta_release**  <br>*optional*|string|
|**Query**|**is_official_release**  <br>*optional*|string|
|**Query**|**limit**  <br>*optional*|string|
|**Query**|**offset**  <br>*optional*|string|
|**Query**|**other**  <br>*optional*|string|
|**Query**|**prob_crashes**  <br>*optional*|string|
|**Query**|**released_after**  <br>*optional*|string|
|**Query**|**released_before**  <br>*optional*|string|
|**Query**|**released_on**  <br>*optional*|string|
|**Query**|**smpl**  <br>*optional*|string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**200**|No Content|


#### Tags

* versions


#### Example HTTP request

##### Request path
```
/hiccup_stats/api/v1/versions/
```


##### Request query
```
json :
{
  "build_fingerprint" : "string",
  "first_seen_after" : "string",
  "first_seen_before" : "string",
  "first_seen_on" : "string",
  "heartbeats" : "string",
  "is_beta_release" : "string",
  "is_official_release" : "string",
  "limit" : "string",
  "offset" : "string",
  "other" : "string",
  "prob_crashes" : "string",
  "released_after" : "string",
  "released_before" : "string",
  "released_on" : "string",
  "smpl" : "string"
}
```






<a name="securityscheme"></a>
## Security

<a name="basic"></a>
### basic
*Type* : basic



