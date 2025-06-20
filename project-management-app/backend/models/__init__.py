from ..database import Base  # Make Base accessible from models package

# Import all model classes here to ensure they are registered with Base.metadata
from .user import User, UserRole
from .project import Project
from .deliverable import Deliverable, DeliverablePriority, DeliverableStatus
from .consultant_profile import ConsultantProfile
from .finance import ProjectBudget, Payment, PaymentStatus

# You can also define __all__ if you want to control what 'from models import *' imports
__all__ = [
    "Base",
    "User", "UserRole",
    "Project",
    "Deliverable", "DeliverablePriority", "DeliverableStatus",
    "ConsultantProfile",
    "ProjectBudget", "Payment", "PaymentStatus",
]
