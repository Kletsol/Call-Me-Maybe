*This project has been created as part of the 42 curriculum by lbonnet*

# Call-Me-Maybe 🤙

## Description

The goal of this project is to create a function calling tool that translates natural language
prompts into structured function calls. Given a question like "What is the sum of 40 and
2 ?", your solution should not return 42, but instead provide:

- The function name: fn_add_numbers,
- The arguments: {"a": 40, "b" : 2},

these returns being outputted in a JSON file.

## Instructions

### Input

The data/input directory contains two files that serve as input files for our program:

- function_calling_tests.json
- function_definitions.json

Each of these files fulfills a specific role :
- function_calling_tests.json contains a JSON array of natural language prompts. This is the data we'll process in our program.
- function_definitions.json contains the available functions the system can call, each function including function name, argument names and types, return type and the function's description.

### Output

The program output is a single JSON file with all the JSON objects resulting from the processed prompts, each object containing the following keys (the type is specified for clarity only, it must not be included in the output):

|Key|Value|Type|
|---|---|---|
|prompt|The original natural-language request|str|
|name|The name of the function to call|str|
|parameters|All required arguments with the correct types|obj|

## Resources

## Additional sections

### -> Algorithm explanation

### -> Design decisions

### -> Performance analysis

### -> Challenges faced

### -> Testing strategy

### -> Example usage