import sys
import json
import time
import os
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import Twin, TwinProperties


def module_patch_twin(IOT_HUB_CONNECTION_STRING, DEVICE_ID, MODULE_ID, desired_module_twin):
    try:
        # RegistryManager
        iothub_registry_manager = IoTHubRegistryManager(IOT_HUB_CONNECTION_STRING)

        module_twin = iothub_registry_manager.get_module_twin(DEVICE_ID, MODULE_ID)
        print ( "" )
        print ( "Module twin properties before update: " )
        print ( "{0}".format(module_twin.properties) )

        # I need to change all desired properties to NULL before updating them all keys like "property3":2.0 to "property3":null
        delete_twin_properties = module_twin.properties
        # create empty module twin object
        print(delete_twin_properties)
        twin_properties = module_twin.properties.desired
        desired = {}

        for key, value in twin_properties.items():
            # key string contains no "$" char and value is not None
            if "$" not in key and value is not None:
                desired[key] = None
            else:
                # delete all properties that have $ in key
                continue

        # print the updated twin properties to confirm
        print(f"Updated Twin Properties: {desired}")
        del_twin_patch = Twin()
        del_twin_patch.properties = TwinProperties(desired=desired)
        del_module_twin = iothub_registry_manager.update_module_twin(
            DEVICE_ID, MODULE_ID, del_twin_patch, module_twin.etag
        )
        print ( "" )
        print ( "Module twin properties nulled     :" )
        time.sleep(5)
        # new values to witn from the file
        twin_patch = Twin(properties=TwinProperties(desired=desired_module_twin))
        updated_module_twin = iothub_registry_manager.update_module_twin(
            DEVICE_ID, MODULE_ID, twin_patch, module_twin.etag
        )
        print ( "" )
        print ( "Module twin properties after update     :" )
        print ( "{0}".format(updated_module_twin.properties) )

    except Exception as ex:
        print ( "Unexpected error {0}".format(ex) )
    except KeyboardInterrupt:
        print ( "IoTHubRegistryManager sample stopped" )

if __name__ == '__main__':
    # check if required arguments are provided
    if len(sys.argv) < 5:
        print("Usage: python module_twin.py <config_file>")
        sys.exit(1)

    CONNECTION_STRING = sys.argv[1]
    DEVICE_ID = sys.argv[2]
    MODULE_ID = sys.argv[3]

    # create module twin object with desired properties
    print(DEVICE_ID)
    # read configuration file
    config_file = sys.argv[4]
    with open(config_file, 'r') as f:
        config = json.load(f)

    twin = config["desired"]

    # call module_twin function with desired configuration

    module_patch_twin(CONNECTION_STRING, DEVICE_ID, MODULE_ID, twin)