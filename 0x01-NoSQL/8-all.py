#!/usr/bin/env python3
"""
a Python function that lists all documents in a collection:
"""
import pymongo


def list_all(mongo_collection):
    """Lists all collections"""
    if not mongo_collection:
        return []
    mongo_document = mongo_collection.find()
    return [doc for doc in mongo_document]
