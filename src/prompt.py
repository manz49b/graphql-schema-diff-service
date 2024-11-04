def get_prompt(schema_v1, schema_v2):
    example_one = """Input:
    Schema v1: 
    type Query {
    getUser(id: ID!): User
    }

    type User {
    id: ID
    name: String
    age: Int
    email: String
    phoneNumber: String
    }

    Schema v2:
    type Query {
    getUser(id: ID!): User
    getUserByEmail(email: String!): User
    }

    type User {
    id: ID!
    name: String!
    email: String!
    phoneNumber: String
    isActive: Boolean
    }

    Output:
    {
    "changes": [
        {
        "type": "User",
        "field": "id",
        "change": "Field 'id' made non-nullable",
        "breaking": true,
        "release_note": "The `id` field on `User` has been changed to non-nullable. This is a breaking change; any existing data where `id` is null will cause errors."
        },
        {
        "type": "User",
        "field": "name",
        "change": "Field 'name' made non-nullable",
        "breaking": true,
        "release_note": "The `name` field on `User` is now non-nullable. This is a breaking change, and clients should ensure all `User` entries include a `name` value."
        },
        {
        "type": "User",
        "field": "email",
        "change": "Field 'email' made non-nullable",
        "breaking": true,
        "release_note": "The `email` field on `User` has been updated to non-nullable, marking a breaking change. Ensure all `User` entries include an `email` value."
        },
        {
        "type": "User",
        "field": "isActive",
        "change": "Added new Boolean field 'isActive'",
        "breaking": false,
        "release_note": "A new `isActive` field has been added to the `User` type, allowing clients to check if a user is active. This addition is non-breaking."
        },
        {
        "type": "Query",
        "field": "getUserByEmail",
        "change": "Added new query 'getUserByEmail'",
        "breaking": false,
        "release_note": "A new query `getUserByEmail` has been added. Clients can now retrieve a user by email address. This change is non-breaking."
        }
    ],
    "release_notes": {
        "summary": "This release introduces several breaking changes, including updates to `User` fields (making `id`, `name`, and `email` non-nullable) and new additions such as the `isActive` field and `getUserByEmail` query."
    }
    }
    """

    example_two = """Input:
    Schema v1:
    type Query {
    listProducts(category: String): [Product]
    }

    type Product {
    id: ID!
    name: String!
    price: Float!
    inStock: Boolean
    }

    Schema v2:
    type Query {
    listProducts(category: String, sortBy: String): [Product]
    getProduct(id: ID!): Product
    }

    type Product {
    id: ID!
    name: String!
    price: Float!
    currency: String
    stockCount: Int
    }

    Output:
    {
    "changes": [
        {
        "type": "Query",
        "field": "listProducts",
        "change": "Added new optional input parameter 'sortBy'",
        "breaking": false,
        "release_note": "The `listProducts` query now accepts an optional `sortBy` parameter, allowing clients to sort products. This is a non-breaking change."
        },
        {
        "type": "Query",
        "field": "getProduct",
        "change": "Added new query 'getProduct'",
        "breaking": false,
        "release_note": "A new query `getProduct` has been introduced, enabling clients to fetch a product by its ID. This addition is non-breaking."
        },
        {
        "type": "Product",
        "field": "currency",
        "change": "Added new String field 'currency'",
        "breaking": false,
        "release_note": "The `currency` field has been added to the `Product` type, allowing clients to see the currency of the product's price. This is a non-breaking change."
        },
        {
        "type": "Product",
        "field": "stockCount",
        "change": "Added new Int field 'stockCount'",
        "breaking": false,
        "release_note": "A new field `stockCount` has been added to the `Product` type. Clients can now view the number of items in stock. This is a non-breaking change."
        }
    ],
    "release_notes": {
        "summary": "This release includes non-breaking enhancements to the `listProducts` query with a new `sortBy` parameter, new fields `currency` and `stockCount` in `Product`, and a new query `getProduct` for fetching product details by ID."
    }
    }
    """

    prompt = f"""You are a tool designed to detect differences between two GraphQL schemas. Generate a summary of breaking and non-breaking changes.

    Given two GraphQL schemas (Schema v1 and Schema v2) as inputs, follow these steps:
    1. Parse the schemas to identify differences such as added, removed, or changed fields, types, or parameters.
    2. For each change, determine if it is a breaking or non-breaking change based on compatibility with existing queries.
    3. Generate a natural language summary suitable for release notes based on these changes. Each entry should describe the change, the type and field affected, and specify if it is breaking or non-breaking.
    4. Structure your response with an overall summary in the release notes and detail each change individually.

    Return your response in JSON format with the following structure:

    {{
    "changes": [
        {{
        "type": "<Type>",
        "field": "<Field>",
        "change": "<Description of the change>",
        "breaking": <true or false>,
        "release_note": "<Detailed explanation for release notes>"
        }},
        ...
    ],
    "release_notes": {{
        "summary": "<High-level summary of the release including both breaking and non-breaking changes>"
    }}
    }}

    Here are two example scenarios to guide your response:
    {example_one}
    {example_two}

    Below are the GraphQL schemas to review:
    Schema v1:
    {schema_v1}

    Schema v2:
    {schema_v2}
    """
    return prompt