# graphql-schema-diff-service

Certainly! Here’s a README project description based on your task requirements:

---

# GraphQL Schema Diff Service

## Overview
The **GraphQL Schema Diff Service** is a tool designed to detect breaking and non-breaking changes between two versions of a GraphQL schema. It produces a structured JSON report summarizing detected differences, including natural language release notes. This tool is intended to be integrated within a CI/CD pipeline to automatically generate release notes and notify API consumers of any impactful changes to the schema.

## Features
- **Schema Comparison**: Detects changes in field names, types, and parameters between two schema versions.
- **Breaking and Non-Breaking Changes**: Flags breaking changes (e.g., renamed or removed fields) and non-breaking enhancements (e.g., added fields).
- **Detailed Release Notes**: Generates natural language summaries for release notes, ideal for inclusion in update notifications or email distributions.
- **Structured JSON Output**: Returns change information in JSON format to support easy parsing and integration with other tools.

## Example Use Case
Given two versions of a GraphQL schema:
- *Schema Version 1*:
  ```graphql
  type Query {
    getWeather(location: String!): Weather
  }

  type Weather {
    temperature: Float
    description: String
    humidity: Int
    windSpeed: Float
  }
  ```

- *Schema Version 2*:
  ```graphql
  type Query {
    getWeather(city: String!): Weather
  }

  type Weather {
    temperature: Float
    description: String
    humidity: Int
    windSpeed: Float
    visibility: Int
  }
  ```

The tool will generate an output JSON highlighting changes such as renamed parameters or added fields:
```json
{
  "changes": [
    {
      "type": "Query",
      "field": "getWeather",
      "change": "Renamed input parameter 'location' to 'city'",
      "breaking": true,
      "release_note": "The input parameter for `getWeather` has been renamed from `location` to `city`. This is a breaking change, so make sure to update any queries that use `location` to `city`."
    },
    {
      "type": "Weather",
      "field": "visibility",
      "change": "Added new scalar field 'visibility'",
      "breaking": false,
      "release_note": "We've added a new `visibility` field to the `Weather` type. You can now get visibility information in your weather queries without modifying existing ones. This is a non-breaking change."
    }
  ],
  "release_notes": {
    "summary": "This release introduces a breaking change with the renaming of the `location` parameter to `city` in the `getWeather` query, and a non-breaking enhancement with the addition of a new `visibility` field in the `Weather` type."
  }
}
```

## Getting Started

### Prerequisites
- **Conda**
- **Python3.8+**
- **Libraries**: Ensure the required libraries are installed via `conda.yaml`

### Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/graphql-schema-diff-service.git
   cd graphql-schema-diff-service
   ```

2. **Install dependencies**:
Assuming you have conda, install Mamba (a fast, drop-in replacement for Conda) by running
    ```bash
    conda install -n base -c conda-forge mamba
    ```
Set your base environment (replace the path with the actual path you want to use).
    ```bash
        export BASE_ENV_DIR=/opt/homebrew/Caskroom/mambaforge/base/envs
    ```

To install the conda environment, update the yaml file with your environment prefix and add a Jupyter kernel.
    ```bash
        mamba env create --file conda.yaml
    ```

Every time you update a package make sure you update the conda.yaml file and 
run the code below to auto update your environment.
    ```bash
        mamba env update --file conda.yaml --prune
    ```

### Usage
1. **Prepare Schema Files**: Place your GraphQL schema versions in `.txt` format in the `/data` directory.
2. **Run the Service**:
   ```bash
   python app.py
   ```
3. The tool will output a JSON file summarizing changes and providing release notes.

## Project structure

```bash
graphql-schema-diff-service/
├── **src/**
│   ├── **main.py**            # Entry point of the service
│   ├── **schema_parser.py**    # Handles GraphQL schema parsing
│   ├── **diff_checker.py**     # Logic for identifying breaking changes
│   ├── **release_notes_generator.py**  # Generates natural language release notes
│   ├── **utils.py**            # Helper functions
│   └── **app.py**              # Service endpoint definition (e.g., FastAPI, Flask)
├── **tests/**
│   ├── **unit/**
│   │   ├── **test_schema_parser.py**
│   │   ├── **test_diff_checker.py**
│   │   └── **test_release_notes_generator.py**
│   ├── **integration/**
│   │   └── **test_end_to_end.py**
│   └── **fixtures/**
│       ├── **schema-1-example.txt**
│       └── **schema-2-example.txt**
├── **docs/**
│   └── **README.md**           # Project setup, usage, and deployment instructions
├── **requirements.txt**        # Dependencies
├── **Dockerfile**              # Docker setup for easy deployment (optional)
├── **.github/workflows**       # GitHub Actions for CI/CD (optional)
└── **output-examples/**
    └── **output-example.json**  # Example output for reference
```

### Future Enhancements
- Support for additional schema formats (e.g., REST/OpenAPI specifications).
- Enhanced breaking-change detection for nested types and custom directives.
- Integration with version control for automatic schema diff checks on commit.

## Contributing
Contributions are welcome! Please submit issues or feature requests, and feel free to open pull requests to improve the project.