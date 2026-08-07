from datetime import datetime

from SmartApi import SmartConnect
import pyotp

from app.core.security import decrypt


class AngelService:
    """
    Runtime session manager
    """

    ACTIVE_SESSIONS = {}

    @classmethod
    def login(
        cls,
        member,
    ):

        api_key = decrypt(member.api_key)
        password = decrypt(member.password)
        totp_secret = decrypt(member.totp_secret)

        totp = pyotp.TOTP(
            totp_secret
        ).now()

        smart = SmartConnect(
            api_key=api_key
        )

        response = smart.generateSession(
            member.client_id,
            password,
            totp,
        )

        if not response.get("status"):

            return {
                "success": False,
                "message": response.get(
                    "message",
                    "Login Failed",
                ),
            }

        data = response["data"]

        refresh_token = data["refreshToken"]

        profile = smart.getProfile(
            refresh_token
        )

        if not profile.get("status"):

            return {
                "success": False,
                "message": "Profile Fetch Failed",
            }

        feed_token = smart.getfeedToken()

        cls.ACTIVE_SESSIONS[
            member.client_id
        ] = {
            "member_id": member.id,
            "member_name": member.member_name,
            "smart": smart,
            "jwt_token": data["jwtToken"],
            "refresh_token": refresh_token,
            "feed_token": feed_token,
            "profile": profile["data"],
            "login_time": datetime.now(),
            "status": "ONLINE",
        }

        return {
            "success": True,
            "message": "Login Successful",
        }

    @classmethod
    def logout(
        cls,
        client_id: str,
    ):

        if client_id in cls.ACTIVE_SESSIONS:
            del cls.ACTIVE_SESSIONS[
                client_id
            ]

        return True

    @classmethod
    def is_logged_in(
        cls,
        client_id: str,
    ):

        return (
            client_id
            in cls.ACTIVE_SESSIONS
        )

    @classmethod
    def get_session(
        cls,
        client_id: str,
    ):

        return cls.ACTIVE_SESSIONS.get(
            client_id
        )

    @classmethod
    def login_all(
        cls,
        members,
    ):

        result = []

        for member in members:

            res = cls.login(member)

            result.append(
                {
                    "member": member.member_name,
                    "client_id": member.client_id,
                    "success": res["success"],
                    "message": res["message"],
                }
            )

        return result

    @classmethod
    def logout_all(cls):

        cls.ACTIVE_SESSIONS.clear()

        return True

    @classmethod
    def login_selected(cls, members):

        result = []

        success = 0
        failed = 0

        for member in members:

            try:

                res = cls.login(member)

                if res["success"]:
                    success += 1
                else:
                    failed += 1

                result.append({
                    "member_id": member.id,
                    "member_name": member.member_name,
                    "client_id": member.client_id,
                    "success": res["success"],
                    "message": res["message"]
                })

            except Exception as e:

                failed += 1

                result.append({
                    "member_id": member.id,
                    "member_name": member.member_name,
                    "client_id": member.client_id,
                    "success": False,
                    "message": str(e)
                })

        return {
            "total": len(members),
            "success": success,
            "failed": failed,
            "result": result
        }

    @classmethod
    def online_members(cls):

        return len(cls.ACTIVE_SESSIONS)