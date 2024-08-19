import json
from collections.abc import Iterable

from src.ollama.model import get_all_ollama_models, get_model_info


class ModelFileBuilder:
    def __init__(self, foundation_model, gguf_path):
        self._is_valid_fm(foundation_model)
        self.foundation_model = foundation_model
        self.gguf_path = gguf_path
        self.model_info = self._get_foundation_model_info(foundation_model)
        self._modelfile = []

    @property
    def modelfile(self):
        return "\n".join(self._modelfile)
    
    def build(self):
        if self._modelfile:
            self._modelfile = []

        self._modelfile.append(f"FROM {self.gguf_path}\n")
        
        if "template" in self.model_info:
            self._modelfile.append(f"""TEMPLATE "{self.model_info['template']}"\n""")

        if "params" in self.model_info:
            params = json.loads(self.model_info["params"])
            
            for key in params:
                if isinstance(params[key], Iterable):
                    for value in params[key]:
                        self._modelfile.append(f"PARAMETER {key} {value}")
                else:
                    self._modelfile.append(f"PARAMETER {key} {params[key]}")
            return self
    
    def save_modelfile(self, save_path):
        with open(save_path, "w") as f:
            f.write(self.modelfile)

    def _is_valid_fm(self, foundation_model):
        ollama_models = get_all_ollama_models()
        if foundation_model not in ollama_models:
            raise ValueError(f"{foundation_model} is not valid foundation model. refer to https://ollama.com/library")
        return True
    
    def _get_foundation_model_info(self, foundation_model):
        model_info = get_model_info(foundation_model)
        return model_info
    

if __name__ == "__main__":
    mfb = ModelFileBuilder(foundation_model="llama3", gguf_path="./test.gguf").build()
    print(mfb.modelfile)

    if mfb.modelfile:
        mfb.save_modelfile("./Modelfile")