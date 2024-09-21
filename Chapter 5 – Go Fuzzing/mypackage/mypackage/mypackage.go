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
