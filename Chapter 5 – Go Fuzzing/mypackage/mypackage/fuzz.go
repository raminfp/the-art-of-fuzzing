package mypackage

func Fuzz(data []byte) int {
	crasherstrs := []string{"testing1", "testing2", "testing3"}
	GetNext(crasherstrs, string(data))
	return 0
}
