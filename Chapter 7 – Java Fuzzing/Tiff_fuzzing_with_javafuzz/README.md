#### Tiff Fuzzing With Javafuzz


```bash

$ nano src/test/java/com/gitlab/javafuzz/examples/FuzzTiff.java

$ mvn install

$ MAVEN_OPTS="-javaagent:jacocoagent.jar" mvn javafuzz:fuzz -DclassName=com.gitlab.javafuzz.examples.FuzzTiff

$ MAVEN_OPTS="-javaagent:jacocoagent.jar" mvn javafuzz:fuzz -DclassName=com.gitlab.javafuzz.examples.FuzzTiff
[INFO] Scanning for projects...
[INFO] 
[INFO] --------------------< com.gitlab.javafuzz:examples >--------------------
[INFO] Building examples 1.0
[INFO] --------------------------------[ jar ]---------------------------------
[INFO] 
[INFO] --- javafuzz-maven-plugin:1.24:fuzz (default-cli) @ examples ---
urls for URLClassLoader: [file:/javafuzz-fuzzing-example/target/test-classes/, file:/javafuzz-fuzzing-example/target/classes/, file:/root/.m2/repository/mil/nga/tiff/2.0.0/tiff-2.0.0.jar, file:/root/.m2/repository/org/yaml/snakeyaml/1.25/snakeyaml-1.25.jar, file:/root/.m2/repository/com/gitlab/javafuzz/javafuzz-maven-plugin/1.24/javafuzz-maven-plugin-1.24.jar, file:/root/.m2/repository/org/apache/maven/maven-plugin-api/3.6.2/maven-plugin-api-3.6.2.jar, file:/root/.m2/repository/org/apache/maven/maven-model/3.6.2/maven-model-3.6.2.jar, file:/root/.m2/repository/org/apache/maven/maven-artifact/3.6.2/maven-artifact-3.6.2.jar, file:/root/.m2/repository/org/eclipse/sisu/org.eclipse.sisu.plexus/0.3.3/org.eclipse.sisu.plexus-0.3.3.jar, file:/root/.m2/repository/javax/enterprise/cdi-api/1.0/cdi-api-1.0.jar, file:/root/.m2/repository/javax/annotation/jsr250-api/1.0/jsr250-api-1.0.jar, file:/root/.m2/repository/org/codehaus/plexus/plexus-utils/3.2.1/plexus-utils-3.2.1.jar, file:/root/.m2/repository/org/codehaus/plexus/plexus-classworlds/2.6.0/plexus-classworlds-2.6.0.jar, file:/root/.m2/repository/org/apache/maven/maven-core/3.6.2/maven-core-3.6.2.jar, file:/root/.m2/repository/org/apache/maven/maven-settings/3.6.2/maven-settings-3.6.2.jar, file:/root/.m2/repository/org/apache/maven/maven-settings-builder/3.6.2/maven-settings-builder-3.6.2.jar, file:/root/.m2/repository/org/codehaus/plexus/plexus-interpolation/1.25/plexus-interpolation-1.25.jar, file:/root/.m2/repository/org/sonatype/plexus/plexus-sec-dispatcher/1.4/plexus-sec-dispatcher-1.4.jar, file:/root/.m2/repository/org/sonatype/plexus/plexus-cipher/1.4/plexus-cipher-1.4.jar, file:/root/.m2/repository/org/apache/maven/maven-builder-support/3.6.2/maven-builder-support-3.6.2.jar, file:/root/.m2/repository/org/apache/maven/maven-repository-metadata/3.6.2/maven-repository-metadata-3.6.2.jar, file:/root/.m2/repository/org/apache/maven/maven-model-builder/3.6.2/maven-model-builder-3.6.2.jar, file:/root/.m2/repository/org/apache/maven/maven-resolver-provider/3.6.2/maven-resolver-provider-3.6.2.jar, file:/root/.m2/repository/org/slf4j/slf4j-api/1.7.25/slf4j-api-1.7.25.jar, file:/root/.m2/repository/org/apache/maven/resolver/maven-resolver-impl/1.4.1/maven-resolver-impl-1.4.1.jar, file:/root/.m2/repository/org/apache/maven/resolver/maven-resolver-api/1.4.1/maven-resolver-api-1.4.1.jar, file:/root/.m2/repository/org/apache/maven/resolver/maven-resolver-spi/1.4.1/maven-resolver-spi-1.4.1.jar, file:/root/.m2/repository/org/apache/maven/resolver/maven-resolver-util/1.4.1/maven-resolver-util-1.4.1.jar, file:/root/.m2/repository/org/apache/maven/shared/maven-shared-utils/3.2.1/maven-shared-utils-3.2.1.jar, file:/root/.m2/repository/commons-io/commons-io/2.5/commons-io-2.5.jar, file:/root/.m2/repository/org/eclipse/sisu/org.eclipse.sisu.inject/0.3.3/org.eclipse.sisu.inject-0.3.3.jar, file:/root/.m2/repository/com/google/inject/guice/4.2.1/guice-4.2.1-no_aop.jar, file:/root/.m2/repository/aopalliance/aopalliance/1.0/aopalliance-1.0.jar, file:/root/.m2/repository/com/google/guava/guava/25.1-android/guava-25.1-android.jar, file:/root/.m2/repository/com/google/code/findbugs/jsr305/3.0.2/jsr305-3.0.2.jar, file:/root/.m2/repository/org/checkerframework/checker-compat-qual/2.0.0/checker-compat-qual-2.0.0.jar, file:/root/.m2/repository/com/google/errorprone/error_prone_annotations/2.1.3/error_prone_annotations-2.1.3.jar, file:/root/.m2/repository/com/google/j2objc/j2objc-annotations/1.1/j2objc-annotations-1.1.jar, file:/root/.m2/repository/org/codehaus/mojo/animal-sniffer-annotations/1.14/animal-sniffer-annotations-1.14.jar, file:/root/.m2/repository/javax/inject/javax.inject/1/javax.inject-1.jar, file:/root/.m2/repository/org/codehaus/plexus/plexus-component-annotations/2.0.0/plexus-component-annotations-2.0.0.jar, file:/root/.m2/repository/org/apache/commons/commons-lang3/3.8.1/commons-lang3-3.8.1.jar]
#0 READ units: 0
#1 NEW     cov: 20023 corp: 2 exec/s: 0 rss: 40 MB
#2 NEW     cov: 20091 corp: 3 exec/s: 1000 rss: 40 MB
#3 NEW     cov: 20099 corp: 4 exec/s: 1000 rss: 40 MB
#4 NEW     cov: 20115 corp: 5 exec/s: 1000 rss: 40 MB
#5 NEW     cov: 20126 corp: 6 exec/s: 1000 rss: 40 MB
#6 NEW     cov: 20136 corp: 7 exec/s: 0 rss: 40 MB
#7 NEW     cov: 20144 corp: 8 exec/s: 0 rss: 40 MB
#8 NEW     cov: 20150 corp: 9 exec/s: 1000 rss: 40 MB
#9 NEW     cov: 20153 corp: 10 exec/s: 0 rss: 40 MB
#10 NEW     cov: 20159 corp: 11 exec/s: 0 rss: 40 MB
#12 NEW     cov: 20162 corp: 12 exec/s: 1000 rss: 40 MB
#15 NEW     cov: 20163 corp: 13 exec/s: 1000 rss: 40 MB
#19 NEW     cov: 20166 corp: 14 exec/s: 1000 rss: 40 MB
#23 NEW     cov: 20168 corp: 15 exec/s: 1000 rss: 40 MB
#29 NEW     cov: 20172 corp: 16 exec/s: 1000 rss: 40 MB
#36 NEW     cov: 20174 corp: 17 exec/s: 1000 rss: 40 MB
#39 NEW     cov: 20181 corp: 18 exec/s: 1000 rss: 41 MB
#42 NEW     cov: 20182 corp: 19 exec/s: 1000 rss: 41 MB
#139 NEW     cov: 20183 corp: 20 exec/s: 3000 rss: 42 MB
#1420 NEW     cov: 20184 corp: 21 exec/s: 5000 rss: 22 MB
#6307 NEW     cov: 20185 corp: 22 exec/s: 6000 rss: 38 MB
#25796 PULSE     cov: 20185 corp: 22 exec/s: 6000 rss: 45 MB
#25797 NEW     cov: 20187 corp: 23 exec/s: -1 rss: 45 MB
#25798 NEW     cov: 20188 corp: 24 exec/s: 1000 rss: 45 MB
#45450 PULSE     cov: 20188 corp: 24 exec/s: 6000 rss: 12 MB
#65014 PULSE     cov: 20188 corp: 24 exec/s: 6000 rss: 14 MB
#84771 PULSE     cov: 20188 corp: 24 exec/s: 6000 rss: 14 MB
#90692 NEW     cov: 20189 corp: 25 exec/s: 6000 rss: 34 MB
#110448 PULSE     cov: 20189 corp: 25 exec/s: 6000 rss: 36 MB
#130276 PULSE     cov: 20189 corp: 25 exec/s: 6000 rss: 37 MB
#149938 PULSE     cov: 20189 corp: 25 exec/s: 6000 rss: 37 MB
#169738 PULSE     cov: 20189 corp: 25 exec/s: 6000 rss: 38 MB
#180709 NEW     cov: 20200 corp: 26 exec/s: 6000 rss: 30 MB
#196638 NEW     cov: 20202 corp: 27 exec/s: 6000 rss: 32 MB
#216379 PULSE     cov: 20202 corp: 27 exec/s: 6000 rss: 34 MB
#236163 PULSE     cov: 20202 corp: 27 exec/s: 6000 rss: 34 MB
#256003 PULSE     cov: 20202 corp: 27 exec/s: 6000 rss: 36 MB
#275886 PULSE     cov: 20202 corp: 27 exec/s: 6000 rss: 38 MB
#295949 PULSE     cov: 20202 corp: 27 exec/s: 6000 rss: 41 MB
#310928 NEW     cov: 20203 corp: 28 exec/s: 6000 rss: 34 MB
#331017 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 39 MB
#351125 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 43 MB
#371208 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 47 MB
#391313 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 12 MB
#411430 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 16 MB
#431545 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 20 MB
#451657 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 24 MB
#471771 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 28 MB
#491884 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 32 MB
#511994 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 37 MB
#532105 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 41 MB
#552212 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 45 MB
#572320 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 49 MB
#592432 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 14 MB
#612547 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 18 MB
#632662 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 22 MB
#652765 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 26 MB
#672854 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 30 MB
#692964 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 34 MB
#713050 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 38 MB
#733169 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 43 MB
#753279 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 47 MB
#773363 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 11 MB
#793476 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 16 MB
#813592 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 20 MB
#833704 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 24 MB
#853823 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 28 MB
#873936 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 32 MB
#894041 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 36 MB
#914153 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 41 MB
#934271 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 45 MB
#954386 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 49 MB
#974503 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 14 MB
#994617 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 18 MB
#1014735 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 22 MB
#1034797 PULSE     cov: 20203 corp: 28 exec/s: 6000 rss: 26 MB
#1052815 NEW     cov: 20215 corp: 29 exec/s: 6000 rss: 48 MB
java.lang.IndexOutOfBoundsException
        at java.base/java.nio.ByteBuffer.wrap(ByteBuffer.java:395)
        at mil.nga.tiff.io.ByteReader.readShort(ByteReader.java:264)
        at mil.nga.tiff.io.ByteReader.readUnsignedShort(ByteReader.java:288)
        at mil.nga.tiff.io.ByteReader.readUnsignedShort(ByteReader.java:275)
        at mil.nga.tiff.TiffReader.parseTIFFImage(TiffReader.java:195)
        at mil.nga.tiff.TiffReader.readTiff(TiffReader.java:163)
        at mil.nga.tiff.TiffReader.readTiff(TiffReader.java:105)
        at mil.nga.tiff.TiffReader.readTiff(TiffReader.java:91)
        at com.gitlab.javafuzz.examples.FuzzTiff.fuzz(FuzzTiff.java:13)
        at com.gitlab.javafuzz.core.Fuzzer.start(Fuzzer.java:72)
        at com.gitlab.javafuzz.maven.FuzzGoal.execute(FuzzGoal.java:63)
        at org.apache.maven.plugin.DefaultBuildPluginManager.executeMojo(DefaultBuildPluginManager.java:137)
        at org.apache.maven.lifecycle.internal.MojoExecutor.execute(MojoExecutor.java:210)
        at org.apache.maven.lifecycle.internal.MojoExecutor.execute(MojoExecutor.java:156)
        at org.apache.maven.lifecycle.internal.MojoExecutor.execute(MojoExecutor.java:148)
        at org.apache.maven.lifecycle.internal.LifecycleModuleBuilder.buildProject(LifecycleModuleBuilder.java:117)
        at org.apache.maven.lifecycle.internal.LifecycleModuleBuilder.buildProject(LifecycleModuleBuilder.java:81)
        at org.apache.maven.lifecycle.internal.builder.singlethreaded.SingleThreadedBuilder.build(SingleThreadedBuilder.java:56)
        at org.apache.maven.lifecycle.internal.LifecycleStarter.execute(LifecycleStarter.java:128)
        at org.apache.maven.DefaultMaven.doExecute(DefaultMaven.java:305)
        at org.apache.maven.DefaultMaven.doExecute(DefaultMaven.java:192)
        at org.apache.maven.DefaultMaven.execute(DefaultMaven.java:105)
        at org.apache.maven.cli.MavenCli.execute(MavenCli.java:957)
        at org.apache.maven.cli.MavenCli.doMain(MavenCli.java:289)
        at org.apache.maven.cli.MavenCli.main(MavenCli.java:193)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
        at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
        at java.base/java.lang.reflect.Method.invoke(Method.java:566)
        at org.codehaus.plexus.classworlds.launcher.Launcher.launchEnhanced(Launcher.java:282)
        at org.codehaus.plexus.classworlds.launcher.Launcher.launch(Launcher.java:225)
        at org.codehaus.plexus.classworlds.launcher.Launcher.mainWithExitCode(Launcher.java:406)
        at org.codehaus.plexus.classworlds.launcher.Launcher.main(Launcher.java:347)
crash was written to crash-9c3696c091aa56aa7db4b6ff65fcc841b99bd5976689f6ee67b1999baaa54c9b
```
