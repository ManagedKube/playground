# Aqara Water Leak Sensor

## The idea
The idea is to not have to use IFTTT and if not, then what can we do?

We can use the Aqara developer's portal and hit the Aqara API directly.  Their API has a push (to a queue or http endpoint) and
it also has a RESTful api to get the device status.  

Using Github Actions, we can either setup a thing to continuously query the RESTful interface or setup a thing to subscribe
and listen to the queue (probably the better and nicer way).  Once something interesting happens like a water leak status, it
can call the Kasa API (there are no public APIs) to turn off the smart plug.  

## Useful links

Main developer docs:
* https://opendoc.aqara.cn/en/

Device resource list 
* Has information on what a device can return
* https://developer.aqara.com/console/equipment-resources

Error codes:
* https://opendoc.aqara.cn/en/docs/developmanual/apiIntroduction/errorCode.html

HTTP call auth:
* https://opendoc.aqara.cn/en/docs/developmanual/apiIntroduction/signGenerationRules.html

Kasa/TP-link
* https://github.com/piekstra/tplink-cloud-api - hits the Kasa cloud to control the device.  Dont have to be running locally
* https://github.com/python-kasa/python-kasa - has to run locally to control your devices

# Testing

## Get authorization verification

```
{
  "intent": "config.auth.getAuthCode",
  "data": {
    "account": "garlandk@gmail.com",
    "accountType": 0,
    "accessTokenValidity": "1h"
  }
}
```

Auth code goes to your email

Obtaion access-token call with the access code

```
{
  "code": 0,
  "requestId": "2305.17962.17089837838041313",
  "message": "Success",
  "msgDetails": null,
  "result": {
    "expiresIn": "28800",
    "openId": "318055013841211841031126020097",
    "accessToken": "bcbaf87737e3472686d54361cb8ac7b8",
    "refreshToken": "02bdd40ff0338c0dfa22d249c576be6c"
  }
}
```

## Device Management -> Query device information
This gets the list of devices information only.  Doesnt return water leak status.

```
{
  "intent": "query.device.info",
  "data": {
    "dids": [
      "lumi.158d0008797ea4",
      "lumi.158d00094d4395",
      "lumi.158d000774d0c6"
    ],
    "positionId": "",
    "pageNum": 1,
    "pageSize": 50
  }
}
```

Response:
```
{
  "code": 0,
  "requestId": "f1287336bf3c42e0b1adda209e3ab877.7757330.17089838590051137",
  "message": "Success",
  "msgDetails": null,
  "result": {
    "data": [
      {
        "parentDid": "lumi1.54ef44425bba",
        "positionId": "real2.917766513731264512",
        "createTime": 1695958236910,
        "timeZone": "GMT-08:00",
        "model": "lumi.sensor_wleak.aq1",
        "updateTime": 1695958236910,
        "modelType": 3,
        "state": 1,                         <---- state of the device on/off: Status: 0-offline 1-online

        "firmwareVersion": "0.0.0_0006",
        "deviceName": "Water Leak Sensor-tv area",
        "did": "lumi.158d0008797ea4"
      },
      {
        "parentDid": "lumi1.54ef44425bba",
        "positionId": "real2.917766513731264512",
        "createTime": 1705965205424,
        "timeZone": "GMT-08:00",
        "model": "lumi.sensor_wleak.aq1",
        "updateTime": 1705965205424,
        "modelType": 3,
        "state": 1,
        "firmwareVersion": "0.0.0_0006",
        "deviceName": "Water Leak Sensor - dining area",
        "did": "lumi.158d00094d4395"
      },
      {
        "parentDid": "lumi1.54ef44425bba",
        "positionId": "real2.917766513731264512",
        "createTime": 1705965689110,
        "timeZone": "GMT-08:00",
        "model": "lumi.sensor_wleak.aq1",
        "updateTime": 1705965689110,
        "modelType": 3,
        "state": 1,
        "firmwareVersion": "0.0.0_0006",
        "deviceName": "Water Leak - Christie room",
        "did": "lumi.158d000774d0c6"
      }
    ],
    "totalCount": 3
  }
}
```

## Device Resource Management -> Query device attribute value
Query input:
```
{
  "intent": "query.resource.value",
  "data": {
    "resources": [
      {
        "subjectId": "lumi.158d000774d0c6",
        "resourceIds": [
          "3.1.85"
        ]
      }
    ]
  }
}
```

Response:
```
{
  "code": 0,
  "requestId": "4a4b579250ac434e8310a4957917181f.7272165.17089846806972285",
  "message": "Success",
  "msgDetails": null,
  "result": [
    {
      "timeStamp": 1708984119343,
      "resourceId": "3.1.85",
      "value": "1",                         <----I put the sensor in water
      "subjectId": "lumi.158d000774d0c6"
    }
  ]
}
```

The problem with this method is that it has a complicated way of authorization.  It needs
the access code which is sent to your email/sms: https://opendoc.aqara.com/en/docs/developmanual/authManagement/aqaraauthMode.html

Kinda sucks b/c then if the token doesnt refresh in time, it will need a new access token
to be sent to the phone/email.

# Queue
They use https://github.com/apache/rocketmq-client-python.

This auth method seems more static.  When you enable the send message to the queue, it gives you all of the key info

MQ message subscription address: uspro-opdmq-broker1.aqara.com:9876
topic: 12118352361261998086cfc1
group: 12118352361261998086cfc1
accessKey: K.1211111111111111
secretKey: tfw7xxxxxxxxxx-foo


Use rockettmq ( http://rocketmq.apache.org ) as the MQ message queue, enable the acl security authentication mechanism, select the access key as the current authentication secretKey, and keyId as the current authentication accessKey. 