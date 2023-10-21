from typing import TypeVar, Generic, List, Type
from pymongo import MongoClient, IndexModel, ASCENDING
from datetime import datetime
import json
from typing import List

with open('Config/config.json', 'r') as f:
    config = json.load(f)

T = TypeVar('T')

class GenericMongoRepository(Generic[T]):
    def __init__(self, _exchange : str, _symbol: str, _interval : str, model: Type[T]):
        self.client = MongoClient(config['ConnectionStrings']['mongodb'])
        self.db = self.client[config['ConnectionStrings']['database']]
        self.collection = self.db[f'{_exchange}_{_symbol}_{_interval}']
        self.model = model
        self.collection.create_indexes([IndexModel([("OpenTime", ASCENDING)], unique=True)])

    def Insert(self, item: T):
        insert_result = self.collection.insert_one(item.dict())
        return insert_result.inserted_id

    def InsertMany(self, items: List[T]):
        try:
            items_dict_list = [item.dict() for item in items]  # Pydantic modellerini dict'e çevir
            insert_result = self.collection.insert_many(items_dict_list, ordered=False)
            return insert_result.inserted_ids  # ID'leri döndür
        except:
            print('InsertMany error.')
            return []
    
    def GetDataWithDate(self, _startDate, _endDate) -> List[T]:
        cursor = self.collection.find({'OpenTime': {'$gte': _startDate, '$lte': _endDate}})
        return [self.model(**item) for item in cursor]
    
    def GetLastKline(self) -> T:
        cursor = self.collection.find({}).sort('OpenTime', -1).limit(1)
        return self.model(**cursor[0])
    
    def GetAll(self) -> T:
        cursor = self.collection.find({}).sort('OpenTime', 1)
        return [self.model(**item) for item in cursor]
