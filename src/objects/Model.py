from llm_sdk.llm_sdk import Small_LLM_Model


class Model(Small_LLM_Model):

    # def find_token(self, prompt_message: str, previous_tokens: str = '', skip: bool = False):
    #     prompt = f"{prompt_message}, {previous_tokens}"
    #     tensors = self.encode(prompt)
    #     probas = self.get_logits_from_input_ids(tensors.tolist()[0])
    #     sorted_tokens = sorted(probas, reverse=True)
    #     token = probas.index(sorted_tokens[skip])
    #     return self.decode(token)

    def find_multiple_tokens(self, prompt_message: str,
                             previous_tokens: str = '', skip: bool = False):
        prompt = f"{prompt_message}, {previous_tokens}"
        tensors = self.encode(prompt)
        probas = self.get_logits_from_input_ids(tensors.tolist()[0])
        sorted_tokens = sorted(probas, reverse=True)
        while True:
            yield self.decode(probas.index(sorted_tokens[skip]))
            skip += 1
