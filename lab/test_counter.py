"""
Test Cases for Counter Web Service

Requirements for the counter service
- The API must be RESTful.
- The endpoint must be called `/counters`.
- The data returned should be this {"name":"some_name", "counter":0}
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a 409 conflict error code.
- The service must be able to update a counter by name.
- The service must be able to get a counter's current value.
- The service must be able to delete a counter.
"""
