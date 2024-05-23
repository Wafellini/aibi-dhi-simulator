from environment.fogg_behavioural_model import Patient
import numpy as np

class PatientProfile(Patient):
    def __init__(self, patient_profile = "", stress_level=0, fatigue_level=0, habit_strength=5, behaviour_threshold=25, has_family=True,
                 good_time=1, habituation=False, time_preference_update_step = 100000000):
        
        # "resiliant" does is mildly affected by stress and fatigue and does not get motivated by competition
        # "competition_motivated" does well when compared to peers and suffers in high stress and fatigue situations
        # "self_improver" does well when the habit is strongand when compared to peers and suffers in high stress and fatigue situations
        self.patient_profile = patient_profile
        self.record = 0
        self.has_cometition = False
        self.stress_level = stress_level
        self.fatigue_level = fatigue_level
        self.habit_strength = habit_strength  # Scale of 1-10, with 10 being a strong habit
        super().__init__(behaviour_threshold=behaviour_threshold, has_family=has_family, good_time=good_time, habituation=habituation, time_preference_update_step=time_preference_update_step)
 
    # override get_motivation() method to take into account the patient profile
    def get_motivation(self):
        number_of_hours_slept = self.awake_list[-24:].count('sleeping')
        sufficient_sleep = 1 if number_of_hours_slept > 7 else 0
        peer_comparison = self._compare_with_peers()
        record_break = self._break_own_record()
        stress_response = self._response_to_stress()
        fatigue_response = self._response_to_fatigue()
        return self.valence + self.has_family + self.last_activity_score + sufficient_sleep + peer_comparison + record_break + stress_response + fatigue_response

    def _compare_with_peers(self):
        if self.patient_profile not in ["competition_motivated", "self_improver", "resiliant"]:
            return 0

        # Sample hours of walking from a normal distribution with mean 5 and standard deviation 2
        peers_walked = np.random.normal(5, 2)

        # Compare with peers
        if self.patient_profile in ["competition_motivated", "self_improver"]:
            try:
                # print(self.h_nonstationary[-1], peers_walked)
                if self.h_nonstationary[-1] > peers_walked:
                    return 0.1
                else:
                    return 0
            except IndexError:
                return 0
            
        return 0
    
    def _break_own_record(self):
        if self.patient_profile not in ["competition_motivated", "self_improver", "resiliant"]:
            return 0

        # Check if the patient has broken their own record
        if self.patient_profile in ["competition_motivated", "self_improver"]:
            try:
                if self.motion_activity_list.count('walking') > self.record:
                    self.record = self.motion_activity_list.count('walking')
                    return 0.1
                else:
                    return 0
            except IndexError:
                return 0
        
        return 0

    def _response_to_stress(self):
        if self.patient_profile not in ["competition_motivated", "self_improver"]:
            return -0.1 * self.stress_level

        # If stress level is high, the patient is less likely to engage in physical activity
        if self.patient_profile in ["resiliant"]:
            if self.stress_level > 9:
                return -0.1
    
        return 0

    def _response_to_fatigue(self):
        if self.patient_profile not in ["competition_motivated", "self_improver"]:
            return -0.1 * self.fatigue_level

        if self.patient_profile in ["resiliant"]:
            # If fatigue level is high, the patient is less likely to engage in physical activity
            if self.fatigue_level > 8:
                return -0.1
            if self.fatigue_level > 6:
                return -0.05 * np.random.randint(0, 1)
    
        return 0
