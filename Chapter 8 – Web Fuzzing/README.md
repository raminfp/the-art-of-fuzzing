# Fuzzing JavaScript npm/nodejs/code using jsfuzz

## Install jsfuzz
``` sh
# Install the project
npm i jsfuzz

# More info here:
## https://gitlab.com/gitlab-org/security-products/analyzers/fuzzers/jsfuzz
```

## Choose your target (omggif)

omggif is a JavaScript implementation of a GIF 89a encoder and decoder.

npm: https://www.npmjs.com/package/omggif
github: https://github.com/deanm/omggif


## Create your fuzz target

omggif code example: https://github.com/deanm/omggif/blob/master/example_node.js

jsfuzz target example: https://gitlab.com/gitlab-org/security-products/analyzers/fuzzers/jsfuzz/-/blob/master/examples/jpeg/fuzz.js

``` javascript
var omggif = require('omggif');

function fuzz(data) {
    try {
        var gr = new omggif.GifReader(data);
    } catch (e) {
        if (e.message.indexOf('Invalid GIF') !== -1  ||
            e.message.indexOf('Invalid') !== -1  ||
            //e.message.indexOf('Cannot read property') !== -1  ||
            //e instanceof TypeError ||
            e.message.indexOf('Unknown') !== -1) {
        } else {
            throw e;
        }
    }
}

module.exports = {
    fuzz
};
```

## Run the fuzzer

``` sh
jsfuzz fuzz_omggif.js corpus_omggif
#0 READ units: 38
#1 NEW     cov: 58 corp: 39 exec/s: 2 rss: 37.94 MB
#2 NEW     cov: 60 corp: 40 exec/s: Infinity rss: 37.94 MB
#4 NEW     cov: 89 corp: 41 exec/s: 2000 rss: 38.04 MB
#5 NEW     cov: 95 corp: 42 exec/s: Infinity rss: 38.04 MB
#7 NEW     cov: 122 corp: 43 exec/s: 2000 rss: 38.04 MB
#11 NEW     cov: 132 corp: 44 exec/s: 4000 rss: 38.04 MB
#13 NEW     cov: 135 corp: 45 exec/s: Infinity rss: 38.04 MB
#15 NEW     cov: 144 corp: 46 exec/s: 2000 rss: 38.04 MB
#18 NEW     cov: 148 corp: 47 exec/s: Infinity rss: 38.04 MB
#20 NEW     cov: 151 corp: 48 exec/s: 2000 rss: 38.04 MB
#22 NEW     cov: 153 corp: 49 exec/s: Infinity rss: 38.04 MB
#23 NEW     cov: 154 corp: 50 exec/s: Infinity rss: 38.04 MB
#24 NEW     cov: 157 corp: 51 exec/s: 1000 rss: 38.04 MB
#27 NEW     cov: 162 corp: 52 exec/s: Infinity rss: 38.04 MB
#29 NEW     cov: 164 corp: 53 exec/s: 2000 rss: 38.04 MB
#31 NEW     cov: 166 corp: 54 exec/s: Infinity rss: 38.04 MB
#38 NEW     cov: 168 corp: 55 exec/s: 7000 rss: 38.04 MB
#39760 PULSE     cov: 168 corp: 55 exec/s: 15712 rss: 40.95 MB
[...]
```

## TypeError: Cannot read property 'toString' of undefined

``` sh
TypeError: Cannot read property 'toString' of undefined
    at new GifReader (/home/fuzz/node_modules/omggif/omggif.js:1:72365)
    at Worker.fuzz [as fn] (/home/fuzz/Documents/projects/fuzzing_javascript_jsfuzz/fuzz_omggif.js:1:1747)
    at process.<anonymous> (/home/fuzz/Documents/webassembly/emsdk/node/12.18.1_64bit/lib/node_modules/jsfuzz/build/src/worker.js:55:30)
    at process.emit (events.js:315:20)
    at emit (internal/child_process.js:876:12)
    at processTicksAndRejections (internal/process/task_queues.js:85:21)
crash was written to crash-43ae95899e8a3875e5b1ebcc488fb84bfecde96f1e8a841ff4b1218fd2517841
crash(hex)=47494638396146baf789385ff221
Worker exited

```

## Reproduce the bug

Reproducer:
``` javascript
var omggif = require('omggif');

data = Buffer.from('47494638396146baf789385ff221', 'hex')

omggif.GifReader(data);
````

Crash:
``` sh
$ nodejs repro_omggif_TypeError.js             scop@scop
/home/scop/node_modules/omggif/omggif.js:459
                "Unknown graphic control label: 0x" + buf[p-1].toString(16));
                                                               ^

TypeError: Cannot read property 'toString' of undefined
    at Object.GifReader (/home/scop/node_modules/omggif/omggif.js:459:64)
    at Object.<anonymous> (/home/scop/Documents/projects/fuzzing_javascript_jsfuzz/repro_omggif_TypeError.js:5:8)
    at Module._compile (internal/modules/cjs/loader.js:778:30)
    at Object.Module._extensions..js (internal/modules/cjs/loader.js:789:10)
    at Module.load (internal/modules/cjs/loader.js:653:32)
    at tryModuleLoad (internal/modules/cjs/loader.js:593:12)
    at Function.Module._load (internal/modules/cjs/loader.js:585:3)
    at Function.Module.runMain (internal/modules/cjs/loader.js:831:12)
    at startup (internal/bootstrap/node.js:283:19)
    at bootstrapNodeJSCore (internal/bootstrap/node.js:623:3)
```

