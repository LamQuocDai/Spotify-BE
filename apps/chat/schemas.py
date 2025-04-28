from pydantic import BaseModel
class PrivateMessageIn(BaseModel):
    id_sender: int
    id_receiver: int
    message: str
