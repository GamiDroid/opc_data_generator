
## Getting Started

Run docker container:
```
docker compose up --build
```

Run docker container detached:
```
docker compose up --build -d
```

### Configure nodes

Supported data types: 
 - Double
 - Integer 
 - Boolean

```json
{
    "Nodes": [
        {
            "Namespace": "ns=2;s=freeopcua.Tags.pressure",
            "Name": "Pressure",
            "StartValue": 10.5,
            "DataType": "Double"
        },
        {
            "Namespace": "ns=2;s=freeopcua.Tags.speed",
            "Name": "Speed",
            "StartValue": 100,
            "DataType": "Integer"
        },
        {
            "Namespace": "ns=2;s=freeopcua.Tags.switch",
            "Name": "Switch",
            "StartValue": true,
            "DataType": "Boolean"
        }
    ]
}
```

## Special Thanks

- https://medium.com/@muhammadfaiznoh/getting-started-with-opc-ua-in-docker-c68a883d5c65
- https://github.com/FreeOpcUa/opcua-asyncio
