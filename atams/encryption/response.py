"""
Response Encryption System
AES-256 encryption for GET endpoint responses

IMPORTANT: All GET endpoints MUST use encryption by default
Can be disabled via ENCRYPTION_ENABLED=false in .env
"""
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
from typing import Any, Dict


class ResponseEncryption:
    """Handle response encryption/decryption using AES-256"""

    def __init__(self, encryption_key: str, encryption_iv: str):
        # Ensure key and IV are exactly the right length
        self.key = encryption_key.encode('utf-8')[:32].ljust(32, b'\0')
        self.iv = encryption_iv.encode('utf-8')[:16].ljust(16, b'\0')

    def encrypt(self, data: str) -> str:
        """
        Encrypt string data using AES-256

        Args:
            data: String to encrypt

        Returns:
            Base64 encoded encrypted string
        """
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        padded_data = pad(data.encode('utf-8'), AES.block_size)
        encrypted = cipher.encrypt(padded_data)
        return base64.b64encode(encrypted).decode('utf-8')

    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypt encrypted string

        Args:
            encrypted_data: Base64 encoded encrypted string

        Returns:
            Decrypted string
        """
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        encrypted_bytes = base64.b64decode(encrypted_data)
        decrypted = cipher.decrypt(encrypted_bytes)
        return unpad(decrypted, AES.block_size).decode('utf-8')


def create_response_encryption(encryption_key: str, encryption_iv: str):
    """Factory function untuk create ResponseEncryption"""
    return ResponseEncryption(encryption_key, encryption_iv)


def create_encrypt_response_function(encryption_enabled: bool, encryption: ResponseEncryption):
    """
    Factory function untuk create encrypt_response_data dengan closure

    Args:
        encryption_enabled: Flag untuk enable/disable encryption
        encryption: Instance dari ResponseEncryption

    Returns:
        Function untuk encrypt response data
    """
    def encrypt_response_data(response_data: Any) -> Dict[str, Any]:
        """
        Encrypt response data for GET endpoints

        Args:
            response_data: Response object to encrypt

        Returns:
            Dict with encrypted data field

        Example:
            response = DataResponse(success=True, message="Success", data=user_data)
            if encryption_enabled:
                return encrypt_response_data(response)
            return response
        """
        if not encryption_enabled:
            return response_data

        # Convert response to JSON string
        # Use model_dump_json() if available (Pydantic v2), else model_dump with mode='json'
        if hasattr(response_data, 'model_dump_json'):
            json_data = response_data.model_dump_json()
        elif hasattr(response_data, 'model_dump'):
            import json
            json_data = json.dumps(response_data.model_dump(mode='json'))
        else:
            import json
            json_data = json.dumps(response_data, default=str)

        # Encrypt
        encrypted = encryption.encrypt(json_data)

        # Return wrapped response
        return {
            "encrypted": True,
            "data": encrypted
        }

    return encrypt_response_data
