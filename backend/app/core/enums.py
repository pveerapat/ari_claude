import enum


class UserRole(str, enum.Enum):
    farmer = "farmer"
    ari_staff = "ari_staff"
    farm_coordinator = "farm_coordinator"
    agronomist = "agronomist"
    reviewer = "reviewer"
    admin = "admin"
    root = "root"


class EntryType(str, enum.Enum):
    note = "note"
    consultation = "consultation"


class EntryContext(str, enum.Enum):
    general_note = "general_note"
    registered_farm = "registered_farm"
    external_observation = "external_observation"
    interview = "interview"


class ItemType(str, enum.Enum):
    photo = "photo"
    video = "video"
    voice = "voice"
    text = "text"
    file = "file"
    link = "link"


class ExternalAI(str, enum.Enum):
    chatgpt = "chatgpt"
    gemini = "gemini"
    claude = "claude"
    other = "other"


class UploadStatus(str, enum.Enum):
    pending = "pending"
    uploading = "uploading"
    failed = "failed"
    completed = "completed"


class FollowUpOutcome(str, enum.Enum):
    improved = "improved"
    same = "same"
    worse = "worse"
    unknown = "unknown"


class FarmerStatus(str, enum.Enum):
    owner = "owner"
    owner_family = "owner_family"
    farm_staff = "farm_staff"


class MembershipStatus(str, enum.Enum):
    pending_farm_approval = "pending_farm_approval"
    active = "active"
    rejected = "rejected"
    suspended = "suspended"
    revoked = "revoked"


class AccountStatus(str, enum.Enum):
    active = "active"
    active_pending_verification = "active_pending_verification"
    pending_review = "pending_review"
    suspended = "suspended"
    rejected = "rejected"
    revoked = "revoked"
