import sys
import json
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import Twin, TwinProperties, Module

def module_replace_twin(IOT_HUB_CONNECTION_STRING, DEVICE_ID, MODULE_ID, desired_module_twin):
    module_exists = True
    try:
        # RegistryManager
        iothub_registry_manager = IoTHubRegistryManager(IOT_HUB_CONNECTION_STRING, DEVICE_ID, MODULE_ID)
        # delete existing twin and get it again to get the etag
        module_twin = iothub_registry_manager.get_module_twin(DEVICE_ID, MODULE_ID)
        print ( "" )
        print ( "Module twin properties before update    :" )
        print ( "{0}".format(module_twin.properties) )
    except Exception as ex:
        print ( "When trying to read module twin: Unexpected error {0}".format(ex) )
        module_exists = False
        # replace existing twin properties with new properties
        # in this example, we replace the entire twin properties

    if module_exists:
        iothub_registry_manager.delete_module(DEVICE_ID, MODULE_ID)
        print ( "Deleted existing module to nuke module twin" )
   
    try:        
        # create module again
        iothub_registry_manager.create_module_with_certificate_authority(DEVICE_ID, MODULE_ID, DEVICE_ID)
        print(f"Module {MODULE_ID} created for device {DEVICE_ID}.")

       # Create the Twin object
        module_twin = iothub_registry_manager.get_module_twin(DEVICE_ID, MODULE_ID)
        print(desired_module_twin)
        etag = module_twin.etag
        # Define the desired properties
        new_twin = Twin(properties=TwinProperties(desired=desired_module_twin))
        updated_module_twin = iothub_registry_manager.update_module_twin(
            DEVICE_ID, MODULE_ID, new_twin, etag
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

    twin = config[ "desired"]

    # call module_twin function with desired configuration

    module_replace_twin(CONNECTION_STRING, DEVICE_ID, MODULE_ID, twin)