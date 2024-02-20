# letter rdp - python translation
## Building a Parser from scratch

### Links:
[Building a Parser from scratch](https://www.dmitrysoshnikov.education/p/parser-from-scratch/)
by `Dmitry Soshnikov`

### Getting Started
The parser is written / translated in python3. 
It has minimal dependencies ( `deepdiff` ).

Install requirements:
```
pip3 install -r requirements.txt
```

### Unit Tests
Everything under `./__tests__` folder.

Run all the tests
```
python3 __tests__/run.py
```

### Usage
Run the 'binary' against the example file located in the `./__tests__/example.lt` file:
```
./bin/letter-rdp -f ./__tests__/example.lt
```

Run it against an input string:
```
./bin/letter-rdp -e 'class MyClass {}'
```

### Tools used
- [AST Explorer](https://astexplorer.net)