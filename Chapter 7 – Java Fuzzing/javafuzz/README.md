
# Javafuzz: coverage-guided fuzz testing for Java

Javafuzz is coverage-guided [fuzzer](https://developer.mozilla.org/en-US/docs/Glossary/Fuzzing) 
for testing Java packages.

Fuzzing for safe languages like nodejs is a powerful strategy for finding bugs like unhandled exceptions, logic bugs,
security bugs that arise from both logic bugs and Denial-of-Service caused by hangs and excessive memory usage.

Fuzzing can be seen as a powerful and efficient strategy in real-world software in addition to classic unit-tests.

## Usage

### Fuzz Target

The first step is to implement the following function (also called a fuzz target):

```java
public class FuzzExample extends AbstractFuzzTarget {
    public void fuzz(byte[] data) {
        try {
            BufferedImage image = ImageIO.read(new ByteArrayInputStream(data));
        } catch (IOException e) {
            // ignore as we expect this exception
        }
    }
}
```


### Installing
Add this to your `pom.xml`

```yaml
  <dependencies>
    <dependency>
      <groupId>dev.fuzzit.javafuzz</groupId>
      <artifactId>core</artifactId>
      <version>1.23-SNAPSHOT</version>
      <scope>test</scope>
    </dependency>
  </dependencies>

<plugin>
        <plugin>
          <groupId>dev.fuzzit.javafuzz</groupId>
          <artifactId>javafuzz-maven-plugin</artifactId>
          <version>1.22</version>
        </plugin>
</plugins>
```


### Running

The next step is to javafuzz with your fuzz target function


```bash
docker run -it maven:3.6.2-jdk-11 /bin/bash
cd javafuzz
mvn install
cd examples
cp javafuzz\javafuzz-maven-plugin\src\main\resources\jacocoagent-exp.jar jacocoagent.jar
MAVEN_OPTS="-javaagent:jacocoagent.jar" mvn javafuzz:fuzz -DclassName=dev.fuzzit.javafuzz.examples.FuzzYaml
```


```bash


# Output:
#0 READ units: 0
#1 NEW     cov: 61 corp: 0 exec/s: 1 rss: 23.37 MB
#23320 PULSE     cov: 61 corp: 1 exec/s: 10614 rss: 35.3 MB
#96022 NEW     cov: 70 corp: 1 exec/s: 11320 rss: 129.95 MB
#96971 NEW     cov: 78 corp: 2 exec/s: 10784 rss: 129.95 MB
#97046 NEW     cov: 79 corp: 3 exec/s: 9375 rss: 129.95 MB
#97081 NEW     cov: 81 corp: 4 exec/s: 11666 rss: 129.95 MB
#97195 NEW     cov: 93 corp: 5 exec/s: 9500 rss: 129.95 MB
#97216 NEW     cov: 97 corp: 6 exec/s: 10500 rss: 129.95 MB
#97238 NEW     cov: 102 corp: 7 exec/s: 11000 rss: 129.95 MB
#97303 NEW     cov: 108 corp: 8 exec/s: 10833 rss: 129.96 MB
#97857 PULSE     cov: 108 corp: 9 exec/s: 225 rss: 129.96 MB
#97857 PULSE     cov: 108 corp: 9 exec/s: 0 rss: 940.97 MB
#97857 PULSE     cov: 108 corp: 9 exec/s: 0 rss: 1566.01 MB
```

This example quickly finds an infinite hang which takes all the memory in `jpeg-js`.

### Corpus

Javafuzz will generate and test various inputs in an infinite loop. `corpus` is optional directory and will be used to
save the generated testcases so later runs can be started from the same point and provided as seed corpus.

Javafuzz can also start with an empty directory (i.e no seed corpus) though some valid test-cases in the seed corpus
may speed up the fuzzing substantially.  

Javafuzz tries to mimic some of the arguments and output style from [libFuzzer](https://llvm.org/docs/LibFuzzer.html).

More fuzz targets examples (for real and popular libraries) are located under the examples directory and
bugs that were found using those targets are listed in the trophies section.

### Coverage

For coverage instrumentation we use [JaCoCo library](https://github.com/jacoco/jacoco)


