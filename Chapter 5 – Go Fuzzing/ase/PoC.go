package main

import (
        "strings"
        "github.com/arolek/ase"
)

func main() {

        var crashers = []string{
                "ASEF\x00A000000\x00A0000\x00\x00",
        }

        for _, f := range crashers {
                ase.Decode(strings.NewReader(f))
        }
}
