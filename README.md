# FIWARE Orion × OpenWhisk

This is experiment repository to connect FIWARE Orion and OpenWhisk action.

## Why connection FIWARE Orion and OpenWhisk action

When using FIWARE Orion, notification destination business logic may be required.
We plan to make it easy to register business logic using a combination of FIWARE Orion and FaaS (Function as a Service).

---

# Create AirConditioner entity

```
curl localhost:1026/v2/entities -s -S -H 'Content-Type: application/json' -d @- <<EOF
{
  "id": "AirConditioner1",
  "type": "AirConditioner",
  "status": {
    "value": "OFF",
    "type": "string"
  }
}
EOF
```

# Create Room entity

```
curl localhost:1026/v2/entities -s -S -H 'Content-Type: application/json' -d @- <<EOF
{
  "id": "Room1",
  "type": "Room",
  "temperature": {
    "value": 20,
    "type": "float"
  }
}
EOF
```

# Create  action

Set orion_endpoint and threshold as a parameter

```
wsk -i action create switchAC switch_ac.py --param orion_endpoint http://xxx.xxx.xxx.xxx:1026 --param threshold 30
```

# Update  action

```
wsk -i action update "/_/switchAC" --web true
```

# Create api

Get api endpoint.

```
wsk -i api create /switchAC post switchAC --response-type json
```

# Create subscription

```
curl -v localhost:1026/v2/subscriptions -s -S -H 'Content-Type: application/json' -d @- <<EOF
{
  "description": "A subscription to get info about Room1",
  "subject": {
    "entities": [
      {
        "id": "Room1",
        "type": "Room"
      }
    ],
    "condition": {
      "attrs": [
        "temperature"
      ]
    }
  },
  "notification": {
    "http": {
      "url": "http://xxxxxxxxx:9090/api/xxxxxxxxxxxxxxx/switchAC"
    },
    "attrs": [
      "temperature"
    ]
  },
  "expires": "2040-01-01T14:00:00.00Z",
  "throttling": 5
}
EOF
```

# Update temperature of Room1

```
curl -v localhost:1026/v2/op/update -s -S -H 'Content-Type: application/json' -d @- <<EOF
{
  "actionType": "update",
  "entities": [
    {
      "type": "Room",
      "id": "Room1",
      "temperature": {
        "value": 40,
        "type": "float"
      }
    }
  ]
}
EOF
```

# Make sure state of AirConditioner1


```
curl -v  localhost:1026/v2/entities/ | jq
```

```
[
  {
    "id": "AirConditioner1",
    "type": "AirConditioner",
    "status": {
      "type": "string",
      "value": "ON",
      "metadata": {}
    }
  },
  {
    "id": "Room1",
    "type": "Room",
    "temperature": {
      "type": "float",
      "value": 40,
      "metadata": {}
    }
  }
]
