
from app.db.connection import supabase_connection


class UserRepository:

    def __init__(self):
        self.client = supabase_connection.connect()

    # Get user by email
    def get_user_by_email(self, email: str):

        response = (
            self.client
            .table("users")
            .select("*")
            .eq("email", email)
            .execute()
        )

        if response.data:
            return response.data[0]

        return None

    # Create a new user
    def create_user(self, user):

        response = (
            self.client
            .table("users")
            .insert(user.to_dict())
            .execute()
        )

        return response.data


# Create repository object
user_repository = UserRepository()
