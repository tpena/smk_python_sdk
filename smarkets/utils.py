
import re
from google.protobuf.descriptor import FieldDescriptor

class MessageSerializer(object):
    @classmethod
    def serialize(cls, message):
        serialized = {}

        keys = message.DESCRIPTOR.fields_by_name.keys()
        if keys:
            for tag, field in message.DESCRIPTOR.fields_by_number.iteritems():
                value = getattr(message, field.name)
                if field.label == FieldDescriptor.LABEL_REPEATED:
                    serializedChild = []
                    for child in getattr(message, field.name):
                        serializedChild.append(cls._serialize_value(field, child))
                    serialized[field.name] = serializedChild
                else:
                    serialized[field.name] = cls._serialize_value(field, value)

        return serialized

    @classmethod
    def _serialize_value(cls, field, value):
        if field.type == FieldDescriptor.TYPE_BOOL:
            return value
        elif field.type in (FieldDescriptor.TYPE_MESSAGE, FieldDescriptor.TYPE_GROUP):
            return cls.serialize(value)
        elif field.type == FieldDescriptor.TYPE_ENUM:
            name = field.enum_type.values[value-1].name
            prefix = cls.enum_descriptor_prefix(field.enum_type.name)

            print field.enum_type.name, name, prefix
            return cls.strip_enum_prefix(name, prefix)
        else:
            return value

    @classmethod
    def enum_descriptor_prefix(cls, name):
        name_lc = name.lower()

        for suffix in ('reason', 'type'):
            idx = name_lc.rfind(suffix)
            if idx != -1:
                print idx, name[0:idx]
                return cls.uncamel(name[0:idx]).upper()

        return cls.uncamel(name).upper()

    @classmethod
    def uncamel(cls, name):
        return re.sub('(?!^)([A-Z]+)', r'_\1', name)

    @classmethod
    def strip_enum_prefix(cls, enum_name, strip_prefix=None):
        if strip_prefix:
            name = re.sub(r'^%s_' % strip_prefix, '', enum_name)
        else:
            name = enum_name

        return name
