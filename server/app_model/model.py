import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TextIteratorStreamer,
    pipeline
)
from langchain.llms.huggingface_pipeline import HuggingFacePipeline

class Model():
    def __init__(self):

        bnb_config= BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type='nf4',
            bnb_4bit_use_double_quant=True,
        )

        model= 'mistralai/Mistral-7B-Instruct-v0.2'

        tokenizer= AutoTokenizer.from_pretrained(model, use_fast=False)
        llm= AutoModelForCausalLM.from_pretrained(
            model,
            device_map= 'cuda:0',
            torch_dtype=torch.float16,
            quantization_config= bnb_config,
            #attn_implementation= 'flash_attention_2',
        )
        self.streamer= TextIteratorStreamer(
            tokenizer,
            timeout=0,
            skip_prompt=True,
            skip_special_tokens=True
        )

        self.pipe= pipeline(
            task='text-generation',
            model=llm,
            tokenizer=tokenizer,
            pad_token_id= tokenizer.eos_token_id,
            streamer= self.streamer,
            device_map='cuda:0',
            max_new_tokens=512
        )

    def __call__(self):
        return HuggingFacePipeline(pipeline=self.pipe)
