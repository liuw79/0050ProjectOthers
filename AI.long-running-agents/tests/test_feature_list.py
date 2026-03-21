import pytest
import json
import tempfile
import os
from src.core.feature_list import Feature, FeatureListManager

def test_load_feature_list():
    features_data = [{
        "category": "functional",
        "description": "Test feature",
        "steps": ["Step 1", "Step 2"],
        "passes": False
    }]
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        json.dump(features_data, f)
        temp_path = f.name

    try:
        manager = FeatureListManager(temp_path)
        features = manager.load()
        assert len(features) == 1
        assert features[0].description == "Test feature"
        assert features[0].passes is False
    finally:
        os.unlink(temp_path)

def test_get_pending_features():
    features_data = [
        {"category": "functional", "description": "Done", "steps": [], "passes": True},
        {"category": "functional", "description": "Pending", "steps": [], "passes": False}
    ]
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        json.dump(features_data, f)
        temp_path = f.name

    try:
        manager = FeatureListManager(temp_path)
        pending = manager.get_pending()
        assert len(pending) == 1
        assert pending[0].description == "Pending"
    finally:
        os.unlink(temp_path)

def test_update_feature_status():
    features_data = [{"category": "functional", "description": "Test", "steps": [], "passes": False}]
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        json.dump(features_data, f)
        temp_path = f.name

    try:
        manager = FeatureListManager(temp_path)
        manager.update_status(0, passes=True)
        features = manager.load()
        assert features[0].passes is True
    finally:
        os.unlink(temp_path)
