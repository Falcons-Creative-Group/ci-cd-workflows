import os

import shotgun_api3

# Constants for ShotGrid API connection
SG_BASE_URL = os.environ.get("SG_BASE_URL")
SG_SCRIPT_NAME = os.environ.get("SG_SCRIPT_NAME")
SG_SCRIPT_KEY = os.environ.get("SG_SCRIPT_KEY")

# Constants for toolkit bundle
BUNDLE_NAME = os.environ.get("BUNDLE_NAME")
# BUNDLE_DESCRIPTION = os.environ.get("BUNDLE_DESCRIPTION")
ZIP_FILE_PATH = os.environ.get("ZIP_FILE_PATH")

# Toolkit Bundle entity type
ENTITY_TYPE = "CustomNonProjectEntity10"


if __name__ == "__main__":
    print("SG_BASE_URL: {}".format(SG_BASE_URL))
    print("SG_SCRIPT_NAME: {}".format(SG_SCRIPT_NAME))
    print("SG_SCRIPT_KEY: {}".format(SG_SCRIPT_KEY))
    print("BUNDLE_NAME: {}".format(BUNDLE_NAME))
    # print("BUNDLE_DESCRIPTION: {}".format(BUNDLE_DESCRIPTION))
    print("ZIP_FILE_PATH: {}".format(ZIP_FILE_PATH))
    
    # Connect to ShotGrid
    sg = shotgun_api3.Shotgun(SG_BASE_URL, SG_SCRIPT_NAME, SG_SCRIPT_KEY)
    print("Connected to ShotGrid!")

    # Create the toolkit bundle
    bundle_data = {
        "code": BUNDLE_NAME,
        # "description": BUNDLE_DESCRIPTION,
    }
    bundle = sg.create(ENTITY_TYPE, bundle_data)
    print("Created toolkit bundle : {}".format(bundle))

    # print("Uploading zip file to Toolkit Bundle (id: {})...".format(bundle["id"]))
    # attachment_entity_id = sg.upload(ENTITY_TYPE, bundle["id"], ZIP_FILE_PATH, field_name="sg_payload")
    # print("Attachment entity id: {}".format(attachment_entity_id))
