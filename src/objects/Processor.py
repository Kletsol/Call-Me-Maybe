from src.objects import Model


class Processor():
    def __init__(self, prompts: list, functions: list, llm: Model):
        self.__prompts = prompts
        self.__functions = functions
        self.__llm = llm

    def process_prompt(self):
        ids_list = []
        logits_list = []
        for prompt in self.__prompts:
            id = self.__llm.encode(prompt)
            ids_list.append(id)
        print(ids_list)
        for id in ids_list:
            logit = self.__llm.get_logits_from_input_ids(ids_list)
            logits_list.append(logit)
        return logits_list
