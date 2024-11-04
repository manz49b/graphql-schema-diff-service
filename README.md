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
Sure! Below is the modified README section that includes the additional scoring information for both the LLM scoring method and the Python scoring method. I have added a new section titled **Scoring Comparison** to provide clarity on the evaluation metrics used in your project.

```markdown
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

## Scoring Comparison
The project includes scoring evaluations for the generated release notes using two different methods: a Large Language Model (LLM) scoring method and a traditional Python scoring method. Below are the results of the evaluations:

### LLM Scoring:
- **BLEU Score**: 0.0000
- **ROUGE Score**: 
  ```json
  {
    "rouge-1": {"r": 0.6923076923076923, "p": 0.5625, "f": 0.6206896502259216},
    "rouge-2": {"r": 0.28125, "p": 0.25, "f": 0.26470587737024226},
    "rouge-l": {"r": 0.5384615384615384, "p": 0.4375, "f": 0.4827586157431629}
  }
  ```
- **Exact Match**: False


### Python Methodology Scoring:
- **BLEU Score**: 0.0000
- **ROUGE Score**: 
  ```json
  {
    "rouge-1": {"r": 0.34615384615384615, "p": 0.47368421052631576, "f": 0.39999999512098766},
    "rouge-2": {"r": 0.0625, "p": 0.1111111111111111, "f": 0.07999999539200027},
    "rouge-l": {"r": 0.34615384615384615, "p": 0.47368421052631576, "f": 0.39999999512098766}
  }
  ```
- **Exact Match**: False

This scoring comparison provides insights into the performance of the generated release notes, allowing developers to evaluate the effectiveness of the output from both the LLM and traditional methods.

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
../../graphql-schema-diff-service/
├── tests
├── docs
│   └── .gitkeep
├── README.md
├── .gitignore
├── .env
├── conda.yaml
├── .git
├── data
│   ├── output-example-1.txt
│   ├── schema-1-example-1.txt
│   ├── schema-2-example-1.txt
│   ├── output-example.txt
│   ├── schema-1-example.txt
│   └── schema-2-example.txt
├── reports
│   └── .gitkeep
└── src
    ├── json_tools.py
    ├── claude.py
    ├── release_notes_generator.py
    ├── __pycache__
    │   ├── schema_diff.cpython-310.pyc
    │   ├── base.cpython-310.pyc
    │   ├── claude.cpython-310.pyc
    │   ├── prompt.cpython-310.pyc
    │   ├── eval.cpython-310.pyc
    │   ├── json.cpython-310.pyc
    │   ├── json_tools.cpython-310.pyc
    │   └── schema_parser.cpython-310.pyc
    ├── temp.ipynb
    ├── app.py
    ├── prompt.py
    ├── eval.py
    ├── main.py
    ├── schema_parser.py
    ├── schema_diff.py
    └── base.py
```

### Future Enhancements
- Support for additional schema formats (e.g., REST/OpenAPI specifications).
- Enhanced breaking-change detection for nested types and custom directives.
- Integration with version control for automatic schema diff checks on commit.

## Contributing
Contributions are welcome! Please submit issues or feature requests, and feel free to open pull requests to improve the project.