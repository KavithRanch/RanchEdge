# API (Application Programmable Interface)
APIs are abstraction mechanisms which defines a contract which defines how clients can interact with services.
Contract includes:
* What requests can be made
* How to make requests
* What responses to expect
* Error Responses:
``` bash
200 OK
201 Created
204 No Content
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
422 Validation Error
500 Server Error
```

## Table of Contents
- [Types of APIs](#types-of-apis)
- [Design Principles](#key-design-principles)
- [Design Process and Approaches](#design-process-and-approaches)
- [Application Protocols](#application-protocols)
- [API Design By Type](#designing-api-by-type)
    - [REST APIs](#rest-apis)
    - [GraphQL APIs](#graphql-apis)
- [Authentication](#authentication)

## Types of APIs
1. **REST (Representational State Transfer)**
    * It is _resource-based_. Each request can perform allowable CRUD operations for a resource
    * It is _stateless_. Each request contains all information required to perform the action. It purposefully doesn't rely on prior request information as each one is treated entirely separately.
    * Request Components & CRUD Operations:
    ```bash
    # Request components
    /events/{id}?min_ev=0.05&limit=20
    Path: /events/{id}
    Query Parameters: ?min_ev=0.05&limit=20 
    Headers: Authorization token and etc.
    Body (POST/PUT/PATCH): JSON formatted body

    # CRUD Operations
    GET: Read
    POST: Create
    PUT: Update (full replacement)
    PATCH: Update (partial update of item)
    DELETE: Delete
    ```

2. **GraphQL**
    * GraphQL was made to avoid clients from having to call multiple APIs in order to retrieve information (all of which they didn't need) and still end up not having exactly what they require.
    * It uses _query language_. Each request allows clients to retrieve **exactly** what they want.
    * No over/under-fetching of information.
    * System typically has one endpoint `/graphql` and all requests are sent here.

## Key Design Principles
1. Consistency:
    * Consistent naming patterns between endpoints

2. Simplicity:
    * Focus on core use cases

3. Security:
    * Authentication/Authorization through tokens
    * Input validation
    * Rate limiting (# of requests a client can make within a specific time window)

4. Performance:
    * Efficient caching strategies
    * Pagination (Avoid sending all data at once and instead in chunks). Can be done in two ways:
        1. Offset Pagination: limit: # of records returned | offset: # of records to skip
            * `?limit=20&offset=0` means return first 20 entries
            * `?limit=20&offset=20` means skip first 20 and return the next 20 entries
            * `?limit=20&offset=40` means skip first 40 and return the next 20 entries
        2. Cursor Pagination: limit if # of records returned and cursor is a point to where to start 
            * cursor is usually based on id column
            * `?limit=20&cursor=2` says start at pointer to second index and return next 20 vals. It would then return 
            ```json
            {
                "data": [...],
                "cursor": 22 // The starting index of next batch
            }
            ```
    * Minimize round trips (# of requests needed to get all information for a specfic task)
    * Minimize payloads

## Design Process and Approaches
### Process
The API Design Process can be broken down into 4 simple steps:
1. Identify user core cases and stories
2. Define scope and boundaries
3. Determine performance requirements
4. Consider security constraints

### Approaches
There are 3 main approaches all valid depending on the scenario:
1. _Top-Down_ begins with **high-level user requirements** and **workflows**. API design is built around these before backend implementation
    * User-driven approach
    * Commonly used in technical interviews to see if you have good general understanding
    * Also used in industry when new functionality looking to be implemented and it is known to need an API
2. _Bottom-Up_ begins with **existing data models** and **capabilities**. API design is built around existing functionality to provide abstraction for frontend or client requests.
    * Commonly used in industry when company already has functionality in place and is looking to expose certain features
3. _Contract-First_ begins with an **OpenAPI specification/contract**. OpenAPI is the standard for API documentation and in contract-first, API design is built in agreement with this foundation before backend development.
    * Interface driven approach
    * Typically used in the workforce when multiple teams are involved and a standard agreement for what the proposed API will do is needed before proceeding with development

## Application Protocols 
Application layer protocols play a large role in API design as they define how the API communicates, how the endpoints are structured, performance expectations and how security is handled

||API Communication|API Design (Endpoint structure)|Performance Expectations|Security|
|:--:|:---:|:---:|:---:|:---:|
|**HTTP/HTTPS**|Send request &rarr; Receive Response (server can only send messages in response to request)|Design around **resources**. Ex. GET /events, GET /markets, GET /ev_opportunities & etc.||Secured through JWT authorization tokens, API keys, OAuth|
|**WebSockets**|Persistent connection & Bidirectional messasing/Server-push (server can send messages without user requesting for updates)|Design around **events** changing frequently. Ex. on_new_snapshot, on_new_event, on_ev_found & etc.|| Custom Auth "handshake" to setup persistent connection|
|**gRPC**|||||


* _HTTP/HTTPS is great for Data Retrieval and CRUD operations_
* _WebSockets is ideal for Real-Time Data communication and low-latency interactions_

## Designing API by Type
### REST APIs
* Since REST APIs are built around resources, we look to convert each relevant business domain/item into a REST resource
    * Convert domains to plural nouns for resources
        * Ex. Event &rarr; events, EV Opportunity &rarr; ev-opportunities & etc.
* We don't typically return all results at once to save bandwidth and improve performance so we can use:
    1. _Filtering_: Filter by certain column values
    2. _Sorting_: Sorting by ascending or descending values
    3. _Pagination_: Return certain amount of results each time (See section 4 design principles for types of pagination)
* Keep the **external** APIs versioned `/api/v1/...` &rarr; `/api/v2/...` so that in the event backwards-incompatible changes are made, the old clients can still use the old api as normally would, and as new clients roll in, they can use the newer version.
    * Such changes would include:
        - Renaming or Removing fields
        - Changing Data Types 
        - Changing Response Structure
        - Changing Auth Behaviour
        - Changing Endpoint Semantics
    * Should older clients decide to migrate their systems to newer versions of the API that is up to them, but we can't assume they will do so.

### GraphQL APIs
* GraphQL APIs are made to handle specific query like requests from clients

## Authentication
Authentication is specifically used to check and confirms the identity of the user.

There are many forms of authentication:
1. Basic Username and Password
    * Rarely used for external APIs since considered easily exploitable
2. **Bearer Token Authentication**
    * Each request is sent with a Bearer access token so that API can either validate or reject request
    * Standard approach for API design since they are fast and stateless
3. **OAuth2 + JWT**
    * Allows to authenticate with trusted provider like Google, Github, Facebook and issues an JWT access token if login is valid
4. Single Sign-On SSO + Identity Protocol
    * Used in enterprises where one login allows access to all enterprise applications

## Authorization
Authorization specifies which actions and resources the user has access to use.

3 Common Authorization Models:
1. **Role-Based Access Control RBAC**
    * Users are assigned roles and they are provided with access to specified resources based on role.
        - Typical roles might include Admin, Editor Viewer
    * Most widely-used 
2. Attribute-Based Access Control ABAC
    * It is based off user attributes and resource attributes and can create certain rules.
    * Can also conbine with environment attributes like time of day, location, device type and etc.
3. Access Control List ACL
    * Each resource has its own permission list containing users and their assigned access level.
    * Hard to scale well where there are a lot of users

## API Security
We have 7 main techniques to protect APIs from unwanted usage/attacks

1. Rate Limiting
    * Limiting the number of requests per user to avoid users spamming requests and blocking access for other users
        * Limiting can occur in the following forms:
        -   Limit for users per endpoint
        -   Limit of requests per User/IP address
        