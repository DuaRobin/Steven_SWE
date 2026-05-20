import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.credit_card_features import CreditCardFeatures
from main import app


def test_app_exists():
    assert app is not None


def test_feature_count():
    features = CreditCardFeatures.model_fields.keys()
    assert len(features) == 23


def test_target_not_in_features():
    features = CreditCardFeatures.model_fields.keys()
    assert "default_payment_next_month" not in features
