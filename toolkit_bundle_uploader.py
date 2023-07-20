import os
import logging

import shotgun_api3

# Constants for ShotGrid API connection
SG_BASE_URL = os.environ.get("SG_BASE_URL")
SG_SCRIPT_NAME = os.environ.get("SG_SCRIPT_NAME")
SG_SCRIPT_KEY = os.environ.get("SG_SCRIPT_KEY")

# Constants for toolkit bundle
BUNDLE_NAME = os.environ.get("BUNDLE_NAME")
# BUNDLE_DESCRIPTION = os.environ.get("BUNDLE_DESCRIPTION")
BUNDLE_TAG_NAME = os.environ.get("BUNDLE_TAG_NAME")
ZIP_FILE_PATH = os.environ.get("ZIP_FILE_PATH")

# Toolkit Bundle entity type
ENTITY_TYPE = "CustomNonProjectEntity10"


if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    logger.info("SG_BASE_URL: {}".format(SG_BASE_URL))
    logger.info("SG_SCRIPT_NAME: {}".format(SG_SCRIPT_NAME))
    logger.info("SG_SCRIPT_KEY: {}".format(SG_SCRIPT_KEY))
    logger.info("BUNDLE_NAME: {}".format(BUNDLE_NAME))
    # logger.info("BUNDLE_DESCRIPTION: {}".format(BUNDLE_DESCRIPTION))
    logger.info("ZIP_FILE_PATH: {}".format(ZIP_FILE_PATH))
    
    # Connect to ShotGrid
    sg = shotgun_api3.Shotgun(SG_BASE_URL, SG_SCRIPT_NAME, SG_SCRIPT_KEY)
    logger.info("Connected to ShotGrid!")

    # First, try to find an existing toolkit bundle entity
    filters = [
        ["code", "is", BUNDLE_NAME]
    ]
    # Find the entity
    existing_bundle = sg.find_one(ENTITY_TYPE, filters)

    if not existing_bundle:
        logger.info("Toolkit bundle '{}' not found!".format(BUNDLE_NAME))

        # Create the toolkit bundle
        bundle_data = {
            "code": BUNDLE_NAME,
            # "description": BUNDLE_DESCRIPTION,
        }

        # Find the tag eneitty
        existing_tag = sg.find_one("Tag", [["name", "is", BUNDLE_TAG_NAME]])
        if existing_tag:
            bundle_data["tags"] = [existing_tag]
        else:
            # Give warning
            logger.warning("Tag '{}' not found!".format(BUNDLE_TAG_NAME))
        
        # Create the bundle  
        logger.info("Creating toolkit bundle with data: {}".format(bundle_data))
        existing_bundle = sg.create(ENTITY_TYPE, bundle_data)

    # logger.info("Uploading zip file to Toolkit Bundle (id: {})...".format(bundle["id"]))
    # attachment_entity_id = sg.upload(ENTITY_TYPE, bundle["id"], ZIP_FILE_PATH, field_name="sg_payload")
    # logger.info("Attachment entity id: {}".format(attachment_entity_id))
