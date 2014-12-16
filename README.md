testrail-python
===============

A high-level interface to Testrail API via python

This is not a complete implementation of API methods provided by Testrail in
documentation here: http://docs.gurock.com/testrail-api2/start (but it may
become one some day).
I was creating a library useful for scripting. Many operations should not be
perform via scripts. For example managing suite structure is easier in
user interface. Also bulk methods provided by API is quite useless in script,
which can easily do bulk operations itself. So I did not implement some methods
to keep the application simple.

Currently only latest version (4.0) of Testrail is supported.

How to use
==========

Import and configuration:
```python
from testrail import Testrail

Testrail(host='192.168.1.1', port='8080',
         user='someuser@domain.dom', password='somepassword')
```

Simple example in which I create new run and add results in it.
```python
my_project = Testrail.get_project_by_name('My Favourite Project')
suite = my_project.get_suite_by_name('Best suite ever')

cases_to_run = suite.cases(types=['Functionality', 'UI'],
                           priorities=['Normal'])

new_run = suite.add_run(name='Normal func test', assignedto='V.Spiridonov',
                        include_all=False, cases=cases_to_run)

for test in new_run.tests():
    test.set_passed(comment='Ok')

```


See examples in testrail-examples.py file.
