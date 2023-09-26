from collections import defaultdict
from datetime import datetime, timedelta
from aiohttp import ClientSession
from env import NeisEnv
import utils
from aiocache import cached, Cache
from aiocache.serializers import PickleSerializer

EXCLUDED_SCHEDULE_NAMES = [
    "토요휴업일",
    "일요휴업일",
    "토요휴업일(대체)",
    "일요휴업일(대체)",
    "토요휴업일(대체공휴일)",
    "일요휴업일(대체공휴일)",
]


class Schedule:
    @staticmethod
    async def get(month: int = None):
        start_date, end_date = await utils.month_range(month)

        return await Schedule._fetch(start_date, end_date)

    @staticmethod
    @cached(ttl=86400, cache=Cache.MEMORY, serializer=PickleSerializer())
    async def _fetch(start: datetime, end: datetime):
        async with ClientSession() as session:
            response = await session.get(
                "https://open.neis.go.kr/hub/SchoolSchedule",
                params={
                    "KEY": NeisEnv.API_KEY,
                    "Type": "json",
                    "ATPT_OFCDC_SC_CODE": NeisEnv.SC_CODE,
                    "SD_SCHUL_CODE": NeisEnv.SCHOOL_CODE,
                    "AA_FROM_YMD": start.strftime("%Y%m%d"),
                    "AA_TO_YMD": end.strftime("%Y%m%d"),
                },
            )

            content = await response.json(content_type=None)

            schedule = content.get("SchoolSchedule", [None, None])[1]

            if not schedule:
                return None

            schedule = schedule.get("row", [])

            # group by AA_YMD
            grouped_schedule = defaultdict(list)
            for item in schedule:
                grouped_schedule[item.get("AA_YMD")].append(item)

            formatted_data = [
                {
                    "date": datetime.strptime(date, "%Y%m%d").strftime(
                        "%Y-%m-%dT00:00:00"
                    ),
                    "data": [
                        item.get("EVENT_NM")
                        for item in items
                        if item.get("EVENT_NM") not in EXCLUDED_SCHEDULE_NAMES
                    ],
                }
                for date, items in grouped_schedule.items()
            ]

            return [item for item in formatted_data if item.get("data")]
