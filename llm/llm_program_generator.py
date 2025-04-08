from __future__ import annotations
import math
import os
from typing import Dict, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import numpy as np

from llm.prompt_generator import PromptGenerator
from llm.utils import get_program_str_from_llm_response_dsl, get_program_str_from_llm_response_python
from prog_policies.utils import get_env_name
from prog_policies.base import BaseDSL

CHATGPT_KEY = os.getenv("OPENAI_KEY")

class LLMProgramGenerator:
    def __init__(
        self,
        seed: int,
        task: str,
        dsl: BaseDSL,
        llm_program_num: int,
        temperature: float = 1.0,
        top_p: float = 1.0,
    ) -> None:
        self.seed = seed
        self.task = task
        self.env_name = get_env_name(task)
        self.dsl = dsl
        self.ratio = 1.5
        self.llm_program_num = llm_program_num
        self.model_name = "gpt-4-turbo-2024-04-09"
        self.temperature = temperature
        self.top_p = top_p

        self.np_rng = np.random.RandomState(self.seed)

    def _call_llm(
        self,
        system_prompt: str,
        user_prompt: str,
        llm_program_num: int,
    ) -> str | List[str | Dict]:
        chatgpt = ChatOpenAI(
            api_key=CHATGPT_KEY,
            model=self.model_name,
            temperature=self.temperature,
            n=llm_program_num,
            model_kwargs={"top_p": self.top_p},
        )
        response = chatgpt.generate(
            [
                [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=user_prompt),
                ]
            ]
        ).generations[0]

        return list(map(lambda x: x.text, response))

    def _get_program_list_from_llm_response_python_to_dsl(self, response) -> list[str]:
        program_str_list = []
        for x in response:
            tmp = []
            try:
                program_str = get_program_str_from_llm_response_python(x, env_name=self.env_name)
                tmp.append(program_str)
            except:
                pass
            
            try:
                program_str = get_program_str_from_llm_response_dsl(x, env_name=self.env_name)
                tmp.append(program_str)
            except:
                pass
            
            program_str_list.append(tmp)
        return program_str_list
    
    
    def _get_program_list_from_llm_response_python(self, response) -> list[str]:
        program_str_list = []
        for x in response:
            try:
                program_str = get_program_str_from_llm_response_python(x, env_name=self.env_name)
                program_str_list.append(program_str)
            except:
                pass
        return program_str_list
    
    def _get_program_list_from_llm_response_dsl(self, response) -> list[str]:
        program_str_list = []
        for x in response:
            try:
                program_str = get_program_str_from_llm_response_dsl(x, env_name=self.env_name)
                program_str_list.append(program_str)
            except:
                pass
        return program_str_list

    def get_program_list_python_to_dsl(self):
        program_list = []
        record_list = []
        attempts = 0
        program_num = self.llm_program_num
        while len(program_list) < program_num:
            attempts += 1
            seed = self.np_rng.randint(0, 2**32)
            llm_program_num = math.ceil((program_num - len(program_list)) * self.ratio)
            prompt_generator = PromptGenerator(self.task)
            system_prompt = prompt_generator.get_system_prompt_python_to_dsl()
            user_prompt = prompt_generator.get_user_prompt_python_to_dsl()
            llm_response = self._call_llm(system_prompt, user_prompt, llm_program_num)
            program_str_list = self._get_program_list_from_llm_response_python_to_dsl(llm_response)
            for candidates in program_str_list:
                tmp = []
                for candidate in candidates:
                    try:
                        program = self.dsl.parse_str_to_node(candidate)
                        tmp.append(program)
                    except:
                        pass
                if len(tmp) > 0:
                    program_list.append(self.np_rng.choice(tmp))
                    
            available_program_num = len(program_list)
            print(f"Attempts: {attempts}, Program_nums: {available_program_num}")
            
            if len(program_list) > program_num:
                program_list = program_list[:program_num]
            program_str_list = [self.dsl.parse_node_to_str(program) for program in program_list]
            
            record_list.append(
                {
                    "seed": seed,
                    "temperature": self.temperature,
                    "top_p": self.top_p,
                    "system_prompt": system_prompt,
                    "user_prompt": user_prompt,
                    "llm_response": llm_response,
                    "available_program_num": available_program_num,
                    "program_str_list": program_str_list,
                }
            )

        log = {"attemps": attempts, "record_list": record_list}

        return program_list, log
    
    def get_program_list_python(self):
        program_list = []
        record_list = []
        attempts = 0
        program_num = self.llm_program_num
        while len(program_list) < program_num:
            attempts += 1
            seed = self.np_rng.randint(0, 2**32)
            llm_program_num = math.ceil((program_num - len(program_list)) * self.ratio)
            prompt_generator = PromptGenerator(self.task)
            system_prompt = prompt_generator.get_system_prompt_python()
            user_prompt = prompt_generator.get_user_prompt_python()
            llm_response = self._call_llm(system_prompt, user_prompt, llm_program_num)
            program_str_list = self._get_program_list_from_llm_response_python(llm_response)
            for program_str in program_str_list:
                try:
                    program = self.dsl.parse_str_to_node(program_str)
                    program_list.append(program)
                except:
                    pass
                
            available_program_num = len(program_list)
            print(f"Attempts: {attempts}, Program_nums: {available_program_num}")
            
            if len(program_list) > program_num:
                program_list = program_list[:program_num]
            program_str_list = [self.dsl.parse_node_to_str(program) for program in program_list]
            
            record_list.append(
                {
                    "seed": seed,
                    "temperature": self.temperature,
                    "top_p": self.top_p,
                    "system_prompt": system_prompt,
                    "user_prompt": user_prompt,
                    "llm_response": llm_response,
                    "available_program_num": available_program_num,
                    "program_str_list": program_str_list,
                }
            )

        log = {"attemps": attempts, "record_list": record_list}

        return program_list, log
    
    def get_program_list_dsl(self):
        program_list = []
        record_list = []
        attempts = 0
        program_num = self.llm_program_num
        while len(program_list) < program_num:
            attempts += 1
            seed = self.np_rng.randint(0, 2**32)
            llm_program_num = math.ceil((program_num - len(program_list)) * self.ratio)
            prompt_generator = PromptGenerator(self.task)
            system_prompt = prompt_generator.get_system_prompt_dsl()
            user_prompt = prompt_generator.get_user_prompt_dsl()
            llm_response = self._call_llm(system_prompt, user_prompt, llm_program_num)
            program_str_list = self._get_program_list_from_llm_response_dsl(llm_response)
            for program_str in program_str_list:
                try:
                    program = self.dsl.parse_str_to_node(program_str)
                    program_list.append(program)
                except:
                    pass
            
            available_program_num = len(program_list)
            print(f"Attempts: {attempts}, Program_nums: {available_program_num}")
            
            if len(program_list) > program_num:
                program_list = program_list[:program_num]
            program_str_list = [self.dsl.parse_node_to_str(program) for program in program_list]    
            
            record_list.append(
                {
                    "seed": seed,
                    "temperature": self.temperature,
                    "top_p": self.top_p,
                    "system_prompt": system_prompt,
                    "user_prompt": user_prompt,
                    "llm_response": llm_response,
                    "available_program_num": available_program_num,
                    "program_str_list": program_str_list,
                }
            )

        log = {"attemps": attempts, "record_list": record_list}

        return program_list, log

    
