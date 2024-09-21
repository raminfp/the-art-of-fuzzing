/* Advanced IPv6 Socket Manipulation for Python
 *
 * Copyright © 2021 United States Government as represented by Joseph Ishac.
 * No copyright is claimed in the United States under Title 17, U.S.Code.
 * All Other Rights Reserved.
 *
 */
//#define __UAPI_DEF_IPV6_OPTIONS 1
#define IPV6_FLOWLABEL_MGR  32
#define IPV6_FLOWINFO_SEND  33

#include "Python.h"
#include "structmember.h"
#include <math.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <linux/in6.h>
#include <arpa/inet.h>

#if PY_MAJOR_VERSION >= 3
  #define PyInt_AsLong PyLong_AsLong
  #define PyInt_FromLong PyLong_FromLong
  #define PyInt_Check PyLong_Check
#endif

/* static PyObject *err; */

typedef struct {
  PyObject_HEAD
} IPV6;

long create_flow_label (int, struct sockaddr_in6 *);

/* destructor */
static void
IPV6_dealloc(IPV6* self)
{
  // Free the object itself
  Py_TYPE(self)->tp_free((PyObject*)self);
}

/* constructor */
static PyObject *
IPV6_new(PyTypeObject *type, PyObject *args)
{
  IPV6 *self;

  // REFCOUNT NOTE: Call auto adds reference, macro Py_INCREF not needed
  self = (IPV6 *)type->tp_alloc(type, 0);
  if (self != NULL) 
  {
    return (PyObject *)self;
  }
  return PyErr_NoMemory();
}

/*  initialize */
static PyObject *
IPV6_init(IPV6 *self)
{
  Py_RETURN_NONE;
}

/* declare members to python */
// Nothing to declare
static PyMemberDef IPV6_members[] = {
    {NULL} /* Sentinel */
};

/* * * * * * * * * * * * * * Methods * * * * * * * * * * * * * */

/* get_flow_label - This method gets a random flow label from the kernel and
 * also turns on flow labels for a given Python socket or socket file descriptor
 * (the latter may only be possible in Linux).  It returns a new Python
 * four-tuple (host, port, flowinfo, scopeid) address for AF_INET6 address
 * family. The flowinfo part of this tuple will have been updated with the flow
 * label obtained from the kernel. The user may supply the initial AF_INET6
 * address when making this method call.
 * 
 * For Example:
 *   import ipv6
 *   # Set-up a IPv6 Socket ...
 *   sockaddr = ipv6.get_flow_label(sock,*sockaddr)
 */
static PyObject *
get_flow_label (IPV6 *self, PyObject *args)
{
  PyObject *socket;
  int sock;
  socklen_t len;
  struct sockaddr_storage addr;
  struct sockaddr_in6 *addr_in6;
  PyObject *answer;
  long result = 0;
  char msg[300];
  char v6dst[INET6_ADDRSTRLEN]="::1";
  char *ptr;
  int  v6port=-1;
  long v6flow=0;
  int  v6scope=0;
  int debug_family;

// FOR REFERENCE:
// struct sockaddr_in6 {
//     sa_family_t     sin6_family;   /* AF_INET6 */
//     in_port_t       sin6_port;     /* port number */
//     uint32_t        sin6_flowinfo; /* IPv6 flow information */
//     struct in6_addr sin6_addr;     /* IPv6 address */
//     uint32_t        sin6_scope_id; /* Scope ID (new in 2.4) */
// };
// 
// struct in6_addr {
//     unsigned char   s6_addr[16];   /* IPv6 address */
// };

  if ((! PyArg_ParseTuple(args, "O|sili", &socket, &ptr, &v6port, &v6flow, &v6scope)))
  {
    PyErr_SetString(PyExc_ValueError, "Malformed Request! Required: (Socket Object or Socket FD), Optional: (Host, Port, FlowInfo, Scope)");
    return NULL;
  }

  //if (socket == Py_None) {
  //  PyErr_SetString(PyExc_ValueError, "None is not a valid socket");
  //  return NULL;
  //}

  //strncpy (v6dst, ptr, sizeof(v6dst) );
  strcpy(v6dst, ptr);
  if (PyInt_Check(socket))
  {
    // Assume they passed the Socket File Descriptor
    sock = (int) PyInt_AsLong(socket);
    if (sock == -1)
    {
      PyErr_SetString(PyExc_RuntimeError, "Unable to Convert Socket Descriptor!");
      return NULL;
    }
  } else {
    // If we were passed a socket we might need to do this...
    answer = PyObject_CallMethod(socket,"fileno",NULL);
    if (answer == NULL)
    {
      PyErr_SetString(PyExc_RuntimeError, "Bad Socket Descriptor!");
      Py_DECREF(answer);
      return NULL;
    }
    if (PyInt_Check(answer))
    {
      sock = (int) PyInt_AsLong(answer);
      if (sock == -1)
      {
        PyErr_SetString(PyExc_RuntimeError, "Unable to Convert Socket Descriptor!");
        Py_DECREF(answer);
        return NULL;
      }
    } else {
      PyErr_SetString(PyExc_RuntimeError, "Bad Answer from Fileno!");
      Py_DECREF(answer);
      return NULL;
    }
    Py_DECREF(answer);
  }

  len = sizeof addr;
  getpeername(sock, (struct sockaddr *)&addr, &len);
  // Only care about IPv6
  if (addr.ss_family != AF_INET)
  {
    debug_family = addr.ss_family;
    addr_in6 = (struct sockaddr_in6*)&addr;
  } else {
    PyErr_SetString(PyExc_RuntimeError, "Passed a Non-IPv6 Socket!");
    return NULL;
  }

  if (addr_in6->sin6_family != AF_INET6) {
    // Perhaps we are not connected - either used supplied info or get local info?
    // Get local info
    getsockname(sock, (struct sockaddr *)&addr, &len);
    if (addr.ss_family != AF_INET)
    {
      debug_family = addr.ss_family;
      addr_in6 = (struct sockaddr_in6*)&addr;
    } else {
      PyErr_SetString(PyExc_RuntimeError, "Passed a Non-IPv6 Local Socket!");
      return NULL;
    }
    // Info Supplied if port > 0
    if (v6port > 0)
    {
      addr_in6->sin6_port = htons(v6port);
      inet_pton(AF_INET6, v6dst, &(addr_in6->sin6_addr));
      addr_in6->sin6_flowinfo = htonl(v6flow);
      addr_in6->sin6_scope_id = v6scope;
    }
  }
  if (addr_in6->sin6_family != AF_INET6) {
    snprintf(msg,sizeof(msg),"Unexpected Error! Sock (%d): [%d, %d], %d, %d, %d, %d",sock,AF_INET6,debug_family,addr_in6->sin6_family,ntohs(addr_in6->sin6_port),addr_in6->sin6_flowinfo,addr_in6->sin6_scope_id);
    PyErr_SetString(PyExc_RuntimeError, msg);
    return NULL;
  }
  
  inet_ntop(AF_INET6, &(addr_in6->sin6_addr), v6dst, INET6_ADDRSTRLEN);
  result = create_flow_label(sock,addr_in6);
  if (result == -1)
  {
    // Creation Failed!!
    return NULL;
  }
  v6port = ntohs(addr_in6->sin6_port);
  v6flow = ntohl(result);
  return(Py_BuildValue("(sili)",v6dst,v6port,v6flow,v6scope));
}


// FOR REFERENCE:
// struct in6_flowlabel_req
// {
//   struct in6_addr flr_dst;
//   __u32 flr_label;
//   __u8 flr_action;
//   __u8 flr_share;
//   __u16 flr_flags;
//   __u16 flr_expires;
//   __u16 flr_linger;
//   __u32 __flr_pad;
// };

long
create_flow_label (int sock, struct sockaddr_in6 *addr)
{
  struct in6_flowlabel_req flr;
  int on = 1;
  char msg[300];
  
  //flr.flr_label = addr->sin6_flowinfo;
  flr.flr_label = 0;
  flr.flr_action = IPV6_FL_A_GET;
  flr.flr_flags = IPV6_FL_F_CREATE;
  flr.flr_share = IPV6_FL_S_EXCL;
  flr.flr_dst = addr->sin6_addr;
  flr.flr_expires = 0;
  flr.flr_linger = 0;
  flr.__flr_pad = 0;

  if (setsockopt(sock, IPPROTO_IPV6, IPV6_FLOWLABEL_MGR, &flr, sizeof(flr)) == -1)
  {
    snprintf(msg,sizeof(msg),"Failed to set flow label: %s",strerror(errno));
    PyErr_SetString(PyExc_RuntimeError, msg);
    return -1;
  }
  if (setsockopt(sock, IPPROTO_IPV6, IPV6_FLOWINFO_SEND, &on, sizeof(on)) == -1)
  {
    snprintf(msg,sizeof(msg),"Unable to enable flow labels: %s",strerror(errno));
    PyErr_SetString(PyExc_RuntimeError, msg);
    return -1;
  }
  addr->sin6_flowinfo=flr.flr_label;
  return flr.flr_label;
}

/* deslare methods to python */
static PyMethodDef IPV6_methods[] = {
    {"get_flow_label", (PyCFunction)get_flow_label, METH_VARARGS, 
        "Get and use a random flow label from the kernel."},
    {NULL, NULL, 0, NULL}  /* Sentinel */
};

static PyTypeObject IPV6Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "ipv6.IPV6",
    .tp_basicsize = sizeof(IPV6),
    .tp_doc = "IPv6 Object",
    .tp_new = (void *)IPV6_new,
    .tp_dealloc = (destructor)IPV6_dealloc,
    .tp_methods = IPV6_methods,
    .tp_members = IPV6_members,
    .tp_init = (initproc)IPV6_init,
};

static PyMethodDef module_methods[] = {
    {"get_flow_label", (PyCFunction)get_flow_label, METH_VARARGS, 
        "Get and use a random flow label from the kernel."},
    {NULL, NULL, 0, NULL} /* Sentinel */
};

#if PY_MAJOR_VERSION >= 3
  #define MOD_ERROR_VAL NULL
  #define MOD_SUCCESS_VAL(val) val
  #define MOD_INIT(name) PyMODINIT_FUNC PyInit_##name(void)
  #define MOD_DEF(ob, name, doc, methods) \
    static struct PyModuleDef moduledef = { \
      PyModuleDef_HEAD_INIT, name, doc, -1, methods, }; \
    ob = PyModule_Create(&moduledef);
#else
  #define MOD_ERROR_VAL
  #define MOD_SUCCESS_VAL(val)
  #define MOD_INIT(name) void init##name(void)
  #define MOD_DEF(ob, name, doc, methods) \
    ob = Py_InitModule3(name, methods, doc);
#endif
  
MOD_INIT(ipv6)
{
    PyObject* m;

    if (PyType_Ready(&IPV6Type) < 0)
        return MOD_ERROR_VAL;

    MOD_DEF(m, "ipv6", "IPV6 Object base type.", module_methods)

    if (m == NULL)
        return MOD_ERROR_VAL;

    Py_INCREF(&IPV6Type);
    PyModule_AddObject(m, "IPV6", 
        (PyObject *)&IPV6Type);

    return MOD_SUCCESS_VAL(m);
}
