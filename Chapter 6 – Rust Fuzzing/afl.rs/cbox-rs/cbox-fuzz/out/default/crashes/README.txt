Command line used to find this crash:

/root/.local/share/afl.rs/rustc-1.53.0-53cb7b0/afl.rs-0.10.1/afl/bin/afl-fuzz -i in -o out target/debug/cbox-fuzz

If you can't reproduce a bug outside of afl-fuzz, be sure to set the same
memory limit. The limit used for this fuzzing session was 0 B.

Need a tool to minimize test cases before investigating the crashes or sending
them to a vendor? Check out the afl-tmin that comes with the fuzzer!

Found any cool bugs in open-source tools using afl-fuzz? If yes, please drop
an mail at <afl-users@googlegroups.com> once the issues are fixed

  https://github.com/AFLplusplus/AFLplusplus

