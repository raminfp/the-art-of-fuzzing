# Fuzzing Java code using Jazzer 

## Install Jazzer
``` sh
# clone the fuzzer project
git clone --depth 1 --recursive https://github.com/CodeIntelligenceTesting/jazzer

# install jazzer
cd jazzer
bazel run //:jazzer

# help for install
# https://github.com/CodeIntelligenceTesting/jazzer#installation
```

## Choose your target (jsoup)

target: jsoup: Java HTML Parser
github: https://github.com/jhy/jsoup
maven: https://mvnrepository.com/artifact/org.jsoup/jsoup

## Create your fuzz target

jsoup code example: https://github.com/jhy/jsoup/blob/master/src/test/java/org/jsoup/parser/HtmlParserTest.java

jazzer target example: https://github.com/CodeIntelligenceTesting/jazzer/blob/main/examples/src/main/java/com/example/FastJsonFuzzer.java

``` java

package com.example;

import org.jsoup.Jsoup;
import com.code_intelligence.jazzer.api.FuzzedDataProvider;

public class JSoupFuzzer {
  public static void fuzzerTestOneInput(FuzzedDataProvider data) {
    try {
      Jsoup.parse(data.consumeRemainingAsString());
    } catch (IllegalArgumentException ignored) {
    }
  }
}
```

## Modify maven/bazel configs

### Slow method

Add `"org.jsoup:jsoup:1.13.1"` inside `maven.bzl`:
``` sh
diff --git a/maven.bzl b/maven.bzl
index 621faac..460dc39 100644
--- a/maven.bzl
+++ b/maven.bzl
@@ -28,4 +28,5 @@ MAVEN_ARTIFACTS = [
     "com.fasterxml.jackson.dataformat:jackson-dataformat-cbor:2.12.1",
     "com.alibaba:fastjson:1.2.75",
     "com.beust:klaxon:5.5",
+    "org.jsoup:jsoup:1.13.1",
 ]

```

Add the following to `examples/BUILD.bazel`:
``` sh
java_fuzz_target_test(
    name = "JSoupFuzzer",
    srcs = [
        "src/main/java/com/example/JSoupFuzzer.java",
    ],
    target_class = "com.example.JSoupFuzzer",
    deps = [
        "@maven//:org_jsoup_jsoup",
    ],
)
```

### Fast method

Copy the files I'm providing using this command:
``` sh
cd jazzer
cp ../maven.bzl .
cp ../BUILD.bazel examples/BUILD.bazel
cp ../JSoupFuzzer.java examples/src/main/java/com/example/
```

## Run the fuzzer

``` sh
# rebuild maven cache
REPIN=1 bazel run @unpinned_maven//:pin

# run the fuzzer for jsoup
./bazelisk-linux-amd64 run //examples:JSoupFuzzer

# create a corpora folder
mkdir input_jsoup

# Launch the fuzzer with the corpora
./bazelisk-linux-amd64 run //examples:JSoupFuzzer -- /home/user/jazzer/input_jsoup
```

## java.lang.IllegalArgumentException 

``` sh
== Java Exception: java.lang.IllegalArgumentException: String must not be empty
  at org.jsoup.helper.Validate.notEmpty(Validate.java:92)
  at org.jsoup.nodes.Node.absUrl(Node.java:180)
  at org.jsoup.nodes.Node.attr(Node.java:72)
  at org.jsoup.nodes.Node.absUrl(Node.java:185)
  at org.jsoup.nodes.Node.hasAttr(Node.java:105)
  at org.jsoup.parser.HtmlTreeBuilderState$7.inBodyStartTag(HtmlTreeBuilderState.java:357)
  at org.jsoup.parser.HtmlTreeBuilderState$7.process(HtmlTreeBuilderState.java:282)
  at org.jsoup.parser.HtmlTreeBuilder.process(HtmlTreeBuilder.java:136)
  at org.jsoup.parser.TreeBuilder.runParser(TreeBuilder.java:66)
  at org.jsoup.parser.TreeBuilder.parse(TreeBuilder.java:47)
  at org.jsoup.parser.Parser.parse(Parser.java:107)
  at org.jsoup.Jsoup.parse(Jsoup.java:58)
  at com.example.JSoupFuzzer.fuzzerTestOneInput(JSoupFuzzer.java:14)
DEDUP_TOKEN: 39fdca2dbdec18ac
== libFuzzer crashing input ==
MS: 2 ShuffleBytes-CMP- DE: "abs:"-; base unit: 5a76a6c6b4be62f44682b7721fab8b543aa749d3
0x3c,0x1f,0x3c,0x62,0x6f,0x64,0x79,0x9,0x11,0x0,0x0,0xc,0xd,0x0,0x19,0x79,0x9,0x61,0x62,0x73,0x3a,0x0,0x0,0x0,0xc,0x41,0xf4,0xbe,0xc3,0x8f,0xff,0xc8,0x79,0x9,0x61,0x62,0x73,0x3a,0xc,0x41,0x3c,0x70,0xc,0xd,0x0,0x41,0x79,0x9,0x61,0x41,0x79,0x9,0x11,0x0,0x0,0xc,0xd,0x0,0x41,0x79,0x9,0x61,0x62,0x73,0x3a,0x0,0x0,0x0,0xc,0x41,0xf4,0xbe,0xc3,0x8f,0xf3,0xf2,0xff,0xc8,0x79,0x9,0x61,0x62,0x73,0x3a,0x61,0x62,0x73,0x3a,0xc,0x41,0x3c,0x70,0xc,0x1f,0x3c,0xd,0x0,0xf2,0xff,0xc8,0x79,0x9,0x61,0x62,0x73,0x2a,0x9,0x61,0x62,0x73,0x3a,0x2f,0x3c,
<\x1f<body\x09\x11\x00\x00\x0c\x0d\x00\x19y\x09abs:\x00\x00\x00\x0cA\xf4\xbe\xc3\x8f\xff\xc8y\x09abs:\x0cA<p\x0c\x0d\x00Ay\x09aAy\x09\x11\x00\x00\x0c\x0d\x00Ay\x09abs:\x00\x00\x00\x0cA\xf4\xbe\xc3\x8f\xf3\xf2\xff\xc8y\x09abs:abs:\x0cA<p\x0c\x1f<\x0d\x00\xf2\xff\xc8y\x09abs*\x09abs:/<
```

## java.lang.NullPointerException

``` sh
== Java Exception: java.lang.NullPointerException
  at org.jsoup.parser.HtmlTreeBuilderState$9.process(HtmlTreeBuilderState.java:934)
  at org.jsoup.parser.HtmlTreeBuilder.process(HtmlTreeBuilder.java:136)
  at org.jsoup.parser.TreeBuilder.runParser(TreeBuilder.java:66)
  at org.jsoup.parser.TreeBuilder.parse(TreeBuilder.java:47)
  at org.jsoup.parser.Parser.parse(Parser.java:107)
  at org.jsoup.Jsoup.parse(Jsoup.java:58)
  at com.example.JSoupFuzzer.fuzzerTestOneInput(JSoupFuzzer.java:14)
DEDUP_TOKEN: 9e9179ac336f418f
== libFuzzer crashing input ==
MS: 1 CrossOver-; base unit: 3a83a71f96b11e0b444cf18410e33a8f508156a5

```
