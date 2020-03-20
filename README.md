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

```python
from directus_api import DirectusClient

url = "http://123.45.678.90:8080"
project = "Directus"

# Creates a Directus client object
client = DirectusClient(url, project)

# Create a Directus client from a user (generates access token)
client = DirectusClient(url, project, email="email@example.com", password="password")

# Get a list of all items in a collection
client.get_items_list("photos")

# Get a specific item in a collection by id
client.get_item("photos", 1)

# Get a list of all files (requires full constructor with email and password)
client.get_files_list()

# Get a specific file (requires full constructor with email and password)
client.get_file(1)

# Create a new item in a collection (requires full constructor with email and password)
item = {name: "Directus", id: 1}
client.create_item("collection_name", item)
```

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

For more details, please see the `Makefile` file.
