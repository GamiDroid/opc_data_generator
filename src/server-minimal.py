import asyncio
import logging
import random
import json
from asyncua import Server, ua


async def main():
    _logger = logging.getLogger("asyncua")
    # setup our server
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

    # setup our own namespace
    uri = "http://examples.freeopcua.github.io"
    idx = await server.register_namespace(uri)

    with open('config.json', 'r') as file:
        config = json.load(file)

    # defined update ranges
    double_min = -0.5
    double_max = 0.6
    int_min = -1
    int_max = 1

    # Mapping from our config type to asyncua VariantTypes.
    datatype_mapping = {
        "boolean": ua.VariantType.Boolean,
        "int32": ua.VariantType.Int32,
        "int64": ua.VariantType.Int64,
        "double": ua.VariantType.Double,
        "string": ua.VariantType.String
    }

    # populating our address space
    myobj = await server.nodes.objects.add_object(idx, "MyObject")

    # Create nodes list that stores the variable node, its data type, and mode.
    opcs = []
    for nodeConfig in config['Nodes']:
        ns = nodeConfig['Namespace']
        name = nodeConfig.get("Name", "MyVariable")
        start = nodeConfig["StartValue"]
        data_type = nodeConfig.get("DataType", "Double")  # Default to Double if not specified

        # Allow override of the default variant type.
        variant = datatype_mapping.get(data_type.lower(), ua.VariantType.Double)
        
        mode = nodeConfig.get("Mode", "READ")  # Default to READ if not specified

        # Create node variable with the correct variant type.
        node = await myobj.add_variable(ns, name, start, varianttype=variant)
        await node.set_writable()
        opcs.append({"node": node, "DataType": data_type, "Mode": mode})

    _logger.info("Starting server!")
    async with server:
        while True:
            await asyncio.sleep(1)
            for item in opcs:
                node = item["node"]
                data_type = item["DataType"]
                mode = item["Mode"].lower()

                # If mode is WRITE, skip updates.
                if mode == "write":
                    continue

                current_value = await node.get_value()
                new_val = current_value  # default

                if data_type.lower() == "double":
                    random_offset = random.uniform(double_min, double_max)
                    new_val = current_value + random_offset
                    # clamp value between 0.0 and 100.0
                    if new_val > 100.0:
                        new_val = 100.0
                    elif new_val < 0.0:
                        new_val = 0.0

                elif data_type.lower() == "int32":
                    random_offset = random.randint(int_min, int_max)
                    new_val = int(current_value + random_offset)
                    # wrap the value as a Variant with type Int32
                    new_val = ua.Variant(new_val, ua.VariantType.Int32)

                elif data_type.lower() == "int64":
                    random_offset = random.randint(int_min, int_max)
                    new_val = int(current_value + random_offset)
                    # wrap the value as a Variant with type Int64
                    new_val = ua.Variant(new_val, ua.VariantType.Int64)

                elif data_type.lower() == "boolean":
                    # randomly toggle boolean (50% chance)
                    if random.random() < 0.5:
                        new_val = not current_value
                    else:
                        new_val = current_value
                        
                elif data_type.lower() == "string":
                    # generate a random 6-character string
                    new_val = ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(6))

                else:
                    _logger.warning("Unknown DataType '%s' for node %s", data_type, node)
                    continue

                # _logger.info("Set value of %s (type: %s) to %s", node, data_type, new_val)
                await node.write_value(new_val)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main(), debug=True)