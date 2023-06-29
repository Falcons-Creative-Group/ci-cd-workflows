import os

import shotgun_api3

# Constants for ShotGrid API connection
SG_BASE_URL = os.environ.get("SG_BASE_URL")
SG_SCRIPT_NAME = os.environ.get("SG_SCRIPT_NAME")
SG_SCRIPT_KEY = os.environ.get("SG_SCRIPT_KEY")

# Constants for pipeline configuration
CONFIG_NAME = "My Pipeline Config"
CONFIG_DESCRIPTION = "Description of my pipeline configuration"
ZIP_FILE_PATH = os.environ.get("ZIP_FILE_PATH")
# List of users allowed to use the configuration
# 2498 is the ID of the "Kei Ikeda" user for now
USER_ID = 2498


if __name__ == "__main__":
    print("SG_BASE_URL: {}".format(SG_BASE_URL))
    print("SG_SCRIPT_NAME: {}".format(SG_SCRIPT_NAME))
    print("SG_SCRIPT_KEY: {}".format(SG_SCRIPT_KEY))
    print("CONFIG_NAME: {}".format(CONFIG_NAME))
    print("CONFIG_DESCRIPTION: {}".format(CONFIG_DESCRIPTION))
    print("ZIP_FILE_PATH: {}".format(ZIP_FILE_PATH))
    
    # Connect to ShotGrid
    sg = shotgun_api3.Shotgun(SG_BASE_URL, SG_SCRIPT_NAME, SG_SCRIPT_KEY)
    print("Connected to ShotGrid!")

    # Get the user information
    user = sg.find_one("HumanUser", [["id", "is", USER_ID]], ["login"])
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

    # # Read the zip file as binary data
    # with open(ZIP_FILE_PATH, "rb") as file:
    #     file_contents = file.read()

    # upload_data = {
    #         "path": ZIP_FILE_PATH,
    #         "name": os.path.basename(ZIP_FILE_PATH),
    #         "content_type": "application/zip",
    #         "entity_type": "PipelineConfiguration",
    #         "entity_id": config["id"],  # Replace with the ID of the pipeline configuration entity
    #         "field_name": "uploaded_config",  # Replace with the field name of the file field in the entity schema
    #         "data": file_contents,
    #     }

    # sg.upload("Attachment", upload_data)
    # print("Zip file uploaded and associated with the 'uploaded config' field.")
