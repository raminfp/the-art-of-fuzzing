// +build gofuzz

package checkmail


// Fuzz function to be used by https://github.com/dvyukov/go-fuzz
func Fuzz(data []byte) int {

    ValidateFormat(string(data))
    return 0
}
