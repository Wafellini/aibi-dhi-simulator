from environment.fogg_behavioural_model import Patient

#ProfileA - Moderate Response to Stress and Fatigue
#ProfileA leans on habit strength to maintain activity under stress or fatigue, with a moderate reduction in activity engagement.
class ProfileAPatient(Patient):
    def __init__(self, stress_level=0, fatigue_level=0, habit_strength=5):
        super().__init__()
        self.stress_level = stress_level
        self.fatigue_level = fatigue_level
        self.habit_strength = habit_strength  # Scale of 1-10, with 10 being a strong habit
        
    def step(self, action):
        if self.stress_level > 5 or self.fatigue_level > 5:
            return self._reduce_effectiveness_due_to_stress_or_fatigue(action)
        return super().step(action)
    
    def _reduce_effectiveness_due_to_stress_or_fatigue(self, action):
        observation, reward, done, info = super().step(action)
        # Adjust reward based on habit strength; stronger habits are less affected
        reward *= (0.5 + self.habit_strength / 20)  # Slightly better reward for strong habits
        return observation, reward, done, info
    
#ProfileB - Low Response to Stress and Fatigue
#ProfileB values activities that contribute to well-being, showing a slight increase in engagement for these activities even under stress or fatigue.
class ProfileBPatient(Patient):
    def __init__(self, stress_level=0, fatigue_level=0, well_being_value=5):
        super().__init__()
        self.stress_level = stress_level
        self.fatigue_level = fatigue_level
        self.well_being_value = well_being_value  # Value placed on activities that directly contribute to well-being
        
    def step(self, action):
        if self.stress_level > 5 or self.fatigue_level > 5:
            return self._reduce_effectiveness_due_to_stress_or_fatigue(action)
        return super().step(action)
    
    def _reduce_effectiveness_due_to_stress_or_fatigue(self, action):
        observation, reward, done, info = super().step(action)
        # No reward under high stress or fatigue unless the activity is highly valued for well-being
        reward *= (0.1 + self.well_being_value / 10)  # Slightly better reward for high well-being activities
        return observation, reward, done, info
    
#ProfileC - High External Motivation, Low Response to Stress and Fatigue
#ProfileC is driven by achievements but completely disengages under stress or fatigue, despite their high external motivation.
class ProfileCPatient(Patient):
    def __init__(self, stress_level=0, fatigue_level=0, achievements=0):
        super().__init__()
        self.stress_level = stress_level
        self.fatigue_level = fatigue_level
        self.achievements = achievements  # Number of achievements
        
    def step(self, action):
        action = self._enhance_action_based_on_achievements(action)
        if self.stress_level > 5 or self.fatigue_level > 5:
            return self._reduce_effectiveness_due_to_stress_or_fatigue(action)
        return super().step(action)
    
    def _enhance_action_based_on_achievements(self, action):
        # Increase the reward based on the number of achievements
        enhanced_action = action + self.achievements / 10  # Example of enhancing action
        return enhanced_action
    
    def _reduce_effectiveness_due_to_stress_or_fatigue(self, action):
        observation, reward, done, info = super().step(action)
        # No reward under high stress or fatigue, achievements can't offset this
        reward = 0
        return observation, reward, done, info