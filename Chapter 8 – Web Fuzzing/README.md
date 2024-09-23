# Chapter 8 – Web Fuzzing

This chapter delves into various techniques and tools for fuzzing web applications, with a special focus on JavaScript engines, web parsers, and compression algorithms. The examples are based on real-world scenarios, as seen in the directory structure.

## Introduction to Web Fuzzing

An overview of web fuzzing, its importance in securing web applications, and the tools and techniques commonly used to find vulnerabilities in web technologies.

## Fuzzing Demo

### Web Fuzzing Tools and Frameworks

1. **Decompress Fuzzing**
   
   Exploring the `decompress_fuzzing` directory to understand how to fuzz decompression algorithms.

   - Setting up fuzzing tools for decompression testing
   - Crafting inputs that stress-test decompression logic
   - Detecting vulnerabilities in various compression formats

2. **Fuzzing Chrome V8 JavaScript Engine**
   
   An in-depth analysis of the `fuzzing_chrome_v8` directory to fuzz the Chrome V8 JavaScript engine.

   - Introduction to the architecture of Chrome V8
   - Writing fuzz targets for JavaScript execution environments
   - Identifying memory corruption and security flaws in JavaScript engines

3. **Fuzzing JavaScript Libraries with JSFuzz**

   An examination of the `fuzzing_javascript_jsfuzz` directory to fuzz JavaScript libraries using JSFuzz.

   - Setting up JSFuzz for JavaScript fuzzing
   - Writing fuzz targets for complex JavaScript applications
   - Identifying cross-site scripting (XSS) and injection vulnerabilities

4. **Wast-Parser Fuzzing**

   Exploring the `wast-parser_fuzzing` directory to fuzz WebAssembly text (WAST) parsers.

   - Crafting fuzz inputs for WebAssembly
   - Uncovering bugs in WebAssembly parsers and runtimes
   - Testing the security of WebAssembly components in modern browsers

## Comparative Analysis and Advanced Techniques

5. **Decompression Fuzzing: Chrome V8 vs. Other Tools**
   
   A comparative analysis between different fuzzing techniques and tools used for Chrome V8 and decompression algorithms.

   - Assessing the strengths and weaknesses of various fuzzing approaches
   - Performance comparisons for different decompression fuzzers
   - Best practices for fuzzing JavaScript engines and compression libraries

6. **Fuzzing WebAssembly Parsers**

   A deep dive into WebAssembly parser fuzzing, comparing various fuzzing tools and their effectiveness.

   - Coverage analysis of WebAssembly parser fuzzers
   - Identifying areas where fuzzing can improve the robustness of WebAssembly runtimes

## Best Practices and Guidelines

7. **Writing Effective Web Fuzz Targets**

   Best practices for writing fuzz targets that effectively test web applications, parsers, and JavaScript engines.

   - Strategies for maximizing code coverage in web fuzzing
   - Common pitfalls in writing fuzz targets for web technologies
   - Techniques to fuzz different types of web-related libraries

8. **Integrating Web Fuzzing into Development Workflows**

   Guidelines for incorporating fuzzing into web development and testing processes.

   - Automating fuzzing in web CI/CD pipelines
   - Combining unit testing with fuzz testing for web applications
   - Encouraging web developers to adopt fuzzing as a routine part of security testing

## Performance Optimization in Web Fuzzing

Techniques for improving the speed and efficiency of web fuzzing.

- Profiling web fuzz targets for performance bottlenecks
- Optimizing fuzz targets for JavaScript and WebAssembly engines
- Parallelizing fuzzing tasks for large-scale web applications

## Conclusion

A summary of the key takeaways from web fuzzing techniques and best practices, along with a discussion on the future of fuzzing in the web ecosystem. This includes the role of fuzzing in ensuring the security and stability of modern web applications and engines.


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

