# from typing import Any, Dict, Iterator, List, Mapping, Optional

# from langchain_core.callbacks.manager import CallbackManagerForLLMRun
# from langchain_core.language_models.llms import LLM
# from langchain_core.outputs import GenerationChunk

# class OpenRouterLLM(LLM):
#     n:int
    
#     def _call(
#         self,
#         prompt: str,
#         stop: Optional[List[str]] = None,
#         run_manager: Optional[CallbackManagerForLLMRun] = None,
#         **kwargs: Any,
#     ) -> str:
#         if stop is not None:
#             raise ValueError("stop kwargs are not permitted.")
#         return prompt[: self.n]
            
#     @property
#     def _identifying_params(self) -> Dict[str, Any]:
#         return {
#             "model_name": ""
#         }
        
#     @property
#     def _llm_type(self) -> str:
#         """Get the type of language model used by this chat model. Used for logging purposes only."""
#         return "custom"