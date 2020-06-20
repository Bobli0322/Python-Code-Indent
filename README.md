# Python-Code-Indent
Automatically fix indentation in Python code

For this to work program code must provide indentation hints formatted as following:
```python
if a == 0:#{0 
    pass
    if b == 0:#{1
        pass
    #}1
    pass
#}0
```
For comments to be ignored use '##'

For more examples of indentation hints please look in pyCodeIndent.py.

Use this script by the following command:

python pyCodeIndent.py myCode.py

Formatted code is written to myCode_ind.py

**Limitations**\
- If indentation hints are not properly formatted, it does not show where the issue is.\
- It can only process one file at a time.
