package main

import (
	"fmt"
	"runtime"
	"sync"
)

func main() {

	counter := 0

	const num = 15
	var wg sync.WaitGroup
	wg.Add(num)

	for i := 0; i < num; i++ {
		go func() {
			temp := counter
			runtime.Gosched()
			temp++
			counter = temp
			wg.Done()
		}()
	}
	wg.Wait()
	fmt.Println("count:", counter)
}