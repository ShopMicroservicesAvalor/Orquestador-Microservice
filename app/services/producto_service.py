from sqlalchemy.orm import Session
from models.producto import ProductoModel
from typing import List, Optional


async def get_all_productos(
    db: Session, skip: int = 0, limit: int = 100, activo: Optional[bool] = None
) -> List[ProductoModel]:

    try:
        query = db.query(ProductoModel)

        if activo is not None:
            query = query.filter(ProductoModel.activo == activo)

        return query.offset(skip).limit(limit).all()
    except Exception as e:
        raise f"Error al listar productos detalles: {str(e)}"
