import heapq

class PriorityQueue(object):
    """
    Implements a nice priority queue on top of heapq.
    """
    
    def __init__(self):
        # the internal storage list for our queue
        self.__queue = []
        
        # set for efficient membership testing
        self.__member_set = set([])
        
    def put(self, item, priority):
        """
        Insert an item into the queue with a given priority number.
        """
        
        heapq.heappush(self.__queue, (priority, item))
        self.__member_set.add(item)
    
    def get(self):
        """
        Return the item with the smallest priority number and remove it
        from the queue.
        """
        
        # prevent getting items from an empty queue
        if self.empty():
            raise IndexError("Could not 'get()', queue is empty.")
        
        # dequeue an item and remove it from the member set
        priority, item = heapq.heappop(self.__queue)
        self.__member_set.remove(item)
        
        return item
    
    def empty(self):
        """
        Returns 'True' if the internal queue is empty, 'False' otherwise.
        """
        
        return len(self.__queue) == 0
    
    def __contains__(self, item):
        """
        Returns whether the queue contains a given item.  Uses set
        membership testing for lookup, so should be efficient.
        """
        
        return item in self.__member_set
    
    def __len__(self):
        return len(self.__queue)
    
    def __str__(self):
        return str(self.__queue__)
