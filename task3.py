from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Column, Date, String, Time, create_engine
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
import uuid

# Создание подключения к БД: 'Тип_БД+драйвер://пользователь:пароль@хост/имя_БД?driver=ODBC+driver+17+for+SQL+Server'
#форма для упрощения кода
base_url = r"mssql+pyodbc://lz6:12345@DESKTOP-PPBSL4D\GFHDTHEV/Shard{}?driver=ODBC+Driver+17+for+SQL+Server&Encrypt=yes&TrustServerCertificate=yes"
#cоздаем словарь, чтобы далее сопоставлять с каким именно подключением заносить данные
#{0: Engine(Shard0)} и тд
engines = {i: create_engine(base_url.format(i)) for i in range(12)}

class Base(DeclarativeBase):
    pass

class User_Logs(Base):
    __tablename__ = "User_Logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    username = Column(String, nullable=False)
    user_action = Column(String, nullable=False)
    action_date = Column(Date, nullable=False)
    action_time = Column(Time, nullable=False)
    action_result = Column(String, nullable=False)

#проходим по всем бд и проверяем созданы ли таблицы
for shard_id, engine in engines.items():
    Base.metadata.create_all(bind=engine)
    print(f"Проверка Shard{shard_id}")

print("=" * 50)

def inputt(engine, input_data: User_Logs):
    with Session(autoflush=False, expire_on_commit=False, bind=engine) as db:
        db.add(input_data)
        db.commit()

def sendto_shard(input_data: User_Logs, current_shard: int):
    #берем подключение из словаря
    target_engine = engines.get(current_shard)
    
    if not target_engine:
        print(f"Не найдено подключение для {current_shard}")
        return current_shard

    #записываем данные
    inputt(engine=target_engine, input_data=input_data)
    print(f'Данные пользователя "{input_data.username}" записаны в {current_shard}')
    
    #если current_shard = 11, то (11 + 1) % 12 = 0
    #далее пойдет по кругу
    next_shard = (current_shard + 1) % 12
    
    return next_shard

def main():
    current_shard = 0 #создаем первоначальное значение для выюора
    
    for i in range(1, 16): 
        input_data = User_Logs(
            username=f"User_{i}", 
            user_action="DELETE", 
            action_date=f"2023-01-{i}", 
            action_time=f"{i}:{i}:{i}", 
            action_result="OK"
        )
        
        current_shard = sendto_shard(input_data, current_shard=current_shard)

if __name__ == "__main__":
    main()