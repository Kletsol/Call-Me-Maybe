from llm_sdk.llm_sdk import Small_LLM_Model


class Model(Small_LLM_Model):

    def get_probable_logits(self, prompt, history):
        prompt_to_process = f"<|im_start|>user\n{prompt}<|im_end|>\n" + \
            f"<|im_start|>assistant\n<think>\n\n</think>\n\n{history}"
        tensors = self.encode(prompt_to_process)
        probas = self.get_logits_from_input_ids(tensors.tolist()[0])
        sorted_logits = sorted(probas, reverse=True)
        return probas, sorted_logits

    def generate_single_token(
            self, prompt: str, history: str = "") -> str:
        probas, sorted_logits = self.get_probable_logits(prompt, history)
        logit = probas.index(sorted_logits[0])
        return self.decode(logit)

    def generate_tokens(
            self, prompt: str, history: str = ""):
        probas, sorted_logits = self.get_probable_logits(prompt, history)
        index = 0
        while True:
            yield self.decode(probas.index(sorted_logits[index]))
            index += 1
