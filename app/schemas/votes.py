from pydantic import BaseModel, ConfigDict
from datetime import datetime
import uuid

class Vote(BaseModel):
    post_id: 