# -*- coding: utf-8 -*-

"""djangoflash.codec test cases.
"""

from unittest import TestCase

from django.core.exceptions import SuspiciousOperation

from djangoflash import codec
from djangoflash.codec import pickle_impl, json_impl, json_zlib_impl, BaseCodec
from djangoflash.models import FlashScope


class CodecTestCase(TestCase):
    """Tests methods used to parse flash storage URIs and create flash storage
    objects.
    """
    def test_get_pickle_codec_by_alias(self):
        """Codec: 'pickle' should resolve to Pickle-based codec.
        """
        codec_impl = codec.get_codec('pickle')
        self.assertTrue(isinstance(codec_impl, pickle_impl.CodecClass))

    def test_get_json_codec_by_alias(self):
        """Codec: 'json' should resolve to JSON-based codec.
        """
        codec_impl = codec.get_codec('json')
        self.assertTrue(isinstance(codec_impl, json_impl.CodecClass))

    def test_get_json_zlib_codec_by_alias(self):
        """Codec: 'json_zlib' should resolve to JSON/zlib-based codec.
        """
        codec_impl = codec.get_codec('json_zlib')
        self.assertTrue(isinstance(codec_impl, json_impl.CodecClass))
        self.assertTrue(isinstance(codec_impl, json_zlib_impl.CodecClass))

    def test_get_codec_by_module_name(self):
        """Codec: 'djangoflash.codec.json_impl' should resolve to JSON-based codec.
        """
        codec_impl = codec.get_codec('djangoflash.codec.json_impl')
        self.assertTrue(isinstance(codec_impl, json_impl.CodecClass))

    def test_get_codec_by_invalid_module_name(self):
        """Codec: Should raise an error when resolving a module name that doesn't exists.
        """
        operation = lambda: codec.get_codec('invalid.module.path')
        self.assertRaises(ImportError, operation)

    def test_get_codec_by_invalid_module(self):
        """Codec: Should raise an error when module doesn't provide a codec class.
        """
        operation = lambda: codec.get_codec('djangoflash.models')
        self.assertRaises(AttributeError, operation)


class BaseCodecTestCase(TestCase):
    """Tests the tampered checks and signing logic.
    """
    def setUp(self):
        """Creates a codec and a sample flash.
        """
        self.codec = json_impl.CodecClass()
        self.flash = FlashScope()
        self.flash['info'] = 'Info'
        self.flash.update()
        self.expected = 'eyJfc2Vzc2lvbiI6IHsiaW5mbyI6ICJJbmZvIn0sICJfdXNlZCI6' \
                        'IHsiaW5mbyI6IG51bGx9fWZk\nNDViYTljMmU3MWJlZjBjYjcxOW' \
                        'EwYjdlYzJlZjUx\n'

    def test_encode_and_sign(self):
        """Codec: BaseCodec should return an encoded and signed version of the flash.
        """
        encoded_and_signed = self.codec.encode_and_sign(self.flash)
        self.assertEqual(self.expected, encoded_and_signed)

    def test_decoded_signed(self):
        """Codec: BaseCodec should decode an encoded and signed version of the flash.
        """
        flash = self.codec.decode_signed(self.expected)
        self.assertEqual('Info', flash['info'])
        flash.update()
        self.assertFalse('info' in flash)

    def test_decoded_tampered(self):
        """Codec: BaseCodec should not decode a tampered version of the flash.
        """
        tampered = 'eyJfc2Vzc2lvbiI6IHsiaW6mbyI6ICJJbmZvIn0sICJfdXNlZCI6IHsia' \
                   'W5mbyI6IG51bGx9fWZk\nNDViYTljMmU3MWJlZjBjYjcxOWEwYjdlYzJl' \
                   'ZjUx\n'
        operation = lambda: self.codec.decode_signed(tampered)
        self.assertRaises(SuspiciousOperation, operation)


class PickleCodecTestCase(TestCase):
    """Tests the Pickle-based serialization codec implementation.
    """
    def setUp(self):
        """Creates a Pickle-based codec and a sample flash.
        """
        self.codec = pickle_impl.CodecClass()
        self.flash = FlashScope()
        self.flash['info'] = 'Info'
        self.flash.update()
        self.expected = '\x80\x02cdjangoflash.models\nFlashScope\nq\x01)\x81q' \
                        '\x02}q\x03(U\x03nowq\x04cdjangoflash.models\n_Immedi' \
                        'ateFlashScopeAdapter\nq\x05)\x81q\x06}q\x07U\x08dele' \
                        'gateq\x08h\x02sbU\x08_sessionq\t}q\nU\x04infoq\x0bU' \
                        '\x04Infoq\x0csU\x05_usedq\r}q\x0eh\x0bNsub.'

    def test_encode(self):
        """Codec: Pickle-based codec should return a Pickle dump of the flash.
        """
        self.assertEqual(self.expected, self.codec.encode(self.flash))

    def test_decode(self):
        """Codec: Pickle-based codec should restore the flash from a Pickle dump string.
        """
        flash = self.codec.decode(self.expected)
        self.assertEqual('Info', flash['info'])
        flash.update()
        self.assertFalse('info' in flash)


class JSONCodecTestCase(TestCase):
    """Tests the JSON-based serialization codec implementation.
    """
    def setUp(self):
        """Creates a JSON-based codec and a sample flash.
        """
        self.expected = '{"_session": {"info": "Info"}, ' \
                        '"_used": {"info": null}}'
        self.codec = json_impl.CodecClass()
        self.flash = FlashScope()
        self.flash['info'] = 'Info'
        self.flash.update()

    def test_encode(self):
        """Codec: JSON-based codec should return a JSON version of the flash.
        """
        self.assertEqual(self.expected, self.codec.encode(self.flash))

    def test_decode(self):
        """Codec: JSON-based codec should restore the flash from a JSON string.
        """
        flash = self.codec.decode(self.expected)
        self.assertEqual('Info', flash['info'])
        flash.update()
        self.assertFalse('info' in flash)


class JSONZlibCodecTestCase(TestCase):
    """Tests the JSON/zlib-based serialization codec implementation.
    """
    def setUp(self):
        """Creates a JSON\zlib-based codec and a sample flash.
        """
        self.expected = 'x\x9c\xabV\x8a/N-.\xce\xcc\xcfS\xb2R\xa8V\xca\xccK' \
                        '\xcb\x072\x94<At\xad\x8e\x82R|iqj\n\xb2T^iNNm-\x00' \
                        '\xf5\xa2\x12\x03'
        self.codec = json_zlib_impl.CodecClass()
        self.flash = FlashScope()
        self.flash['info'] = 'Info'
        self.flash.update()

    def test_encode(self):
        """Codec: JSON\zlib-based codec should return a zlib compressed JSON version of the flash.
        """
        self.assertEqual(self.expected, self.codec.encode(self.flash))

    def test_decode(self):
        """Codec: JSON\zlib-based codec should restore the flash from a zlib compressed JSON string.
        """
        flash = self.codec.decode(self.expected)
        self.assertEqual('Info', flash['info'])
        flash.update()
        self.assertFalse('info' in flash)
