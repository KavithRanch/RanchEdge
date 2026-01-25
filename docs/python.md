# (New) Things I Learned/Had Forgotten in Python

## Data Types
* **Iterable[T]** defines a capability that the object can be iterated over and get items of data type [T].
    * It is an abstraction for all iterable data types like lists, tuples, set, dict.
    * It does not guarantee that indexing, mutability and others are available.
    * Best used for function parameters if we know we just need to loop through the contents and don't assume the uderlying data type.
