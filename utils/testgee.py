import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "apikey.json"


def implicit():
    from google.cloud import storage

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API  request
    buckets = list(storage_client.list_buckets())
    print(buckets)


# implicit()
import ee

ee.Authenticate()
ee.Initialize()
print(ee.Image("NASA/NASADEM_HGT/001").get("title").getInfo())
