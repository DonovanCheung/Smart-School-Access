# Audit Log Management

    GET att_case_hacks/audit_log/fetch_all

## Description
Get list of all audit logs

***

## Requires authentication
* Authentication not implemented yet

***

## Parameters

No parameters

***

## Return format
A JSON array.

***

## Errors
All known errors cause the resource to return a JSON array containing at least 'success' and 'error' keys describing the status and source of error.

***

## Example
**Request**

    GET att_case_hacks/audit_log/fetch_all
    
**Return**
``` json
{
  "response": [
    {
        "lock_id": "lock_1",
        "created_at": "2018-10-01 18:37:49",
        "user_id": "admin",
        "action": "failed attempt to unlock lock_1 by admin",
        "modified_at": "2018-10-01 18:37:49"
    },
    {
        "lock_id": "emergency",
        "created_at": "2018-10-01 18:37:25",
        "user_id": "",
        "action": "Emergency is set to True",
        "modified_at": "2018-10-01 18:37:25"
    },
    {
        "lock_id": "lock_1",
        "created_at": "2018-10-01 18:33:56",
        "user_id": "admin",
        "action": "successful attempt to unlock lock_1 by admin",
        "modified_at": "2018-10-01 18:33:56"
    }
  ],
  "success": true,
  "error": []
}
```
