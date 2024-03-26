#!/usr/bin/env python3
"""
Python script that provides some stats about Nginx logs
stored in MongoDB:
"""
import pymongo


def log_nginx_stats(mongo_collection):
    """provides stats on Nginx logs"""
    print(f"{mongo_collection.estimated_document_count()} logs")

    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = mongo_collection.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, count))

    get_counts = mongo_collection.count_documents(
        {"method": "GET", "path": "/status"})
    print("{} status check".format(get_counts))


if __name__ == "__main__":
    mongo_collection = MongoClient('mongodb://127.0.0.1:27017').logs.nginx
    log_nginx_stats(mongo_collection)
