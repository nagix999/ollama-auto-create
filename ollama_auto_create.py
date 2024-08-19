import os
import subprocess

import click
from huggingface_hub import snapshot_download
from src.ollama.modelfile import ModelFileBuilder


def download_hf_model(repo_id, model_name, cache_dir, token):
    absolute_path = snapshot_download(
        repo_id=repo_id,
        cache_dir=cache_dir,
        local_dir=f"./models/huggingface/{model_name}",
        token=token,
        local_dir_use_symlinks=False, 
        revision="main"
    )
    return absolute_path

@click.command()
@click.option("--repo_id", help="A user or an organization name and a repo name separated by a /")
@click.option("--cache_dir", help="Path to the folder where cached files are stored.")
@click.option("--token", help="A token to be used for the download.")
@click.option("--fm", help="input foundation model to create Modelfile")
@click.option("--rm", is_flag=True, default=False)
def main(repo_id: str, cache_dir: str | None, token: str | None, fm: str, rm: bool):
    venv_path = "./venv"
    python_executable = os.path.join(venv_path, "Scripts", "python.exe")

    model_name = repo_id.split("/")[-1]
    absolute_path = download_hf_model(repo_id, model_name, cache_dir, token)
    gguf_path = f"./models/gguf/{model_name}.gguf"
    modelfile_path = f"./modelfiles/Modelfile_{model_name}"
    
    process = subprocess.Popen(
        [python_executable, "-u", f"./llama.cpp/convert_hf_to_gguf.py", absolute_path, "--outfile", gguf_path, "--outtype", "q8_0"], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
    )
    
    stdout, stderr = process.communicate()
    print(stdout.decode())
    print(stderr.decode())

    mfb = ModelFileBuilder(fm, gguf_path).build()
    if mfb.modelfile:
        mfb.save_modelfile(modelfile_path)

    process = subprocess.Popen(
        ["ollama", "create", model_name, "-f", modelfile_path], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
    )

    stdout, stderr = process.communicate()
    print(stdout.decode())
    print(stderr.decode())
    

if __name__ == "__main__":
    main()