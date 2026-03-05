"""
Firebase configuration and initialization module.
Centralizes Firebase setup to prevent initialization conflicts.
"""
import os
import json
from typing import Dict, Any
import firebase_admin
from firebase_admin import credentials, firestore, auth
from google.cloud.firestore_v1.client import Client as FirestoreClient
import logging

logger = logging.getLogger(__name__)


class FirebaseConfig:
    """Manages Firebase configuration and initialization"""
    
    _initialized: bool = False
    _firestore_client: FirestoreClient = None
    _auth_client = None
    
    @classmethod
    def initialize(cls, config_path: str = None) -> None:
        """
        Initialize Firebase Admin SDK with robust error handling.
        
        Args:
            config_path: Path to Firebase service account JSON file.
                        If None, uses environment variables.
        
        Raises:
            ValueError: If Firebase configuration is missing
            RuntimeError: If Firebase initialization fails
        """
        if cls._initialized:
            logger.warning("Firebase already initialized")
            return
        
        try:
            if config_path and os.path.exists(config_path):
                # Load from file
                cred = credentials.Certificate(config_path)
            else:
                # Load from environment variables
                firebase_config = {
                    "type": "service_account",
                    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
                    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
                    "private_key": os.getenv("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n"),
                    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
                    "client_id": os.getenv("FIRE