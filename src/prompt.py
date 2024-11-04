def get_examples():
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
    "breaking": True,
    "release_note": "The `id` field on `User` has been changed to non-nullable. This is a breaking change; any existing data where `id` is null will cause errors."
    },
    {
    "type": "User",
    "field": "name",
    "change": "Field 'name' made non-nullable",
    "breaking": True,
    "release_note": "The `name` field on `User` is now non-nullable. This is a breaking change, and clients should ensure all `User` entries include a `name` value."
    },
    {
    "type": "User",
    "field": "email",
    "change": "Field 'email' made non-nullable",
    "breaking": True,
    "release_note": "The `email` field on `User` has been updated to non-nullable, marking a breaking change. Ensure all `User` entries include an `email` value."
    },
    {
    "type": "User",
    "field": "isActive",
    "change": "Added new Boolean field 'isActive'",
    "breaking": False,
    "release_note": "A new `isActive` field has been added to the `User` type, allowing clients to check if a user is active. This addition is non-breaking."
    },
    {
    "type": "Query",
    "field": "getUserByEmail",
    "change": "Added new query 'getUserByEmail'",
    "breaking": False,
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
    "breaking": False,
    "release_note": "The `listProducts` query now accepts an optional `sortBy` parameter, allowing clients to sort products. This is a non-breaking change."
    },
    {
    "type": "Query",
    "field": "getProduct",
    "change": "Added new query 'getProduct'",
    "breaking": False,
    "release_note": "A new query `getProduct` has been introduced, enabling clients to fetch a product by its ID. This addition is non-breaking."
    },
    {
    "type": "Product",
    "field": "currency",
    "change": "Added new String field 'currency'",
    "breaking": False,
    "release_note": "The `currency` field has been added to the `Product` type, allowing clients to see the currency of the product's price. This is a non-breaking change."
    },
    {
    "type": "Product",
    "field": "stockCount",
    "change": "Added new Int field 'stockCount'",
    "breaking": False,
    "release_note": "A new field `stockCount` has been added to the `Product` type. Clients can now view the number of items in stock. This is a non-breaking change."
    }
],
"release_notes": {
    "summary": "This release includes non-breaking enhancements to the `listProducts` query with a new `sortBy` parameter, new fields `currency` and `stockCount` in `Product`, and a new query `getProduct` for fetching product details by ID."
}
}
"""
    example_three = """Schema v1:
    type Query {
  getUser(id: ID!): User
  listUsers(role: String): [User]
}

type User {
  id: ID
  username: String
  email: String
  age: Int
  address: Address
  status: UserStatus
}

type Address {
  street: String
  city: String
  postalCode: String
}

enum UserStatus {
  ACTIVE
  INACTIVE
}

Schema v2:
type Query {
  getUser(id: ID!): User
  listUsers(role: String, activeOnly: Boolean): [User!]
  getUserStatus(id: ID!): UserStatus!
}

type User {
  id: ID!
  username: String!
  email: String!
  age: Int
  address: Address!
  status: UserStatus!
  createdAt: String
}

type Address {
  street: String!
  city: String!
  postalCode: String!
  country: String!
}

enum UserStatus {
  ACTIVE
  INACTIVE
  SUSPENDED
}

Output:
{
  "changes": [
    {
      "type": "Query",
      "field": "listUsers",
      "change": "Added new optional parameter 'activeOnly'",
      "breaking": false,
      "release_note": "The `listUsers` query now accepts an optional `activeOnly` parameter to filter by active users only."
    },
    {
      "type": "Query",
      "field": "getUserStatus",
      "change": "Added new query",
      "breaking": false,
      "release_note": "Added new `getUserStatus` query to fetch a user's status by ID."
    },
    {
      "type": "User",
      "field": "id",
      "change": "Field made non-nullable",
      "breaking": true,
      "release_note": "The `id` field in User type is now required (non-nullable)."
    },
    {
      "type": "User",
      "field": "username",
      "change": "Field made non-nullable",
      "breaking": true,
      "release_note": "The `username` field in User type is now required (non-nullable)."
    },
    {
      "type": "User",
      "field": "email",
      "change": "Field made non-nullable",
      "breaking": true,
      "release_note": "The `email` field in User type is now required (non-nullable)."
    },
    {
      "type": "User",
      "field": "status",
      "change": "Field made non-nullable",
      "breaking": true,
      "release_note": "The `status` field in User type is now required (non-nullable)."
    },
    {
      "type": "User",
      "field": "createdAt",
      "change": "Added new field",
      "breaking": false,
      "release_note": "Added new optional `createdAt` field to the User type."
    },
    {
      "type": "Address",
      "field": "street",
      "change": "Field made non-nullable",
      "breaking": true,
      "release_note": "The `street` field in Address type is now required (non-nullable)."
    },
    {
      "type": "Address",
      "field": "city",
      "change": "Field made non-nullable",
      "breaking": true,
      "release_note": "The `city` field in Address type is now required (non-nullable)."
    },
    {
      "type": "Address",
      "field": "postalCode",
      "change": "Field made non-nullable",
      "breaking": true,
      "release_note": "The `postalCode` field in Address type is now required (non-nullable)."
    },
    {
      "type": "Address",
      "field": "country",
      "change": "Added new field",
      "breaking": false,
      "release_note": "Added new required `country` field to Address type."
    },
    {
      "type": "UserStatus",
      "field": "SUSPENDED",
      "change": "Added new enum value",
      "breaking": false,
      "release_note": "Added new `SUSPENDED` status to the UserStatus enum."
    }
  ],
  "release_notes": {
    "summary": "This release introduces several changes to the schema, including new fields, parameter updates, and non-nullable requirements. The `listUsers` query now has an `activeOnly` filter, and `getUserStatus` was added as a new query. Non-null constraints were added across `User` and `Address` types, and a `SUSPENDED` status was added to the `UserStatus` enum."
  }
}
"""
    return example_one, example_two, example_three

def get_prompt_1(schema_v1, schema_v2):
    example_one, example_two, example_three = get_examples()
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
        "breaking": <True or False>,
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
    prompt_version = 1
    return prompt, prompt_version

def get_prompt_2(schema_v1, schema_v2):
    example_one, example_two, example_three = get_examples()
    prompt=f"""You are a tool designed to detect differences between two GraphQL schemas. Your task is to generate a summary of breaking and non-breaking changes.

**Instructions:**
1. Given two GraphQL schemas (Schema v1 and Schema v2) as inputs, parse the schemas to identify differences such as added, removed, or changed fields, types, or parameters.
2. For each change, determine if it is breaking (incompatible with existing queries) or non-breaking (backward compatible).
3. Generate a natural language summary suitable for release notes based on these changes. Each entry should describe the change, the type and field affected, and specify if it is breaking or non-breaking.
4. Structure your response with an overall summary in the release notes and detail each change individually.
5. Do not provide preamble or afterwords only return the JSON object.

**Expected Output Format:**
Return your response in JSON format with the following structure:

```json
{{
    "changes": [
        {{
            "type": "<Type>",
            "field": "<Field>",
            "change": "<Description of the change>",
            "breaking": <True or False>,
            "release_note": "<Detailed explanation for release notes>"
        }},
        ...
    ],
    "release_notes": {{
        "summary": "<High-level summary of the release including both breaking and non-breaking changes>"
    }}
}}
```

**Examples:**
{example_one}
{example_two}

Below are the GraphQL schemas to review:
Schema v1:
{schema_v1}

Schema v2:
{schema_v2}

**Note:** Review and parse the provided GraphQL schemas accurately, identifying all changes in fields, parameters, and types.
Do not provide preamble or afterwords only return the JSON object.
"""
    prompt_version = 2 
    return prompt, prompt_version

def get_prompt_3(schema_v1, schema_v2):
    example_one, example_two, example_three = get_examples()
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
        "breaking": <True or False>,
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
    {example_three}

    Below are the GraphQL schemas to review:
    Schema v1:
    {schema_v1}

    Schema v2:
    {schema_v2}
    """
    prompt_version = 3
    return prompt, prompt_version

def get_prompt_4(schema_v1, schema_v2):
    example_one, example_two, example_three = get_examples()
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
        "breaking": <True or False>,
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
    {example_three}

    Below are the GraphQL schemas to review:
    Schema v1:
    {schema_v1}

    Schema v2:
    {schema_v2}
    """
    prompt_version = 3
    return prompt, prompt_version

def get_prompt_5(schema_v1, schema_v2):
    example_one, example_two, example_three = get_examples()
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
        "breaking": <True or False>,
        "release_note": "<Detailed explanation for release notes>"
        }},
        ...
    ],
    "release_notes": {{
        "summary": "<High-level summary of the release including both breaking and non-breaking changes>"
    }}
    }}

    Here are two example scenarios to guide your response:
    {example_two}
    {example_three}

    Below are the GraphQL schemas to review:
    Schema v1:
    {schema_v1}

    Schema v2:
    {schema_v2}
    """
    prompt_version = 5
    return prompt, prompt_version

def get_prompt_6(schema_v1, schema_v2):
    example_one, example_two, example_three = get_examples()
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
        "change": "<Description of the change including specific field names and type of change>",
        "breaking": <True or False>,
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
    prompt_version = 6
    return prompt, prompt_version

def get_prompt_7(schema_v1, schema_v2):
    example_one, example_two, example_three = get_examples()
    prompt = f"""You are a tool designed to detect differences between two GraphQL schemas. Generate a summary of breaking and non-breaking changes.

Given two GraphQL schemas (Schema v1 and Schema v2), perform the following steps:

Identify Differences: Parse the schemas to detect changes, including added, removed, or modified fields, types, or parameters.
Classify Changes: For each identified change, classify it as either:
Breaking Change: A modification that alters existing query behavior, such as renaming or removing fields, which requires clients to update their queries.
Non-Breaking Change: An addition or change that does not affect existing queries, such as adding new fields or parameters that clients can use without any disruption.
Generate Summary: Create a natural language summary for release notes. Each entry should clearly state:
The type of change (breaking or non-breaking)
The affected type and field
A concise description of the change
Structure Response: Format the output with:
An overall summary in the release notes.
Detailed entries for each change.

Return your response in JSON format with the following structure:

{{
"changes": [
    {{
    "type": "<Type>",
    "field": "<Field>",
    "change": "<Description of the change>",
    "breaking": <True or False>,
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
    prompt_version = 7
    return prompt, prompt_version