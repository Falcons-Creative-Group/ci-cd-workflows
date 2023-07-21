import os

import shotgun_api3

# Constants for ShotGrid API connection
SG_BASE_URL = os.environ.get("SG_BASE_URL")
SG_SCRIPT_NAME = os.environ.get("SG_SCRIPT_NAME")
SG_SCRIPT_KEY = os.environ.get("SG_SCRIPT_KEY")

# Constants for toolkit bundle
BUNDLE_NAME = os.environ.get("BUNDLE_NAME")
BUNDLE_DESCRIPTION = os.environ.get("BUNDLE_DESCRIPTION")
BUNDLE_TAG_NAME = os.environ.get("BUNDLE_TAG_NAME")
ZIP_FILE_PATH = os.environ.get("ZIP_FILE_PATH")

# Toolkit Bundle entity type
ENTITY_TYPE = "CustomNonProjectEntity10"


if __name__ == "__main__":
    print("SG_BASE_URL: {}".format(SG_BASE_URL))
    print("SG_SCRIPT_NAME: {}".format(SG_SCRIPT_NAME))
    print("SG_SCRIPT_KEY: {}".format(SG_SCRIPT_KEY))
    print("BUNDLE_NAME: {}".format(BUNDLE_NAME))
    print("BUNDLE_DESCRIPTION: {}".format(BUNDLE_DESCRIPTION))
    print("ZIP_FILE_PATH: {}".format(ZIP_FILE_PATH))
    
    # Connect to ShotGrid
    sg = shotgun_api3.Shotgun(SG_BASE_URL, SG_SCRIPT_NAME, SG_SCRIPT_KEY)
    print("Connected to ShotGrid!")

    # First, try to find an existing toolkit bundle entity
    filters = [
        ["code", "is", BUNDLE_NAME]
    ]
    # Find the entity
    existing_bundle = sg.find_one(ENTITY_TYPE, filters)

    if not existing_bundle:
        print("Toolkit bundle '{}' not found!".format(BUNDLE_NAME))

        # Create the toolkit bundle
        bundle_data = {
            "code": BUNDLE_NAME,
            "description": BUNDLE_DESCRIPTION,
        }

        # Find the tag eneitty
        existing_tag = sg.find_one("Tag", [["name", "is", BUNDLE_TAG_NAME]])
        if existing_tag:
            bundle_data["tags"] = [existing_tag]
        else:
            # Give warning
            print("Tag '{}' not found!".format(BUNDLE_TAG_NAME))
        
        # Create the bundle  
        print("Creating toolkit bundle with data: {}".format(bundle_data))
        existing_bundle = sg.create(ENTITY_TYPE, bundle_data)

    print("Uploading zip file to Toolkit Bundle (id: {})...".format(existing_bundle["id"]))
    attachment_entity_id = sg.upload(ENTITY_TYPE, existing_bundle["id"], ZIP_FILE_PATH, field_name="sg_payload")
    print("Attachment entity id: {}".format(attachment_entity_id))
