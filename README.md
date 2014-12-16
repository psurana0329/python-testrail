testrail-python
===============

A high-level interface to Testrail API via python

This is not a complete implementation of API methods provided by Testrail in
documentation here: http://docs.gurock.com/testrail-api2/start
I was creating a library useful for scripting. Many operations should not be
perform via scripts. For example managing suite structure is easier in
user interface. Also bulk methods provided by API is quite useless in script,
which can easily do bulk operations itself. So I did not implement some methods
to keep the application simple.


See examples in testrail-examples.py file.

Currently only latest version (4.0) of Testrail is supported.