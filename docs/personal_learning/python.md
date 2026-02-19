# (New) Things I Learned/Had Forgotten in Python

## Python Functions
* **enumerate(iterable)** is used to return both an item from list and an associated index
    * Can be used on lists, dictionaries, strings, tuples and so on...
 ```python
 fruits = ['apple', 'banana', 'cherry'] 
 
 for index, fruit in enumerate(fruits):
    print(f"Index {index}: {fruit}")

# Output:
# Index 0: apple
# Index 1: banana
# Index 2: cherry
```

* **sorted(iterable, key=__) vs. iterable.sort(key=___)**
    * These functions both sort an iterable.
    * sorted() returns a sorted item while .sort() returns nothing and instead sorts the original iterable
    * Can use key param to sort by a certain value
```python
unsorted_list = [[2, 4], [1, 5], [3, 5]]
sorted_list = sorted(list)
sorted_list = sorted(list, key=)
```

* **{dict}.setdefault(key, value)**
    * This will create either an object {key: value} in the dictionary if key doesn't exist else it will return the object
    * Can be used with .append for a useful function of adding an key:value pair whether the key exists already or not
```python
test_dict = {}
test_dict.setdefault("key", []).append(["value1", "value2"])

# This creates an entry in test_dict with "key" as the key and sets it equal to a dictionary. 
# It then appends the list into our list at "key"

# This is the same as the following:
if name not in past:
    past[name] = []

past[name].append((t, city, i))
```


## Data Types
* **Dictionaries** can be used to store key, value pairs and are usually declared with {}
    * `dict.items()` -> [(key1, value1), (key2, value2)...]

* **Iterable[T]** defines a capability that the object can be iterated over and get items of data type [T].
    * It is an abstraction for all iterable data types like lists, tuples, set, dict.
    * It does not guarantee that indexing, mutability and others are available.
    * Best used for function parameters if we know we just need to loop through the contents and don't assume the uderlying data type.
