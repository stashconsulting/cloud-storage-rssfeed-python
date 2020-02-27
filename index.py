from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom
from google.cloud import storage

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def gather_items(parent_element, data):
    for item_data in data:
        item_data = item_data.__dict__
        item = SubElement(parent_element, 'item')

        title = SubElement(item, 'title')
        title.text = item_data['name']

        link = SubElement(item, 'link')
        link.text = item_data['_properties']['selfLink']

        description = SubElement(item, 'description')
        description.text = item_data['_properties']['name']

def upload_blob(bucket, content, destination_blob_name):
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(content)


def main(event, context):
    # Enable Storage
    storage_client = storage.Client()

    # Reference an existing bucket.
    bucket_name = 'image-food-files2'
    bucket = storage_client.get_bucket(bucket_name)
    folder_name = 'food/'
    blobs = storage_client.list_blobs(bucket_name, prefix=folder_name)
    files = iter(blobs)
    next(files)
    channel = Element('channel')
    title = SubElement(channel, 'title')
    title.text = "podcasts"
    comment = Comment('Generated for Learning')
    channel.append(comment)
    gather_items(channel, files)
    upload_blob(bucket, prettify(channel), 'rssfeed.xml')
