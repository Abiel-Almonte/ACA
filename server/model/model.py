from vllm.engine.async_llm_engine import AsyncLLMEngine
from vllm.engine.arg_utils import AsyncEngineArgs
from transformers import AutoTokenizer
import os

MODEL= os.path.join(os.path.dirname(__file__), './Mistral-7B-Instruct-v0.2-awq') #quantized
GPU_UTIL= 0.95
MAX_LEN= 8192

class vLLM_Engine():
    def __init__(self):

        engine_args= AsyncEngineArgs(
            MODEL,
            max_model_len=MAX_LEN,
            gpu_memory_utilization=GPU_UTIL,
        )

        self.tokenizer= AutoTokenizer.from_pretrained(MODEL)
        self.llm= AsyncLLMEngine.from_engine_args(engine_args)
