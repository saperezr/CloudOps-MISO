#!/usr/bin/env python
import unittest
import sys
import os

# Asegurarse de que el directorio raíz y src estén en el path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Descubrir y cargar todas las pruebas
loader = unittest.TestLoader()
start_dir = os.path.join(os.path.dirname(__file__), 'tests')
suite = loader.discover(start_dir, pattern='test_*.py')

# Ejecutar las pruebas
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

# Salir con el código de estado apropiado
sys.exit(not result.wasSuccessful()) 