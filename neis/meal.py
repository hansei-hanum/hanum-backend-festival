import re
from aiohttp import ClientSession
from env import NeisEnv
from datetime import datetime, timedelta


class MealAPI:
    @staticmethod
    async def fetch_range(range: int):
        async with ClientSession() as session:
            today = datetime.now().strftime("%Y%m%d")
            to = (datetime.now() + timedelta(days=range - 1)).strftime("%Y%m%d")
            response = await session.get(
                "https://open.neis.go.kr/hub/mealServiceDietInfo",
                params={
                    "KEY": NeisEnv.API_KEY,
                    "Type": "json",
                    "ATPT_OFCDC_SC_CODE": NeisEnv.SC_CODE,
                    "SD_SCHUL_CODE": NeisEnv.SCHOOL_CODE,
                    "MLSV_FROM_YMD": today,
                    "MLSV_TO_YMD": to,
                },
            )

            content = await response.json(content_type=None)

            diet_info = content.get("mealServiceDietInfo", [None, None])[1]

            if not diet_info:
                return None

            diet_info = diet_info.get("row", [])

            return [
                {
                    "date": meal.get("MLSV_YMD"),
                    "data": [
                        food.strip()
                        for food in re.sub(
                            r"\([^)]*\)", "", meal.get("DDISH_NM")
                        ).split("<br/>")
                    ],
                }
                for meal in diet_info
            ]

    @staticmethod
    async def fetch(date: str):
        pass
