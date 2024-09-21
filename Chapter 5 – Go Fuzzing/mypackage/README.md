### Simple Package for fuzzing

```bash
$ mkdir /root/go/src/mypackage 

$ nano /root/go/src/mypackage/mypackage.go

package mypackage
func GetNext(strs []string, match string) string {
	for strI, strV := range strs {
		if strV == match {
			return strs[strI+1]
		} else {
			continue
		}
	}
	return ""
}

$ nano /root/go/src/mypackage/fuzz.go

package mypackage

func Fuzz(data []byte) int {
	crasherstrs := []string{"testing1", "testing2", "testing3"}
	GetNext(crasherstrs, string(data))
	return 0
}


$ cd /root/go/src/mypackage/

$ /root/go/bin/go-fuzz-build

$ /root/go/bin/go-fuzz
```