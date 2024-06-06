class SerializationMixin:
    """
    A class to be mixed in to core models to handle DTO transformations in a modular way.

    :param include_optional: Condition for adding relationship-defined attributes to DTO. Default value set to True.

    Returns a dictionary.

    """
    _serialization_keys = []
    _deserialization_keys = []

    def serialize(self, include_optional=True):
        """
        Method for serializing an object.

        :param include_optional: Condition for adding relationship-defined attributes to DTO. Default value set to True.

        Returns a dictionary
        """

        data = {key: getattr(self, key) for key in self._serialization_keys}

        if include_optional:
            for attr in self._optional_serialization_keys():
                data[attr] = getattr(self, attr)
        return data

    @classmethod
    def _optional_serialization_keys(cls):
        """
        Method for specifying model-unique optional attributes that should be included when serializing objects.

        :param cls: Relevant model class

        Returns a list
        """

        return []

    @classmethod
    def deserialize(cls, data):
        """
        Method for deserializing objects.
        Constructs a new instance of class `cls` using the values from provided dict `data` based on keys specified in relevant model's `deserialize_keys`.

        :param cls: Relevant model class
        :param data: Relevant data to deserialize

        Returns an instance of class `cls`
        """

        obj_data = {key: data[key] for key in cls._deserialization_keys}

        return cls(**obj_data)
