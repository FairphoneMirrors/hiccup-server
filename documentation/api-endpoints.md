# Hiccup API


<a name="overview"></a>
## Overview

### Version information
*Version* : v1


### URI scheme
*BasePath* : /


### Consumes

* `application/json`


### Produces

* `application/json`




<a name="paths"></a>
## Paths

<a name="hiccup_api_v1_crashreports_create"></a>
### POST /hiccup/api/v1/crashreports/

#### Description
Create a crash report


#### Body parameter
*Name* : data  
*Flags* : required  
*Type* : [CrashReport](#crashreport)


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**201**|The crash report has been successfully created.|[CreateCrashreportResponseSchema](#createcrashreportresponseschema)|
|**400**|Invalid input.|No Content|
|**404**|No device with the given uuid could be found.|No Content|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/crashreports/
```


##### Request body
```json
{
  "id" : "string",
  "logfiles" : [ "string" ],
  "uuid" : "string",
  "device_local_id" : 0,
  "date" : "string",
  "is_fake_report" : true,
  "app_version" : 0,
  "uptime" : "string",
  "build_fingerprint" : "string",
  "radio_version" : "string",
  "boot_reason" : "string",
  "power_on_reason" : "string",
  "power_off_reason" : "string",
  "next_logfile_key" : 0,
  "created_at" : "string"
}
```


#### Example HTTP response

##### Response 201
```json
{
  "device_local_id" : 0
}
```


<a name="hiccup_api_v1_crashreports_list"></a>
### GET /hiccup/api/v1/crashreports/

#### Description
List crash reports


#### Parameters

|Type|Name|Description|Schema|
|---|---|---|---|
|**Query**|**build_fingerprint**  <br>*optional*||string|
|**Query**|**device**  <br>*optional*||string|
|**Query**|**limit**  <br>*optional*|Number of results to return per page.|integer|
|**Query**|**offset**  <br>*optional*|The initial index from which to return the results.|integer|
|**Query**|**radio_version**  <br>*optional*||string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**200**|[Response 200](#hiccup_api_v1_crashreports_list-response-200)|

<a name="hiccup_api_v1_crashreports_list-response-200"></a>
**Response 200**

|Name|Description|Schema|
|---|---|---|
|**count**  <br>*required*|**Example** : `0`|integer|
|**next**  <br>*optional*|**Example** : `"string"`|string (uri)|
|**previous**  <br>*optional*|**Example** : `"string"`|string (uri)|
|**results**  <br>*required*|**Example** : `[ "[crashreport](#crashreport)" ]`|< [CrashReport](#crashreport) > array|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/crashreports/
```


#### Example HTTP response

##### Response 200
```json
"object"
```


<a name="hiccup_api_v1_crashreports_read"></a>
### GET /hiccup/api/v1/crashreports/{id}/

#### Description
Get a crash report


#### Parameters

|Type|Name|Description|Schema|
|---|---|---|---|
|**Path**|**id**  <br>*required*|A unique integer value identifying this crashreport.|integer|


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**200**||[CrashReport](#crashreport)|
|**404**|Not found.|No Content|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/crashreports/0/
```


#### Example HTTP response

##### Response 200
```json
{
  "id" : "string",
  "logfiles" : [ "string" ],
  "uuid" : "string",
  "device_local_id" : 0,
  "date" : "string",
  "is_fake_report" : true,
  "app_version" : 0,
  "uptime" : "string",
  "build_fingerprint" : "string",
  "radio_version" : "string",
  "boot_reason" : "string",
  "power_on_reason" : "string",
  "power_off_reason" : "string",
  "next_logfile_key" : 0,
  "created_at" : "string"
}
```


<a name="hiccup_api_v1_crashreports_update"></a>
### PUT /hiccup/api/v1/crashreports/{id}/

#### Description
Update a crash report


#### Parameters

|Type|Name|Description|Schema|
|---|---|---|---|
|**Path**|**id**  <br>*required*|A unique integer value identifying this crashreport.|integer|


#### Body parameter
*Name* : data  
*Flags* : required  
*Type* : [CrashReport](#crashreport)


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**200**||[CrashReport](#crashreport)|
|**400**|Invalid input.|No Content|
|**404**|Not found.|No Content|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/crashreports/0/
```


##### Request body
```json
{
  "id" : "string",
  "logfiles" : [ "string" ],
  "uuid" : "string",
  "device_local_id" : 0,
  "date" : "string",
  "is_fake_report" : true,
  "app_version" : 0,
  "uptime" : "string",
  "build_fingerprint" : "string",
  "radio_version" : "string",
  "boot_reason" : "string",
  "power_on_reason" : "string",
  "power_off_reason" : "string",
  "next_logfile_key" : 0,
  "created_at" : "string"
}
```


#### Example HTTP response

##### Response 200
```json
{
  "id" : "string",
  "logfiles" : [ "string" ],
  "uuid" : "string",
  "device_local_id" : 0,
  "date" : "string",
  "is_fake_report" : true,
  "app_version" : 0,
  "uptime" : "string",
  "build_fingerprint" : "string",
  "radio_version" : "string",
  "boot_reason" : "string",
  "power_on_reason" : "string",
  "power_off_reason" : "string",
  "next_logfile_key" : 0,
  "created_at" : "string"
}
```


<a name="hiccup_api_v1_crashreports_delete"></a>
### DELETE /hiccup/api/v1/crashreports/{id}/

#### Description
Delete a crash report


#### Parameters

|Type|Name|Description|Schema|
|---|---|---|---|
|**Path**|**id**  <br>*required*|A unique integer value identifying this crashreport.|integer|


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**204**||No Content|
|**404**|Not found.|No Content|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/crashreports/0/
```


<a name="hiccup_api_v1_crashreports_partial_update"></a>
### PATCH /hiccup/api/v1/crashreports/{id}/

#### Description
Partially update a crash report


#### Parameters

|Type|Name|Description|Schema|
|---|---|---|---|
|**Path**|**id**  <br>*required*|A unique integer value identifying this crashreport.|integer|


#### Body parameter
*Name* : data  
*Flags* : required  
*Type* : [CrashReport](#crashreport)


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**200**||[CrashReport](#crashreport)|
|**400**|Invalid input.|No Content|
|**404**|Not found.|No Content|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/crashreports/0/
```


##### Request body
```json
{
  "id" : "string",
  "logfiles" : [ "string" ],
  "uuid" : "string",
  "device_local_id" : 0,
  "date" : "string",
  "is_fake_report" : true,
  "app_version" : 0,
  "uptime" : "string",
  "build_fingerprint" : "string",
  "radio_version" : "string",
  "boot_reason" : "string",
  "power_on_reason" : "string",
  "power_off_reason" : "string",
  "next_logfile_key" : 0,
  "created_at" : "string"
}
```


#### Example HTTP response

##### Response 200
```json
{
  "id" : "string",
  "logfiles" : [ "string" ],
  "uuid" : "string",
  "device_local_id" : 0,
  "date" : "string",
  "is_fake_report" : true,
  "app_version" : 0,
  "uptime" : "string",
  "build_fingerprint" : "string",
  "radio_version" : "string",
  "boot_reason" : "string",
  "power_on_reason" : "string",
  "power_off_reason" : "string",
  "next_logfile_key" : 0,
  "created_at" : "string"
}
```


<a name="hiccup_api_v1_devices_create"></a>
### POST /hiccup/api/v1/devices/

#### Description
Create a device


#### Body parameter
*Name* : data  
*Flags* : required  
*Type* : [Device](#device)


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**201**||[Device](#device)|
|**400**|Invalid input.|No Content|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/
```


##### Request body
```json
{
  "id" : 0,
  "board_date" : "string",
  "last_heartbeat" : "string",
  "uuid" : "string",
  "imei" : "string",
  "chipset" : "string",
  "token" : "string",
  "next_per_crashreport_key" : 0,
  "next_per_heartbeat_key" : 0,
  "user" : 0
}
```


#### Example HTTP response

##### Response 201
```json
{
  "id" : 0,
  "board_date" : "string",
  "last_heartbeat" : "string",
  "uuid" : "string",
  "imei" : "string",
  "chipset" : "string",
  "token" : "string",
  "next_per_crashreport_key" : 0,
  "next_per_heartbeat_key" : 0,
  "user" : 0
}
```


<a name="hiccup_api_v1_devices_list"></a>
### GET /hiccup/api/v1/devices/

#### Description
List devices


#### Parameters

|Type|Name|Description|Schema|
|---|---|---|---|
|**Query**|**board_date**  <br>*optional*||string|
|**Query**|**chipset**  <br>*optional*||string|
|**Query**|**limit**  <br>*optional*|Number of results to return per page.|integer|
|**Query**|**offset**  <br>*optional*|The initial index from which to return the results.|integer|
|**Query**|**uuid**  <br>*optional*||string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**200**|[Response 200](#hiccup_api_v1_devices_list-response-200)|

<a name="hiccup_api_v1_devices_list-response-200"></a>
**Response 200**

|Name|Description|Schema|
|---|---|---|
|**count**  <br>*required*|**Example** : `0`|integer|
|**next**  <br>*optional*|**Example** : `"string"`|string (uri)|
|**previous**  <br>*optional*|**Example** : `"string"`|string (uri)|
|**results**  <br>*required*|**Example** : `[ "[device](#device)" ]`|< [Device](#device) > array|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/
```


#### Example HTTP response

##### Response 200
```json
"object"
```


<a name="hiccup_api_v1_devices_register_create"></a>
### POST /hiccup/api/v1/devices/register/

#### Description
Register a new device.

This endpoint will generate a django user for the new device. The device is
identified by a uuid, and authenticated with a token.
We generate the uuid here as this makes it easier to deal with collisions.


#### Body parameter
*Name* : data  
*Flags* : required  
*Type* : [DeviceCreate](#devicecreate)


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**200**|The device has been successfully registered.|[DeviceRegisterResponseSchema](#deviceregisterresponseschema)|
|**400**|Invalid input.|No Content|


#### Tags

* hiccup


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/register/
```


##### Request body
```json
{
  "board_date" : "string",
  "chipset" : "string"
}
```


#### Example HTTP response

##### Response 200
```json
{
  "uuid" : "string",
  "token" : "string"
}
```


<a name="hiccup_api_v1_devices_crashreports_read"></a>
### GET /hiccup/api/v1/devices/{device__uuid}/crashreports/{device_local_id}/

#### Description
Get a crash report


#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**device__uuid**  <br>*required*|string|
|**Path**|**device_local_id**  <br>*required*|integer|


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**200**||[CrashReport](#crashreport)|
|**404**|Not found.|No Content|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/crashreports/0/
```


#### Example HTTP response

##### Response 200
```json
{
  "id" : "string",
  "logfiles" : [ "string" ],
  "uuid" : "string",
  "device_local_id" : 0,
  "date" : "string",
  "is_fake_report" : true,
  "app_version" : 0,
  "uptime" : "string",
  "build_fingerprint" : "string",
  "radio_version" : "string",
  "boot_reason" : "string",
  "power_on_reason" : "string",
  "power_off_reason" : "string",
  "next_logfile_key" : 0,
  "created_at" : "string"
}
```


<a name="hiccup_api_v1_devices_crashreports_update"></a>
### PUT /hiccup/api/v1/devices/{device__uuid}/crashreports/{device_local_id}/

#### Description
Update a crash report


#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**device__uuid**  <br>*required*|string|
|**Path**|**device_local_id**  <br>*required*|integer|


#### Body parameter
*Name* : data  
*Flags* : required  
*Type* : [CrashReport](#crashreport)


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**200**||[CrashReport](#crashreport)|
|**400**|Invalid input.|No Content|
|**404**|Not found.|No Content|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/crashreports/0/
```


##### Request body
```json
{
  "id" : "string",
  "logfiles" : [ "string" ],
  "uuid" : "string",
  "device_local_id" : 0,
  "date" : "string",
  "is_fake_report" : true,
  "app_version" : 0,
  "uptime" : "string",
  "build_fingerprint" : "string",
  "radio_version" : "string",
  "boot_reason" : "string",
  "power_on_reason" : "string",
  "power_off_reason" : "string",
  "next_logfile_key" : 0,
  "created_at" : "string"
}
```


#### Example HTTP response

##### Response 200
```json
{
  "id" : "string",
  "logfiles" : [ "string" ],
  "uuid" : "string",
  "device_local_id" : 0,
  "date" : "string",
  "is_fake_report" : true,
  "app_version" : 0,
  "uptime" : "string",
  "build_fingerprint" : "string",
  "radio_version" : "string",
  "boot_reason" : "string",
  "power_on_reason" : "string",
  "power_off_reason" : "string",
  "next_logfile_key" : 0,
  "created_at" : "string"
}
```


<a name="hiccup_api_v1_devices_crashreports_delete"></a>
### DELETE /hiccup/api/v1/devices/{device__uuid}/crashreports/{device_local_id}/

#### Description
Delete a crash report


#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**device__uuid**  <br>*required*|string|
|**Path**|**device_local_id**  <br>*required*|integer|


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**204**||No Content|
|**404**|Not found.|No Content|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/crashreports/0/
```


<a name="hiccup_api_v1_devices_crashreports_partial_update"></a>
### PATCH /hiccup/api/v1/devices/{device__uuid}/crashreports/{device_local_id}/

#### Description
Partially update a crash report


#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**device__uuid**  <br>*required*|string|
|**Path**|**device_local_id**  <br>*required*|integer|


#### Body parameter
*Name* : data  
*Flags* : required  
*Type* : [CrashReport](#crashreport)


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**200**||[CrashReport](#crashreport)|
|**400**|Invalid input.|No Content|
|**404**|Not found.|No Content|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/crashreports/0/
```


##### Request body
```json
{
  "id" : "string",
  "logfiles" : [ "string" ],
  "uuid" : "string",
  "device_local_id" : 0,
  "date" : "string",
  "is_fake_report" : true,
  "app_version" : 0,
  "uptime" : "string",
  "build_fingerprint" : "string",
  "radio_version" : "string",
  "boot_reason" : "string",
  "power_on_reason" : "string",
  "power_off_reason" : "string",
  "next_logfile_key" : 0,
  "created_at" : "string"
}
```


#### Example HTTP response

##### Response 200
```json
{
  "id" : "string",
  "logfiles" : [ "string" ],
  "uuid" : "string",
  "device_local_id" : 0,
  "date" : "string",
  "is_fake_report" : true,
  "app_version" : 0,
  "uptime" : "string",
  "build_fingerprint" : "string",
  "radio_version" : "string",
  "boot_reason" : "string",
  "power_on_reason" : "string",
  "power_off_reason" : "string",
  "next_logfile_key" : 0,
  "created_at" : "string"
}
```


<a name="hiccup_api_v1_devices_read"></a>
### GET /hiccup/api/v1/devices/{uuid}/

#### Description
Get a device


#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**uuid**  <br>*required*|string|


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**200**||[Device](#device)|
|**404**|Not found.|No Content|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/
```


#### Example HTTP response

##### Response 200
```json
{
  "id" : 0,
  "board_date" : "string",
  "last_heartbeat" : "string",
  "uuid" : "string",
  "imei" : "string",
  "chipset" : "string",
  "token" : "string",
  "next_per_crashreport_key" : 0,
  "next_per_heartbeat_key" : 0,
  "user" : 0
}
```


<a name="hiccup_api_v1_devices_update"></a>
### PUT /hiccup/api/v1/devices/{uuid}/

#### Description
Update a device


#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**uuid**  <br>*required*|string|


#### Body parameter
*Name* : data  
*Flags* : required  
*Type* : [Device](#device)


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**200**||[Device](#device)|
|**400**|Invalid input.|No Content|
|**404**|Not found.|No Content|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/
```


##### Request body
```json
{
  "id" : 0,
  "board_date" : "string",
  "last_heartbeat" : "string",
  "uuid" : "string",
  "imei" : "string",
  "chipset" : "string",
  "token" : "string",
  "next_per_crashreport_key" : 0,
  "next_per_heartbeat_key" : 0,
  "user" : 0
}
```


#### Example HTTP response

##### Response 200
```json
{
  "id" : 0,
  "board_date" : "string",
  "last_heartbeat" : "string",
  "uuid" : "string",
  "imei" : "string",
  "chipset" : "string",
  "token" : "string",
  "next_per_crashreport_key" : 0,
  "next_per_heartbeat_key" : 0,
  "user" : 0
}
```


<a name="hiccup_api_v1_devices_delete"></a>
### DELETE /hiccup/api/v1/devices/{uuid}/

#### Description
Delete a device


#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**uuid**  <br>*required*|string|


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**204**||No Content|
|**404**|Not found.|No Content|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/
```


<a name="hiccup_api_v1_devices_partial_update"></a>
### PATCH /hiccup/api/v1/devices/{uuid}/

#### Description
Make a partial update for a device


#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**uuid**  <br>*required*|string|


#### Body parameter
*Name* : data  
*Flags* : required  
*Type* : [Device](#device)


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**200**||[Device](#device)|
|**400**|Invalid input.|No Content|
|**404**|Not found.|No Content|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/
```


##### Request body
```json
{
  "id" : 0,
  "board_date" : "string",
  "last_heartbeat" : "string",
  "uuid" : "string",
  "imei" : "string",
  "chipset" : "string",
  "token" : "string",
  "next_per_crashreport_key" : 0,
  "next_per_heartbeat_key" : 0,
  "user" : 0
}
```


#### Example HTTP response

##### Response 200
```json
{
  "id" : 0,
  "board_date" : "string",
  "last_heartbeat" : "string",
  "uuid" : "string",
  "imei" : "string",
  "chipset" : "string",
  "token" : "string",
  "next_per_crashreport_key" : 0,
  "next_per_heartbeat_key" : 0,
  "user" : 0
}
```


<a name="hiccup_api_v1_devices_crashreports_create"></a>
### POST /hiccup/api/v1/devices/{uuid}/crashreports/

#### Description
Create a crash report


#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**uuid**  <br>*required*|string|


#### Body parameter
*Name* : data  
*Flags* : required  
*Type* : [CrashReport](#crashreport)


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**201**|The crash report has been successfully created.|[CreateCrashreportResponseSchema](#createcrashreportresponseschema)|
|**400**|Invalid input.|No Content|
|**404**|No device with the given uuid could be found.|No Content|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/crashreports/
```


##### Request body
```json
{
  "id" : "string",
  "logfiles" : [ "string" ],
  "uuid" : "string",
  "device_local_id" : 0,
  "date" : "string",
  "is_fake_report" : true,
  "app_version" : 0,
  "uptime" : "string",
  "build_fingerprint" : "string",
  "radio_version" : "string",
  "boot_reason" : "string",
  "power_on_reason" : "string",
  "power_off_reason" : "string",
  "next_logfile_key" : 0,
  "created_at" : "string"
}
```


#### Example HTTP response

##### Response 201
```json
{
  "device_local_id" : 0
}
```


<a name="hiccup_api_v1_devices_crashreports_list"></a>
### GET /hiccup/api/v1/devices/{uuid}/crashreports/

#### Description
List crash reports


#### Parameters

|Type|Name|Description|Schema|
|---|---|---|---|
|**Path**|**uuid**  <br>*required*||string|
|**Query**|**build_fingerprint**  <br>*optional*||string|
|**Query**|**device**  <br>*optional*||string|
|**Query**|**limit**  <br>*optional*|Number of results to return per page.|integer|
|**Query**|**offset**  <br>*optional*|The initial index from which to return the results.|integer|
|**Query**|**radio_version**  <br>*optional*||string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**200**|[Response 200](#hiccup_api_v1_devices_crashreports_list-response-200)|

<a name="hiccup_api_v1_devices_crashreports_list-response-200"></a>
**Response 200**

|Name|Description|Schema|
|---|---|---|
|**count**  <br>*required*|**Example** : `0`|integer|
|**next**  <br>*optional*|**Example** : `"string"`|string (uri)|
|**previous**  <br>*optional*|**Example** : `"string"`|string (uri)|
|**results**  <br>*required*|**Example** : `[ "[crashreport](#crashreport)" ]`|< [CrashReport](#crashreport) > array|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/crashreports/
```


#### Example HTTP response

##### Response 200
```json
"object"
```


<a name="hiccup_api_v1_devices_crashreports_logfile_put_create"></a>
### POST /hiccup/api/v1/devices/{uuid}/crashreports/{device_local_id}/logfile_put/{filename}/

#### Description
Upload a log file for a crash report.


#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**device_local_id**  <br>*required*|string|
|**Path**|**filename**  <br>*required*|string|
|**Path**|**uuid**  <br>*required*|string|


#### Body parameter
*Name* : data  
*Flags* : required  
*Type* : [LogFile](#logfile)


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**201**|Created|No Content|
|**400**|Invalid input.|No Content|
|**404**|Crashreport does not exist.|No Content|


#### Consumes

* `\*/*`


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/crashreports/string/logfile_put/string/
```


##### Request body
```json
{
  "id" : 0,
  "logfile_type" : "string",
  "logfile" : "string",
  "crashreport_local_id" : 0,
  "created_at" : "string",
  "crashreport" : 0
}
```


<a name="hiccup_api_v1_devices_heartbeats_create"></a>
### POST /hiccup/api/v1/devices/{uuid}/heartbeats/

#### Description
Create a heartbeat


#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**uuid**  <br>*required*|string|


#### Body parameter
*Name* : data  
*Flags* : required  
*Type* : [HeartBeat](#heartbeat)


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**201**||[HeartBeat](#heartbeat)|
|**400**|Invalid input.|No Content|
|**404**|No device with the given uuid could be found.|No Content|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/heartbeats/
```


##### Request body
```json
{
  "id" : "string",
  "uuid" : "string",
  "device_local_id" : 0,
  "date" : "string",
  "app_version" : 0,
  "uptime" : "string",
  "build_fingerprint" : "string",
  "radio_version" : "string",
  "created_at" : "string"
}
```


#### Example HTTP response

##### Response 201
```json
{
  "id" : "string",
  "uuid" : "string",
  "device_local_id" : 0,
  "date" : "string",
  "app_version" : 0,
  "uptime" : "string",
  "build_fingerprint" : "string",
  "radio_version" : "string",
  "created_at" : "string"
}
```


<a name="hiccup_api_v1_devices_heartbeats_list"></a>
### GET /hiccup/api/v1/devices/{uuid}/heartbeats/

#### Description
List heartbeats


#### Parameters

|Type|Name|Description|Schema|
|---|---|---|---|
|**Path**|**uuid**  <br>*required*||string|
|**Query**|**build_fingerprint**  <br>*optional*||string|
|**Query**|**device**  <br>*optional*||string|
|**Query**|**limit**  <br>*optional*|Number of results to return per page.|integer|
|**Query**|**offset**  <br>*optional*|The initial index from which to return the results.|integer|
|**Query**|**radio_version**  <br>*optional*||string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**200**|[Response 200](#hiccup_api_v1_devices_heartbeats_list-response-200)|

<a name="hiccup_api_v1_devices_heartbeats_list-response-200"></a>
**Response 200**

|Name|Description|Schema|
|---|---|---|
|**count**  <br>*required*|**Example** : `0`|integer|
|**next**  <br>*optional*|**Example** : `"string"`|string (uri)|
|**previous**  <br>*optional*|**Example** : `"string"`|string (uri)|
|**results**  <br>*required*|**Example** : `[ "[heartbeat](#heartbeat)" ]`|< [HeartBeat](#heartbeat) > array|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/heartbeats/
```


#### Example HTTP response

##### Response 200
```json
"object"
```


<a name="hiccup_api_v1_devices_heartbeats_read"></a>
### GET /hiccup/api/v1/devices/{uuid}/heartbeats/{device_local_id}/

#### Description
Get a heartbeat


#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**device_local_id**  <br>*required*|integer|
|**Path**|**uuid**  <br>*required*|string|


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**200**||[HeartBeat](#heartbeat)|
|**404**|Not found.|No Content|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/heartbeats/0/
```


#### Example HTTP response

##### Response 200
```json
{
  "id" : "string",
  "uuid" : "string",
  "device_local_id" : 0,
  "date" : "string",
  "app_version" : 0,
  "uptime" : "string",
  "build_fingerprint" : "string",
  "radio_version" : "string",
  "created_at" : "string"
}
```


<a name="hiccup_api_v1_devices_heartbeats_update"></a>
### PUT /hiccup/api/v1/devices/{uuid}/heartbeats/{device_local_id}/

#### Description
Update a heartbeat


#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**device_local_id**  <br>*required*|integer|
|**Path**|**uuid**  <br>*required*|string|


#### Body parameter
*Name* : data  
*Flags* : required  
*Type* : [HeartBeat](#heartbeat)


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**200**||[HeartBeat](#heartbeat)|
|**400**|Invalid input.|No Content|
|**404**|Not found.|No Content|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/heartbeats/0/
```


##### Request body
```json
{
  "id" : "string",
  "uuid" : "string",
  "device_local_id" : 0,
  "date" : "string",
  "app_version" : 0,
  "uptime" : "string",
  "build_fingerprint" : "string",
  "radio_version" : "string",
  "created_at" : "string"
}
```


#### Example HTTP response

##### Response 200
```json
{
  "id" : "string",
  "uuid" : "string",
  "device_local_id" : 0,
  "date" : "string",
  "app_version" : 0,
  "uptime" : "string",
  "build_fingerprint" : "string",
  "radio_version" : "string",
  "created_at" : "string"
}
```


<a name="hiccup_api_v1_devices_heartbeats_delete"></a>
### DELETE /hiccup/api/v1/devices/{uuid}/heartbeats/{device_local_id}/

#### Description
Delete a heartbeat


#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**device_local_id**  <br>*required*|integer|
|**Path**|**uuid**  <br>*required*|string|


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**204**||No Content|
|**404**|Not found.|No Content|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/heartbeats/0/
```


<a name="hiccup_api_v1_devices_heartbeats_partial_update"></a>
### PATCH /hiccup/api/v1/devices/{uuid}/heartbeats/{device_local_id}/

#### Description
Partially update a heartbeat


#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**device_local_id**  <br>*required*|integer|
|**Path**|**uuid**  <br>*required*|string|


#### Body parameter
*Name* : data  
*Flags* : required  
*Type* : [HeartBeat](#heartbeat)


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**200**||[HeartBeat](#heartbeat)|
|**400**|Invalid input.|No Content|
|**404**|Not found.|No Content|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/devices/string/heartbeats/0/
```


##### Request body
```json
{
  "id" : "string",
  "uuid" : "string",
  "device_local_id" : 0,
  "date" : "string",
  "app_version" : 0,
  "uptime" : "string",
  "build_fingerprint" : "string",
  "radio_version" : "string",
  "created_at" : "string"
}
```


#### Example HTTP response

##### Response 200
```json
{
  "id" : "string",
  "uuid" : "string",
  "device_local_id" : 0,
  "date" : "string",
  "app_version" : 0,
  "uptime" : "string",
  "build_fingerprint" : "string",
  "radio_version" : "string",
  "created_at" : "string"
}
```


<a name="hiccup_api_v1_heartbeats_create"></a>
### POST /hiccup/api/v1/heartbeats/

#### Description
Create a heartbeat


#### Body parameter
*Name* : data  
*Flags* : required  
*Type* : [HeartBeat](#heartbeat)


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**201**||[HeartBeat](#heartbeat)|
|**400**|Invalid input.|No Content|
|**404**|No device with the given uuid could be found.|No Content|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/heartbeats/
```


##### Request body
```json
{
  "id" : "string",
  "uuid" : "string",
  "device_local_id" : 0,
  "date" : "string",
  "app_version" : 0,
  "uptime" : "string",
  "build_fingerprint" : "string",
  "radio_version" : "string",
  "created_at" : "string"
}
```


#### Example HTTP response

##### Response 201
```json
{
  "id" : "string",
  "uuid" : "string",
  "device_local_id" : 0,
  "date" : "string",
  "app_version" : 0,
  "uptime" : "string",
  "build_fingerprint" : "string",
  "radio_version" : "string",
  "created_at" : "string"
}
```


<a name="hiccup_api_v1_heartbeats_list"></a>
### GET /hiccup/api/v1/heartbeats/

#### Description
List heartbeats


#### Parameters

|Type|Name|Description|Schema|
|---|---|---|---|
|**Query**|**build_fingerprint**  <br>*optional*||string|
|**Query**|**device**  <br>*optional*||string|
|**Query**|**limit**  <br>*optional*|Number of results to return per page.|integer|
|**Query**|**offset**  <br>*optional*|The initial index from which to return the results.|integer|
|**Query**|**radio_version**  <br>*optional*||string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**200**|[Response 200](#hiccup_api_v1_heartbeats_list-response-200)|

<a name="hiccup_api_v1_heartbeats_list-response-200"></a>
**Response 200**

|Name|Description|Schema|
|---|---|---|
|**count**  <br>*required*|**Example** : `0`|integer|
|**next**  <br>*optional*|**Example** : `"string"`|string (uri)|
|**previous**  <br>*optional*|**Example** : `"string"`|string (uri)|
|**results**  <br>*required*|**Example** : `[ "[heartbeat](#heartbeat)" ]`|< [HeartBeat](#heartbeat) > array|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/heartbeats/
```


#### Example HTTP response

##### Response 200
```json
"object"
```


<a name="hiccup_api_v1_heartbeats_read"></a>
### GET /hiccup/api/v1/heartbeats/{id}/

#### Description
Get a heartbeat


#### Parameters

|Type|Name|Description|Schema|
|---|---|---|---|
|**Path**|**id**  <br>*required*|A unique integer value identifying this heart beat.|integer|


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**200**||[HeartBeat](#heartbeat)|
|**404**|Not found.|No Content|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/heartbeats/0/
```


#### Example HTTP response

##### Response 200
```json
{
  "id" : "string",
  "uuid" : "string",
  "device_local_id" : 0,
  "date" : "string",
  "app_version" : 0,
  "uptime" : "string",
  "build_fingerprint" : "string",
  "radio_version" : "string",
  "created_at" : "string"
}
```


<a name="hiccup_api_v1_heartbeats_update"></a>
### PUT /hiccup/api/v1/heartbeats/{id}/

#### Description
Update a heartbeat


#### Parameters

|Type|Name|Description|Schema|
|---|---|---|---|
|**Path**|**id**  <br>*required*|A unique integer value identifying this heart beat.|integer|


#### Body parameter
*Name* : data  
*Flags* : required  
*Type* : [HeartBeat](#heartbeat)


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**200**||[HeartBeat](#heartbeat)|
|**400**|Invalid input.|No Content|
|**404**|Not found.|No Content|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/heartbeats/0/
```


##### Request body
```json
{
  "id" : "string",
  "uuid" : "string",
  "device_local_id" : 0,
  "date" : "string",
  "app_version" : 0,
  "uptime" : "string",
  "build_fingerprint" : "string",
  "radio_version" : "string",
  "created_at" : "string"
}
```


#### Example HTTP response

##### Response 200
```json
{
  "id" : "string",
  "uuid" : "string",
  "device_local_id" : 0,
  "date" : "string",
  "app_version" : 0,
  "uptime" : "string",
  "build_fingerprint" : "string",
  "radio_version" : "string",
  "created_at" : "string"
}
```


<a name="hiccup_api_v1_heartbeats_delete"></a>
### DELETE /hiccup/api/v1/heartbeats/{id}/

#### Description
Delete a heartbeat


#### Parameters

|Type|Name|Description|Schema|
|---|---|---|---|
|**Path**|**id**  <br>*required*|A unique integer value identifying this heart beat.|integer|


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**204**||No Content|
|**404**|Not found.|No Content|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/heartbeats/0/
```


<a name="hiccup_api_v1_heartbeats_partial_update"></a>
### PATCH /hiccup/api/v1/heartbeats/{id}/

#### Description
Partially update a heartbeat


#### Parameters

|Type|Name|Description|Schema|
|---|---|---|---|
|**Path**|**id**  <br>*required*|A unique integer value identifying this heart beat.|integer|


#### Body parameter
*Name* : data  
*Flags* : required  
*Type* : [HeartBeat](#heartbeat)


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**200**||[HeartBeat](#heartbeat)|
|**400**|Invalid input.|No Content|
|**404**|Not found.|No Content|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/heartbeats/0/
```


##### Request body
```json
{
  "id" : "string",
  "uuid" : "string",
  "device_local_id" : 0,
  "date" : "string",
  "app_version" : 0,
  "uptime" : "string",
  "build_fingerprint" : "string",
  "radio_version" : "string",
  "created_at" : "string"
}
```


#### Example HTTP response

##### Response 200
```json
{
  "id" : "string",
  "uuid" : "string",
  "device_local_id" : 0,
  "date" : "string",
  "app_version" : 0,
  "uptime" : "string",
  "build_fingerprint" : "string",
  "radio_version" : "string",
  "created_at" : "string"
}
```


<a name="hiccup_api_v1_logfiles_list"></a>
### GET /hiccup/api/v1/logfiles/

#### Description
List log files


#### Parameters

|Type|Name|Description|Schema|
|---|---|---|---|
|**Query**|**limit**  <br>*optional*|Number of results to return per page.|integer|
|**Query**|**offset**  <br>*optional*|The initial index from which to return the results.|integer|


#### Responses

|HTTP Code|Schema|
|---|---|
|**200**|[Response 200](#hiccup_api_v1_logfiles_list-response-200)|

<a name="hiccup_api_v1_logfiles_list-response-200"></a>
**Response 200**

|Name|Description|Schema|
|---|---|---|
|**count**  <br>*required*|**Example** : `0`|integer|
|**next**  <br>*optional*|**Example** : `"string"`|string (uri)|
|**previous**  <br>*optional*|**Example** : `"string"`|string (uri)|
|**results**  <br>*required*|**Example** : `[ "[logfile](#logfile)" ]`|< [LogFile](#logfile) > array|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/logfiles/
```


#### Example HTTP response

##### Response 200
```json
"object"
```


<a name="hiccup_api_v1_logfiles_read"></a>
### GET /hiccup/api/v1/logfiles/{id}/

#### Description
Get a log file


#### Parameters

|Type|Name|Description|Schema|
|---|---|---|---|
|**Path**|**id**  <br>*required*|A unique integer value identifying this log file.|integer|


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**200**||[LogFile](#logfile)|
|**404**|Not found.|No Content|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/logfiles/0/
```


#### Example HTTP response

##### Response 200
```json
{
  "id" : 0,
  "logfile_type" : "string",
  "logfile" : "string",
  "crashreport_local_id" : 0,
  "created_at" : "string",
  "crashreport" : 0
}
```


<a name="hiccup_api_v1_logfiles_update"></a>
### PUT /hiccup/api/v1/logfiles/{id}/

#### Description
Update a log file


#### Parameters

|Type|Name|Description|Schema|
|---|---|---|---|
|**Path**|**id**  <br>*required*|A unique integer value identifying this log file.|integer|


#### Body parameter
*Name* : data  
*Flags* : required  
*Type* : [LogFile](#logfile)


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**200**||[LogFile](#logfile)|
|**400**|Invalid input.|No Content|
|**404**|Not found.|No Content|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/logfiles/0/
```


##### Request body
```json
{
  "id" : 0,
  "logfile_type" : "string",
  "logfile" : "string",
  "crashreport_local_id" : 0,
  "created_at" : "string",
  "crashreport" : 0
}
```


#### Example HTTP response

##### Response 200
```json
{
  "id" : 0,
  "logfile_type" : "string",
  "logfile" : "string",
  "crashreport_local_id" : 0,
  "created_at" : "string",
  "crashreport" : 0
}
```


<a name="hiccup_api_v1_logfiles_delete"></a>
### DELETE /hiccup/api/v1/logfiles/{id}/

#### Description
Delete a log file


#### Parameters

|Type|Name|Description|Schema|
|---|---|---|---|
|**Path**|**id**  <br>*required*|A unique integer value identifying this log file.|integer|


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**204**||No Content|
|**404**|Not found.|No Content|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/logfiles/0/
```


<a name="hiccup_api_v1_logfiles_partial_update"></a>
### PATCH /hiccup/api/v1/logfiles/{id}/

#### Description
Partially update a log file


#### Parameters

|Type|Name|Description|Schema|
|---|---|---|---|
|**Path**|**id**  <br>*required*|A unique integer value identifying this log file.|integer|


#### Body parameter
*Name* : data  
*Flags* : required  
*Type* : [LogFile](#logfile)


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**200**||[LogFile](#logfile)|
|**400**|Invalid input.|No Content|
|**404**|Not found.|No Content|


#### Tags

* hiccup


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup/api/v1/logfiles/0/
```


##### Request body
```json
{
  "id" : 0,
  "logfile_type" : "string",
  "logfile" : "string",
  "crashreport_local_id" : 0,
  "created_at" : "string",
  "crashreport" : 0
}
```


#### Example HTTP response

##### Response 200
```json
{
  "id" : 0,
  "logfile_type" : "string",
  "logfile" : "string",
  "crashreport_local_id" : 0,
  "created_at" : "string",
  "crashreport" : 0
}
```


<a name="hiccup_stats_api_v1_device_overview_read"></a>
### GET /hiccup_stats/api/v1/device_overview/{uuid}/

#### Description
Get some general statistics for a device.


#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**uuid**  <br>*required*|string|


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**200**|OK|[DeviceStatOverview](#devicestatoverview)|
|**404**|Not found.|No Content|

<a name="devicestatoverview"></a>
**DeviceStatOverview**

|Name|Description|Schema|
|---|---|---|
|**board_date**  <br>*optional*|**Example** : `"string"`|string|
|**crashes_per_day**  <br>*optional*|**Example** : `0.0`|number|
|**crashreports**  <br>*optional*|**Example** : `0`|integer|
|**heartbeats**  <br>*optional*|**Example** : `0`|integer|
|**last_active**  <br>*optional*|**Example** : `"string"`|string|
|**smpl_per_day**  <br>*optional*|**Example** : `0.0`|number|
|**smpls**  <br>*optional*|**Example** : `0`|integer|
|**uuid**  <br>*optional*|**Example** : `"string"`|string|


#### Tags

* hiccup_stats


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup_stats/api/v1/device_overview/string/
```


#### Example HTTP response

##### Response 200
```json
"object"
```


<a name="hiccup_stats_api_v1_device_report_history_read"></a>
### GET /hiccup_stats/api/v1/device_report_history/{uuid}/

#### Description
Get the report history of a device


#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**uuid**  <br>*required*|string|


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**200**|OK|< [DeviceReportHistoryEntry](#devicereporthistoryentry) > array|
|**404**|Not found.|No Content|

<a name="devicereporthistoryentry"></a>
**DeviceReportHistoryEntry**

|Name|Description|Schema|
|---|---|---|
|**date**  <br>*optional*|**Example** : `"string"`|string|
|**heartbeats**  <br>*optional*|**Example** : `0`|integer|
|**other**  <br>*optional*|**Example** : `0`|integer|
|**prob_crashes**  <br>*optional*|**Example** : `0`|integer|
|**smpl**  <br>*optional*|**Example** : `0`|integer|


#### Tags

* hiccup_stats


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup_stats/api/v1/device_report_history/string/
```


#### Example HTTP response

##### Response 200
```json
[ "object" ]
```


<a name="hiccup_stats_api_v1_device_update_history_read"></a>
### GET /hiccup_stats/api/v1/device_update_history/{uuid}/

#### Description
Get the update history of a device


#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**uuid**  <br>*required*|string|


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**200**|OK|< [DeviceUpdateHistoryEntry](#deviceupdatehistoryentry) > array|
|**404**|Not found.|No Content|

<a name="deviceupdatehistoryentry"></a>
**DeviceUpdateHistoryEntry**

|Name|Description|Schema|
|---|---|---|
|**build_fingerprint**  <br>*optional*|**Example** : `"string"`|string|
|**heartbeats**  <br>*optional*|**Example** : `0`|integer|
|**max**  <br>*optional*|**Example** : `0`|integer|
|**other**  <br>*optional*|**Example** : `0`|integer|
|**prob_crashes**  <br>*optional*|**Example** : `0`|integer|
|**smpl**  <br>*optional*|**Example** : `0`|integer|
|**update_date**  <br>*optional*|**Example** : `"string"`|string|


#### Tags

* hiccup_stats


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup_stats/api/v1/device_update_history/string/
```


#### Example HTTP response

##### Response 200
```json
[ "object" ]
```


<a name="hiccup_stats_api_v1_logfile_download_read"></a>
### GET /hiccup_stats/api/v1/logfile_download/{id}/

#### Description
Get a log file.


#### Parameters

|Type|Name|Schema|
|---|---|---|
|**Path**|**id**  <br>*required*|string|


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**200**|OK|file|
|**404**|Not found.|No Content|


#### Tags

* hiccup_stats


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|
|**apiKey**|**[Device token authentication](#device-token-authentication)**|


#### Example HTTP request

##### Request path
```
/hiccup_stats/api/v1/logfile_download/string/
```


#### Example HTTP response

##### Response 200
```json
"file"
```


<a name="hiccup_stats_api_v1_radio_version_daily_list"></a>
### GET /hiccup_stats/api/v1/radio_version_daily/

#### Description
View for listing RadioVersionDaily instances.


#### Parameters

|Type|Name|Description|Schema|
|---|---|---|---|
|**Query**|**date**  <br>*optional*||string|
|**Query**|**date_end**  <br>*optional*||string|
|**Query**|**date_start**  <br>*optional*||string|
|**Query**|**heartbeats**  <br>*optional*||number|
|**Query**|**limit**  <br>*optional*|Number of results to return per page.|integer|
|**Query**|**offset**  <br>*optional*|The initial index from which to return the results.|integer|
|**Query**|**other**  <br>*optional*||number|
|**Query**|**prob_crashes**  <br>*optional*||number|
|**Query**|**smpl**  <br>*optional*||number|
|**Query**|**version**  <br>*optional*||string|
|**Query**|**version__is_beta_release**  <br>*optional*||string|
|**Query**|**version__is_official_release**  <br>*optional*||string|
|**Query**|**version__radio_version**  <br>*optional*||string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**200**|[Response 200](#hiccup_stats_api_v1_radio_version_daily_list-response-200)|

<a name="hiccup_stats_api_v1_radio_version_daily_list-response-200"></a>
**Response 200**

|Name|Description|Schema|
|---|---|---|
|**count**  <br>*required*|**Example** : `0`|integer|
|**next**  <br>*optional*|**Example** : `"string"`|string (uri)|
|**previous**  <br>*optional*|**Example** : `"string"`|string (uri)|
|**results**  <br>*required*|**Example** : `[ "[radioversiondaily](#radioversiondaily)" ]`|< [RadioVersionDaily](#radioversiondaily) > array|


#### Tags

* hiccup_stats


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|


#### Example HTTP request

##### Request path
```
/hiccup_stats/api/v1/radio_version_daily/
```


#### Example HTTP response

##### Response 200
```json
"object"
```


<a name="hiccup_stats_api_v1_radio_versions_list"></a>
### GET /hiccup_stats/api/v1/radio_versions/

#### Description
View for listing RadioVersion instances.


#### Parameters

|Type|Name|Description|Schema|
|---|---|---|---|
|**Query**|**first_seen_after**  <br>*optional*||string|
|**Query**|**first_seen_before**  <br>*optional*||string|
|**Query**|**first_seen_on**  <br>*optional*||string|
|**Query**|**heartbeats**  <br>*optional*||number|
|**Query**|**is_beta_release**  <br>*optional*||string|
|**Query**|**is_official_release**  <br>*optional*||string|
|**Query**|**limit**  <br>*optional*|Number of results to return per page.|integer|
|**Query**|**offset**  <br>*optional*|The initial index from which to return the results.|integer|
|**Query**|**other**  <br>*optional*||number|
|**Query**|**prob_crashes**  <br>*optional*||number|
|**Query**|**radio_version**  <br>*optional*||string|
|**Query**|**released_after**  <br>*optional*||string|
|**Query**|**released_before**  <br>*optional*||string|
|**Query**|**released_on**  <br>*optional*||string|
|**Query**|**smpl**  <br>*optional*||number|


#### Responses

|HTTP Code|Schema|
|---|---|
|**200**|[Response 200](#hiccup_stats_api_v1_radio_versions_list-response-200)|

<a name="hiccup_stats_api_v1_radio_versions_list-response-200"></a>
**Response 200**

|Name|Description|Schema|
|---|---|---|
|**count**  <br>*required*|**Example** : `0`|integer|
|**next**  <br>*optional*|**Example** : `"string"`|string (uri)|
|**previous**  <br>*optional*|**Example** : `"string"`|string (uri)|
|**results**  <br>*required*|**Example** : `[ "[radioversion](#radioversion)" ]`|< [RadioVersion](#radioversion) > array|


#### Tags

* hiccup_stats


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|


#### Example HTTP request

##### Request path
```
/hiccup_stats/api/v1/radio_versions/
```


#### Example HTTP response

##### Response 200
```json
"object"
```


<a name="hiccup_stats_api_v1_status_list"></a>
### GET /hiccup_stats/api/v1/status/

#### Description
Get the number of devices, crashreports and heartbeats


#### Responses

|HTTP Code|Description|Schema|
|---|---|---|
|**200**|OK|[Status](#status)|

<a name="status"></a>
**Status**

|Name|Description|Schema|
|---|---|---|
|**crashreports**  <br>*optional*|**Example** : `0`|integer|
|**devices**  <br>*optional*|**Example** : `0`|integer|
|**heartbeats**  <br>*optional*|**Example** : `0`|integer|


#### Tags

* hiccup_stats


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|


#### Example HTTP request

##### Request path
```
/hiccup_stats/api/v1/status/
```


#### Example HTTP response

##### Response 200
```json
"object"
```


<a name="hiccup_stats_api_v1_version_daily_list"></a>
### GET /hiccup_stats/api/v1/version_daily/

#### Description
View for listing VersionDaily instances.


#### Parameters

|Type|Name|Description|Schema|
|---|---|---|---|
|**Query**|**date**  <br>*optional*||string|
|**Query**|**date_end**  <br>*optional*||string|
|**Query**|**date_start**  <br>*optional*||string|
|**Query**|**heartbeats**  <br>*optional*||number|
|**Query**|**limit**  <br>*optional*|Number of results to return per page.|integer|
|**Query**|**offset**  <br>*optional*|The initial index from which to return the results.|integer|
|**Query**|**other**  <br>*optional*||number|
|**Query**|**prob_crashes**  <br>*optional*||number|
|**Query**|**smpl**  <br>*optional*||number|
|**Query**|**version**  <br>*optional*||string|
|**Query**|**version__build_fingerprint**  <br>*optional*||string|
|**Query**|**version__is_beta_release**  <br>*optional*||string|
|**Query**|**version__is_official_release**  <br>*optional*||string|


#### Responses

|HTTP Code|Schema|
|---|---|
|**200**|[Response 200](#hiccup_stats_api_v1_version_daily_list-response-200)|

<a name="hiccup_stats_api_v1_version_daily_list-response-200"></a>
**Response 200**

|Name|Description|Schema|
|---|---|---|
|**count**  <br>*required*|**Example** : `0`|integer|
|**next**  <br>*optional*|**Example** : `"string"`|string (uri)|
|**previous**  <br>*optional*|**Example** : `"string"`|string (uri)|
|**results**  <br>*required*|**Example** : `[ "[versiondaily](#versiondaily)" ]`|< [VersionDaily](#versiondaily) > array|


#### Tags

* hiccup_stats


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|


#### Example HTTP request

##### Request path
```
/hiccup_stats/api/v1/version_daily/
```


#### Example HTTP response

##### Response 200
```json
"object"
```


<a name="hiccup_stats_api_v1_versions_list"></a>
### GET /hiccup_stats/api/v1/versions/

#### Description
View for listing versions.


#### Parameters

|Type|Name|Description|Schema|
|---|---|---|---|
|**Query**|**build_fingerprint**  <br>*optional*||string|
|**Query**|**first_seen_after**  <br>*optional*||string|
|**Query**|**first_seen_before**  <br>*optional*||string|
|**Query**|**first_seen_on**  <br>*optional*||string|
|**Query**|**heartbeats**  <br>*optional*||number|
|**Query**|**is_beta_release**  <br>*optional*||string|
|**Query**|**is_official_release**  <br>*optional*||string|
|**Query**|**limit**  <br>*optional*|Number of results to return per page.|integer|
|**Query**|**offset**  <br>*optional*|The initial index from which to return the results.|integer|
|**Query**|**other**  <br>*optional*||number|
|**Query**|**prob_crashes**  <br>*optional*||number|
|**Query**|**released_after**  <br>*optional*||string|
|**Query**|**released_before**  <br>*optional*||string|
|**Query**|**released_on**  <br>*optional*||string|
|**Query**|**smpl**  <br>*optional*||number|


#### Responses

|HTTP Code|Schema|
|---|---|
|**200**|[Response 200](#hiccup_stats_api_v1_versions_list-response-200)|

<a name="hiccup_stats_api_v1_versions_list-response-200"></a>
**Response 200**

|Name|Description|Schema|
|---|---|---|
|**count**  <br>*required*|**Example** : `0`|integer|
|**next**  <br>*optional*|**Example** : `"string"`|string (uri)|
|**previous**  <br>*optional*|**Example** : `"string"`|string (uri)|
|**results**  <br>*required*|**Example** : `[ "[version](#version)" ]`|< [Version](#version) > array|


#### Tags

* hiccup_stats


#### Security

|Type|Name|
|---|---|
|**oauth2**|**[Google OAuth](#google-oauth)**|


#### Example HTTP request

##### Request path
```
/hiccup_stats/api/v1/versions/
```


#### Example HTTP response

##### Response 200
```json
"object"
```




<a name="definitions"></a>
## Definitions

<a name="crashreport"></a>
### CrashReport

|Name|Description|Schema|
|---|---|---|
|**app_version**  <br>*required*|**Minimum value** : `-2147483648`  <br>**Maximum value** : `2147483647`  <br>**Example** : `0`|integer|
|**boot_reason**  <br>*required*|**Length** : `1 - 200`  <br>**Example** : `"string"`|string|
|**build_fingerprint**  <br>*required*|**Length** : `1 - 200`  <br>**Example** : `"string"`|string|
|**created_at**  <br>*optional*  <br>*read-only*|**Example** : `"string"`|string (date-time)|
|**date**  <br>*required*|**Example** : `"string"`|string (date-time)|
|**device_local_id**  <br>*optional*|**Example** : `0`|integer|
|**id**  <br>*optional*  <br>*read-only*|**Example** : `"string"`|string|
|**is_fake_report**  <br>*optional*|**Example** : `true`|boolean|
|**logfiles**  <br>*optional*  <br>*read-only*|**Example** : `[ "string" ]`|< string (uri) > array|
|**next_logfile_key**  <br>*optional*|**Minimum value** : `0`  <br>**Maximum value** : `2147483647`  <br>**Example** : `0`|integer|
|**power_off_reason**  <br>*required*|**Length** : `1 - 200`  <br>**Example** : `"string"`|string|
|**power_on_reason**  <br>*required*|**Length** : `1 - 200`  <br>**Example** : `"string"`|string|
|**radio_version**  <br>*optional*|**Length** : `1 - 200`  <br>**Example** : `"string"`|string|
|**uptime**  <br>*required*|**Length** : `1 - 200`  <br>**Example** : `"string"`|string|
|**uuid**  <br>*required*|**Length** : `1 - 64`  <br>**Example** : `"string"`|string|


<a name="createcrashreportresponseschema"></a>
### CreateCrashreportResponseSchema

|Name|Description|Schema|
|---|---|---|
|**device_local_id**  <br>*optional*|**Example** : `0`|integer|


<a name="device"></a>
### Device

|Name|Description|Schema|
|---|---|---|
|**board_date**  <br>*required*|**Example** : `"string"`|string (date-time)|
|**chipset**  <br>*optional*|**Maximal length** : `200`  <br>**Example** : `"string"`|string|
|**id**  <br>*optional*  <br>*read-only*|**Example** : `0`|integer|
|**imei**  <br>*optional*|**Maximal length** : `32`  <br>**Example** : `"string"`|string|
|**last_heartbeat**  <br>*required*|**Example** : `"string"`|string (date-time)|
|**next_per_crashreport_key**  <br>*optional*|**Minimum value** : `0`  <br>**Maximum value** : `2147483647`  <br>**Example** : `0`|integer|
|**next_per_heartbeat_key**  <br>*optional*|**Minimum value** : `0`  <br>**Maximum value** : `2147483647`  <br>**Example** : `0`|integer|
|**token**  <br>*optional*|**Maximal length** : `200`  <br>**Example** : `"string"`|string|
|**user**  <br>*required*|**Example** : `0`|integer|
|**uuid**  <br>*optional*  <br>*read-only*|**Minimum length** : `1`  <br>**Example** : `"string"`|string|


<a name="devicecreate"></a>
### DeviceCreate

|Name|Description|Schema|
|---|---|---|
|**board_date**  <br>*required*|**Example** : `"string"`|string (date-time)|
|**chipset**  <br>*required*|**Maximal length** : `200`  <br>**Example** : `"string"`|string|


<a name="deviceregisterresponseschema"></a>
### DeviceRegisterResponseSchema

|Name|Description|Schema|
|---|---|---|
|**token**  <br>*optional*|**Maximal length** : `200`  <br>**Example** : `"string"`|string|
|**uuid**  <br>*optional*  <br>*read-only*|**Minimum length** : `1`  <br>**Example** : `"string"`|string|


<a name="heartbeat"></a>
### HeartBeat

|Name|Description|Schema|
|---|---|---|
|**app_version**  <br>*required*|**Minimum value** : `-2147483648`  <br>**Maximum value** : `2147483647`  <br>**Example** : `0`|integer|
|**build_fingerprint**  <br>*required*|**Length** : `1 - 200`  <br>**Example** : `"string"`|string|
|**created_at**  <br>*optional*  <br>*read-only*|**Example** : `"string"`|string (date-time)|
|**date**  <br>*required*|**Example** : `"string"`|string (date-time)|
|**device_local_id**  <br>*optional*|**Example** : `0`|integer|
|**id**  <br>*optional*  <br>*read-only*|**Example** : `"string"`|string|
|**radio_version**  <br>*optional*|**Length** : `1 - 200`  <br>**Example** : `"string"`|string|
|**uptime**  <br>*required*|**Length** : `1 - 200`  <br>**Example** : `"string"`|string|
|**uuid**  <br>*required*|**Length** : `1 - 64`  <br>**Example** : `"string"`|string|


<a name="logfile"></a>
### LogFile

|Name|Description|Schema|
|---|---|---|
|**crashreport**  <br>*required*|**Example** : `0`|integer|
|**crashreport_local_id**  <br>*optional*|**Minimum value** : `0`  <br>**Maximum value** : `2147483647`  <br>**Example** : `0`|integer|
|**created_at**  <br>*optional*  <br>*read-only*|**Example** : `"string"`|string (date-time)|
|**id**  <br>*optional*  <br>*read-only*|**Example** : `0`|integer|
|**logfile**  <br>*optional*  <br>*read-only*|**Example** : `"string"`|string (uri)|
|**logfile_type**  <br>*optional*|**Length** : `1 - 36`  <br>**Example** : `"string"`|string|


<a name="radioversion"></a>
### RadioVersion

|Name|Description|Schema|
|---|---|---|
|**first_seen_on**  <br>*required*|**Example** : `"string"`|string (date)|
|**heartbeats**  <br>*optional*|**Minimum value** : `-2147483648`  <br>**Maximum value** : `2147483647`  <br>**Example** : `0`|integer|
|**id**  <br>*optional*  <br>*read-only*|**Example** : `0`|integer|
|**is_beta_release**  <br>*optional*|**Example** : `true`|boolean|
|**is_official_release**  <br>*optional*|**Example** : `true`|boolean|
|**other**  <br>*optional*|**Minimum value** : `-2147483648`  <br>**Maximum value** : `2147483647`  <br>**Example** : `0`|integer|
|**prob_crashes**  <br>*optional*|**Minimum value** : `-2147483648`  <br>**Maximum value** : `2147483647`  <br>**Example** : `0`|integer|
|**radio_version**  <br>*required*|**Length** : `1 - 200`  <br>**Example** : `"string"`|string|
|**released_on**  <br>*required*|**Example** : `"string"`|string (date)|
|**smpl**  <br>*optional*|**Minimum value** : `-2147483648`  <br>**Maximum value** : `2147483647`  <br>**Example** : `0`|integer|


<a name="radioversiondaily"></a>
### RadioVersionDaily

|Name|Description|Schema|
|---|---|---|
|**date**  <br>*required*|**Example** : `"string"`|string (date)|
|**heartbeats**  <br>*optional*|**Minimum value** : `-2147483648`  <br>**Maximum value** : `2147483647`  <br>**Example** : `0`|integer|
|**id**  <br>*optional*  <br>*read-only*|**Example** : `0`|integer|
|**other**  <br>*optional*|**Minimum value** : `-2147483648`  <br>**Maximum value** : `2147483647`  <br>**Example** : `0`|integer|
|**prob_crashes**  <br>*optional*|**Minimum value** : `-2147483648`  <br>**Maximum value** : `2147483647`  <br>**Example** : `0`|integer|
|**radio_version**  <br>*required*|**Minimum length** : `1`  <br>**Example** : `"string"`|string|
|**smpl**  <br>*optional*|**Minimum value** : `-2147483648`  <br>**Maximum value** : `2147483647`  <br>**Example** : `0`|integer|
|**version**  <br>*required*|**Example** : `0`|integer|


<a name="version"></a>
### Version

|Name|Description|Schema|
|---|---|---|
|**build_fingerprint**  <br>*required*|**Length** : `1 - 200`  <br>**Example** : `"string"`|string|
|**first_seen_on**  <br>*required*|**Example** : `"string"`|string (date)|
|**heartbeats**  <br>*optional*|**Minimum value** : `-2147483648`  <br>**Maximum value** : `2147483647`  <br>**Example** : `0`|integer|
|**id**  <br>*optional*  <br>*read-only*|**Example** : `0`|integer|
|**is_beta_release**  <br>*optional*|**Example** : `true`|boolean|
|**is_official_release**  <br>*optional*|**Example** : `true`|boolean|
|**other**  <br>*optional*|**Minimum value** : `-2147483648`  <br>**Maximum value** : `2147483647`  <br>**Example** : `0`|integer|
|**prob_crashes**  <br>*optional*|**Minimum value** : `-2147483648`  <br>**Maximum value** : `2147483647`  <br>**Example** : `0`|integer|
|**released_on**  <br>*required*|**Example** : `"string"`|string (date)|
|**smpl**  <br>*optional*|**Minimum value** : `-2147483648`  <br>**Maximum value** : `2147483647`  <br>**Example** : `0`|integer|


<a name="versiondaily"></a>
### VersionDaily

|Name|Description|Schema|
|---|---|---|
|**build_fingerprint**  <br>*required*|**Minimum length** : `1`  <br>**Example** : `"string"`|string|
|**date**  <br>*required*|**Example** : `"string"`|string (date)|
|**heartbeats**  <br>*optional*|**Minimum value** : `-2147483648`  <br>**Maximum value** : `2147483647`  <br>**Example** : `0`|integer|
|**id**  <br>*optional*  <br>*read-only*|**Example** : `0`|integer|
|**other**  <br>*optional*|**Minimum value** : `-2147483648`  <br>**Maximum value** : `2147483647`  <br>**Example** : `0`|integer|
|**prob_crashes**  <br>*optional*|**Minimum value** : `-2147483648`  <br>**Maximum value** : `2147483647`  <br>**Example** : `0`|integer|
|**smpl**  <br>*optional*|**Minimum value** : `-2147483648`  <br>**Maximum value** : `2147483647`  <br>**Example** : `0`|integer|
|**version**  <br>*required*|**Example** : `0`|integer|




<a name="securityscheme"></a>
## Security

<a name="device-token-authentication"></a>
### Device token authentication
Authenticate using a token that was returned on successful registration of a new device. The token can only be used to authenticate requests that target the device with the matching UUID. The token has to be put in the request header: 'Authorization: Token <AUTH_TOKEN>'

*Type* : apiKey  
*Name* : Authorization  
*In* : HEADER


<a name="google-oauth"></a>
### Google OAuth
Authenticate using a Google account. Only E-mail addresses in the @fairphone.com domain are allowed.

*Type* : oauth2  
*Flow* : implicit  
*Token URL* : /accounts/google/login/callback/



