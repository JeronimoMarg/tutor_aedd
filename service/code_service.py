from pathlib import Path
import subprocess

from repository.environment import Environment

class CodeService(object):
    def __init__(self, env: Environment):
        self.cpp_version = env.CPP_VERSION

    def compile_cpp(self, source_file: str, output_file: str = "a.out") -> tuple[bool, str]:
        source_path = Path(source_file)
        if not source_path.exists():
            return False, f"Archivo no encontrado: {source_file}"

        cmd = ["g++", str(source_file), "-std=" + self.cpp_version, "-o", output_file]
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False  # No lanza excepción si falla
            )
            if result.returncode == 0:
                return True, result.stdout or "Compilación exitosa."
            else:
                return False, result.stderr
        except Exception as e:
            return False, f"Error al ejecutar el compilador: {e}"