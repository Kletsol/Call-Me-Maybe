from src.objects import Model


class Processor():
    def __init__(self, prompts: list, functions: list, llm: Model):
        self.__prompts = prompts
        self.__functions = functions
        self.__llm = llm

    def process_prompt(self):
        ids_list = []
        for prompt in self.__prompts:
            id = self.__llm.encode(prompt)
            ids_list.append(id)
        logits = self.__llm.get_logits_from_input_ids(ids_list)
        return logits
