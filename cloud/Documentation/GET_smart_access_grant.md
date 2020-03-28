# Audit Log Management

    GET att_case_hacks/smart_access/grant

## Description
Grant access to a particular lock to a user

***

## Requires authentication
* Authentication not implemented yet

***

## Parameters

- **user_id** _(required)_ — User ID which will receive access.
- **lock_id** _(required)_  — Lock ID whose access will be granted to user.
- **granted_by** _(required)_ — User ID responsible for granting access (requires as authentication is not implemented yet).
- **access_time** _(optional)_ — Time in seconds for which access will be valid. (default: 1 year)

***

## Return format
A JSON array.

***

## Errors
All known errors cause the resource to return a JSON array containing at least 'success' and 'error' keys describing the status and source of error.

***

## Example
**Request**

    GET att_case_hacks/smart_access/grant
    
**Query Parameters**
    
    user_id=U1234
    lock_id=L1234
    granted_by=U5678
    access_time=600
    
**Return**
``` json
{
    "response": null,
    "error": [],
    "success": true
}
```
