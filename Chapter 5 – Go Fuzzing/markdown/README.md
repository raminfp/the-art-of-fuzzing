#### go-fuzz example

```bash

$ go get github.com/dvyukov/go-fuzz/go-fuzz
$ go get github.com/dvyukov/go-fuzz/go-fuzz-build



$ nano fuzz.go

// +build gofuzz

package markdown

// Fuzz function to be used by https://github.com/dvyukov/go-fuzz
func Fuzz(data []byte) int {
    Parse(data, nil)
    return 0
}

# create a working directory for the fuzzer
$ mkdir -p fuzz-workdir

# copy the files that seed fuzzing to corpus sub-directory of working directory
$ mkdir -p fuzz-workdir/corpus
$ cp testdata/*.text fuzz-workdir/corpus

# generate the fuzzing program. This compiles fuzz.go we wrote earlier
# generates fuzzer executable and markdown-fuzz.zip that packages
# data to drive fuzzing process
$ go-fuzz-build github.com/gomarkdown/markdown




$ go-fuzz -bin=./markdown-fuzz.zip -workdir=fuzz-workdir


Fixed : https://github.com/gomarkdown/markdown/commit/5dd4b50fe81eda60f173e242ece05f24c5cc5cec
```