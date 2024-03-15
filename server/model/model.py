from vllm.engine.async_llm_engine import AsyncLLMEngine
from vllm.engine.arg_utils import AsyncEngineArgs
from transformers import AutoTokenizer

MODEL= '/home/abiel/workspace/ACA_Fullstack/server/model/Mistral-7B-Instruct-v0.2-awq' #quantized
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
