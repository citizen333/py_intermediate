from abc import ABC, abstractmethod

class Hero:
    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []
        self.stats = {
            "HP": 128,  # health points
            "MP": 42,  # magic points, 
            "SP": 100,  # skill points
            "Strength": 15,  # сила
            "Perception": 4,  # восприятие
            "Endurance": 8,  # выносливость
            "Charisma": 2,  # харизма
            "Intelligence": 3,  # интеллект
            "Agility": 8,  # ловкость 
            "Luck": 1  # удача
        }

    def get_positive_effects(self):
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.negative_effects.copy()

    def get_stats(self):
        return self.stats.copy()


class AbstractEffect(Hero, ABC):
    def __init__(self, base):
        self.base = base
        
    @abstractmethod
    def get_positive_effects(self):
        pass
    
    @abstractmethod
    def get_negative_effects(self):
        pass
    
    @abstractmethod
    def get_stats_change(self):
        pass
        
    def get_stats(self):
        stats = self.base.get_stats()
        for stat, buff in self.get_stats_change().items():
            stats[stat] += buff
        return stats


class AbstractPositive(AbstractEffect, ABC):
    @abstractmethod
    def get_positive_effects(self):
        pass
    
    def get_negative_effects(self):
        return self.base.get_negative_effects()
    
    @abstractmethod
    def get_stats_change(self):
        pass

class AbstractNegative(AbstractEffect, ABC):
    def get_positive_effects(self):
        return self.base.get_positive_effects()
    
    @abstractmethod
    def get_negative_effects(self):
        pass
    
    @abstractmethod
    def get_stats_change(self):
        pass

class Berserk(AbstractPositive):
    def get_positive_effects(self):
        return self.base.get_positive_effects() + ['Berserk']
    
    def get_stats_change(self):
        stats_change = {
            "HP": 50,  # health points
            "Strength": 7,  # сила
            "Perception": -3,  # восприятие
            "Endurance": 7,  # выносливость
            "Charisma": -3,  # харизма
            "Intelligence": -3,  # интеллект
            "Agility": 7,  # ловкость 
            "Luck": 7  # удача
        }
        return stats_change


class Blessing(AbstractPositive):
    def get_positive_effects(self):
        return self.base.get_positive_effects() + ['Blessing']
    
    def get_stats_change(self):
        stats_change = {
            "Strength": 2,  # сила
            "Perception": 2,  # восприятие
            "Endurance": 2,  # выносливость
            "Charisma": 2,  # харизма
            "Intelligence": 2,  # интеллект
            "Agility": 2,  # ловкость 
            "Luck": 2  # удача
        }
        return stats_change


class Weakness(AbstractNegative):
    def get_negative_effects(self):
        return self.base.get_negative_effects() + ['Weakness']
    
    def get_stats_change(self):
        stats_change = {
            "Strength": -4,  # сила
            "Endurance": -4,  # выносливость
            "Agility": -4
        }
        return stats_change


class EvilEye(AbstractNegative):
    def get_negative_effects(self):
        return self.base.get_negative_effects() + ['EvilEye']
    
    def get_stats_change(self):
        stats_change = {
            "Luck": -10
        }
        return stats_change


class Curse(AbstractNegative):
    def get_negative_effects(self):
        return self.base.get_negative_effects() + ['Curse']
    
    def get_stats_change(self):
        stats_change = {
            "Strength": -2,  # сила
            "Perception": -2,  # восприятие
            "Endurance": -2,  # выносливость
            "Charisma": -2,  # харизма
            "Intelligence": -2,  # интеллект
            "Agility": -2,  # ловкость 
            "Luck": -2  # удача
        }
        return stats_change