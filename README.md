# 🦙 LLaWa: TinyLLaMA WebAssembly In-Browser LLM

This project brings a quantized [TinyLLaMA-1.1B](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0) model to the browser using [llama.cpp](https://github.com/ggerganov/llama.cpp) compiled to WebAssembly with [Emscripten](https://emscripten.org/). It runs entirely client-side — no server, no Python backend, just JavaScript and WASM.

## 🚀 Features

- Fully client-side LLM inference in the browser
- Built with `llama.cpp` and compiled via `emcc`
- Uses quantized GGUF model (e.g., `Q4_K_M`)
- Swappable model support planned

## 🛠️ Setup Instructions

### 1. Clone this repo and install dependencies

```bash
git clone https://github.com/yourname/llawa.git
cd llawwa
```

### 2. Install Emscripten

```bash
git clone https://github.com/emscripten-core/emsdk.git
cd emsdk
./emsdk install latest
./emsdk activate latest
source ./emsdk_env.sh
cd ..
```

### 3. Clone `llama.cpp` (outside this repo)

```bash
git clone https://github.com/ggerganov/llama.cpp.git
```

_Note: llama.cpp is ignored via `.gitignore` and expected to live outside your repo directory._

## 🔨 Build Instructions

### Compile GGML C dependencies:

```bash
emcc -O3 -Iinclude -Iggml/include -Isrc -Icommon -c ggml/src/ggml.c -o ggml.o
emcc -O3 -Iinclude -Iggml/include -Isrc -Icommon -c ggml/src/ggml-alloc.c -o ggml-alloc.o
emcc -O3 -Iinclude -Iggml/include -Isrc -Icommon -c ggml/src/ggml-quants.c -o ggml-quants.o
```

### Compile the full WebAssembly module:

```bash
em++ -O3 -std=c++17 \
  -s USE_PTHREADS=1 \
  -s PTHREAD_POOL_SIZE=4 \
  -s ALLOW_MEMORY_GROWTH=1 \
  -s MODULARIZE=1 \
  -s EXPORT_NAME="llama" \
  -s EXPORTED_FUNCTIONS=_main \
  -s EXPORTED_RUNTIME_METHODS=ccall,cwrap \
  -Iinclude -Iggml/include -Isrc -Icommon -Iggml/src \
  wasm_main.cpp \
  src/llama.cpp \
  src/llama-util.cpp \
  src/llama-log.cpp \
  src/llama-model.cpp \
  src/llama-kv-cache.cpp \
  src/llama-sampling.cpp \
  src/llama-batched.cpp \
  ggml/src/ggml-backend.cpp \
  ggml-alloc.o ggml-quants.o ggml.o \
  -o llama.js
```

## 🧪 Usage

Serve the generated `llama.js` and `llama.wasm` using a static web server:

```bash
python3 -m http.server
```

Open `index.html` in your browser. Make sure your GGUF model is available in the virtual FS or fetched from the web.

## 🧠 Model Info

Model used:

- [`TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf`](https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF)
- Format: GGUF
- Size: ~480MB
- Quantized (runs in-browser without GPU)

You can swap in other small GGUF-compatible models later.

## 📂 Project Structure

/
├── src/                 # llama.cpp source files
├── ggml/                # Tensor/math backend
├── wasm_main.cpp        # WASM entrypoint
├── llama.js             # Emscripten JS glue output
├── index.html           # Basic UI
├── .gitignore
└── README.md

## 📜 License

MIT License. llama.cpp is also licensed under MIT.

## 🙏 Credits

- [ggerganov/llama.cpp](https://github.com/ggerganov/llama.cpp)
- [TinyLLaMA](https://huggingface.co/TinyLlama)
- [TheBloke](https://huggingface.co/TheBloke) for quantized model releases
