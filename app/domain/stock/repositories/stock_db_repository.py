from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.stock import Stock
from datetime import datetime

class StockDbRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_stock(self, stock_data: dict) -> Stock:
        db_stock = Stock(**stock_data)
        self.db.add(db_stock)
        self.db.commit()
        self.db.refresh(db_stock)
        return db_stock

    def get_stock_by_id(self, stock_id: int) -> Optional[Stock]:
        return self.db.query(Stock).filter(Stock.id == stock_id).first()

    def get_stock_by_code(self, stock_code: str) -> Optional[Stock]:
        return self.db.query(Stock).filter(Stock.code == stock_code).first()

    def get_all_stocks(self, skip: int = 0, limit: int = 100) -> List[Stock]:
        return self.db.query(Stock).offset(skip).limit(limit).all()

    def update_stock(self, stock_id: int, stock_data: dict) -> Optional[Stock]:
        db_stock = self.db.query(Stock).filter(Stock.id == stock_id).first()
        if db_stock:
            for key, value in stock_data.items():
                setattr(db_stock, key, value)
            db_stock.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(db_stock)
        return db_stock

    def delete_stock(self, stock_id: int) -> bool:
        db_stock = self.db.query(Stock).filter(Stock.id == stock_id).first()
        if db_stock:
            self.db.delete(db_stock)
            self.db.commit()
            return True
        return False
