import datetime
from base64 import b64decode
from typing import List
from uuid import UUID

import jwt
from browser.models import (Folder, InstanceBrowser,
                            UserProfileInstanceBrowserRelation)
from browser.serializers import BrowserInstanceSerializer
from folder.serializers import FolderSerializer, ShareFolderSerializer
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# private_key = b"""-----BEGIN RSA PRIVATE KEY-----\n
# MIIG4wIBAAKCAYEA1MSdsaPH2ShtjOo4c02+DbYcTdwUBLY+vNSXr2tV8/jGU059
# Jak9CA7VSlKR/fik18D7Lq1beLjW56kV4Xvm3qmpxOc3eNGmj8dqtO0G3Lp1FAZz
# xlu2SZsHmmVq9isZcN70apkwlDgIZ11NVIq/1iXzr0pIRMKkMNHTGBGBkYOrIcgd
# H2elvIqfiit6Gts/zho4YCjgyn/r3Vgy/jCu6VbfwE9xVY/DB4srD5LrZMabRzN2
# YwSTI+sRqpbt7I7nZ6o8CuyqHDLjbO9VzE0povBshTfoyog9XGcQHwTmWn4bdnsh
# 2I1x3gQpaqxdRs4vnKmXJ9GvC/sYla0GYXyDecpgjITqx3QA6aKx9+EVh/o6owYT
# HXaToVkP7U5m8cqaloQFfA8HLsGDg9A0QaMtixnX7KtT/ZvKFMcazRJ1GX42Uaeu
# O1opZKtjBHLtmaPadNeZdD77VytwY2UHeW5QSnfpos7IxUTATpd6KTWUV3snVQny
# iltCI1BHJC01sWePAgMBAAECggGAEG1tz31ZvMaGTs72tNBX0C8zWD+ZvBNmHKY9
# X+nlpQScK2pv9yxt7eVXSnm9k+JSt+XKfvwbh+KdlR1U9yfd12s6FF3VxppJReib
# sIRsdzZeO8GTxsjl9iDmIWGbNI53VGOic2iIe6kn3PMzOUfNL/eWLP6LPePZUXuh
# 1MXlPxrvZ5hPx1D1Vu1NDBn3P4OWFY+osqP1Vy0xRNG+fim8F4ABnpODqJuE71wr
# YvRxAELlUkYC6fo8chWAM6+bhxwxVaGiIKluikmVJtt0/aAcKR6fUogGfcumRGPp
# HzFRDZBVdLmVwbpVrfCbULP7wYk2A5QMu2skAlZSYtyWJbBRXvgweEXepJaXC6FW
# atD5ypi1kSX9K71BRM7DKrmY2/RsyR6Y8a2PdiOHB5MNYKoeH5o2k0htsV2zUspo
# 4nER4AB5a5fEysGg3yCST+m2q7UOBvcB0LblE/0sNuOGtCNPmtChdZxspsVRm2ID
# XkKrljy+cdOsxZ0iVcvGhyJRhlCBAoHBAOn6KMfbB11uliVyouFfV5ZoiWPeIXbF
# wkAnev+8kF/GmYU7bAFAhRg2qzwqTVlC2eeG+dHKgr9+xHjsTOIoLB/5jPgcIfY9
# l0lZ9LmNwwvI3wg6XWnwQf9X97YZ1E1A3TpBU5XNzTo7hVtZgHDIf4ufB5sDhZ1S
# nXf/+uBe7gJMMnizpq/tqr+0oPJd4uac1rTp2wsFx6MJjOR8kijZOnr3SdKNU3xo
# shZWlRHy9qCjftxTIuOFSxdEZhJUm87w8QKBwQDoy2hYI0hMn3+lwu30lk4+LGSW
# 9ij7AzyTVcRR9FbYciTMQ24IrK020A9rDXkVkJ6FeTbCtT3UkFOlz3JZkEpvY/qd
# Mf8hfd5IO68R1Z5lZpLCFAqcIRUE9l7En9nMiuqdDPZJfhUjhlajzhQotYEv1Fqq
# WDmK0IaklSfGJt0LVsZSuINErHaC5HjJocL86Cqao9a1rxgJA7maCfirwABAafHc
# 6OhFuW5Pi6IXj9QbM7PgbGjIIXPDFfs7FkqF4H8CgcEAu0MACJSAXIL5oJcTTZVl
# IHgiHc/WsJyuT3JJuwxL8Juem0dntcjRvQNkIQ8qQNqEVA1vPDz8UA9BaBaXohnM
# 1vp/nMPHWrEIuChK+YdAJ9poxskPoo4sBBV/qDsb84iKhulp4GeKbaTdorMLXTja
# /AAXsjUrZzKL3VL+kzzm+OfLLVd7fSqWkkAa4F/MDg5QuRLBwRyrHw2xud0Jja/u
# YiQw7Vc3Dkcs4TwCqw7t3Lt9+RCAx+ASrViM6PbWjNXBAoHAa0fiDEwmM3mFn+RX
# ONJTuH9I0/EZLaRuNA/ga0xJAXKI1sF0YfcB1DLKCDGrTW7aPvR/cfeISP9CLTWO
# owvF4dOXWP4Db3HMEEnBAl0Jo/1DQMFvqkfsod7QCZkJDCQwvrOMhI3gPADayJ5d
# 1+zdXidkqQADdJ9ojUxXig+66lDREKoLhIheDTAxIeq0K0zq5Vz/w7avQug+jmht
# +uh+tTCdz4peEFPGLE5TIrybqPWIvbH4D9KqwIrOvoolSdENAoHAaa+n0ZXGovFy
# Hjk02KSinY80b0VzOKKXCh3vc5+2WAS9Ar4no7Cobt5QhKA0GtYpLSCmUFRvsZ1P
# Gemb/FH+yC5nLvKaDOpHktZONIARP8e9R1ku9o+9lOFAIU0MYHx0Ep0y4XWgMrTp
# UuP3ai7zn++ag7Lu1QEm5pQAd2n+zMuKZbBISVA9fPbC9RkJX66E4zVbsEUnDDBD
# 9Rlu+3Dc0LwSjtAxXPDInmEh2mp3O/aZtMPVUPgDA4Ig7GbQC6W/\n
# -----END RSA PRIVATE KEY-----"""

private_key = "secret"


class FolderCreateView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FolderSerializer

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        folder = Folder.objects.create(**serializer.validated_data)

        return Response(data=self.serializer_class(folder).data)


class ShareFolderPermissionView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ShareFolderSerializer

    def post(self, request, folder_uuid: UUID) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        share_data = serializer.validated_data
        share_data["folder_id"] = folder_uuid
        share_data["exp"] = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

        token = jwt.encode(share_data, private_key, algorithm="HS256")
        return Response(data={"share_token": token, "url": f"/folder/add/{token}"})


@api_view(["GET", "PUT"])
@permission_classes(
    [
        IsAuthenticated,
    ]
)
def folder_view(request, folder_uuid: UUID) -> Response:
    response = {}

    if request.method == "GET":
        try:
            response["data"] = FolderSerializer(Folder.objects.get(id=folder_uuid))
        except Folder.DoesNotExist:
            response["status"] = status.HTTP_404_NOT_FOUND

    elif request.method == "PUT":
        serializer = FolderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            Folder.objects.filter(id=folder_uuid).update(**serializer.data)
            response["status"] = status.HTTP_200_OK
        except Exception:
            response["status"] = status.HTTP_400_BAD_REQUEST

    return Response(**response)


@api_view(["GET", "POST"])
@permission_classes(
    [
        IsAuthenticated,
    ]
)
def add_folder_view(request, shared_token: str) -> Response:
    def add_browser_to_relation(
        browser_id, user, rule
    ) -> UserProfileInstanceBrowserRelation:
        return UserProfileInstanceBrowserRelation.objects.create(
            user_id=user.id, browser_id=browser_id, is_creator=False, rule_type=rule
        )

    token_data = jwt.decode(shared_token, private_key, algorithms=["HS256"])

    browsers: List[BrowserInstanceSerializer] = list(
        map(
            lambda b: BrowserInstanceSerializer(b).data,
            InstanceBrowser.objects.filter(folder_id=token_data["folder_id"]),
        )
    )
    relations: List[InstanceBrowser] = list(
        map(
            lambda b: add_browser_to_relation(
                b["id"], request.user, token_data["rule"]
            ),
            browsers,
        )
    )

    return Response(data=browsers)
