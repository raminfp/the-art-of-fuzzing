# Chapter 3 – Symbolic Execution & Concolic Execution

This chapter delves into the advanced techniques of symbolic execution and concolic execution, exploring various tools and applications based on the provided directory structure.

## Introduction to Symbolic and Concolic Execution

A brief overview of symbolic execution and concolic execution, their differences, and their importance in software testing and security analysis.

## Symbolic Execution Tools and Techniques

### 1. KLEE
An in-depth look at KLEE, a symbolic virtual machine built on top of the LLVM compiler infrastructure.
- Setting up KLEE
- Running symbolic execution with KLEE
- Interpreting KLEE's output

### 2. angr
Exploring angr, a multi-architecture binary analysis toolkit with capabilities for both static and symbolic analysis.
- Key features of angr
- Symbolic execution using angr
- Case studies and practical applications

### 3. symcc
An introduction to symcc, a compiler wrapper that adds symbolic execution capabilities to unmodified programs.
- How symcc works
- Integrating symcc into existing projects
- Comparing symcc with other symbolic execution tools

## Concolic Execution and Hybrid Approaches

### 4. Driller
Examining Driller, a concolic execution engine that combines fuzzing with symbolic execution.
- The concept behind Driller
- Setting up and using Driller
- Advantages of combining fuzzing and symbolic execution

### 5. AFL Integration
Exploring how symbolic and concolic execution can be integrated with American Fuzzy Lop (AFL) for more effective fuzzing.

#### 5.1 afl_driller
- Combining AFL with Driller for enhanced bug discovery

#### 5.2 afl_symcc
- Integrating AFL with symcc for improved code coverage

## Practical Applications and Case Studies

### 6. Analyzing Small Programs
Using tiny_regex_c as an example to demonstrate symbolic execution on a small, focused codebase.
- Setting up the environment
- Running symbolic execution
- Analyzing results and identifying potential vulnerabilities

### 7. Image Processing Analysis
Exploring symbolic execution techniques for image processing libraries and applications, referencing the 'img' directory.
- Challenges in symbolically executing image processing code
- Strategies for effective analysis
- Case study: Identifying vulnerabilities in an image processing routine

## Advanced Topics and Future Directions

### 8. Scaling Symbolic Execution
Discussing techniques to handle the state explosion problem and improve performance for large codebases.

### 9. Combining Static Analysis with Symbolic Execution
Exploring ways to enhance symbolic execution with static analysis techniques for more comprehensive code coverage.

## Conclusion

Summarizing the key points of symbolic and concolic execution, their strengths and limitations, and their place in the broader context of software testing and security analysis.

## Additional Resources

### http://software-lab.org/teaching/winter2020/pa/
