import sys
import json
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import Twin, TwinProperties



CONNECTION_STRING = "YourIoTHubConnectionString"
DEVICE_ID = "myFirstDevice"
MODULE_ID = "myFirstModule"

def module_patch_twin(IOT_HUB_CONNECTION_STRING, DEVICE_ID, MODULE_ID, desired_module_twin):
    try:
        # RegistryManager
        iothub_registry_manager = IoTHubRegistryManager(CONNECTION_STRING)

        module_twin = iothub_registry_manager.get_module_twin(DEVICE_ID, MODULE_ID)
        print ( "" )
        print ( "Module twin properties before update    :" )
        print ( "{0}".format(module_twin.properties) )

        # Update twin
        twin_patch = Twin()
        twin_patch.properties = TwinProperties(desired=desired_module_twin)
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

    # read configuration file
    config_file = sys.argv[4]
    with open(config_file, 'r') as f:
        config = json.load(f)

    twin = config["desired"]

    # call module_twin function with desired configuration

    module_patch_twin(CONNECTION_STRING, DEVICE_ID, MODULE_ID, twin)