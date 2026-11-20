import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from pprint import pprint


@dataclass
class Record:
    id: int
    name: str
    data: list


GLOBAL_LIST: list[Record] = []


class BackupData:
    def __init__(self, database: list[Record]) -> None:
        self.database = database

        self.full_dir = Path("folder_1")
        self.increment_dir = Path("folder_2")
        self.differential_dir = Path("folder_3")

        self.full_dir.mkdir(exist_ok=True)
        self.increment_dir.mkdir(exist_ok=True)
        self.differential_dir.mkdir(exist_ok=True)

        self.last_full_ids: set[int] = set()

        self.last_backup_ids: set[int] = set()

        self.full_count = 0
        self.increment_count = 0
        self.differential_count = 0

    @staticmethod
    def _save(path: Path, records: list[Record]) -> None:
        data = [asdict(record) for record in records]

        with path.open("w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4,
            )

    def full_backup(self) -> None:
        self.full_count += 1

        path = self.full_dir / f"full_{self.full_count}.json"

        self._save(path, self.database)

        current_ids = {record.id for record in self.database}

        self.last_full_ids = current_ids.copy()
        self.last_backup_ids = current_ids.copy()

        print(
            f"[FULL] Сохранено {len(self.database)} записей -> {path}"
        )

    def increment(self) -> None:
        new_records = [
            record
            for record in self.database
            if record.id not in self.last_backup_ids
        ]

        if not new_records:
            print("[INCREMENT] Новых данных нет")
            return

        self.increment_count += 1

        path = (
            self.increment_dir / f"increment_{self.increment_count}.json"
        )

        self._save(path, new_records)

        self.last_backup_ids.update(
            record.id for record in new_records
        )

        print(
            f"[INCREMENT] Сохранено {len(new_records)} записей -> {path}"
        )

    def differential(self) -> None:
        new_records = [
            record
            for record in self.database
            if record.id not in self.last_full_ids
        ]

        if not new_records:
            print("[DIFFERENTIAL] Новых данных нет")
            return

        self.differential_count += 1

        path = (
            self.differential_dir
            / f"differential_{self.differential_count}.json"
        )

        self._save(path, new_records)

        print(
            f"[DIFFERENTIAL] Сохранено {len(new_records)} записей -> {path}"
        )



def main():
    record_id = 0

    print("== Запуск БД ==")
    print("Загрузка данных в бд: ")

    backup = BackupData(GLOBAL_LIST)


    for i in range(1, 101):
        record_id += 1

        GLOBAL_LIST.append(
            Record(
                id=record_id,
                name=f"record_{i}",
                data=[random.randint(20, 40)],
            )
        )

    backup.full_backup()


    for i in range(101, 201):
        record_id += 1

        GLOBAL_LIST.append(
            Record(
                id=record_id,
                name=f"record_{i}",
                data=[random.randint(20, 40)],
            )
        )

        if i % 10 == 0:
            backup.differential()

        if i % 20 == 0:
            backup.increment()

    pprint(GLOBAL_LIST[:5])
    print(f"Осталось еще {len(GLOBAL_LIST) - 5}")


if __name__ == '__main__':
    main()


