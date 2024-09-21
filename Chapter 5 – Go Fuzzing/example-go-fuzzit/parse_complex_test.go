package parser

// This is just an example of a generational fuzzer which benchmarks the resutls against a coverage guided fuzzer
// This won't find the results for never probabbly ...

import (
	fuzz "github.com/google/gofuzz"
	"testing"
)

func TestGenerationalFuzzerParseComplex(t *testing.T) {
	f := fuzz.New()
	var inputString string
	for true {
		f.Fuzz(&inputString)
		ParseComplex([]byte(inputString))
	}
}

func TestParseComplex(t *testing.T) {
	var parseTests = []struct {
		in  string
		out bool
	}{
		{"invalid", false},
		{"invalid2", false},
		{"invalid3", false},
	}

	for _, tc := range parseTests {
		res := ParseComplex([]byte(tc.in))
		if res != tc.out{
			t.Errorf("was expecting %v but receieved %v", tc.out, res)
		}
	}
}
