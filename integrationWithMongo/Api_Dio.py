from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from pymongo import MongoClient

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String)
    endereco = Column(String)
    contas = relationship('Conta', back_populates='cliente')

class Conta(Base):
    __tablename__ = 'contas'
    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    saldo = Column(Integer)
    agencia = Column(String)
    num = Column(Integer)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    cliente = relationship('Cliente', back_populates='contas')

engine = create_engine('sqlite:///banco.db')
Base.metadata.create_all(engine)

from Api_Dio import Cliente, Conta, engine

Session = sessionmaker(bind=engine)
session = Session()

cliente1 = Cliente(nome='Alberto')
conta1 = Conta(tipo="Corrente", saldo=1200, agencia='0001', num=12345, cliente=cliente1)
conta2 = Conta(tipo="Poupança", saldo=2000, agencia='0002', num=67890, cliente=cliente1)
session.add(cliente1)
session.add(conta1)
session.add(conta2)
session.commit()

clientes = session.query(Cliente).all()
for cliente in clientes:
    print(f"Cliente: {cliente.nome}, CPF: {cliente.cpf}, Endereço: {cliente.endereco}")
for conta in cliente.contas:
    print(f"Conta {conta.tipo}: Saldo {conta.saldo}, Agência: {conta.agencia}, Número: {conta.num}")

client = MongoClient('mongodb+srv://giovane541996:gl542015@cluster0.3flj3l2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['database']
collection = db['collection']
collection.insert_one({
    "nome": "Alberto",
    "CPF": "065825856",
    "endereço": "Rua B",
    "contas": [
        {"Tipo": "Corrente", "saldo": 1200, "agencia": "0001", "num": 12345},
        {"Tipo": "Poupança", "saldo": 2000, "agencia": "0002", "num": 67890}
]
})

clientes = session.query(Cliente).all()
for cliente in clientes:
    print(f"Cliente: {cliente.nome}, CPF: {cliente.cpf}, Endereço: {cliente.endereco}")
for conta in cliente.contas:
    print(f"Conta {conta.tipo}: Saldo {conta.saldo}, Agência: {conta.agencia}, Número: {conta.num}")