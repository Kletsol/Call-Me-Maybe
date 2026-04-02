*This project has been created as part of the 42 curriculum by lbonnet*

# Call Me Maybe 🤙

## 📝 Description

The goal of this project is to create a function calling tool that translates natural language
prompts into structured function calls. Given a question like "What is the sum of 40 and
2 ?", your solution should not return 42, but instead provide:

- The function name: fn_add_numbers,
- The arguments: {"a": 40, "b" : 2},

these returns being outputted in a JSON file.

## 🖥️ Instructions

### ⤵️ Input

The data/input directory contains two files that serve as input files for our program:

- function_calling_tests.json
- function_definitions.json

Each of these files fulfills a specific role :
- function_calling_tests.json contains a JSON array of natural language prompts. This is the data we'll process in our program.
- function_definitions.json contains the available functions the system can call, each function including function name, argument names and types, return type and the function's description.

### ⤴️ Output

The program outputs a single JSON file with all the JSON objects resulting from the processed prompts, each object containing the following keys (the type is specified for clarity only, it must not be included in the output):

|Key|Value|Type|
|---|---|---|
|prompt|The original natural-language request|str|
|name|The name of the function to call|str|
|parameters|All required arguments with the correct types|obj|

## 📚 Resources

Several resources were used to complete this project:
- https://unsloth.ai/docs/models/qwen3-how-to-run-and-fine-tune to learn how to run Qwen3, format prompts and all kinds of important details like switching between thinking and non-thinking modes for example.

- https://docs.python.org/fr/3/library/json.html and https://realpython.com/python-json/ to understand how json files are formatted, how to load, create and work with it to process all the data in input files and generate a 100% valid JSON file in output.

- https://docs.python.org/fr/3/howto/argparse.html and https://docs.python.org/3/library/argparse.html as the library argparse was used in conjunction with pydantic for the general parsing of the project.

- https://www.datacamp.com/tutorial/python-uv to learn more about UV, the package manager I used both for the project himself and for its virtual environment management.

## 🚀 Additional sections

### -> Algorithm explanation
The algorithm I chose is quite simple: The program receives a list of prompt, processes each one of them independently by sending, successively, to the LLM:
    - A prompt to retrieve the function's name
    - A prompt to retrieve the function's parameters
Each of these steps is encoded, converted to numercial IDs, processed by the LLM and its result is sorted by probability, before constrained decoding filters what is a good output and what isn't.

- For the function's name:
    - We take the generated tokens from most probable to least probable.
    - For each token, we browse the available functions. If it starts with the token, we append it to a list.
    - If there's more than one function in the list once we've reached the end of the available functions, that list becomes the new "available functions"
    - This process is repeated until there's only one function in the list, that function being the correct one.

- For the parameters:
    - We got the right function name in the previous step, so we use it here to specify to the LLM what parameters we need.
    - Once we got the tokens, we can treat them with the appropriate constrained decoding depending on the type of parameter expected (number, string...)

All the results are then stored in a dictionary, ready to be written in the output file.

### -> Design decisions
My design choices are primarily related to the need of speed and efficacity, as detailed in the two next sections (-> Performance analysis & Challenges faced). Apart from that, it's essentially an amalgam of personal logic and discussion with colleagues.

### -> Performance analysis
The programs accuracy, speed and reliability depends, above all, on the LLM himself. However, I've been able to set up multiple processus to improve these performances:
- Constrained decoding allowed me to sort the tokens to keep the most interesting of them, limiting possible errors for both accuracy and reliability,
- Speed has been quite a challenge, more explications on this subject in the next section.

Overall, my program achieves rather good results, being fast and precise enough to stay far below 5 minutes with correct results : 1 minute 9 seconds to process the eleven prompts of the subject.

### -> Challenges faced
The main challenge in this project was, for me, to be able to get correct results in a time short enough to respect the subject's requisitions. My first tests were way too slow, and it took me a lot of time to figure out how I could reduce it. I finally got great results with a simple, yet not easy to find, manipulation:
Until then, the prompt I was sending to the LLM only contained the original prompt and the list of available functions, like that :

```python
prompt = f"{available_functions},{prompt.PROMPT}"
```
As I said, this resulted in a very long processing time (almost 4 minutes 30 in total for 11 prompts)
However, simply precising the prompt gave me massive improvements in terms of processing time:

```python
prompt = f"Here are the functions you can access to resolve the prompt:{available_functions}. And here is the prompt: {prompt.PROMPT}"
```
Does that seem logical to you ?  Well, to me, it didn't...
### -> Testing strategy
Most of my tests are based on the prompts in the function_calling_tests provided by the subject. I myself did some other tests, including tests about error management, before validating the project.

### -> Example usage
To run the program, execute the following command in a terminal:
```
make run
```
You also can run the program with your own source files:
```
uv run python3 -m src --flags
```
The following flags are allowed:
|Flag|Action|Usage
|---|---|---|
|--functions_definition|Change the path to the functions definitions file|uv run python3 -m src --functions_definition path_to_file|
|--input|Change the path to the prompts file|uv run python3 -m src --input path_to_file|
|--output|Change the path to the output file|uv run python3 -m src --output path_to_file|
|--visual|Makes the visualizer active|uv run python3 -m src --visual|