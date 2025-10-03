"""
Base Repository Pattern
Provides standardized methods for ORM and Native SQL operations

IMPORTANT PATTERNS:

1. ORM USAGE (Recommended for simple CRUD):
   - Use built-in methods: get(), get_multi(), create(), update(), delete()
   - SQLAlchemy handles transactions automatically
   - Type-safe with model validation

   Example:
   ```python
   # In repository
   from atams.db.repository import BaseRepository
   from app.models.user import User as UserModel

   class UserRepository(BaseRepository[UserModel]):
       def __init__(self):
           super().__init__(UserModel)

   # In service
   user_repo = UserRepository()
   user = user_repo.get(db, user_id=1)
   new_user = user_repo.create(db, {"u_name": "John"})
   ```

2. NATIVE SQL USAGE (For complex queries):
   - Use execute_raw_sql() or execute_raw_sql_dict()
   - Always use parameterized queries to prevent SQL injection
   - Must handle transaction manually if needed

   Example:
   ```python
   # In repository
   def get_users_with_stats(self, db: Session, min_age: int):
       query = '''
           SELECT u.u_id, u.u_name, COUNT(o.order_id) as total_orders
           FROM users u
           LEFT JOIN orders o ON u.u_id = o.user_id
           WHERE u.age >= :min_age
           GROUP BY u.u_id, u.u_name
       '''
       return self.execute_raw_sql_dict(db, query, {"min_age": min_age})

   # In service
   users_stats = user_repo.get_users_with_stats(db, min_age=18)
   ```

3. TRANSACTION HANDLING:
   - ORM methods auto-commit
   - For Native SQL with multiple operations, use db.begin()

   Example:
   ```python
   with db.begin():
       self.execute_raw_sql(db, "INSERT INTO ...", params)
       self.execute_raw_sql(db, "UPDATE ...", params)
   ```
"""
from typing import TypeVar, Generic, Type, Optional, List, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func, text

from atams.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Base repository for database operations
    Supports both ORM and Native SQL approaches
    """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    # ==================== ORM METHODS ====================

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        Get single record by ID using ORM

        Args:
            db: Database session
            id: Primary key value

        Returns:
            Model instance or None if not found
        """
        return db.query(self.model).filter(self.model.u_id == id).first()

    def get_multi(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        """
        Get multiple records with pagination using ORM

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of model instances
        """
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: Dict[str, Any]) -> ModelType:
        """
        Create new record using ORM

        Args:
            db: Database session
            obj_in: Dictionary with field values

        Returns:
            Created model instance

        Example:
            user = repo.create(db, {"u_name": "John", "u_email": "john@example.com"})
        """
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        db_obj: ModelType,
        obj_in: Dict[str, Any]
    ) -> ModelType:
        """
        Update existing record using ORM

        Args:
            db: Database session
            db_obj: Existing model instance to update
            obj_in: Dictionary with fields to update

        Returns:
            Updated model instance

        Example:
            user = repo.get(db, user_id=1)
            updated = repo.update(db, user, {"u_name": "Jane"})
        """
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        Delete record using ORM

        Args:
            db: Database session
            id: Primary key value

        Returns:
            Deleted model instance or None if not found
        """
        obj = db.query(self.model).filter(self.model.u_id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def count(self, db: Session) -> int:
        """
        Count total records using ORM

        Args:
            db: Database session

        Returns:
            Total count
        """
        return db.query(func.count(self.model.u_id)).scalar()

    # ==================== NATIVE SQL METHODS ====================

    def execute_raw_sql(
        self,
        db: Session,
        query: str,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Any]:
        """
        Execute raw SQL query and return results as tuples

        IMPORTANT: Always use parameterized queries!

        Args:
            db: Database session
            query: SQL query string with :param placeholders
            params: Dictionary of parameter values

        Returns:
            List of tuples (raw query results)

        Example:
            query = "SELECT * FROM users WHERE u_id = :user_id"
            results = repo.execute_raw_sql(db, query, {"user_id": 1})
        """
        result = db.execute(text(query), params or {})
        return result.fetchall()

    def execute_raw_sql_dict(
        self,
        db: Session,
        query: str,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute raw SQL query and return results as dictionaries

        IMPORTANT: Always use parameterized queries!

        Args:
            db: Database session
            query: SQL query string with :param placeholders
            params: Dictionary of parameter values

        Returns:
            List of dictionaries (column_name: value)

        Example:
            query = '''
                SELECT u_id, u_name, u_email
                FROM users
                WHERE u_created_at >= :start_date
            '''
            results = repo.execute_raw_sql_dict(db, query, {"start_date": "2024-01-01"})
            # Returns: [{"u_id": 1, "u_name": "John", "u_email": "john@example.com"}, ...]
        """
        result = db.execute(text(query), params or {})
        columns = result.keys()
        return [dict(zip(columns, row)) for row in result.fetchall()]

    def check_database_health(self, db: Session) -> bool:
        """
        Check if database connection is healthy

        Args:
            db: Database session

        Returns:
            True if database is healthy, False otherwise

        Example:
            if repo.check_database_health(db):
                print("Database is healthy")
        """
        try:
            db.execute(text("SELECT 1"))
            return True
        except Exception:
            return False

    def execute_raw_sql_scalar(
        self,
        db: Session,
        query: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Execute raw SQL query and return single scalar value

        Args:
            db: Database session
            query: SQL query string
            params: Dictionary of parameter values

        Returns:
            Single value (useful for COUNT, SUM, etc.)

        Example:
            query = "SELECT COUNT(*) FROM users WHERE u_status = :status"
            total = repo.execute_raw_sql_scalar(db, query, {"status": "active"})
        """
        result = db.execute(text(query), params or {})
        return result.scalar()
