from typing import Any, Dict, List
from social_core.backends.oauth import BaseOAuth2


class IonOauth2(BaseOAuth2):  # pylint: disable=abstract-method
    name = "ion"
    AUTHORIZATION_URL = "https://ion.tjhsst.edu/oauth/authorize"
    ACCESS_TOKEN_URL = "https://ion.tjhsst.edu/oauth/token"
    ACCESS_TOKEN_METHOD = "POST"
    EXTRA_DATA = [("refresh_token", "refresh_token", True), ("expires_in", "expires")]

    def get_scope(self) -> List[str]:
        return ["read"]

    def get_user_details(self, response: Dict[str, Any]) -> Dict[str, Any]:
        profile = self.get_json(
            "https://ion.tjhsst.edu/api/profile",
            params={"access_token": response["access_token"]},
        )
        # fields used to populate/update User model
        data = {
            key: profile[key]
            for key in ("first_name", "last_name", "id", "is_student", "is_teacher")
        }
        data["username"] = profile["ion_username"]
        data["email"] = profile["tj_email"]
        data["display_name"] = profile["display_name"]
        data["grade"] = profile["grade"]["name"]

        # profile has some information that I want to populate the user model with
        return data

    def get_user_id(self, details: Dict[str, Any], response: Any) -> int:
        return details["id"]
