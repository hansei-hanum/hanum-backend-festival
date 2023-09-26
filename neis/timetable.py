from collections import defaultdict
from datetime import datetime, timedelta
from aiohttp import ClientSession
from env import NeisEnv
import utils
from aiocache import cached, Cache
from aiocache.serializers import PickleSerializer

DEPARTMANT_BINDING = {
    "CLOUD_SECURITY": "클라우드보안과",
    "NETWORK_SECURITY": "네트워크보안과",
    "HACKING_SECURITY": "해킹보안과",
    "METAVERSE_GAME": "메타버스게임과",
    "GAME": "게임과",
}


class TimeTable:
    @staticmethod
    async def get(department: str, grade: int, classroom: int):
        start_date, end_date = await utils.timetable_range()

        return await TimeTable._fetch(
            department, grade, classroom, start_date, end_date
        )

    @staticmethod
    @cached(ttl=86400, cache=Cache.MEMORY, serializer=PickleSerializer())
    async def _fetch(
        department: str,
        grade: int,
        classroom: int,
        start_date: datetime,
        end_date: datetime,
    ):
        if department not in DEPARTMANT_BINDING:
            return None

        async with ClientSession() as session:
            response = await session.get(
                "https://open.neis.go.kr/hub/hisTimetable",
                params={
                    "KEY": NeisEnv.API_KEY,
                    "Type": "json",
                    "ATPT_OFCDC_SC_CODE": NeisEnv.SC_CODE,
                    "SD_SCHUL_CODE": NeisEnv.SCHOOL_CODE,
                    "DDDEP_NM": DEPARTMANT_BINDING[department],
                    "GRADE": grade,
                    "CLASS_NM": classroom,
                    "TI_FROM_YMD": start_date.strftime("%Y%m%d"),
                    "TI_TO_YMD": end_date.strftime("%Y%m%d"),
                },
            )

            content = await response.json(content_type=None)

            timetable = content.get("hisTimetable", [None, None])[1]

            if not timetable:
                return None

            timetables = timetable.get("row", [])

            grouped_data = defaultdict(list)
            for timetable in timetables:
                date = timetable["ALL_TI_YMD"]
                grouped_data[date].append(timetable["ITRT_CNTNT"])

            time_range = [
                (start_date + timedelta(days=i)).strftime("%Y%m%d")
                for i in range((end_date - start_date).days + 1)
            ]
            for date in time_range:
                grouped_data.setdefault(date, [])

            result = [
                {
                    "date": datetime.strptime(date, "%Y%m%d").strftime(
                        "%Y-%m-%dT00:00:00"
                    ),
                    "data": contents,
                }
                for date, contents in grouped_data.items()
            ]

            return result
