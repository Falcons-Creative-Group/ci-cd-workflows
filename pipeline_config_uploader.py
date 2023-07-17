import os

import shotgun_api3

# Constants for ShotGrid API connection
SG_BASE_URL = os.environ.get("SG_BASE_URL")
SG_SCRIPT_NAME = os.environ.get("SG_SCRIPT_NAME")
SG_SCRIPT_KEY = os.environ.get("SG_SCRIPT_KEY")

# Constants for pipeline configuration
CONFIG_NAME = os.environ.get("CONFIG_NAME")
CONFIG_DESCRIPTION = os.environ.get("CONFIG_DESCRIPTION")
ZIP_FILE_PATH = os.environ.get("ZIP_FILE_PATH")

# Constant for user ID to add to user restriction field
SG_DISABLED_USER_ID = os.environ.get("SG_DISABLED_USER_ID")


if __name__ == "__main__":
    print("SG_BASE_URL: {}".format(SG_BASE_URL))
    print("SG_SCRIPT_NAME: {}".format(SG_SCRIPT_NAME))
    print("SG_SCRIPT_KEY: {}".format(SG_SCRIPT_KEY))
    print("CONFIG_NAME: {}".format(CONFIG_NAME))
    print("CONFIG_DESCRIPTION: {}".format(CONFIG_DESCRIPTION))
    print("ZIP_FILE_PATH: {}".format(ZIP_FILE_PATH))
    print("SG_DISABLED_USER_ID: {}".format(SG_DISABLED_USER_ID))
    
    # Connect to ShotGrid
    sg = shotgun_api3.Shotgun(SG_BASE_URL, SG_SCRIPT_NAME, SG_SCRIPT_KEY)
    print("Connected to ShotGrid!")

    # Get the user information
    user = sg.find_one("HumanUser", [["id", "is", SG_DISABLED_USER_ID]], ["login"])
    print("User: {}".format(user))
    if not user:
        raise Exception("User not found!")

    # Create the pipeline configuration
    config_data = {
        "code": CONFIG_NAME,
        "description": CONFIG_DESCRIPTION,
        "users": [user],
        "plugin_ids": "basic.*",
    }
    config = sg.create("PipelineConfiguration", config_data)
    print("Created pipeline configuration: {}".format(config))

    print("Uploading zip file to Pipeline Config (id: {})...".format(config["id"]))
    attachment_entity_id = sg.upload("PipelineConfiguration", config["id"], ZIP_FILE_PATH, field_name="uploaded_config")
    print("Attachment entity id: {}".format(attachment_entity_id))
