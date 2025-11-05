from enum import Enum

class GradeTier(Enum):
    """Grade level classification."""
    PRIMARY = "K-5"           # Kindergarten to 5th
    MIDDLE = "6-8"            # Middle school
    SECONDARY = "9-12"        # High school
    COLLEGE = "College+"      # College and above
