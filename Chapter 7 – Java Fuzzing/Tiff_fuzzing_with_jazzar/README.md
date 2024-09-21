#### Tiff Fuzzing with Jazzar





```bash

# ./bazelisk-linux-amd64 run //examples:TiffFuzzer                                                                                                                                                                                 1 ⨯ 2 ⚙
INFO: Analyzed target //examples:TiffFuzzer (0 packages loaded, 0 targets configured).
INFO: Found 1 target...
Target //examples:TiffFuzzer up-to-date:
  bazel-bin/examples/TiffFuzzer
INFO: Elapsed time: 0.228s, Critical Path: 0.09s
INFO: 3 processes: 1 internal, 1 linux-sandbox, 1 worker.
INFO: Build completed successfully, 3 total actions
INFO: Build completed successfully, 3 total actions
exec ${PAGER:-/usr/bin/less} "$0" || exit 1
Executing tests from //examples:TiffFuzzer
-----------------------------------------------------------------------------
Java HotSpot(TM) 64-Bit Server VM warning: Sharing is only supported for boot loader classes because bootstrap classpath has been appended
INFO: Loaded 8 hooks from com.code_intelligence.jazzer.sanitizers.Deserialization
INFO: Loaded 1 hooks from com.code_intelligence.jazzer.sanitizers.ReflectiveCall
INFO: Loaded 8649 no-throw method signatures
INFO: Instrumented com.example.TiffFuzzer (took 43 ms, size +48%)
INFO: Instrumented mil.nga.tiff.util.TiffException (took 2 ms, size +36%)
INFO: libFuzzer ignores flags that start with '--'
INFO: Running with entropic power schedule (0xFF, 100).
INFO: Seed: 2735196724
INFO: Loaded 1 modules   (512 inline 8-bit counters): 512 [0x7fb67d510010, 0x7fb67d510210), 
INFO: Loaded 1 PC tables (512 PCs): 512 [0x7fb67c10e010,0x7fb67c110010), 
INFO: -max_len is not provided; libFuzzer will not generate inputs larger than 4096 bytes
INFO: Instrumented mil.nga.tiff.TiffReader (took 16 ms, size +56%)
INFO: Instrumented mil.nga.tiff.io.ByteReader (took 8 ms, size +43%)
INFO: A corpus is not provided, starting from an empty corpus
#2      INITED cov: 8 ft: 8 corp: 1/1b exec/s: 0 rss: 103Mb
#3      NEW    cov: 21 ft: 21 corp: 2/3b lim: 4 exec/s: 0 rss: 103Mb L: 2/2 MS: 1 CopyPart-
#6573   NEW    cov: 36 ft: 37 corp: 3/36b lim: 68 exec/s: 0 rss: 109Mb L: 33/33 MS: 5 ChangeByte-ChangeByte-InsertRepeatedBytes-EraseBytes-InsertRepeatedBytes-
#6586   REDUCE cov: 36 ft: 37 corp: 3/32b lim: 68 exec/s: 0 rss: 109Mb L: 29/29 MS: 3 ChangeBinInt-ChangeBinInt-EraseBytes-
#6609   REDUCE cov: 36 ft: 37 corp: 3/26b lim: 68 exec/s: 0 rss: 109Mb L: 23/23 MS: 3 ShuffleBytes-ChangeByte-EraseBytes-
#6635   REDUCE cov: 36 ft: 37 corp: 3/20b lim: 68 exec/s: 0 rss: 109Mb L: 17/17 MS: 1 EraseBytes-
#6731   REDUCE cov: 36 ft: 37 corp: 3/17b lim: 68 exec/s: 0 rss: 109Mb L: 14/14 MS: 1 EraseBytes-
#6779   REDUCE cov: 36 ft: 37 corp: 3/14b lim: 68 exec/s: 0 rss: 109Mb L: 11/11 MS: 3 ChangeBit-InsertByte-EraseBytes-
#6806   REDUCE cov: 36 ft: 37 corp: 3/13b lim: 68 exec/s: 0 rss: 109Mb L: 10/10 MS: 2 ChangeBinInt-EraseBytes-
#6892   REDUCE cov: 36 ft: 37 corp: 3/12b lim: 68 exec/s: 0 rss: 109Mb L: 9/9 MS: 1 EraseBytes-
#6968   REDUCE cov: 36 ft: 37 corp: 3/11b lim: 68 exec/s: 0 rss: 109Mb L: 8/8 MS: 1 EraseBytes-
#7204   REDUCE cov: 36 ft: 37 corp: 3/7b lim: 68 exec/s: 0 rss: 109Mb L: 4/4 MS: 1 EraseBytes-
INFO: Instrumented mil.nga.tiff.TIFFImage (took 3 ms, size +36%)
#13441  NEW    cov: 38 ft: 39 corp: 4/59b lim: 128 exec/s: 0 rss: 113Mb L: 52/52 MS: 2 CopyPart-InsertRepeatedBytes-
#13463  REDUCE cov: 38 ft: 39 corp: 4/46b lim: 128 exec/s: 0 rss: 113Mb L: 39/39 MS: 2 CrossOver-EraseBytes-
#13476  REDUCE cov: 38 ft: 39 corp: 4/34b lim: 128 exec/s: 0 rss: 113Mb L: 27/27 MS: 3 ShuffleBytes-CopyPart-EraseBytes-
#13494  REDUCE cov: 38 ft: 39 corp: 4/31b lim: 128 exec/s: 0 rss: 113Mb L: 24/24 MS: 3 ChangeByte-ChangeBit-EraseBytes-
#13540  REDUCE cov: 38 ft: 39 corp: 4/20b lim: 128 exec/s: 0 rss: 113Mb L: 13/13 MS: 1 EraseBytes-
#13566  REDUCE cov: 38 ft: 39 corp: 4/14b lim: 128 exec/s: 0 rss: 113Mb L: 7/7 MS: 1 CrossOver-
#13584  REDUCE cov: 38 ft: 39 corp: 4/12b lim: 128 exec/s: 0 rss: 113Mb L: 5/5 MS: 3 ChangeBit-ShuffleBytes-EraseBytes-
#14070  REDUCE cov: 38 ft: 39 corp: 4/10b lim: 128 exec/s: 0 rss: 113Mb L: 3/4 MS: 1 EraseBytes-
#14141  REDUCE cov: 38 ft: 39 corp: 4/9b lim: 128 exec/s: 0 rss: 113Mb L: 2/4 MS: 1 EraseBytes-
#18758  NEW    cov: 39 ft: 40 corp: 5/11b lim: 170 exec/s: 0 rss: 116Mb L: 2/4 MS: 2 ChangeBit-ChangeBit-
#136232 NEW    cov: 40 ft: 41 corp: 6/16b lim: 1330 exec/s: 0 rss: 119Mb L: 5/5 MS: 4 EraseBytes-InsertByte-CopyPart-InsertByte-
#136389 REDUCE cov: 40 ft: 41 corp: 6/14b lim: 1330 exec/s: 0 rss: 119Mb L: 3/4 MS: 2 ChangeBit-EraseBytes-
#139806 REDUCE cov: 40 ft: 41 corp: 6/13b lim: 1360 exec/s: 0 rss: 119Mb L: 2/4 MS: 2 CrossOver-EraseBytes-
#206414 REDUCE cov: 54 ft: 56 corp: 7/23b lim: 2020 exec/s: 0 rss: 123Mb L: 10/10 MS: 3 CopyPart-CrossOver-ShuffleBytes-
#206750 REDUCE cov: 54 ft: 56 corp: 7/21b lim: 2020 exec/s: 0 rss: 123Mb L: 8/8 MS: 1 EraseBytes-
#209061 REDUCE cov: 63 ft: 65 corp: 8/121b lim: 2040 exec/s: 0 rss: 126Mb L: 100/100 MS: 1 InsertRepeatedBytes-
#209180 REDUCE cov: 63 ft: 65 corp: 8/101b lim: 2040 exec/s: 0 rss: 126Mb L: 80/80 MS: 4 ChangeBit-CrossOver-InsertRepeatedBytes-EraseBytes-
#209415 REDUCE cov: 63 ft: 65 corp: 8/83b lim: 2040 exec/s: 0 rss: 126Mb L: 62/62 MS: 5 ChangeByte-ShuffleBytes-ChangeByte-ChangeBit-EraseBytes-
#209417 REDUCE cov: 63 ft: 65 corp: 8/75b lim: 2040 exec/s: 0 rss: 126Mb L: 54/54 MS: 2 ChangeASCIIInt-EraseBytes-
#209464 REDUCE cov: 63 ft: 65 corp: 8/61b lim: 2040 exec/s: 0 rss: 126Mb L: 40/40 MS: 2 ChangeBinInt-EraseBytes-
#209592 REDUCE cov: 63 ft: 65 corp: 8/48b lim: 2040 exec/s: 0 rss: 126Mb L: 27/27 MS: 3 ChangeBit-ChangeBit-EraseBytes-
#209828 REDUCE cov: 63 ft: 65 corp: 8/44b lim: 2040 exec/s: 0 rss: 126Mb L: 23/23 MS: 1 EraseBytes-

== Java Exception: java.lang.IndexOutOfBoundsException
        at java.base/java.nio.ByteBuffer.wrap(ByteBuffer.java:408)
        at mil.nga.tiff.io.ByteReader.readShort(ByteReader.java:266)
        at mil.nga.tiff.io.ByteReader.readUnsignedShort(ByteReader.java:290)
        at mil.nga.tiff.io.ByteReader.readUnsignedShort(ByteReader.java:277)
        at mil.nga.tiff.TiffReader.parseTIFFImage(TiffReader.java:199)
        at mil.nga.tiff.TiffReader.readTiff(TiffReader.java:167)
        at mil.nga.tiff.TiffReader.readTiff(TiffReader.java:109)
        at mil.nga.tiff.TiffReader.readTiff(TiffReader.java:95)
        at com.example.TiffFuzzer.fuzzerTestOneInput(TiffFuzzer.java:26)
DEDUP_TOKEN: 048fbe8202221b42
== libFuzzer crashing input ==
MS: 4 InsertByte-ChangeBinInt-CrossOver-ChangeByte-; base unit: f5a7ae8d7048e5febb25530c8ed3c945e6a26a6c
0x4d,0x4d,0x0,0x2a,0x80,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x1,0x0,0x0,0x2a,0x0,0x0,0x18,0x0,0x4d,0x0,
MM\x00*\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00*\x00\x00\x18\x00M\x00
artifact_prefix='/root/.cache/bazel/_bazel_root/c82b104c68f93e19e57160becd18f8f0/execroot/jazzer/bazel-out/k8-opt/testlogs/examples/TiffFuzzer/test.outputs/'; Test unit written to /root/.cache/bazel/_bazel_root/c82b104c68f93e19e57160becd18f8f0/execroot/jazzer/bazel-out/k8-opt/testlogs/examples/TiffFuzzer/test.outputs/crash-50f8becafa5d99f91a81e1002f5883ac0947916d
Base64: TU0AKoAAAAAAAAAAAAAAAQAAKgAAGABNAA==
reproducer_path='/root/.cache/bazel/_bazel_root/c82b104c68f93e19e57160becd18f8f0/execroot/jazzer/bazel-out/k8-opt/testlogs/examples/TiffFuzzer/test.outputs'; Java reproducer written to /root/.cache/bazel/_bazel_root/c82b104c68f93e19e57160becd18f8f0/execroot/jazzer/bazel-out/k8-opt/testlogs/examples/TiffFuzzer/test.outputs/Crash_50f8becafa5d99f91a81e1002f5883ac0947916d.java

```