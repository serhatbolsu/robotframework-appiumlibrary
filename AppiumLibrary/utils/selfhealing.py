from pymongo import MongoClient, errors
from datetime import datetime
import logging

class SelfHealing:
    """ A utility class for self-healing locators in Robot framework AppiumLibrary.

    The SelfHealing class is designed to enhance the robustness of automated test cases 
    by dynamically identifying and updating locators that fail during execution. When 
    a locator cannot be found, the class attempts to self-heal by leveraging alternative 
    strategies, such as:
    - Searching for similar elements based on attributes.
    - Analyzing the DOM for recently updated or altered locators.

    This class helps reduce test flakiness due to minor changes in the application's UI 
    or DOM structure.
    """
    def __init__(self, host='localhost', port=27017, username='admin', password='adminpassword', auth_Source="admin"):
        try:
            # Create a MongoDB client
            self.client = MongoClient(
                host=host,
                port=port,
                username=username,
                password=password,
                authSource=auth_Source
            )
            logging.info("Connected to MongoDB!")

        except errors.ServerSelectionTimeoutError as e:
            logging.error("MongoDB connection timed out:", e)
        except errors.ConnectionFailure as e:
            logging.error("Failed to connect to MongoDB:", e)
        except errors.OperationFailure as e:
            logging.error("Operation failed on MongoDB:", e)
        except Exception as e:
            logging.error("An unexpected error occurred:", e)

    def add_locator_to_database(self, elements, locator, locator_variable_name):
        """Adds a found element and its associated metadata to the database.

        Parameters
        ----------
        elements : list
            List Of Elements Returned
        locator : str
            locator => {id, xpath, etc...}
        locator_variable_name : str
            the varibale name in robot file
        """
        db = self.client["ROBOT_ELEMENTS"]
        collection = db["elements"]
        item = {
            "name": locator_variable_name,
            "locator": locator,
            "text": elements[0].text,
            "packagename": elements[0].get_attribute("package"),
            "class": elements[0].get_attribute("classname"),
            "resource-id": elements[0].get_attribute("resource-id"),
            "bounds": f"{elements[0].location}, {elements[0].size}",
            "created-at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last-time-passed": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        try:
            result = collection.insert_one(item)
            logging.info(f"Document inserted successfully with ID: {result.inserted_id}")
        except errors.DuplicateKeyError as e:
            logging.error("Duplicate key error: ", e)
        except errors.ConnectionFailure as e:
            logging.error("Failed to connect to MongoDB: ", e)
        except errors.PyMongoError as e:
            logging.error("An error occurred while inserting the document: ", e)
    