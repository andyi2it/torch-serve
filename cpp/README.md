# TorchServe CPP (Experimental Release)
## Requirements
* C++17
* GCC version: gcc-9
## Installation and Running TorchServe CPP

### Install dependencies
```
cd serve
python ts_scripts/install_dependencies.py --cpp --environment dev [--cuda=cu121|cu118]
```
### Building the backend
```
## Dev Build
cd cpp
./build.sh [-g cu121|cu118]

## Install TorchServe from source
cd ..
python ts_scripts/install_from_src.py
```
### Run TorchServe
```
mkdir model_store
torchserve --ncs --start --model-store model_store
```
## Backend
TorchServe cpp backend can run as a process, which is similar to [TorchServe Python backend](https://github.com/pytorch/serve/tree/master/ts). By default, TorchServe supports torch scripted model in cpp backend. Other platforms such as MxNet, ONNX can be supported through custom handlers following the TorchScript example [src/backends/handler/torch_scripted_handler.hh](https://github.com/pytorch/serve/blob/master/cpp/src/backends/handler/torch_scripted_handler.hh).
### Custom Handler
By default, TorchServe cpp provides a handler for TorchScript [src/backends/handler/torch_scripted_handler.hh](https://github.com/pytorch/serve/blob/master/cpp/src/backends/handler/torch_scripted_handler.hh). Its uses the [BaseHandler](https://github.com/pytorch/serve/blob/master/cpp/src/backends/handler/base_handler.hh) which defines the APIs to customize handler.
* [Initialize](https://github.com/pytorch/serve/blob/ba8f96a6e68ca7f63b55d72a21aad364334e4d8e/cpp/src/backends/handler/base_handler.hh#L34)
* [LoadModel](https://github.com/pytorch/serve/blob/ba8f96a6e68ca7f63b55d72a21aad364334e4d8e/cpp/src/backends/handler/base_handler.hh#L41)
* [Preprocess](https://github.com/pytorch/serve/blob/ba8f96a6e68ca7f63b55d72a21aad364334e4d8e/cpp/src/backends/handler/base_handler.hh#L43)
* [Inference](https://github.com/pytorch/serve/blob/ba8f96a6e68ca7f63b55d72a21aad364334e4d8e/cpp/src/backends/handler/base_handler.hh#L49)
* [Postprocess](https://github.com/pytorch/serve/blob/ba8f96a6e68ca7f63b55d72a21aad364334e4d8e/cpp/src/backends/handler/base_handler.hh#L55)
#### Usage
##### Using TorchScriptHandler
* set runtime as "LSP" in model archiver option [--runtime](https://github.com/pytorch/serve/tree/master/model-archiver#arguments)
* set handler as "TorchScriptHandler" in model archiver option [--handler](https://github.com/pytorch/serve/tree/master/model-archiver#arguments)
```
 torch-model-archiver --model-name mnist_base --version 1.0 --serialized-file mnist_script.pt --handler TorchScriptHandler --runtime LSP
```
Here is an [example](https://github.com/pytorch/serve/tree/master/cpp/test/resources/examples/mnist/base_handler) of unzipped model mar file.
##### Using Custom Handler
* build customized handler shared lib. For example [Mnist handler](https://github.com/pytorch/serve/blob/cpp_backend/cpp/src/examples/image_classifier/mnist).
* set runtime as "LSP" in model archiver option [--runtime](https://github.com/pytorch/serve/tree/master/model-archiver#arguments)
* set handler as "libmnist_handler:MnistHandler" in model archiver option [--handler](https://github.com/pytorch/serve/tree/master/model-archiver#arguments)
```
torch-model-archiver --model-name mnist_handler --version 1.0 --serialized-file mnist_script.pt --handler libmnist_handler:MnistHandler --runtime LSP
```
Here is an [example](https://github.com/pytorch/serve/tree/master/cpp/test/resources/examples/mnist/mnist_handler) of unzipped model mar file.

#### Examples
We have created a couple of examples that can get you started with the C++ backend.
The examples are all located under serve/examples/cpp and each comes with a detailed description of how to set it up.
The following examples are available:
* [AOTInductor Llama](../examples/cpp/aot_inductor/llama2/)
* [BabyLlama](../examples/cpp/babyllama/)
* [Llama.cpp](../examples/cpp/llamacpp/)
* [MNIST](../examples/cpp/mnist/)

#### Developing
When making changes to the cpp backend its inconvenient to reinstall TorchServe using ts_scripts/install_from_src.py after every compilation.
To automatically update the model_worker_socket located in ts/cpp/bin/ we can install TorchServe once from source with the `--environment dev`.
This will make the TorchServe installation editable and the updated cpp backend binary is automatically picked up when starting a worker (No restart of TorchServe required).
```
python ts_scripts/install_from_src.py --environment dev
```
