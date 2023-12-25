from config.db_connect import get_collection

class UserAuthenticator:
    def __init__(self, collection_name):
        self.users_collection = get_collection(collection_name)
    def check_login(self, phone_number, password):
        user = self.users_collection.find_one({"手机号": phone_number})
        if not user:
            return {"message": "Invalid username or password", "status": 0}, 401

        if "_id" in user:
            user["_id"] = str(user["_id"])

        if user["密码"] == password:
            return {"message": "Login successful", "status": 1, "data":{"id": user["_id"], "username": user["用户名"]}}, 200
        else:
            return {"message": "Invalid username or password", "status": 0}, 401

    def sms_login(self, username, sms_code):
        # Implementation for SMS code verification
        # This will depend on how your SMS verification system is set up
        # Typically, you'll check the code against a stored code in the database
        pass

    def send_sms_code(self, username):
        # Implementation for sending SMS code
        # You'll need an SMS service provider to send the code
        pass
