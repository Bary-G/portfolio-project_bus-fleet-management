from app.models.base_model import BaseModel


class Report(BaseModel):
    """Class representing a Report entity"""

    def __init__(self, comment):
        super().__init__()
        if not isinstance(comment, str):
            raise TypeError("comment must be a string")
        if not comment.strip():
            raise ValueError("comment cannot be empty")
        if len(comment) > 50:
            raise ValueError("comment cannot exceed 50 characters")
        self.comment = comment

    def to_dict(self):
        """Return a dictionary representation of Report"""
        base_dict = super().to_dict()
        base_dict.update({
            "comment": self.comment
        })
        return base_dict
