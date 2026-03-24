from llm_sdk.llm_sdk import Small_LLM_Model


class Model(Small_LLM_Model):

    def generate_single_token(
            self, prompt_message: str, previous_tokens: str = ""):
        prompt = f"<|im_start|>user\n{prompt_message}<|im_end|>\n" + \
            f"<|im_start|>assistant\n<think>\n\n</think>\n\n{previous_tokens}"
        tensors = self.encode(prompt)
        probas = self.get_logits_from_input_ids(tensors.tolist()[0])
        sorted_tokens = sorted(probas, reverse=True)
        return sorted_tokens

    def generate_tokens(
            self, prompt_message: str, previous_tokens: str = ""):
        prompt = f"<|im_start|>user\n{prompt_message}<|im_end|>\n" + \
            f"<|im_start|>assistant\n<think>\n\n</think>\n\n{previous_tokens}"
        tensors = self.encode(prompt)
        probas = self.get_logits_from_input_ids(tensors.tolist()[0])
        sorted_tokens = sorted(probas, reverse=True)
        index = 0
        while True:
            yield self.decode(probas.index(sorted_tokens[index]))
            index += 1
