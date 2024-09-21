# Fuzzing Go package using go-fuzz

## Install go-fuzz
``` sh
# check here to install golang
# https://golang.org/doc/install

# install go-fuzz
# https://github.com/dvyukov/go-fuzz
go get -u github.com/dvyukov/go-fuzz/go-fuzz github.com/dvyukov/go-fuzz/go-fuzz-build
```

## Compilation
``` sh
# Generate an archive file for libfuzzer
go-fuzz-build -libfuzzer -o gif.a .

# Compile your library with libfuzzer
clang -fsanitize=fuzzer gif.a -o fuzz_gif

# create an input_corpora folder
mkdir input_corpora

# run the fuzzer
./fuzz_gif input_corpora
```

## Going deeper

Search for good GIF input files like:
- https://github.com/strongcourage/fuzzing-corpus/tree/master/gif
- https://github.com/dvyukov/go-fuzz-corpus/tree/master/gif

Understand the GIF format:
- https://en.wikipedia.org/wiki/GIF
- https://github.com/corkami/pics/blob/master/binary/GIF.png
