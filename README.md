# ollama-auto-create

**ollama-auto-create** automates the process of downloading a model from Huggingface, converting it into a GGUF file, and then creating a model in Ollama that uses this file. The script is designed to work in a Windows environment and requires Python 3.10 or higher. **[llama.cpp](https://github.com/ggerganov/llama.cpp)** used for converting models into GGUF format.

## Requirements

-   **Windows OS**
-   **Python 3.10 or higher**
-   **Ollama installed locally** on your system

## Installation

```
git clone https://github.com/nagix999/ollama-auto-create.git
cd ollama-auto-create
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

You can run the script with the following command:

```
python ollama_auto_create.py --repo_id <Huggingface-Repo-ID> --fm <Foundation-Model>
```

`<Huggingface-Repo-ID>`: The repository ID of the model you want to download from Huggingface. For example: hyunseoki/ko-ref-llama2-7b

`<Foundation-Model>`: The name of the foundation model you want to use in Ollama. For example: llama2

## Process

1. **Download Model**: The script downloads the model corresponding to the provided repo_id from Huggingface.
2. **Convert Model**: The downloaded model is converted into a GGUF file, with quantization set to q8_0.
3. **Create Modelfile**: The script generates a Modelfile based on the specified foundation model (fm) for use in Ollama.
4. **Create Model in Ollama**: Finally, the GGUF file and Modelfile are used to create a model in Ollama.

## TODO

1. **Cross-Platform Compatibility**: Update the script to work seamlessly across different operating systems (e.g., Linux, macOS, Windows) rather than being limited to Windows.

2. **Add Logging**: Implement a logging system to track the execution process, errors, and other relevant information for better debugging and monitoring.

3. **Add CLI Arguments**: Introduce additional command-line arguments for more flexibility and control, such as setting output paths, specifying quantization levels, or toggling features.
