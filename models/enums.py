import enum


class RoleType(enum.Enum):
    candidate = "candidate"
    approver = "approver"
    admin = "admin"


class Category(enum.Enum):
    delivery = "delivery"
    pet_sitter = "pet_sitter"
    scooter_charging = "scooter_charging"
    online_surveys = "online_surveys"
    driver = "driver"
    translation = "translation"
    photography = "photography"
    cleaning = "cleaning"
    tutor = "tutor"
    security_officer = "security_officer"
    nanny = "nanny"
    other = "other"
