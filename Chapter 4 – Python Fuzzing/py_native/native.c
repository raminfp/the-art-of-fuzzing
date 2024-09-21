#include <Python.h>


static PyObject *method_overflow(PyObject *self, PyObject *args) {

	char arr[10];
	char *str, *filename = NULL;
	int bytes_copied = -1;


	if (!PyArg_ParseTuple(args, "y*s", &str, &filename)) {
		return NULL;
	}
	if (str != NULL) {
		FILE *fp = fopen(filename, "w");
		if (strcmp(str, "AAAAAAAAA")) {
			int idx = *(int*)str;
			arr[idx] = 'c';
			bytes_copied = fputs(arr, fp);
		}
		fclose(fp);
	}
	return PyLong_FromLong(bytes_copied);
}

static PyMethodDef VulMethods[] = {
	{"overflow", method_overflow, METH_VARARGS,
	"Python interface to expose overflow"
        },
	{NULL, NULL, 0, NULL}
};

static struct PyModuleDef vulmodule = {
	PyModuleDef_HEAD_INIT,
	"overflow",
	"Python interface to expose overflow",
	-1,
	VulMethods

};

PyMODINIT_FUNC PyInit_vuln(void) {
	return PyModule_Create(&vulmodule);

}
