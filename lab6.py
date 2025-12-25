class Firearm:
    """Base firearm class"""
    def __init__(self, magazine_capacity, rate_of_fire, firing_range):
        """
        Initialize firearm
        :param magazine_capacity: Magazine capacity (rounds)
        :param rate_of_fire: Rate of fire (rounds per minute)
        :param firing_range: Firing range (meters)
        """
        self.magazine_capacity = magazine_capacity
        self.rate_of_fire = rate_of_fire
        self.firing_range = firing_range
    
    def time_to_empty_magazine(self):
        """
        Method 1: Calculate time to empty magazine (seconds)
        :return: Time to empty magazine (seconds)
        """
        if self.rate_of_fire <= 0:
            return float('inf')  # Avoid division by zero
        # Convert rounds per minute to rounds per second
        rounds_per_second = self.rate_of_fire / 60.0
        return self.magazine_capacity / rounds_per_second
    
    def __str__(self):
        return (f"Firearm Parameters: Magazine Capacity={self.magazine_capacity} rounds, "
                f"Rate of Fire={self.rate_of_fire} rpm, Range={self.firing_range}m")


class AssaultRifle(Firearm):
    """Assault Rifle class"""
    def __init__(self, magazine_capacity, rate_of_fire, firing_range, burst_mode=False):
        """
        Initialize assault rifle
        :param magazine_capacity: Magazine capacity
        :param rate_of_fire: Rate of fire
        :param firing_range: Firing range
        :param burst_mode: Whether it has burst fire mode (unique field)
        """
        super().__init__(magazine_capacity, rate_of_fire, firing_range)
        self.burst_mode = burst_mode  # Unique field: burst fire mode
        self.weapon_type = "Assault Rifle"  # Weapon type identifier
    
    def fire_rate_to_range_ratio(self):
        """
        Method 2: Ratio of rate of fire to firing range
        :return: Ratio value
        """
        if self.firing_range <= 0:
            return float('inf')  # Avoid division by zero
        return self.rate_of_fire / self.firing_range
    
    def effective_range(self):
        """
        Calculate effective range (assault rifles typically have shorter effective range)
        :return: Effective range (meters)
        """
        return min(self.firing_range * 0.7, 400)  # Assume 70% of nominal range, max 400m
    
    def __str__(self):
        base_info = super().__str__()
        burst_info = "Burst mode supported" if self.burst_mode else "No burst mode"
        return f"{self.weapon_type}\n{base_info}\n{burst_info}, Effective Range={self.effective_range():.1f}m"


class SniperRifle(Firearm):
    """Sniper Rifle class"""
    def __init__(self, magazine_capacity, rate_of_fire, firing_range, scope_magnification):
        """
        Initialize sniper rifle
        :param magazine_capacity: Magazine capacity
        :param rate_of_fire: Rate of fire
        :param firing_range: Firing range
        :param scope_magnification: Scope magnification (unique field)
        """
        super().__init__(magazine_capacity, rate_of_fire, firing_range)
        self.scope_magnification = scope_magnification  # Unique field: scope magnification
        self.weapon_type = "Sniper Rifle"  # Weapon type identifier
    
    def fire_rate_to_range_ratio(self):
        """
        Method 2: Ratio of rate of fire to firing range (sniper rifles typically have slow rate but long range)
        :return: Ratio value
        """
        if self.firing_range <= 0:
            return float('inf')  # Avoid division by zero
        return self.rate_of_fire / self.firing_range
    
    def accuracy_at_range(self, distance):
        """
        Calculate accuracy at specific distance (sniper rifle specific method)
        :param distance: Target distance (meters)
        :return: Accuracy description
        """
        if distance <= self.firing_range * 0.5:
            return "Extremely high accuracy"
        elif distance <= self.firing_range * 0.8:
            return "High accuracy"
        elif distance <= self.firing_range:
            return "Medium accuracy"
        else:
            return "Low accuracy"
    
    def __str__(self):
        base_info = super().__str__()
        return f"{self.weapon_type}\n{base_info}\nScope Magnification={self.scope_magnification}x"


# Additional task: Operator overloading
class FirearmCollection:
    """Firearm collection class for demonstrating operator overloading"""
    def __init__(self, firearms=None):
        self.firearms = firearms if firearms is not None else []
    
    def add_firearm(self, firearm):
        """Add firearm to collection"""
        self.firearms.append(firearm)
    
    def __add__(self, other):
        """
        Overload addition operator: merge two firearm collections
        Check if both objects belong to the same class
        """
        if not isinstance(other, FirearmCollection):
            raise TypeError("Can only merge FirearmCollection objects")
        
        # Create new collection containing all firearms from both collections
        combined_firearms = self.firearms + other.firearms
        return FirearmCollection(combined_firearms)
    
    def total_magazine_capacity(self):
        """Calculate total magazine capacity of all firearms in collection"""
        return sum(firearm.magazine_capacity for firearm in self.firearms)
    
    def __str__(self):
        return f"Firearm Collection: {len(self.firearms)} firearms, Total Magazine Capacity={self.total_magazine_capacity()} rounds"


# Demonstration program
def demonstrate_firearm_classes():
    """Demonstrate firearm class functionality"""
    print("=" * 60)
    print("FIREARM CLASS HIERARCHY DEMONSTRATION")
    print("=" * 60)
    
    # Create base firearm object
    print("\n1. BASE FIREARM CLASS DEMONSTRATION:")
    basic_gun = Firearm(magazine_capacity=30, rate_of_fire=600, firing_range=300)
    print(basic_gun)
    empty_time = basic_gun.time_to_empty_magazine()
    print(f"Magazine empty time: {empty_time:.2f} seconds")
    
    # Create assault rifle object
    print("\n2. ASSAULT RIFLE CLASS DEMONSTRATION:")
    ak47 = AssaultRifle(
        magazine_capacity=30,
        rate_of_fire=600,
        firing_range=400,
        burst_mode=True
    )
    print(ak47)
    print(f"Magazine empty time: {ak47.time_to_empty_magazine():.2f} seconds")
    print(f"Rate of fire to range ratio: {ak47.fire_rate_to_range_ratio():.3f}")
    
    # Create sniper rifle object
    print("\n3. SNIPER RIFLE CLASS DEMONSTRATION:")
    awp = SniperRifle(
        magazine_capacity=10,
        rate_of_fire=40,
        firing_range=800,
        scope_magnification=10
    )
    print(awp)
    print(f"Magazine empty time: {awp.time_to_empty_magazine():.2f} seconds")
    print(f"Rate of fire to range ratio: {awp.fire_rate_to_range_ratio():.3f}")
    print(f"Accuracy at 500m distance: {awp.accuracy_at_range(500)}")
    
    # Demonstrate operator overloading
    print("\n4. OPERATOR OVERLOADING DEMONSTRATION:")
    collection1 = FirearmCollection([ak47])
    collection2 = FirearmCollection([awp])
    
    print(f"Collection 1: {collection1}")
    print(f"Collection 2: {collection2}")
    
    # Merge collections
    combined_collection = collection1 + collection2
    print(f"Combined collection: {combined_collection}")
    
    # Try merging wrong type (will raise exception)
    print("\n5. TYPE CHECKING DEMONSTRATION:")
    try:
        invalid_combination = collection1 + "not a collection"
    except TypeError as e:
        print(f"Type Error: {e}")
    
    # Create more firearms for comparison
    print("\n6. MULTIPLE FIREARMS COMPARISON:")
    m4a1 = AssaultRifle(30, 800, 500, True)
    svd = SniperRifle(10, 30, 1000, 8)
    
    firearms_list = [ak47, awp, m4a1, svd]
    print(ak47+ m4a1)
    
    # print("FIREARM PERFORMANCE COMPARISON:")
    # print("-" * 85)
    # print(f"{'Weapon Type':<20} {'Magazine':<12} {'Rate of Fire':<15} {'Range':<10} {'Empty Time':<15} {'RoF/Range':<12}")
    # print(f"{'':<20} {'Capacity':<12} {'(rpm)':<15} {'(m)':<10} {'(seconds)':<15} {'Ratio':<12}")
    # print("-" * 85)
    
    # for firearm in firearms_list:
    #     if isinstance(firearm, AssaultRifle):
    #         weapon_type = "Assault Rifle"
    #     else:
    #         weapon_type = "Sniper Rifle"
        
    #     print(f"{weapon_type:<20} {firearm.magazine_capacity:<12} {firearm.rate_of_fire:<15} "
    #           f"{firearm.firing_range:<10} {firearm.time_to_empty_magazine():<13.2f} "
    #           f"{firearm.fire_rate_to_range_ratio():<12.3f}")
    
    # print("-" * 85)
    
    # # Analysis of results
    # print("\n7. ANALYSIS:")
    # fastest_empty = min(firearms_list, key=lambda x: x.time_to_empty_magazine())
    # slowest_empty = max(firearms_list, key=lambda x: x.time_to_empty_magazine())
    # highest_ratio = max(firearms_list, key=lambda x: x.fire_rate_to_range_ratio())
    # lowest_ratio = min(firearms_list, key=lambda x: x.fire_rate_to_range_ratio())
    
    # print(f"Fastest magazine empty: {type(fastest_empty).__name__} ({fastest_empty.time_to_empty_magazine():.2f} seconds)")
    # print(f"Slowest magazine empty: {type(slowest_empty).__name__} ({slowest_empty.time_to_empty_magazine():.2f} seconds)")
    # print(f"Highest rate of fire/range ratio: {type(highest_ratio).__name__} ({highest_ratio.fire_rate_to_range_ratio():.3f})")
    # print(f"Lowest rate of fire/range ratio: {type(lowest_ratio).__name__} ({lowest_ratio.fire_rate_to_range_ratio():.3f})")
    
    # # Calculate average values
    # avg_empty_time = sum(f.time_to_empty_magazine() for f in firearms_list) / len(firearms_list)
    # avg_ratio = sum(f.fire_rate_to_range_ratio() for f in firearms_list) / len(firearms_list)
    
    # print(f"\nAverage empty time across all firearms: {avg_empty_time:.2f} seconds")
    # print(f"Average rate of fire/range ratio: {avg_ratio:.3f}")


if __name__ == "__main__":
    demonstrate_firearm_classes()