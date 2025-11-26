"""
Zombie Survival Knapsack Problem Solver
Dynamic Programming Solution for Option 4: 3x3 backpack, no disease, 15 initial points
"""

class ZombieSurvivalKnapsack:
    """
    A class to solve the zombie survival knapsack problem using dynamic programming.
    Tom needs to select items to maximize survival points while fitting in 3x3 backpack.
    """
    
    def __init__(self):
        # Items dictionary: {mark: (space, survival_points)}
        self.items = {
            'r': (3, 25),  # Rifle
            'p': (2, 15),  # Pistol
            'a': (2, 15),  # Ammo
            'm': (2, 20),  # Medkit
            'i': (1, 5),   # Inhaler
            'k': (1, 15),  # Knife
            'x': (3, 20),  # Axe
            't': (1, 25),  # Talisman
            'f': (1, 15),  # Flask
            'd': (1, 10),  # Antidote
            's': (2, 20),  # Supplies
            'c': (2, 20)   # Crossbow
        }
        self.capacity = 9  # 3x3 backpack capacity
        self.initial_points = 15  # Starting survival points
        
    def solve_knapsack(self):
        """
        Solve the knapsack problem using dynamic programming.
        
        Returns:
            tuple: (final_survival_points, list_of_selected_items)
        """
        # Get lists of items, spaces, and values
        item_list = list(self.items.keys())
        space_list = [self.items[item][0] for item in item_list]
        value_list = [self.items[item][1] for item in item_list]
        n = len(item_list)
        
        # Initialize DP table
        # dp[i][w] represents maximum value using first i items with capacity w
        dp = [[0] * (self.capacity + 1) for _ in range(n + 1)]
        
        # Fill DP table using bottom-up approach
        for i in range(1, n + 1):
            current_space = space_list[i-1]
            current_value = value_list[i-1]
            
            for w in range(1, self.capacity + 1):
                if current_space <= w:
                    # Choose between including or excluding current item
                    dp[i][w] = max(dp[i-1][w], 
                                  current_value + dp[i-1][w - current_space])
                else:
                    # Cannot include current item due to space constraints
                    dp[i][w] = dp[i-1][w]
        
        # Backtrack to find selected items
        selected_items = self._backtrack_items(dp, item_list, space_list)
        
        # Calculate final survival points (items points + initial points)
        items_value = sum(self.items[item][1] for item in selected_items)
        final_points = items_value + self.initial_points
        
        return final_points, selected_items
    
    def _backtrack_items(self, dp, item_list, space_list):
        """
        Backtrack through DP table to find which items were selected.
        
        Args:
            dp: Dynamic programming table
            item_list: List of item marks
            space_list: List of item spaces
            
        Returns:
            list: Selected items
        """
        selected_items = []
        w = self.capacity
        n = len(item_list)
        
        # Trace back from bottom-right of DP table
        for i in range(n, 0, -1):
            # If value changed from previous row, item was included
            if dp[i][w] != dp[i-1][w]:
                selected_items.append(item_list[i-1])
                w -= space_list[i-1]
        
        return selected_items
    
    def display_backpack_layout(self, selected_items):
        """
        Display the backpack contents in a 3x3 grid format.
        
        Args:
            selected_items: List of items to display in backpack
        """
        print("\n" + "="*50)
        print("BACKPACK LAYOUT (3×3 GRID)")
        print("="*50)
        
        # Create backpack grid representation
        backpack_grid = [[' ' for _ in range(3)] for _ in range(3)]
        current_row, current_col = 0, 0
        
        # Place items in the grid
        for item in selected_items:
            space_needed = self.items[item][0]
            
            # Check if item fits in current row
            if current_col + space_needed <= 3:
                for i in range(space_needed):
                    backpack_grid[current_row][current_col + i] = item
                current_col += space_needed
                
                # Move to next row if current row is full
                if current_col >= 3:
                    current_row += 1
                    current_col = 0
            else:
                # Move to next row and try again
                current_row += 1
                current_col = 0
                if current_row >= 3:
                    break  # Backpack full
                
                # Place item in new row
                for i in range(space_needed):
                    if current_col + i < 3:
                        backpack_grid[current_row][current_col + i] = item
                current_col += space_needed
        
        # Display the grid with borders
        self._print_grid(backpack_grid)
    
    def _print_grid(self, grid):
        """
        Print the backpack grid with proper formatting.
        
        Args:
            grid: 3x3 grid representing backpack contents
        """
        # Top border
        print("+" + "---+" * 3)
        
        for row in grid:
            print("|", end="")
            for cell in row:
                print(f" {cell} |", end="")
            print("\n+" + "---+" * 3)
    
    def calculate_statistics(self, selected_items):
        """
        Calculate and return statistics about the solution.
        
        Args:
            selected_items: List of selected items
            
        Returns:
            tuple: (total_space_used, items_value, final_points)
        """
        total_space_used = sum(self.items[item][0] for item in selected_items)
        items_value = sum(self.items[item][1] for item in selected_items)
        final_points = items_value + self.initial_points
        
        return total_space_used, items_value, final_points
    
    def find_all_optimal_solutions(self):
        """
        Advanced feature: Find all combinations that achieve maximum value.
        
        Returns:
            list: All optimal item combinations
        """
        item_list = list(self.items.keys())
        space_list = [self.items[item][0] for item in item_list]
        value_list = [self.items[item][1] for item in item_list]
        n = len(item_list)
        
        # First, find maximum value using DP
        dp = [[0] * (self.capacity + 1) for _ in range(n + 1)]
        
        for i in range(1, n + 1):
            current_space = space_list[i-1]
            current_value = value_list[i-1]
            for w in range(1, self.capacity + 1):
                if current_space <= w:
                    dp[i][w] = max(dp[i-1][w], 
                                  current_value + dp[i-1][w - current_space])
                else:
                    dp[i][w] = dp[i-1][w]
        
        max_value = dp[n][self.capacity]
        
        # Find all combinations that achieve max_value
        optimal_combinations = []
        self._find_combinations(dp, item_list, space_list, value_list, 
                               n, self.capacity, [], optimal_combinations, max_value)
        
        return optimal_combinations
    
    def _find_combinations(self, dp, items, spaces, values, i, w, 
                          current_combo, results, target_value):
        """
        Recursively find all combinations that achieve target value.
        """
        if target_value == 0:
            results.append(current_combo[::-1])  # Reverse to maintain order
            return
        
        if i == 0 or w == 0:
            return
        
        # If current item can be included and gives target value
        if spaces[i-1] <= w:
            include_value = values[i-1] + dp[i-1][w - spaces[i-1]]
            if include_value == target_value:
                self._find_combinations(dp, items, spaces, values, i-1, 
                                      w - spaces[i-1], 
                                      current_combo + [items[i-1]], 
                                      results, target_value - values[i-1])
        
        # Exclude current item
        if dp[i-1][w] == target_value:
            self._find_combinations(dp, items, spaces, values, i-1, w, 
                                  current_combo, results, target_value)


def main():
    """
    Main function to demonstrate the knapsack solver.
    """
    print("🧟 ZOMBIE SURVIVAL KNAPSACK SOLVER 🧟")
    print("=" * 50)
    
    # Initialize solver
    solver = ZombieSurvivalKnapsack()
    
    # Display problem parameters
    print(f"Backpack Capacity: {solver.capacity} slots")
    print(f"Initial Survival Points: {solver.initial_points}")
    print(f"Available Items: {len(solver.items)}")
    
    # Solve using dynamic programming
    print("\n" + "="*50)
    print("SOLVING WITH DYNAMIC PROGRAMMING...")
    print("="*50)
    
    final_points, selected_items = solver.solve_knapsack()
    total_space, items_value, calculated_points = solver.calculate_statistics(selected_items)
    
    # Display results
    print(f"✅ OPTIMAL SOLUTION FOUND!")
    print(f"Selected Items: {selected_items}")
    print(f"Space Used: {total_space}/{solver.capacity} slots")
    print(f"Items Survival Points: {items_value}")
    print(f"Initial Bonus: +{solver.initial_points}")
    print(f"FINAL SURVIVAL POINTS: {calculated_points}")
    
    # Display backpack layout
    solver.display_backpack_layout(selected_items)
    
    # Survival check
    if calculated_points > 0:
        print("\n🎉 SUCCESS! Tom can survive the journey! 🎉")
    else:
        print("\n💀 FAILURE! Survival points are negative! 💀")
    
    # Advanced feature: Find all optimal solutions
    print("\n" + "="*50)
    print("ADVANCED: FINDING ALL OPTIMAL SOLUTIONS")
    print("="*50)
    
    try:
        all_optimal = solver.find_all_optimal_solutions()
        if all_optimal:
            print(f"Found {len(all_optimal)} optimal solution(s):")
            for i, solution in enumerate(all_optimal, 1):
                space_used = sum(solver.items[item][0] for item in solution)
                value_used = sum(solver.items[item][1] for item in solution)
                print(f"Solution {i}: {solution} (Space: {space_used}, Value: {value_used})")
        else:
            print("No optimal solutions found.")
    except Exception as e:
        print(f"Advanced feature unavailable: {e}")


if __name__ == "__main__":
    main()