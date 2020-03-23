<h1>
  <img src="https://user-images.githubusercontent.com/522079/43096167-3a1b1118-8e86-11e8-9fb2-7b4e3b1368bc.png" width="40" alt="Directus Logo"/>&nbsp;Directus Python SDK
</h1>

> _This codebase is a work-in-progress. The repo is here as a placeholder for anyone interested in contributing to the software development kit. Pull-requests and contributions are welcome!_

## Requirements

- Python 3.7+

## Installation

Simply install the package from the root directory with:

```sh
pip install .
```

## Usage

### Init client and authentication

```python
from directus import DirectusClient

# Creates a Directus anonymous client object
client = DirectusClient(url="http://localhost:8080", project="directus")

# Create a Directus client from a user (generates access token)
client = DirectusClient(
    url="http://localhost:8080",
    project="directus",
    email="email@example.com",
    password="password"
)
```

### Collections

#### Get a list of all collections

> **Params:** offset (int), single (bool), meta (List of str)

```python
collections, metadata = client.get_collections_list()
```

#### Get a collection

> **Params:** collection (required str), meta (List of str)

```python
collection, metadata = client.get_collection(collection="sports")
```

#### Create a collection

> **Params:** new_collection (required Collection obj), meta (List of str)

```python

new_collection = {
    "collection": "sports",
    "fields": [
        {
            "field": "id",
            "type": "integer",
            "datatype": "int",
            "length": 11,
            "interface": "numeric",
            "primary_key": True
        }
    ]
}

created_collection, metadata = client.create_collection(collection=new_collection)
```

#### Update a collection

> **Params:** collection (required str), data (required dict), meta (List of str)

```python
updated_collection, metadata = client.update_collection(
    collection="sports", data={"note": "Hello World!"}
)
```

#### Delete a collection

**Params:** collection (required str)

```python
collection_is_deleted = client.delete_collection(collection="sports")
```

### Items

#### Get a list of items in a collection

> **Params:** collection (required str), parameters ([ListParameters](#listparameters)), pagination ([ListPagination](#listpagination)), meta (List of str)
>
> By default, if a page is specified, offset will be ignored

```python
sports, metadata = client.get_items_list(collection="sports")
```

#### Get a list of all items in a collection (run through pagination)

> **Params:** collection (required str), parameters ([ListParameters](#listparameters)), pagination ([ListPagination](#listpagination)), meta (List of str)

```python
all_sports, metadata = client.get_all_items_list(collection="sports")
```

#### Get a specific item in a collection by id

> **Params:** collection (required str), item_id (required int), fields (List of str), meta (List of str)

```python
sport, metadata = client.get_item(collection="sports", item_id=1)
```

#### Create an item (with corresponding data model)

> **Params:** collection (required str), item_data (required dict), meta (List of str)

```python
created_sport, metadata = client.create_item(collection="sports", item_data=item_data)
```

#### Update an item

> **Params:** collection (required str), item_id (required int), item_data (required dict), fields (List of str), meta (List of str)

```python
updated_sport, metadata = client.update_item(
    collection="sports", item_id=1, item_data=item_data_to_update
)
```

#### Delete an item

> **Params:** collection (required str), item_id (required int)

```python
sport_deleted = client.delete_item(collection="sports", item_id=1)
```

#### List item revisions

> **Params:** collection (required str), item_id (required int), parameters ([ListParameters](#listparameters)), pagination ([ListPagination](#listpagination)), meta (List of str)
>
> By default, if a page is specified, offset will be ignored

```python
sport_revisions = client.get_item_revisions_list(collection="sports", item_id=1)
```

#### Retrieve an item revision

> **Params:** collection (required str), item_id (required int), offset (required int), fields (List of str), meta (List of str)

```python
sport_revision = client.get_item_revision(collection="sports", item_id=1, offset= 2)
```

#### Revert to a given revision

> **Params:** collection (required str), item_id (required int), revision_id (int), fields (List of str), meta (List of str)

```python
reverted_sport = client.revert_item_revision(
    collection="sports", item_id=1, revision_id=2
)
```

### Files

#### Get a list of files

> **Params:** fields (List of str), parameters ([ListParameters](#listparameters)), pagination ([ListPagination](#listpagination)), meta (List of str)

```python
files, metadata = client.get_files_list()
```

#### Get a specific file by id

> **Params:** file_id (required int), fields (List of str), meta (List of str)

```python
file, metadata = client.get_file(file_id=1)
```

#### Create a file

> **Params:** data (required str), filename_download (str), title (str), description (str), location (str), tags (str), metadata (str), meta (List of str)

```python
file, metadata = client.create_file(data="https://picsum.photos/200/300")
```

### List filters and pagination

#### ListParameters

When you make a GET request on a list, you can add filtering parameters. Then you create a new `ListParameters` object with corresponding properties:

```python
from directus.models import ListParameters

parameters = ListParameters(
    status="published",                             # https://docs.directus.io/api/query/status.html
    fields=["id","name","description","owner.*"],   # https://docs.directus.io/api/query/fields.html
    sort=["created_on","id"],                       # https://docs.directus.io/api/query/sort.html
    query="football",                               # https://docs.directus.io/api/query/q.html
    list_filter="filter[contributors][all]=1,2,3"   # https://docs.directus.io/api/query/filter.html
)

football_sports, meta = items.get_all_items_list(
    collection="sports", parameters=parameters
)
```

> You can also use `single=True` parameter so that only the first element will be returned (see [single](https://docs.directus.io/api/query/single.html))

#### ListPagination

When you make a GET request on a list, you can add pagination parameters. Then you create a new `ListPagination` object with corresponding properties:

```python
from directus.models import ListPagination

pagination = ListPagination(
    limit=50,               # https://docs.directus.io/api/query/limit.html
    offset=101              # https://docs.directus.io/api/query/offset.html
)
```

> You can also use `page=1` (for example) parameter. In this case, offset is ignored (see [page](https://docs.directus.io/api/query/page.html))

## Development

Simply install the project from scratch with the following command:

```sh
make install
```

You can lint or format the code using the following commands:

```sh
make lint
make format
```

Run tests with the following command:

```sh
make test
```

For more details, please see the `Makefile` file.
