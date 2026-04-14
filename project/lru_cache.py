class Node:
    """
    Represents a node in the doubly linked list used by the LRU cache.
    Each node stores a key-value pair and pointers to the previous and next nodes.
    """
    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    """
    Implements a Least Recently Used (LRU) cache.

    This cache uses a combination of a hash map (dictionary) and a doubly linked list.
    The hash map provides O(1) average time complexity for `get` and `put` operations
    to locate nodes. The doubly linked list maintains the order of usage, allowing
    O(1) time complexity for moving nodes to the front (most recently used)
    and removing nodes from the back (least recently used).
    """
    def __init__(self, capacity: int):
        """
        Initializes the LRU cache with a given capacity.

        Args:
            capacity: The maximum number of key-value pairs the cache can hold.
        """
        self.capacity = capacity
        self.cache = {}  # Maps key to Node object
        self.size = 0    # Current number of items in the cache

        # Dummy head and tail nodes for the doubly linked list.
        # These simplify edge cases (e.g., empty list, adding/removing first/last node).
        # self.head.next will always point to the Most Recently Used (MRU) node.
        # self.tail.prev will always point to the Least Recently Used (LRU) node.
        self.head = Node(0, 0) # Dummy node, key and value don't matter
        self.tail = Node(0, 0) # Dummy node
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove_node(self, node: Node):
        """
        Helper method to remove a given node from the doubly linked list.
        This operation does not affect the cache dictionary.
        """
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_node_to_front(self, node: Node):
        """
        Helper method to add a given node to the front (MRU position) of the doubly linked list.
        """
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _move_to_front(self, node: Node):
        """
        Helper method to move an existing node to the front (MRU position) of the list.
        This is used when an item is accessed (get) or updated (put).
        """
        self._remove_node(node)
        self._add_node_to_front(node)

    def get(self, key: int) -> int:
        """
        Retrieves the value associated with the given key from the cache.

        If the key exists, its corresponding node is moved to the front (MRU).
        If the key does not exist, -1 is returned.

        Args:
            key: The key to look up.

        Returns:
            The value associated with the key, or -1 if the key is not found.
        """
        if key not in self.cache:
            return -1

        node = self.cache[key]
        self._move_to_front(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        """
        Inserts or updates a key-value pair in the cache.

        If the key already exists, its value is updated, and the node is moved to the front (MRU).
        If the key does not exist:
            A new node is created and added to the front (MRU).
            If the cache capacity is exceeded, the Least Recently Used (LRU) item is evicted.

        Args:
            key: The key to insert or update.
            value: The value to associate with the key.
        """
        if key in self.cache:
            # Key exists: update value and move to front
            node = self.cache[key]
            node.value = value
            self._move_to_front(node)
        else:
            # Key does not exist: create new node
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_node_to_front(new_node)
            self.size += 1

            # Check if capacity is exceeded
            if self.size > self.capacity:
                # Evict the LRU item (which is self.tail.prev)
                lru_node = self.tail.prev
                self._remove_node(lru_node)
                del self.cache[lru_node.key]
                self.size -= 1

# --- Example Usage ---
if __name__ == "__main__":
    print("Initializing LRUCache with capacity 2...")
    cache = LRUCache(2)

    print("\n--- Performing Operations ---")

    print("1. put(1, 1)")
    cache.put(1, 1)
    # Cache state: {1:1} (MRU: 1)

    print("2. put(2, 2)")
    cache.put(2, 2)
    # Cache state: {1:1, 2:2} (MRU: 2, LRU: 1)

    print("3. get(1) ->", cache.get(1)) # returns 1
    # Key 1 was accessed, so it becomes MRU.
    # Cache state: {2:2, 1:1} (MRU: 1, LRU: 2)

    print("4. put(3, 3)") # Capacity is 2, so key 2 (LRU) will be evicted.
    cache.put(3, 3)
    # Cache state: {1:1, 3:3} (MRU: 3, LRU: 1) - key 2 was evicted

    print("5. get(2) ->", cache.get(2)) # returns -1 (key 2 was evicted)

    print("6. put(4, 4)") # Capacity is 2, so key 1 (LRU) will be evicted.
    cache.put(4, 4)
    # Cache state: {3:3, 4:4} (MRU: 4, LRU: 3) - key 1 was evicted

    print("7. get(1) ->", cache.get(1)) # returns -1 (key 1 was evicted)
    print("8. get(3) ->", cache.get(3)) # returns 3
    # Key 3 was accessed, so it becomes MRU.
    # Cache state: {4:4, 3:3} (MRU: 3, LRU: 4)

    print("9. get(4) ->", cache.get(4)) # returns 4
    # Key 4 was accessed, so it becomes MRU.
    # Cache state: {3:3, 4:4} (MRU: 4, LRU: 3)

    print("\n--- Demonstrating Update and Eviction ---")
    print("10. put(3, 30)") # Update key 3, move to MRU
    cache.put(3, 30)
    # Cache state: {4:4, 3:30} (MRU: 3, LRU: 4)

    print("11. get(3) ->", cache.get(3)) # returns 30
    # Cache state: {4:4, 3:30} (MRU: 3, LRU: 4)

    print("12. put(5, 5)") # Capacity is 2, so key 4 (LRU) will be evicted.
    cache.put(5, 5)
    # Cache state: {3:30, 5:5} (MRU: 5, LRU: 3)

    print("13. get(4) ->", cache.get(4)) # returns -1 (key 4 was evicted)
    print("14. get(3) ->", cache.get(3)) # returns 30
    print("15. get(5) ->", cache.get(5)) # returns 5

    print("\nExample usage complete.")
