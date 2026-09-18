from src.infrastructures.auth.password import hash_password
import re
import uuid


class RegisterUser:
    def __init__(self, repository):
        self.repository = repository
