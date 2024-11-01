# graphql-schema-diff-service

TODO - add your description for the project here!

## Project installation

Assumign you have conda, install Mamba (a fast, drop-in replacement for Conda) by running: conda install -n base -c conda-forge mamba

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

