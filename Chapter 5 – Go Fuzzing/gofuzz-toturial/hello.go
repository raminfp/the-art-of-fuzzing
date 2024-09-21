// +build gofuzz
package main

import (
	"fmt"
	"github.com/google/gofuzz"
)

func main() {

	//f := fuzz.New()
	//var myInt string
	//f.Fuzz(&myInt) // myInt gets a random value
	//fmt.Printf("%s\n", myInt)


	type MyEnum string
	const (
		A MyEnum = "A"
		B MyEnum = "B"
	)
	type MyInfo struct {
		Type MyEnum
		AInfo *string
		BInfo *string
	}

	f := fuzz.New().NilChance(0).Funcs(
		func(e *MyInfo, c fuzz.Continue) {
		        switch c.Intn(2) {
		        case 0:
		                e.Type = A
		                c.Fuzz(&e.AInfo)
		        case 1:
		                e.Type = B
		                c.Fuzz(&e.BInfo)
		        }
		},
	)

	var myObject MyInfo
	f.Fuzz(&myObject)

	fmt.Println("%+v", myObject)

	fmt.Println("%s", myObject.AInfo)

}
