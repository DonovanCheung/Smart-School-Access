# Audit Log Management

    GET att_case_hacks/emergency

## Description
Set or reset emergency situation

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

    GET att_case_hacks/emergency
    
**Body**
    
    lock=True
    
**Return**
``` json
{
    "response": null,
    "error": [],
    "success": true
}
```
