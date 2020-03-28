# Audit Log Management

    GET att_case_hacks/smart_access/verify

## Description
Verify if user has access to a lock

***

## Requires authentication
* Authentication not implemented yet

***

## Parameters

- **user_id** _(required)_ — User ID which will receive access.
- **lock_id** _(required)_  — Lock ID whose access will be granted to user.

***

## Return format
A JSON array.

***

## Errors
All known errors cause the resource to return a JSON array containing at least 'success' and 'error' keys describing the status and source of error.

***

## Example
**Request**

    GET att_case_hacks/smart_access/verify

**Query Parameters**
    
    user_id=U1234
    lock_id=L1234
    
**Return**
``` json
{
    "response": null,
    "error": [],
    "success": true
}
```
