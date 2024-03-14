from vllm.engine.async_llm_engine import AsyncLLMEngine
from vllm.engine.arg_utils import AsyncEngineArgs
from transformers import AutoTokenizer

MODEL= './Mistral-7B-Instruct-v0.2-awq' #quantized
GPU_UTIL= 0.8
MAX_LEN= 1024

class Model():
    def __init__(self):

        self.tokenizer= AutoTokenizer.from_pretrained(MODEL)

        engine_args= AsyncEngineArgs(
            MODEL,
            max_model_len=MAX_LEN,
            gpu_memory_utilization=GPU_UTIL,
        )

        self.engine= AsyncLLMEngine.from_engine_args(engine_args)

    def __call__(self):
        return {'vllm': self.engine, 'tokenizer': self.tokenizer}