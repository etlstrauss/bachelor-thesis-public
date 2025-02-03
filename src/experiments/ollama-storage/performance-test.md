| Kind  | Type  | Performance | Stripe | Model | Model ID |
|--------|---------|--------------|-----------|-------|-----|
| lvm | raid0 | - | no | llama3.1:70b | c0df3564cfe8 |
| lvm | raid0 | - | no | qwen2.5:72b-instruct-q8_0 | 23f2cb48bb9a |
| lvm | raid1 | - | no | llama3.1:70b | c0df3564cfe8 |
| lvm | raid1 | - | no | qwen2.5:72b-instruct-q8_0 | 23f2cb48bb9a |
| lvm | - | - | yes | llama3.1:70b | c0df3564cfe8 |
| lvm | - | - | yes | qwen2.5:72b-instruct-q8_0 | 23f2cb48bb9a |
| md | raid0 | - | no | llama3.1:70b | c0df3564cfe8 |
| md | raid0 | - | no | qwen2.5:72b-instruct-q8_0 | 23f2cb48bb9a |
| md | raid1 | - | no | llama3.1:70b | c0df3564cfe8 |
| md | raid1 | - | no | qwen2.5:72b-instruct-q8_0 | 23f2cb48bb9a |
| md | - | - | yes | llama3.1:70b | c0df3564cfe8 |
| md | - | - | yes | qwen2.5:72b-instruct-q8_0 | 23f2cb48bb9a |

- notice, that that the models won't be used
- the only benefit is, that we can use the model / image files (found in .ollama/models/blobs) to test the read pace with real data
- to ensure reproducibility you will find a list of the used blobs per models at the end of this file
- this is possible, because the blobs names are their sha256 hashes

| Model | Model ID| blob | 
|--------|---------|----|
| llama3.1:70b | c0df3564cfe8 | sha256-a677b4a4b70c45e702b1d600f7905e367733c53898b8be60e3f29272cf334574 |
| llama3.1:70b | c0df3564cfe8 | sha256-948af2743fc78a328dcb3b0f5a31b3d75f415840fdb699e8b1235978392ecf85 |
| llama3.1:70b | c0df3564cfe8 | sha256-0ba8f0e314b4264dfd19df045cde9d4c394a52474bf92ed6a3de22a4ca31a177 |
| llama3.1:70b | c0df3564cfe8 | sha256-56bb8bd477a519ffa694fc449c2413c6f0e1d3b1c88fa7e3c9d88d3ae49d4dcb |
| llama3.1:70b | c0df3564cfe8 | sha256-654440dac7f3ad911ccb39b7e42e2a0228833641b601937134aa3e4b7a389ad7 |
| qwen2.5:72b-instruct-q8_0 | 23f2cb48bb9a | sha256-dd60673d4ffd5da5dc4f9f02c9ffb4a27e5a431a718a9b6244376b35346909f4 |
| qwen2.5:72b-instruct-q8_0 | 23f2cb48bb9a | sha256-66b9ea09bd5b7099cbb4fc820f31b575c0366fa439b08245566692c6784e281e |
| qwen2.5:72b-instruct-q8_0 | 23f2cb48bb9a | sha256-eb4402837c7829a690fa845de4d7f3fd842c2adee476d5341da8a46ea9255175 |
| qwen2.5:72b-instruct-q8_0 | 23f2cb48bb9a | sha256-b5c0e5cf74cf51af1ecbc4af597cfcd13fd9925611838884a681070838a14a50 |
| qwen2.5:72b-instruct-q8_0 | 23f2cb48bb9a | sha256-13dd1e2033e70e07df0a64a8b3a022618b31ec93e6341869f18822e94263cb8e |

