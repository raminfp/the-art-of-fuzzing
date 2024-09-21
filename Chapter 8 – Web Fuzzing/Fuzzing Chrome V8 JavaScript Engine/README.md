# Fuzzing V8 Engine JavaScript WebAssembly API using Dharma

## Install dharma
``` sh
git clone https://github.com/MozillaSecurity/dharma
pip3 install dharma
python3 -m dharma --help
```

## Install honggfuzz
``` sh
git clone https://github.com/google/honggfuzz
make
```

## Install gsutil
``` sh
curl https://sdk.cloud.google.com | bash
gcloud init
```

## Download Chrome/V8 built with ASan
``` sh
gsutil cp $(gsutil ls "gs://chromium-browser-asan/linux-release/asan-linux-release-*.zip" | tail -1) .
```
