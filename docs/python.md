# (New) Things I Learned/Had Forgotten in Python

## Data Types
* **Dictionaries** can be used to store key, value pairs and are usually declared with {}
    * `dict.items()` -> [(key1, value1), (key2, value2)...]

* **Iterable[T]** defines a capability that the object can be iterated over and get items of data type [T].
    * It is an abstraction for all iterable data types like lists, tuples, set, dict.
    * It does not guarantee that indexing, mutability and others are available.
    * Best used for function parameters if we know we just need to loop through the contents and don't assume the uderlying data type.
