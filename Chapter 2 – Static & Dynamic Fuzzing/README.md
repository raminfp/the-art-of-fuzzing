# Chapter 2 – Static & Dynamic Fuzzing

This chapter explores various tools and techniques for both static and dynamic fuzzing, drawing from the examples provided in the directory structure.

## Overview of Fuzzing Tools and Techniques

### 1. AFL (American Fuzzy Lop)
An introduction to AFL, a popular fuzzing tool known for its effectiveness in finding vulnerabilities.

### 2. Honggfuzz
A discussion on Honggfuzz, a security-oriented fuzzer with unique features for both static and dynamic analysis.

### 3. LibFuzzer
An exploration of LibFuzzer, a library for in-process, coverage-guided fuzzing of APIs.

### 4. Radamsa
An overview of Radamsa, a general-purpose fuzzer, with specific examples for:
* JavaScript (radamsa-js)
* Network protocols (radamsa-net)
* PNG files (radamsa-png)

### 5. Static Fuzzing Techniques
A deep dive into static_fuzz methodologies, exploring how to analyze code without execution.

### 6. Dynamic Fuzzing Techniques
Contrasting with static methods, this section covers dynamic fuzzing approaches that involve runtime analysis.

## Specialized Fuzzing Targets

### 7. Image Fuzzing
Focusing on image_mutate techniques for finding vulnerabilities in image processing libraries.

### 8. PHP Sanitization
Examining php-sanitizer tools and techniques for identifying security issues in PHP code.

## Case Studies

### 9. MatrixSSL
An analysis of the MatrixSSL library (version 4.2.1) using various fuzzing techniques.

### 10. Coreutils
Fuzzing strategies applied to GNU Coreutils, a collection of basic file, shell, and text manipulation utilities.

## Additional Topics

### 11. Sanitizers
An overview of sanitization tools and their role in enhancing fuzzing effectiveness.

### 12. Fuzzing Best Practices
Guidelines for setting up and running effective fuzzing campaigns, drawing from the README.md file in the directory.

## Conclusion

A summary of key takeaways from the various static and dynamic fuzzing techniques explored in this chapter, and guidance on choosing the right approach for different scenarios.
