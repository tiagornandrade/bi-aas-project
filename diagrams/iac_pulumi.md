```mermaid
classDiagram
    class Datastream {
        - config
        + __init__(config)
        + create_datastream_network()
        + create_datastream_source()
        + create_datastream_destination()
        + create_datastream_stream(source_connection, destination_connection, bigquery_dataset)
        + create_bigquery_dataset()
    }
```
