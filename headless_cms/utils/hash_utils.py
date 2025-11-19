import hashlib


class HashTracker:
    def __init__(self, initial_data: str | None = None, algo: str = "md5") -> None:
        """
        Initialize the HashTracker instance with an optional initial data and a hashing algorithm.

        Args:
            initial_data (Optional[str]): Initial data to start the hashing process.
                If None, the hash is not initialized.
            algo (str): The hashing algorithm to use (e.g., 'md5', 'sha256'). Defaults to 'md5'.
        """
        self.algo: str = algo
        self.hasher = hashlib.new(
            self.algo
        )  # Initialize hasher at the creation of an instance
        self._current_hash: bytes | None = None
        if initial_data is not None:
            self.update_hash(initial_data)

    def _hash_function(self, data: str) -> bytes:
        """Compute the hash of the given data using the initialized hashing algorithm.

        Args:
            data (str): The data to hash.

        Returns:
            bytes: The hash digest of the data.
        """
        self.hasher.update(data.encode("utf-8"))
        return self.hasher.digest()

    def _combine_hashes(self, hash1: bytes, hash2: bytes) -> bytes:
        """Combines two hash bytes using XOR, intended as a private method.

        Args:
            hash1 (bytes): The first hash.
            hash2 (bytes): The second hash to combine with the first.

        Returns:
            bytes: The result of the XOR combination of the two hashes.
        """
        return bytes(a ^ b for a, b in zip(hash1, hash2, strict=False))

    def update_hash(self, new_data: str | type[int] | None) -> None:
        """
        Update the current hash with new data by combining it with the existing hash.
        If new_data is None, the method does nothing.

        Args:
            new_data (Optional[str]): The new data to add to the current hash. If None, the hash remains unchanged.
        """
        if new_data is None:
            return  # Do nothing if new_data is None

        new_hash: bytes = self._hash_function(str(new_data))
        if self._current_hash is None:
            self._current_hash = new_hash
        else:
            self._current_hash = self._combine_hashes(self._current_hash, new_hash)

    @property
    def current_hash(self) -> str | None:
        """
        Get the current hash state as a hexadecimal string.

        Returns:
            Optional[str]: The current hash in hexadecimal format, or None if no hash has been computed yet.
        """
        return self._current_hash.hex() if self._current_hash else None
