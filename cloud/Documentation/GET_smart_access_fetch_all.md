# Audit Log Management

    GET att_case_hacks/smart_access/fetch_all

## Description
Fetch all users and lock access pair

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

    GET att_case_hacks/smart_access/fetch_all
    
**Return**
``` json
{
    "response": [
        {
            "granted_by": "U5678",
            "created_at": "2018-10-01 18:27",
            "lock_id": "L1234",
            "access_until": "2019-10-01 18:27",
            "user_id": "U1234",
            "modified_at": "2018-10-01 18:27"
        }
    ],
    "error": [],
    "success": true
}
```
