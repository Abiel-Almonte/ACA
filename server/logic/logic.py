from .vectorstore import Vectorstore
from vllm import SamplingParams
from .prompts import (
    CLASSIFICATION_PROMPT,
    NO_CONTEXT_PROMPT,
    STANDALONE_PROMPT,
    CHAT_CONTEXT_PROMPT,
)
import asyncio
from typing import Any

TYPE= 'similarity'
TOP_K= 6
LAMBDA= 0.25

class Router:   
    def __init__(
        self, 
        engine,
    ):
        data= Vectorstore()
        self.llm= engine.llm
        self.tokenizer= engine.tokenizer
        self.vectorstore= data.vectordb
        self.steps= []
    
    async def generate(
        self,
        prompt:Any,
        _uuid:str,
        temperature: float= 0.0,
        max_tokens:int= 512,
        stream: bool= False
    ):
        
        if isinstance(prompt, str):
            response_generator= self.llm.generate(
                prompt,
                SamplingParams(
                    temperature=temperature,
                    max_tokens=max_tokens
                ),
                _uuid
            )
            return await self.output_response(response_generator, stream)

        elif isinstance(prompt, list):
            tokens= self.tokenizer.apply_chat_template(prompt)
            response_generator= self.llm.generate(
                None,
                SamplingParams(
                    temperature=temperature,
                    max_tokens=max_tokens
                ),
                _uuid,
                prompt_token_ids=tokens,
            )
            return await self.output_response(response_generator, stream)
    
    async def output_response(
        self,
        response_generator,
        stream: bool,
    ):
        if stream:
            return self.stream_output(response_generator)

        else:
            return await self.static_output(response_generator) 
                
    async def stream_output(self, response_generator):
        counter= 0
        async for request_output in response_generator:
            output= request_output.outputs[0]
            text= output.text[counter:]
            yield text
            counter+= len(text)

    async def static_output(self, response_generator):
        async for request_output in response_generator:
                pass
        if request_output.finished:
            response= request_output.outputs[0].text
            return response

    def similarity_search(self, standalone_question, top_k):
        retriever= self.vectorstore.as_retriever(
            search_type=TYPE,
            search_kwargs={'k': top_k, 'lamda_mul': LAMBDA}
        )

        docs= retriever.invoke(standalone_question, **{'k':10})
        docs= self._combine_documents(docs)
        return docs 

    def _combine_documents(self, docs):
        combined_doc=''
        for doc in docs:
            combined_doc+= doc.page_content + '\n'
        return combined_doc
        
    async def classify(
        self,
        question: str,
        _uuid: int
    )->str:
        classify_prompt= CLASSIFICATION_PROMPT.format(question=question)

        response= await self.generate(
            classify_prompt,
            _uuid,
            max_tokens=50,
        )

        self.steps.append(f'Classification: {response}')
        return response
    
    async def no_context_pipe(
        self,
        question: str,
        messages: list,
        _uuid: str,
    ):  
        messages.append({'role': 'user', 'content': NO_CONTEXT_PROMPT.format(question= question)})
        no_context_response= await self.generate(
            messages,
            _uuid,
            temperature=0.9,
            max_tokens=128,
            stream=True,
        )

        return no_context_response
    
    async def rephrase(
        self,
        question: str,
        messages: list,
        _uuid: str,
    ):
        messages.append({'role': 'user', 'content': STANDALONE_PROMPT.format(question= question)})
        standalone_question= await self.generate(
            messages,
            _uuid,
            max_tokens=128,
        )

        self.steps.append(f'Standalone Question: {standalone_question}')
        messages.pop()

        return standalone_question

    async def context_pipe(
        self,
        question: str,
        context:str,
        messages: list,
        _uuid: str
    ):
        messages.append({'role': 'user', 'content': CHAT_CONTEXT_PROMPT.format(context= context, question= question)})
        context_response= await self.generate(
            messages,
            _uuid,
            temperature=0.9,
            stream=True
        )

        return context_response

    async def invoke_chat(
        self,
        question: str,
        messages: list,
        _uuid: str,
        top_k: int= TOP_K,
        **kwargs,
    ):
        if len(messages)> 4:
            messages.pop(0)
            messages.pop(0)
            
        classification= await self.classify(question, _uuid)
        await asyncio.sleep(0.0001)

        if 'No' in classification:
            response= await self.no_context_pipe(question, messages, _uuid)
            return response
        else:
            standalone_question= await self.rephrase(question, messages, _uuid)
            context= self.similarity_search(standalone_question, top_k)
            await asyncio.sleep(0.0001)
            response= await self.context_pipe(question, context, messages, _uuid)
            return response