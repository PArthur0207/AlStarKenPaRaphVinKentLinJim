import random
import sys
import io

# Suppress print statements during import
class SuppressOutput:
    def write(self, x): pass
    def flush(self): pass

original_stdout = sys.stdout
sys.stdout = SuppressOutput()
try:
    try:
        # Try relative import first (for package context)
        from .sorting_algo import BubbleSort, SelectionSort, InsertionSort, MergeSort, QuickSort
    except ImportError:
        # Fall back to absolute import (for direct module execution)
        from sorting_algo import BubbleSort, SelectionSort, InsertionSort, MergeSort, QuickSort
finally:
    sys.stdout = original_stdout


class SortingManager:
    
    ALGORITHMS = {
        "bubble": BubbleSort,
        "selection": SelectionSort,
        "insertion": InsertionSort,
        "merge": MergeSort,
        "quick": QuickSort
    }
    
    @staticmethod
    def generate_random_array(size):
        return [random.randint(1, 100) for _ in range(size)]
    
    @staticmethod
    def count_operations(steps):
        comparisons = 0
        swaps = 0
        shifts = 0
        
        for step in steps:
            action = step.get("action", "")
            if action == "compare":
                comparisons += 1
            elif action == "swap":
                swaps += 1
            elif action == "shift":
                shifts += 1
        
        return comparisons, swaps, shifts
    
    @staticmethod
    def format_steps_for_display(steps):
        formatted_steps = []
        
        for i, step in enumerate(steps, 1):
            action = step.get("action", "").upper()
            indices = step.get("indices", [])
            array = step.get("array", [])
            pivot = step.get("pivot", None)
            
            if action == "COMPARE":
                if len(indices) >= 2:
                    desc = f"Step {i}: Compare index {indices[0]} and {indices[1]}"
                else:
                    desc = f"Step {i}: Compare"
            elif action == "SWAP":
                if len(indices) >= 2:
                    desc = f"Step {i}: Swap index {indices[0]} and {indices[1]}"
                else:
                    desc = f"Step {i}: Swap"
            elif action == "SHIFT":
                if len(indices) >= 2:
                    desc = f"Step {i}: Shift index {indices[0]} to {indices[1]}"
                else:
                    desc = f"Step {i}: Shift"
            elif action == "INSERT":
                if len(indices) >= 1:
                    desc = f"Step {i}: Insert at index {indices[0]}"
                else:
                    desc = f"Step {i}: Insert"
            elif action == "MERGE":
                desc = f"Step {i}: Merge arrays"
            else:
                desc = f"Step {i}: {action}"
            
            array_str = str(array)
            formatted_steps.append(f"{desc} → {array_str}")
        
        return formatted_steps
    
    @staticmethod
    def run_sort(algorithm, size):
        """Run sorting algorithm and return formatted results"""
        if algorithm not in SortingManager.ALGORITHMS:
            return {"error": f"Unknown algorithm: {algorithm}"}
        
        if size < 5 or size > 50:
            return {"error": "Array size must be between 5 and 50"}

        data = SortingManager.generate_random_array(size)

        sorter_class = SortingManager.ALGORITHMS[algorithm]
        sorter = sorter_class(data)
        result = sorter.sort()

        comparisons, swaps, shifts = SortingManager.count_operations(result["steps"])

        formatted_steps = SortingManager.format_steps_for_display(result["steps"])
        
        return {
            "algorithm": result["algorithm"],
            "original": result["original"],
            "sorted": result["sorted"],
            "steps": formatted_steps,
            "raw_steps": result["steps"],
            "comparisons": comparisons,
            "swaps": swaps,
            "shifts": shifts,
            "total_steps": len(result["steps"])
        }
