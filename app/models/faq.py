from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base
import json
class FAQ(Base):
    """
    FAQ model to store the main FAQ information (question and answer in a default language).
    One FAQ can have multiple translations in different languages.
    """
    __tablename__ = 'faqs'  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    language = Column(String(10), default='en', nullable=False)  # Default to English

    translations = relationship('FAQTranslation', back_populates='faq')

    def serialize(self):
        return json.dumps({
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'language': self.language
        })

class FAQTranslation(Base):
    """
    FAQTranslation model to store translations of FAQ questions and answers.
    Each translation is linked to a single FAQ and represents the FAQ in a different language.
    """
    __tablename__ = 'faq_translations'

    id = Column(Integer, primary_key=True, index=True)
    faq_id = Column(Integer, ForeignKey('faqs.id'), nullable=False)
    language = Column(String(10), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)

    faq = relationship('FAQ', back_populates='translations')
