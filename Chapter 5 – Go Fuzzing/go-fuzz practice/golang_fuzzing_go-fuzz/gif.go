// +build gofuzz

package gif

import (
	"bytes"
	"image/gif"
)

func Fuzz(data []byte) int {
	gif.DecodeAll(bytes.NewReader(data))
	return 0
}
