import json

from notes.redis_service import RedisService


class RedisNote:

    def __init__(self):
        self.redis = RedisService()

    def set(self, user_id, notes):
        note_id = notes.get("id")
        note_dict = self.get(user_id)
        note_dict.update({note_id: notes})
        self.redis.setter(user_id, json.dumps(note_dict))
        return self.get(user_id)

    def get(self, user_id):
        get_value = self.redis.getter(user_id)
        return json.loads(get_value) if get_value else {}

    def delete(self,user_id, note_id):
        note_dict = self.get(user_id)
        note=note_dict.get(str(note_id))
        if note is not None:
            note_dict.pop(str(note_id))
            self.redis.setter(user_id, json.dumps(note_dict))