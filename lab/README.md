# Practicing Test Driven Development

Welcome to the **Practicing Test Driven Development** lab. It is important to understand the workflow for practicing true test driven development by writing the test cases first to describe the behavior of the code, and then writing the code to make the tests pass, thus ensure that it has that behavior. In this lab we will do just that.

## Requirements

Assume you have been asked to create a web service that can keep track of multiple counters. The web service has the following requirements:

- The API must be RESTful.
- The endpoint must be called `/counters`.
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to get a counter's current value.
- The service must be able to delete a counter.

You have been asked to implement them using TDD principles by writing the test cases first, and then writing the code to make the test cases pass.

## REST API Guidelines Review

There are guidelines for creating REST APIs that enable you to write the test cases for this lab:

| Action | Method | Return code    | URL                     |
|--------|--------|----------------|-------------------------|
| Create | POST   | 201_CREATED    | POST /counters/{name}   |
| Read   | GET    | 200_OK         | GET  /counters/{name}   |
| Update | PUT    | 200_OK         | PUT  /counters/{name}   |
| Delete | DELETE | 204_NO_CONTENT | DELETE /counters/{name} |

Following these guidelines, you can make assumptions about how to call the web service and assert what it should return.

## HTTP Status Codes

Here are some other HTTP status codes that you will need for this lab:

| Code | Status        | Description |
|------|---------------|-------------|
|  200 | HTTP_200_OK   | Success |
|  201 | HTTP_201_CREATED | The requested resource has been created |
|  204 | HTTP_204_NO_CONTENT | There is no further content |
|  404 | HTTP_404_NOT_FOUND | Could not find the resource requested |
|  405 | HTTP_405_METHOD_NOT_ALLOWED | Invalid HTTP method used on an endpoint |
|  409 | HTTP_409_CONFLICT | There is a conflict with your request |

All of these codes are defined in `status.py`. All you need to do is `import status` to use them in your code.
