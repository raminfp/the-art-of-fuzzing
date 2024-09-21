### Compilation
```
CC=clang-6.0  CFLAGS="-fPIE -fsanitize=address,undefined -g" LDFLAGS="-pie" ./configure --enable-exif --enable-mbstring
```

### PHP version
```
php --version
PHP 8.0.0-dev (cli) (built: Dec 19 2019 13:24:08) ( NTS )
Copyright (c) The PHP Group
Zend Engine v4.0.0-dev, Copyright (c) Zend Technologies
```

### How to trigger
```
php -r 'unserialize(file_get_contents("php://stdin"));' < PoC
```

### Result
```
Notice: unserialize(): Error at offset 47 of 48 bytes in Command line code on line 1
php-src-master/ext/date/php_date.c:4026:26: runtime error: 1e+19 is outside the range of representable values of type 'long long'
    #0 0x5be918 in php_date_interval_initialize_from_hash (php-src-master/sapi/cli/php+0x5be918)
    #1 0x5c54ef in zim_DateInterval___wakeup (php-src-master/sapi/cli/php+0x5c54ef)
    #2 0x2848646 in zend_call_function (php-src-master/sapi/cli/php+0x2848646)
    #3 0x283d21e in _call_user_function_ex (php-src-master/sapi/cli/php+0x283d21e)
    #4 0x216ccc3 in var_destroy (php-src-master/sapi/cli/php+0x216ccc3)
    #5 0x216b270 in php_var_unserialize_destroy (php-src-master/sapi/cli/php+0x216b270)
    #6 0x207ec9e in zif_unserialize (php-src-master/sapi/cli/php+0x207ec9e)
    #7 0x37ca76a in ZEND_DO_ICALL_SPEC_RETVAL_UNUSED_HANDLER (php-src-master/sapi/cli/php+0x37ca76a)
    #8 0x2ee704a in execute_ex (php-src-master/sapi/cli/php+0x2ee704a)
    #9 0x2eea2d3 in zend_execute (php-src-master/sapi/cli/php+0x2eea2d3)
    #10 0x285545b in zend_eval_stringl (php-src-master/sapi/cli/php+0x285545b)
    #11 0x2856ce0 in zend_eval_stringl_ex (php-src-master/sapi/cli/php+0x2856ce0)
    #12 0x2856ec3 in zend_eval_string_ex (php-src-master/sapi/cli/php+0x2856ec3)
    #13 0x3aee302 in do_cli (php-src-master/sapi/cli/php+0x3aee302)
    #14 0x3ae9270 in main (php-src-master/sapi/cli/php+0x3ae9270)
    #15 0x7ffff640082f in __libc_start_main /build/glibc-LK5gWL/glibc-2.23/csu/../csu/libc-start.c:291
    #16 0x43f608 in _start (php-src-master/sapi/cli/php+0x43f608)


SUMMARY: UndefinedBehaviorSanitizer: undefined-behavior php-src-master/ext/date/php_date.c:4026:26 in 
```