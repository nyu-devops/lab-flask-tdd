# Copyright 2016, 2026 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Pet Store Service

This service implements a REST API that allows you to Create, Read, Update
and Delete Pets from the inventory of pets in the PetShop
"""

from flask import jsonify, request, url_for, abort
from flask import current_app as app  # Import Flask application
from service.models import Pet
from service.common import status  # HTTP Status Codes


######################################################################
# GET HEALTH CHECK
######################################################################
@app.route("/health")
def health_check():
    """Let them know our heart is still beating"""
    return jsonify(status=200, message="Healthy"), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    app.logger.info("Request for Root URL")
    return (
        jsonify(
            name="Pet Demo REST API Service",
            version="1.0",
            paths=url_for("list_pets", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
# LIST ALL PETS
######################################################################
@app.route("/pets", methods=["GET"])
def list_pets():
    """Returns all of the Pets"""
    app.logger.info("Request for pet list")

    # Return all of the Pets
    pets = Pet.all()

    results = [pet.serialize() for pet in pets]
    app.logger.info("Returning %d pets", len(results))
    return results, status.HTTP_200_OK


######################################################################
# READ A PET
######################################################################
@app.route("/pets/<int:pet_id>", methods=["GET"])
def get_pets(pet_id):
    """
    Retrieve a single Pet

    This endpoint will return a Pet based on it's id
    """
    app.logger.info("Request to Retrieve a pet with id [%s]", pet_id)

    # Attempt to find the Pet and abort if not found
    pet = Pet.find(pet_id)
    if not pet:
        abort(status.HTTP_404_NOT_FOUND, f"Pet with id '{pet_id}' was not found.")

    app.logger.info("Returning pet: %s", pet.name)
    return pet.serialize(), status.HTTP_200_OK


######################################################################
# CREATE A NEW PET
######################################################################
@app.route("/pets", methods=["POST"])
def create_pets():
    """
    Create a Pet
    This endpoint will create a Pet based the data in the body that is posted
    """
    app.logger.info("Request to Create a Pet...")
    check_content_type("application/json")

    pet = Pet()
    # Get the data from the request and deserialize it
    data = request.get_json()
    app.logger.info("Processing: %s", data)
    pet.deserialize(data)

    # Save the new Pet to the database
    pet.create()
    app.logger.info("Pet with new id [%s] saved!", pet.id)

    # Return the location of the new Pet
    location_url = url_for("get_pets", pet_id=pet.id, _external=True)
    return pet.serialize(), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
# UPDATE AN EXISTING PET
######################################################################
@app.route("/pets/<int:pet_id>", methods=["PUT"])
def update_pets(pet_id):
    """
    Update a Pet

    This endpoint will update a Pet based the body that is posted
    """
    app.logger.info("Request to Update a pet with id [%s]", pet_id)
    check_content_type("application/json")

    # Attempt to find the Pet and abort if not found
    pet = Pet.find(pet_id)
    if not pet:
        abort(status.HTTP_404_NOT_FOUND, f"Pet with id '{pet_id}' was not found.")

    # Update the Pet with the new data
    data = request.get_json()
    app.logger.info("Processing: %s", data)
    pet.deserialize(data)

    # Save the updates to the database
    pet.update()

    app.logger.info("Pet with ID: %d updated.", pet.id)
    return pet.serialize(), status.HTTP_200_OK


######################################################################
# DELETE A PET
######################################################################
@app.route("/pets/<int:pet_id>", methods=["DELETE"])
def delete_pets(pet_id):
    """
    Delete a Pet

    This endpoint will delete a Pet based the id specified in the path
    """
    app.logger.info("Request to Delete a pet with id [%s]", pet_id)

    # Delete the Pet if it exists
    pet = Pet.find(pet_id)
    if pet:
        app.logger.info("Pet with ID: %d found.", pet.id)
        pet.delete()

    app.logger.info("Pet with ID: %d delete complete.", pet_id)
    return {}, status.HTTP_204_NO_CONTENT


######################################################################
######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
######################################################################


######################################################################
# Checks the ContentType of a request
######################################################################
def check_content_type(content_type) -> None:
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )
