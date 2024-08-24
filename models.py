from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()

# Association table for the many-to-many relationship between trades and picks
trade_picks_association = Table(
    'trade_picks', Base.metadata,
    Column('trade_id', Integer, ForeignKey('trades.id')),
    Column('pick_id', Integer, ForeignKey('picks.id'))
)

class Pick(Base):
    __tablename__ = 'picks'
    
    id = Column(Integer, primary_key=True)
    round = Column(Integer, nullable=False)
    pick_number = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    original_owner_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    current_owner_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    selection = Column(String, nullable=True)  # Add this line to store the selected player
    
    # Relationships back to the teams, specify the foreign keys explicitly
    original_owner = relationship('Team', foreign_keys=[original_owner_id], back_populates='picks')
    current_owner = relationship('Team', foreign_keys=[current_owner_id])
    team = relationship('Team', foreign_keys=[team_id])

class Team(Base):
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    profile_pic = Column(String, nullable=True)  # Attribute for profile picture
    draft_order = Column(Integer, nullable=True)  # New attribute for draft order
    
    # Relationship to link the team with picks and trades
    picks = relationship('Pick', back_populates='original_owner', foreign_keys='Pick.original_owner_id')
    trades_sent = relationship('Trade', back_populates='sending_team', foreign_keys='Trade.sending_team_id')
    trades_received = relationship('Trade', back_populates='receiving_team', foreign_keys='Trade.receiving_team_id')



class Trade(Base):
    __tablename__ = 'trades'
    
    id = Column(Integer, primary_key=True)
    sending_team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    receiving_team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    trade_details = Column(String, nullable=False)
    
    # Relationships to link to sending and receiving teams
    sending_team = relationship('Team', foreign_keys=[sending_team_id], back_populates='trades_sent')
    receiving_team = relationship('Team', foreign_keys=[receiving_team_id], back_populates='trades_received')
    
    # Many-to-many relationship between trades and picks
    picks_sent = relationship('Pick', secondary=trade_picks_association, backref='trades_sent', primaryjoin=id==trade_picks_association.c.trade_id)
    picks_received = relationship('Pick', secondary=trade_picks_association, backref='trades_received', primaryjoin=id==trade_picks_association.c.trade_id)

# Engine and session setup for SQLite
engine = create_engine('sqlite:///nwoaffl.db')
# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
